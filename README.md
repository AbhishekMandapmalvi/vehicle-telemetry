# Vehicle Telemetry ELT Pipeline

## Project Overview
This project processes raw telemetry data from electric vehicle fleets to produce cleaned and structured data for use in a battery health prediction model. The pipeline is implemented using Databricks and integrates with cloud storage solutions such as Azure Blob Storage or AWS S3 for scalable data storage. The cleaned data is stored in the cleaned_telemetry Delta Lake table, which serves as the input for the battery health prediction model.

## Data Flow and Pipeline Description
1. Data Generator:
   a. The data_generator folder contains scripts to simulate telemetry data streams.
   b. Users can specify the number of vehicles in the fleet and the simulation duration (in minutes).
   c. Running the script generates folders named after each vehicle_id, containing JSON files with telemetry data.
   d. Each file is capped at 1 MB by default (configurable in the script), after which a new file is created.

2. Data Integration:
   a. Use Apache Kafka to stream the generated telemetry data from the local environment to a cloud storage provider of your choice (e.g., Azure Blob Storage or AWS S3).
   b. This ensures seamless integration between local data generation and cloud-based processing.

3. Data Loading:
   a. Configure Databricks' Autoloader to monitor the specified cloud storage location for new data.
   b. The Autoloader automatically detects and ingests new JSON files into the Delta Lake table raw_telemetry.
   c. This step is implemented using the data_loader/main.py script.
   
4. Data Transformation:
   a. Run the data_cleaning.ipynb notebook in Databricks to clean and transform the raw telemetry data.
   b. The cleaning process includes removing invalid records, standardizing timestamps, validating numerical ranges, and enriching data with additional metadata.
   c. The cleaned data is then stored in the cleaned_telemetry Delta Lake table.

5. Workflow Summary:
   The overall workflow can be summarized as follows:
         Data Generator (Local PC/Vehicle) -> Data Integration (Blob/S3 via Kafka) -> Data Loader (data_loader/main.py) -> Data Cleaning (data_cleaning.ipynb)

## Key Features
1. Scalable Cloud Integration: Supports both Azure Blob Storage and AWS S3 for reliable and scalable cloud-based storage.
2. Automated Data Ingestion: Leverages Databricks' Autoloader for real-time detection and ingestion of new telemetry data.
3. Configurable Simulation: Allows users to customize fleet size, simulation duration, and file size limits during data generation.
4. Cleaned Data for Modeling: Produces structured, high-quality telemetry data ready for use in predictive battery health models.

## How to Use
1. Set Up Data Generation:
  a. Place the data_generator folder on your local machine.
  b. Specify fleet size and simulation duration in the script configuration.
  c. Run the script to generate telemetry data streams.

2. Configure Data Integration:
  a. Set up Apache Kafka to stream generated JSON files from your local environment to a cloud provider (Azure Blob Storage or AWS S3).

3. Load Data into Delta Lake:
  a. Configure Databricks' Autoloader in data_loader/main.py to monitor your cloud storage location.
  b. Use data_loader/main.py to ingest raw telemetry data into the raw_telemetry Delta Lake table.

4. Clean and Transform Data:
  a. Open and execute the data_cleaning.ipynb notebook in Databricks.
  b. Verify that cleaned data is stored in the cleaned_telemetry Delta Lake table.

5. Schedule Workflow to Automate Loading and Transformation:
  a. Utilize databricks' workflow/job scheduler function to automate this pipeline. 

## Results:
![image](https://github.com/user-attachments/assets/c6e515de-cf3a-4e25-b849-50facdac9597)
