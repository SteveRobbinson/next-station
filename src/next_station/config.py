from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    train_stations_url: str
    population_grid_url: str
    query_for_train_stations: str
    aws_bucket_name: str
    aws_train_file_name: str
    aws_grid_file_name: str

settings = Settings()
