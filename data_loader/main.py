%python
from autoloader import Telematics_ingestion
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def main():
    """
    Main function to initialize and execute the telemetry ingestion pipeline.

    This function sets up the `Telematics_ingestion` pipeline by:
    - Initializing a Spark session.
    - Configuring the pipeline with paths for schema, source data, target Delta table, and checkpointing.
    - Executing the pipeline to process telemetry data using Databricks Autoloader.

    Workflow:
      1. Creates an instance of the `Telematics_ingestion` class.
      2. Passes configuration paths for schema (`schema.yml`), source data (S3 bucket), 
         target Delta table (`workspace.default.raw_telemetry`), and checkpointing (S3 bucket).
      3. Calls the `run_pipeline` method to start data ingestion and processing.

    Args:
        None

    Returns:
        None

    Notes:
      - Ensure that the S3 bucket paths (`source_path` and `checkpoint_path`) are accessible.
      - The `schema.yml` file should be correctly configured with the telemetry data schema.
      - The target Delta table (`workspace.default.raw_telemetry`) must exist or be created by the pipeline.
    """
    
    pipeline = Telematics_ingestion(
        spark=SparkSession.builder.appName('TelemetryApp').getOrCreate(),
        config_path="/Workspace/Users/email/vehicle-telemetry/config/schema.yml",
        source_path="s3://vehicletelemetry/",
        target_path="workspace.default.raw_telemetry",
        checkpoint_path="s3://vehiclepipelinecache/",
    )
    
    stream_query = pipeline.run_pipeline(spark)
    
if __name__ == "__main__":
    main()
