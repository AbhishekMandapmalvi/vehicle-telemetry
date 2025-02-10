# Databricks notebook source
# DBTITLE 1,library import
import yaml
from datetime import datetime
from vehicle_status import vehicle_status
from apply_constraints import apply_constraints
from interpolation import interpolate_dataframe
from battery_mapping import battery_mapping
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import to_timestamp, to_unix_timestamp, col, lit, when

# COMMAND ----------

# DBTITLE 1,initiate spark session
spark = SparkSession.builder.appName("TelemetryApp").getOrCreate()

# COMMAND ----------

# DBTITLE 1,load data
data = spark.table("workspace.default.raw_telemetry")

# COMMAND ----------

# DBTITLE 1,load specs
dataclean_specs = "/Workspace/Users/abhishekrmandapmalvi@gmail.com/vehicle-telemetry/config/schema.yml"
battery_specs = "/Workspace/Users/abhishekrmandapmalvi@gmail.com/vehicle-telemetry/config/vehicle_hash_table.yml"

# COMMAND ----------

# DBTITLE 1,remove outbound values
data = apply_constraints(data, dataclean_specs)

# COMMAND ----------

# DBTITLE 1,apply battery mapping
data = battery_mapping(data, battery_specs)

# COMMAND ----------

# DBTITLE 1,process timestamps
data = data.withColumn("timestamp", to_timestamp("timestamp")) \
           .withColumn("unix_timestamp", to_unix_timestamp("timestamp"))

# COMMAND ----------

# DBTITLE 1,clean current for vehicle status
data = data.withColumn(
                "battery_current",
                when(
                    (((col("battery_current") > 0) & (col("speed_kmh") > 0)) |
                    ((col("battery_current") < 0) & (col("speed_kmh") <= 0))),
                    lit(None)
                ).otherwise(col("battery_current"))
                )

# COMMAND ----------

# DBTITLE 1,interpolate
data = interpolate_dataframe(data, dataclean_specs)

# COMMAND ----------

# DBTITLE 1,apply vehicle status
data = vehicle_status(data)

# COMMAND ----------

data.select("number_of_cell").dtypes

# COMMAND ----------

# DBTITLE 1,Write data to delta lake
data.write.format("delta").mode("overwrite").saveAsTable("workspace.default.cleaned_telemetry")