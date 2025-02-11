import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

def battery_mapping(data, schema_path):
    """
    Enriches telemetry data by mapping vehicle metadata from a YAML schema file.

    This function reads vehicle metadata (e.g., battery configuration, type, capacity) 
    from a YAML schema file and joins it with the input telemetry data using the 
    `vehicle_id` field. The enriched data includes additional fields such as 
    `commercial_name`, `battery_pack_configuration`, `battery_type`, and more.

    Args:
        data (pyspark.sql.DataFrame): The input telemetry data as a PySpark DataFrame.
        schema_path (str): Path to the YAML file containing vehicle metadata.

    Returns:
        pyspark.sql.DataFrame: The enriched telemetry data with vehicle metadata added.
    """
    
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
