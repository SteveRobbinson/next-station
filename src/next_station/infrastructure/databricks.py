from pyspark.sql import DataFrame

def save_df_in_db(df: DataFrame,
                  table_name: str,
                  save_format: str = 'delta',
                  save_mode: str = 'overwrite'):


    df.write.format(save_format).mode(save_mode).saveAsTable(table_name)
