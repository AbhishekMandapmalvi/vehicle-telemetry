# Configuration Folder

## Overview:
The config folder contains essential configuration files for the vehicle telemetry data pipeline. These files define the schema for telemetry data validation and interpolation, as well as metadata about the vehicles in the fleet. These configurations ensure data consistency, quality, and enrichment during processing.

## Files in this Folder:
### 1. schema.yml:
   This file defines the schema for the raw_telemetry data, including field types, constraints, and interpolation rules. It is used to validate incoming raw telemetry data from blob/s3 storage and apply necessary transformations.
### Key Features:
  a. Field Definitions: Specifies each field's name, type, and description.
  b. Validation Rules: Includes constraints such as minimum and maximum values for numerical fields.
  c. Interpolation Settings: Enables interpolation (e.g., linear or zero-order hold) for missing or invalid data points.
  d. Examples: Provides sample values for each field to clarify expected formats.
### Schema Fields:
| Field Name           | Type    | Nulls Allowed | Interpolation | Constraints          | Description                          |
|----------------------|---------|----------|---------------|----------------------|--------------------------------------|
| `vehicle_id`         | string  | Yes      | No            | N/A                  | Unique vehicle identifier            |
| `timestamp`          | string  | Yes      | No            | Format: `%Y-%m-%d %H:%M:%S` | Event timestamp in UTC              |
| `speed_kmh`          | double  | No       | Linear        | Min: 0, Max: 170     | Vehicle speed in kilometers per hour |
| `battery_voltage`    | double  | No       | ZOH           | Min: 0, Max: 400     | Battery voltage in volts             |
| `battery_current`    | double  | No       | ZOH           | Min: -40, Max: 40    | Battery current in amperes           |
| `battery_soc_percent`| double  | No       | ZOH           | Min: 0, Max: 100     | State of charge percentage           |
| `battery_temp_celsius`| double | No       | ZOH           | Min: -20, Max: 40    | Battery temperature in Celsius       |
| `latitude`           | double  | No       | No            | Min: -90, Max: 90    | GPS latitude coordinate              |
| `longitude`          | double  | No       | No            | Min: -180, Max: 180  | GPS longitude coordinate             |

### 2. vehicle_hash_table.yml:
   This file contains metadata about the vehicles in the fleet. It maps each vehicle_id to detailed information about the vehicle's battery configuration, type, capacity etc. To onboard a new vehicle to fleet add details to this file.
### Key Features:
  a. Vehicle Metadata: Includes details such as commercial name, battery chemistry, pack configuration, nominal voltage, and number of cells.\
  b. Fleet Management: Helps enrich telemetry data with vehicle-specific attributes during processing.

### Vehicle Fields:
| Field Name                  | Description                                      |
|-----------------------------|--------------------------------------------------|
| vehicle_id                  | Unique identifier for the vehicle                |
| commercial_name             | Commercial name of the vehicle                   |
| battery_pack_configuration  | Cell configuration (series x parallel)           |
| battery_type                | Type of battery chemistry (e.g., lithium-ion)    |
| battery_capacity            | Standard battery capacity (kWh)                  |
| nominal_voltage             | Nominal voltage of the battery pack (V)          |
| form_factor                 | Form factor of the battery cells (e.g., pouch)   |
| number_of_cell              | Total number of cells in the battery pack        |

#### Example Vehicle:
vehicle_id: V-001

Commercial Name: Mustang Mach-e

Battery Pack Configuration: 197s2p

Battery Type: Lithium-Ion

Battery Capacity: 100.54 kWh

Nominal Voltage: 800 V

Form Factor: Pouch

Number of Cells: 384
