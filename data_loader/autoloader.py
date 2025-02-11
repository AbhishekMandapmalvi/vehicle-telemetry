import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DateType, DoubleType, StructField
from pyspark.sql.functions import *

class Telematics_ingestion:
    def __init__(self, spark, config_path, source_path, target_path, checkpoint_path):
        """
        Initializes the Telematics_ingestion class with Spark session and configuration paths.

        Args:
            spark (SparkSession): The active Spark session.
            config_path (str): Path to the YAML configuration file defining the schema.
            source_path (str): Path to the source directory containing telemetry JSON files.
            target_path (str): Target Delta table path where processed data will be written.
            checkpoint_path (str): Path for storing checkpoint data for streaming.

        Attributes:
            schema_config (dict): Loaded schema configuration from the YAML file.
            schema (StructType): PySpark schema built from the configuration file.
        """
        self.spark = spark
        self.schema_config = self.load_config(config_path)
        self.source_path = source_path
        self.target_path = target_path
        self.checkpoint_path = checkpoint_path
        self.schema = self.build_schema()

    @staticmethod
    def load_config(schema_config):
        """
        Loads and validates the YAML configuration file.

        Args:
            schema_config (str): Path to the YAML file containing schema configurations.

        Returns:
            dict: Parsed YAML configuration as a dictionary.

        Raises:
            FileNotFoundError: If the YAML file does not exist.
            yaml.YAMLError: If there is an error in parsing the YAML file.
        """
        with open(schema_config, "r") as f:
            config = yaml.safe_load(f)
        
        return config
    
    def build_schema(self):
        """
        Builds a PySpark schema based on the loaded YAML configuration.
        The method maps field types from the YAML configuration to PySpark data types 
        and constructs a `StructType` schema for use in reading telemetry data.

        Returns:
            StructType: PySpark schema built from the YAML configuration.

        Raises:
            ValueError: If an unsupported data type is encountered in the YAML configuration.
        """
        type_mapping = {
            'string': StringType,
            'double': DoubleType
            }
        
        fields = []
        for field in self.schema_config['schema']['fields']:
            try:
                spark_type = type_mapping[field['type']]()
                fields.append(
                    StructField(
                        name=field['name'],
                        dataType=spark_type,
                        nullable=field.get('nullable', False)
                        )
                    )
            except KeyError as e:
                raise ValueError(f"Unsupported data type: {field['type']}") from e
        
        return StructType(fields)

    def run_pipeline(self, spark):
        """
        Executes the streaming ingestion pipeline to process telemetry data using Databricks Autoloader.

        This method leverages Databricks Autoloader to read JSON files from the source path as a streaming 
        DataFrame using the defined schema. It writes the processed data to a Delta table in append mode, 
        with checkpointing enabled for fault tolerance.

        Databricks Autoloader is a highly scalable and efficient file ingestion utility that automatically 
        detects new files in cloud storage and processes them incrementally.

        Args:
            spark (SparkSession): The active Spark session.

        Raises:
            Exception: If any error occurs during streaming read or write operations.

        Workflow:
          1. Reads JSON files from `source_path` using Databricks Autoloader (`readStream` with `cloudFiles`).
          2. Applies the defined schema during ingestion.
          3. Writes processed data to `target_path` Delta table in append mode with checkpointing.
          4. Uses `availableNow` trigger for batch-like processing of currently available files.
          
          Logs messages during execution for tracking progress and errors.
        """
        try:
            # Streaming read with schema and constraints
            print("Starting streaming read...")
            streaming_df = spark.readStream \
                .format("cloudFiles") \
                .option("cloudFiles.format", "json") \
                .schema(self.schema) \
                .load(self.source_path)

            print("Starting write stream...")
            query = streaming_df.writeStream \
                .trigger(availableNow=True) \
                .format("delta") \
                .outputMode("append") \
                .option("checkpointLocation", self.checkpoint_path) \
                .toTable(self.target_path)
            print("Write stream started successfully.")
            
        except Exception as e:
            print(f"Error in run_pipeline: {e}")
            raise

    def log(self, message):
        """Log messages to the console"""
        self.spark.sparkContext.setLogLevel("INFO")
        self.spark.sparkContext.log.info(f"[TelemetryPipeline]{message}")
