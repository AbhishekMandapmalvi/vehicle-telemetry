import yaml
from pyspark.sql.functions import col

def apply_constraints(df, schema_path):
    """
    Filters a PySpark DataFrame based on min/max constraints defined in a YAML schema.
    
    Args:
        df (pyspark.sql.DataFrame): Input DataFrame to be filtered.
        schema_path (str): Path to the YAML schema file containing constraints.
    
    Returns:
        pyspark.sql.DataFrame: Filtered DataFrame with rows violating constraints removed.
    """
    # Load the schema from the YAML file
    with open(schema_path, "r") as schema_file:
        schema = yaml.safe_load(schema_file)
    
    # Extract fields with constraints
    fields_with_constraints = [
        field for field in schema["schema"]["fields"]
        if "constraints" in field
    ]
    
    # Apply filters for each constrained field
    for field in fields_with_constraints:
        column_name = field["name"]
        constraints = field["constraints"]
        
        # Apply min constraint
        if "min" in constraints:
            df = df.filter((col(column_name) >= constraints["min"]) | col(column_name).isNull())
        
        # Apply max constraint
        if "max" in constraints:
            df = df.filter((col(column_name) <= constraints["max"]) | col(column_name).isNull())
    
    return df
