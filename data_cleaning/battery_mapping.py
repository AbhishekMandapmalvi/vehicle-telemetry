import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

def battery_mapping(data, schema_path):
    # Load schema from YAML file
    with open(schema_path, "r") as f:
        schema = yaml.safe_load(f)

    spark = SparkSession.builder.appName("TelemetryApp").getOrCreate()
    vehicles = schema["vehicle"]
    
    vehicle_schema = StructType(
        [StructField("vehicle_id", StringType(), True)] + 
        [StructField("commercial_name", StringType(), True)] + 
        [StructField("battery_pack_configuration", StringType(), True)] + 
        [StructField("battery_type", StringType(), True)] + 
        [StructField("form_factor", StringType(), True)] + 
        [StructField("battery_capacity", DoubleType(), True)] + 
        [StructField("nominal_voltage", DoubleType(), True)] + 
        [StructField("number_of_cell", IntegerType(), True)]
        )

    vehicle_dataframe = spark.createDataFrame(vehicles, schema=vehicle_schema)
    data = data.join(vehicle_dataframe, "vehicle_id")
    
    return data