import logging
from next_station.infrastructure.runner import runner
from next_station.core.exceptions.external import APIResponseError
import requests
from next_station.core.config.settings import settings

logger = logging.getLogger(__name__)

def fetch_train_stations(api_url: str,
                         payload: str,
                         headers: dict = settings.api.headers
                         ) -> requests.Response:

    logger.info(f"Starting to fetch railway_stations from {api_url}")
    response = None

    try:
        response = runner(api_url, 'post', payload, headers = headers, stream=True)

        logger.info(f"Successfully fetched railway stations from {api_url}")
        return response


    except Exception as err:
        logger.exception(f"Failed to fetch railway stations from {api_url}")
        raise APIResponseError(response) from err
