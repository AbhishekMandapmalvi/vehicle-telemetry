from pyspark.sql import functions as F

def vehicle_status(df):
    """
    Determines the operational status of a vehicle based on speed and battery current.
    This function adds a new column, `vehicle_status`, to the input DataFrame. 
    The status is determined using the following logic:
    - "driving": Speed is greater than 1 km/h, and battery current is negative.
    - "recuperation": Speed is greater than 1 km/h, and battery current is positive.
    - "fault": Speed is less than or equal to -1 km/h, and battery current is negative.
    - "charging": Speed is near zero (between -1 and 1 km/h), and battery current is positive.
    - "parking": Speed is near zero (between -1 and 1 km/h), and battery current is zero.
    - "unknown": Any other condition not covered above.

    Args:
        df (pyspark.sql.DataFrame): The input DataFrame containing telemetry data.
        It must include the columns `speed_kmh` and `battery_current`.

    Returns:
        pyspark.sql.DataFrame: The DataFrame with an additional column `vehicle_status` indicating the operational status of the vehicle.
    """
    
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
