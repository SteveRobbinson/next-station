import logging

from pydantic import ValidationError

from next_station.core.exceptions.api import APIResponseError
from next_station.infrastructure.runner import execute_request
from next_station.schemas.http import APIEndpointConfig
from next_station.schemas.worldpop import ApiMetadata, GetFileUrl

logger = logging.getLogger(__name__)


def get_file_url(api_url: str, index: int = -1, redirect: bool = True) -> str:
    logger.info(f"Retrieving file_url from {api_url}")

    try:
        api_endpoint = APIEndpointConfig(
            method="GET", url=api_url, allow_redirects=True
        )
        response = execute_request(api_endpoint)
        response = response.json()
        result = GetFileUrl(**response)

        logger.info(f"Successfully retrieved file url from {api_url}")
        return result[index]

    except Exception as err:
        logger.exception(f"Critical error during file URL retrieval from {api_url}")
        raise APIResponseError() from err


def fetch_metadata(file_url: str) -> str:
    try:
        api_endpoint = APIEndpointConfig(method="HEAD", url=file_url)
        api_response = execute_request(api_endpoint)
        api_metadata = ApiMetadata(**api_response.headers).etag

        return api_metadata

    except ValidationError as err:
        logger.error(f"Parsing metadata from {file_url} failed, {err.errors()}")
        raise
