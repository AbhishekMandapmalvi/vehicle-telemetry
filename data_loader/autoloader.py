import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DateType, DoubleType, StructField
from pyspark.sql.functions import *

class Telematics_ingestion:
    def __init__(self, spark, config_path, source_path, target_path, checkpoint_path):
        self.spark = spark
        self.schema_config = self.load_config(config_path)
        self.source_path = source_path
        self.target_path = target_path
        self.checkpoint_path = checkpoint_path
        self.schema = self.build_schema()

    @staticmethod
    def load_config(schema_config):
        """Load and validate YAML file configurations"""
        with open(schema_config, "r") as f:
            config = yaml.safe_load(f)
        
        return config
    
    def build_schema(self):
        """Build schema from configuration"""
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