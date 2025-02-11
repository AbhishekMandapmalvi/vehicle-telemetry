# %%
# data_generator.ipynb
from faker import Faker
import random
import json
from datetime import datetime, timedelta
import os

# %%
# Initialize Faker instance
fake = Faker()

# Function to randomly decide if a field should be NULL
def randomly_nullify(value, null_probability=0.1):
    """
    Replace the value with None based on a given probability.
    :param value: The original value.
    :param null_probability: Probability of replacing the value with None (default is 10%).
    :return: Either the original value or None.
    """
    return None if random.random() < null_probability else value

# Function to generate random telemetry data for a vehicle
def generate_vehicle_data(vehicle_id, start_time, num_records, null_probability=0.1):
    """
    Generate random telemetry data for a vehicle with optional NULLs.
    :param vehicle_id: ID of the vehicle.
    :param start_time: Starting timestamp for data generation.
    :param num_records: Number of records to generate.
    :param null_probability: Probability of inserting NULLs into fields.
    :return: A list of telemetry records.
    """
    data = []
    current_time = start_time
    
    for _ in range(num_records):
        # Generate telemetry data with possible NULLs
        speed = randomly_nullify(round(random.gauss(-10, 220), 2), null_probability)  # Speed in km/h
        voltage = randomly_nullify(round(random.gauss(-10, 450), 2), null_probability)  # Voltage in V
        current = randomly_nullify(round(random.gauss(-50, 50), 2), null_probability)  # Current in A
        battery_level = randomly_nullify(round(random.gauss(-10, 110), 2), null_probability)  # Battery percentage
        battery_temp = randomly_nullify(round(random.gauss(-50, 50), 2), null_probability)  # Engine temperature in °C
        latitude = randomly_nullify(float(fake.latitude()), null_probability)  # Latitude
        longitude = randomly_nullify(float(fake.longitude()), null_probability)  # Longitude
        
        # Append record to list
        record = {
            "vehicle_id": vehicle_id,
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "speed_kmh": speed,
            "battery_voltage": voltage,
            "battery_current": current,
            "battery_soc_percent": battery_level,
            "battery_temp_celsius": battery_temp,
            "latitude": latitude,
            "longitude": longitude,
        }
        data.append(record)
        
        # Increment time by a random interval (e.g., 1 to 5 seconds)
        current_time += timedelta(seconds=random.randint(1, 5))
    
    return data

# Generate data for multiple vehicles
def generate_fleet_data(num_vehicles, null_probability=0.1):
    """
    Generate telemetry data for multiple vehicles with optional NULLs.
    :param num_vehicles: Number of vehicles to generate data for.
    :param null_probability: Probability of inserting NULLs into fields.
    :return: A list of telemetry records for all vehicles.
    """
    fleet_data = []
    start_time = datetime.now()
    
    for vehicle_id in range(1, num_vehicles + 1):
        vehicle_data = generate_vehicle_data(f"V-{vehicle_id:03}", start_time, random.randint(0, 10), null_probability)
        fleet_data.extend(vehicle_data)
    
    return fleet_data

# %%
def save_vehicle_data(vehicle_id, data, file_index, start_time):
    """Save data to a properly structured file"""
    # Create vehicle directory if needed
    vehicle_dir = os.path.join(BASE_DIR, vehicle_id)
    os.makedirs(vehicle_dir, exist_ok=True)
    
    # Create filename with timestamp and index
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    filename = f"{vehicle_id}_{timestamp}_{file_index}.json"
    filepath = os.path.join(vehicle_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    
    return filepath

# New configuration
ALLOWED_FILE_SIZE = 1 #MB
MAX_FILE_SIZE = ALLOWED_FILE_SIZE * 1024 * 1024  # 1MB in bytes
BASE_DIR = "vehicle_data"

# Modified main loop
vehicle_data = {}  # {vehicle_id: {'data': [], 'file_index': 0}}
start_time = datetime.now()
end_time = start_time + timedelta(minutes=30)

while datetime.now() < end_time:
    fleet_data = generate_fleet_data(num_vehicles=5, null_probability=0.2)
    
    # Organize data by vehicle_id
    for record in fleet_data:
        vid = record['vehicle_id']
        if vid not in vehicle_data:
            vehicle_data[vid] = {
                'data': [],
                'file_index': 0
            }
        
        vehicle_data[vid]['data'].append(record)
        
        # Check size before writing
        current_size = len(json.dumps(vehicle_data[vid]['data']).encode('utf-8'))
        if current_size >= MAX_FILE_SIZE:
            # Save current data
            save_vehicle_data(
                vid,
                vehicle_data[vid]['data'],
                vehicle_data[vid]['file_index'],
                start_time
            )
            
            # Reset buffer and increment index
            vehicle_data[vid]['data'] = []
            vehicle_data[vid]['file_index'] += 1

# Save remaining data after loop ends
for vid in vehicle_data:
    if vehicle_data[vid]['data']:
        save_vehicle_data(
            vid,
            vehicle_data[vid]['data'],
            vehicle_data[vid]['file_index'],
            start_time
        )

print(f"Data saved in {BASE_DIR} directory with vehicle subfolders")

# %%



