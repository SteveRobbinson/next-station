from src.next_station.core.spark import get_spark_session
from src.next_station.infrastructure.load_railway_stations import load_json_source
from src.next_station.quality.df_empty import is_df_empty
from src.next_station.quality.melt_table import melt_table
from src.next_station.core.config import settings
from src.next_station.infrastructure.databricks import save_df_in_db

new_databricks = settings.databricks.model_copy(update={'compute_config': 'sql'})

spark_session = get_spark_session(new_databricks.compute_config)

df = melt_table(df, settings.aws_railway_file_explode_by)

df = is_df_empty(df)

save_df_in_db(df, settings.databricks_railway_stations_table_id)
