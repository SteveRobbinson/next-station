from src.next_station.providers.fetch_railway_stations import fetch_train_stations
from src.next_station.core.config import settings
from src.next_station.infrastructure.s3 import create_s3_client, upload_data_to_s3

s3 = create_s3_client()

train_stations = fetch_train_stations(settings.train_stations_url,
                                      settings.query_for_train_stations)

upload_data_to_s3(settings.aws_bucket_name,
                  settings.aws_train_file_name,
                  train_stations,
                  s3)
