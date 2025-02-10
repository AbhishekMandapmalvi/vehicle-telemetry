from pyspark.sql import functions as F
from pyspark.sql.window import Window
import yaml

def interpolate_dataframe(data, schema_path):
    """
    Interpolates missing values in a DataFrame based on a schema configuration.

    Parameters:
        data (pyspark.sql.DataFrame): The input DataFrame containing data to interpolate.
        schema_path (str): Path to the YAML schema file defining interpolation rules.

    Returns:
        pyspark.sql.DataFrame: The DataFrame with interpolated values.
    """
    interpolation_time_diff = 10
    
    # Load schema from YAML file
    with open(schema_path, "r") as f:
        schema = yaml.safe_load(f)

    fields = schema["schema"]["fields"]

    # Check if 'vehicle_id' exists in the DataFrame
    if "vehicle_id" not in data.columns:
        raise ValueError("Column 'vehicle_id' does not exist in the DataFrame. Please provide a valid partition column.")

    # Iterate over fields to apply interpolation based on the schema
    for field in fields:
        if field["interpolation"]["enabled"]:
            column_name = field["name"]
            interpolation_type = field["interpolation"]["type"]

            # Define window specification (partition by an identifier, order by timestamp)
            window_spec = (
                Window.partitionBy("vehicle_id")  # Adjust based on your data structure
                .orderBy("timestamp")
            )

            if interpolation_type == "linear":
                # Linear interpolation: calculate previous and next values
                prev_value = F.lag(column_name).over(window_spec)
                next_value = F.lead(column_name).over(window_spec)
                prev_time = F.lag(F.unix_timestamp("timestamp")).over(window_spec)
                next_time = F.lead(F.unix_timestamp("timestamp")).over(window_spec)

                # Calculate interpolated value using linear formula
                interpolated_value = F.when(
                    (((next_time - prev_time) != 0) & ((next_time - prev_time) < interpolation_time_diff)),
                    prev_value +
                    ((F.unix_timestamp(F.col("timestamp")) - prev_time) /
                    (next_time - prev_time)) *
                    (next_value - prev_value)
                ).otherwise(prev_value)

                # Update column with interpolated values where null
                data = data.withColumn(
                    column_name,
                    F.when(F.col(column_name).isNull(), interpolated_value).otherwise(F.col(column_name))
                )

            elif interpolation_type == "zoh":
                # Zero-order hold: forward fill using last non-null value
                data = data.withColumn(
                    column_name,
                    F.last(column_name, ignorenulls=True).over(window_spec)
                )

    return data