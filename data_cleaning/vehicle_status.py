from pyspark.sql import functions as F

def vehicle_status(df):
    df = df.withColumn(
        "vehicle_status",
        F.when((df.speed_kmh > 1) & (df.battery_current < 0), "driving")
         .when((df.speed_kmh > 1) & (df.battery_current > 0), "recuperation")
         .when((df.speed_kmh <= -1) & (df.battery_current < 0), "fault")
         .when(((df.speed_kmh < 1) & (df.speed_kmh > -1)) & (df.battery_current > 0), "charging")
         .when(((df.speed_kmh < 1) & (df.speed_kmh > -1)) & (df.battery_current == 0), "parking")
         .otherwise("unknown")
    )
    return df
