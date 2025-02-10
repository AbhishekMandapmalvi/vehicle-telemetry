%python
from autoloader import Telematics_ingestion
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def main():
    pipeline = Telematics_ingestion(
        spark=SparkSession.builder.appName('TelemetryApp').getOrCreate(),
        config_path="/Workspace/Users/abhishekrmandapmalvi@gmail.com/vehicle-telemetry/config/schema.yml",
        source_path="s3://vehicletelemetry/",
        target_path="workspace.default.raw_telemetry",
        checkpoint_path="s3://vehiclepipelinecache/",
    )
    
    stream_query = pipeline.run_pipeline(spark)
    
if __name__ == "__main__":
    main()