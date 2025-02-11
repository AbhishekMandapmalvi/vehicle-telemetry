# Vehicle Telemetry Ingestion Pipeline

## Overview:
This folder contains the implementation of a vehicle telemetry ingestion pipeline using Databricks Autoloader. The pipeline is designed to process streaming JSON telemetry data from cloud storage, validate it against a predefined schema, and write it to a Delta Lake table for further analysis. It ensures scalability, fault tolerance, and efficient data processing.

## Files Description:
### 1. main.py:
This is the entry point for the pipeline. It initializes the Telematics_ingestion class, sets up configurations, and runs the data ingestion pipeline.
#### Key Features:
a. Creates a Spark session.\
b. Configures paths for:\
      i. Schema file (schema.yml).\
      ii. Source data (S3 bucket containing telemetry JSON files).\
      iii. Target Delta table (workspace.default.raw_telemetry).\
      iv. Checkpointing (S3 bucket for fault tolerance).\
c. Executes the pipeline using Databricks Autoloader.

### 2. autoloader.py:
This file contains the Telematics_ingestion class, which implements the core logic of the telemetry ingestion pipeline.
#### Key Features:
a. Schema Loading: Reads schema definitions from a YAML configuration file (schema.yml) and maps them to PySpark data types.\
b. Databricks Autoloader Integration: Uses Autoloader's cloudFiles format to efficiently read JSON files from cloud storage.\
c. Delta Lake Integration: Writes processed data to a Delta Lake table in append mode with checkpointing enabled.\
d. Error Handling: Catches and logs errors during streaming operations.

## How to use:
### Prerequisites:
1. A Databricks environment with access to cloud storage (e.g., AWS S3 or Azure Blob Storage).
2. A YAML schema file (schema.yml) defining telemetry data fields and their types.
3. Telemetry JSON files stored in cloud storage (e.g., S3 bucket).

### Steps:
1. Configure Paths:\
Update paths in main.py for:\
    config_path: Path to your YAML schema file (e.g., /Workspace/.../schema.yml).\
    source_path: Path to your cloud storage containing telemetry JSON files (e.g., s3://vehicletelemetry/).\
    target_path: Target Delta table (e.g., workspace.default.raw_telemetry).\
    checkpoint_path: Path for checkpointing (e.g., s3://vehiclepipelinecache/).
2. Run the Pipeline:\
Execute main.py in your Databricks notebook or cluster.

## Notes:
1. Ensure that your S3 bucket paths (source_path, checkpoint_path) are accessible by Databricks.
2. The Delta table (workspace.default.raw_telemetry) will be created automatically if it does not exist.
3. Use Databricks Autoloader's schema evolution features if you expect changes in your telemetry data structure.
