# Vehicle Telemetry Data Cleaning Scripts

## Overview
This folder contains Python scripts designed to clean raw telemetry data from electric vehicles. The scripts handle data validation, interpolation, enrichment, and transformation to prepare the data for storage in the cleaned_telemetry Delta Lake table. These scripts are used in a Databricks environment as part of a pipeline to clean and enrich telemetry data for downstream analytics and battery health modeling.

## Files in This Folder
### 1. apply_constraints.py:
   This script validates the raw telemetry data against constraints defined in the YAML schema file (schema.yml). It removes rows that violate the specified     minimum and maximum values for certain fields.
#### Key Features:
   a. Loads schema constraints from a YAML file.\
   b. Filters out invalid rows based on field-specific constraints (e.g., speed, battery voltage).\
   c. Ensures data quality before further processing.

### 2. data_mapping.py:
   This script enriches the telemetry data by mapping vehicle metadata (e.g., battery configuration, type, capacity) from the vehicle_hash_table.yml file to the raw telemetry data.
#### Key Features:
   a. Joins raw telemetry data with vehicle metadata using vehicle_id.\
   b. Adds fields such as commercial_name, battery_type, and battery_capacity to the dataset.

### 3. interpolation.py:
   This script interpolates missing or null values in the telemetry dataset based on rules defined in the YAML schema file (schema.yml). It supports both linear interpolation and zero-order hold (ZOH).
#### Key Features:
   a. Handles missing values for numerical fields like speed, battery voltage, and state of charge.\
   b. Linear interpolation: Calculates intermediate values based on neighboring records.\
   c. ZOH: Fills missing values using the last known value.

### 4. vehicle_status.py:
   This script determines the operational status of each vehicle (e.g., driving, charging, parking) based on speed and battery current.
#### Key Features:
   a. Adds a new column vehicle_status to classify vehicle activity.\
   b. Status categories include: "driving", "charging", "parking", "recuperation", "fault", and "unknown".

### 5. data_cleaning.py:
   This Databricks notebook orchestrates the entire data cleaning pipeline. It integrates all other scripts to process raw telemetry data into a cleaned and enriched format.
#### Workflow:
   a. Load raw telemetry data from workspace.default.raw_telemetry.\
   b. Apply constraints using apply_constraints.py.\
   c. Enrich data with vehicle metadata using data_mapping.py.\
   d. Process timestamps into standard formats.\
   e. Interpolate missing values using interpolation.py.\
   f. Determine vehicle status using vehicle_status.py.\
   g. Write cleaned data to the Delta Lake table workspace.default.cleaned_telemetry.
