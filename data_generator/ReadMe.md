# Vehicle Telemetry Data Generator

## Overview:
This script simulates telemetry data for a fleet of vehicles, generating realistic data streams with optional NULL values. The generated data is saved in JSON files organized by vehicle ID, with each file capped at a configurable maximum size (default: 1 MB). The script is designed to run for a specified duration and can be used to test data pipelines or machine learning models.

### Features:
1.  Randomized Data Generation:
    Simulates telemetry fields such as speed, battery voltage, current, state of charge, battery temperature, and GPS coordinates.\
    Includes optional NULL values with a configurable probability to mimic real-world missing data scenarios.

2.  Fleet Simulation:
    Generates data for multiple vehicles simultaneously.\
    Each vehicle's data is stored in its own directory.

3.  File Management:
    Files are capped at a configurable size (default: 1 MB).\
    Automatically creates new files when the size limit is reached.

4.  Configurable Runtime:
    The script runs for a specified duration (default: 30 minutes).

## Key Parameters:
| Parameter           | Default Value   | Description                                                   |
|---------------------|-----------------|---------------------------------------------------------------|
| `ALLOWED_FILE_SIZE` | 1 MB            | Maximum size of each JSON file (in MB).                      |
| `BASE_DIR`          | `vehicle_data`  | Base directory where the generated data will be stored.       |
| `null_probability`  | 0.2             | Probability of inserting NULL values into fields.             |
| `num_vehicles`      | 5               | Number of vehicles in the fleet.                              |
| `end_time`          | +30 minutes     | Duration for which the script will run.                       |

## Sample JSON Record:
{\
    "vehicle_id": "V-001",\
    "timestamp": "2023-10-10 12:00:00",\
    "speed_kmh": 50.25,\
    "battery_voltage": 360.5,\
    "battery_current": -15.3,\
    "battery_soc_percent": 85.7,\
    "battery_temp_celsius": 25.4,\
    "latitude": -37.8136,\
    "longitude": 144.9631\
}

## Directory Structure Example:
vehicle_data/
├── V-001/
│   ├── V-001_20231010_120000_0.json
│   ├── V-001_20231010_120500_1.json
├── V-002/
│   ├── V-002_20231010_120000_0.json
│   ├── V-002_20231010_121000_1.json
...

## Notes
   Ensure sufficient disk space before running the script for extended durations.\
   The script generates random data and should not be used for production purposes without further validation.
