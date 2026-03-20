from src.next_station.ingestion.fetch_train_stations import fetch_train_stations
from src.next_station.config import settings
from src.next_station.ingestion.upload_data_to_s3 import upload_data_to_s3
import boto3

s3 = boto3.client('s3')

train_stations = fetch_train_stations(settings.train_stations_url,
                                      settings.query_for_train_stations)

upload_data_to_s3(settings.aws_bucket_name,
                  settings.aws_train_file_name,
                  train_stations,
                  s3)
