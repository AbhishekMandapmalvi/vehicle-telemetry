from pyspark.sql import functions as F

def vehicle_status(df):
    df = df.withColumn(
        "vehicle_status",
        F.when((df.speed_kmh > 0) | (df.battery_current < 0), "driving")
         .when((df.speed_kmh == 0) & (df.battery_current > 0), "charging")
         .otherwise("idle")
    )
    return df