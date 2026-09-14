import logging
import time

import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout

from next_station.core.exceptions.api import (
    APIRelatedError,
    APIResponseError,
    APITimeoutError,
)
from next_station.schemas.http import APIEndpointConfig

logger = logging.getLogger(__name__)


def _perform_backoff(
    current_retry_count: int,
    base_delay: int = 1,
    backoff_factor: int = 5,
    max_delay: int = 60,
) -> None:

    delay = base_delay + (backoff_factor**current_retry_count)
    sleep_time = min(delay, max_delay)

    time.sleep(sleep_time)


def send_api_request(
    api_endpoint: APIEndpointConfig, max_retries: int = 3
) -> requests.Response:

    for i in range(max_retries):
        try:
            api_endpoint_config = api_endpoint.get_request_config()
            response = requests.request(**api_endpoint_config)
            response.raise_for_status()
            logger.info(f"Request to {api_endpoint_config['url']} succeeded")
            return response

        except (Timeout, ConnectionError) as err:
            if i == max_retries - 1:
                raise APITimeoutError() from err

            logger.warning(
                f"Attempt {i + 1} failed. \nError: {type(err).__name__}\n{err}\nRetrying..."
            )
            _perform_backoff(i)
            continue

        except HTTPError as err:
            status_code = err.response.status_code

            if status_code in [429, 500, 501, 502, 503, 504] and i < max_retries - 1:
                logger.warning(
                    f"Attempt {i + 1} failed with status {status_code}. Retrying..."
                )
                _perform_backoff(i)
                continue

            raise APIResponseError() from err

    raise APIRelatedError()
