from pyspark.sql import DataFrame
from pyspark.sql.functions import explode

def explode_and_flatten(df: DataFrame,
                        explode_by: str
                        ) -> DataFrame:
    
    df_long = df.select(explode(explode_by).alias('node'))
    return df_long.select('node.*')
