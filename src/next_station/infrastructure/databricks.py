from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import concat_ws

def save_df_in_db(df: DataFrame,
                  databricks_address: tuple[str, str, str],
                  save_format: str = 'delta',
                  save_mode: str = 'overwrite'):


    (df.write
    .format(save_format)
    .mode(save_mode)
    .option('mergeSchema', True)
    .saveAsTable('.'.join(databricks_address))
     )
