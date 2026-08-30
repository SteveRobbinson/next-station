import logging
import sys
import time

from pydantic import ValidationError

from next_station.infrastructure.runner import runner
from next_station.schemas.worldpop import ApiMetadata

logger = logging.getLogger(__name__)

def _perform_backoff(current_retry_count: int,
                     base_delay: int = 1,
                     backoff_factor: int = 5,
                     max_delay: int = 60):

    delay = base_delay + (backoff_factor ** current_retry_count)
    sleep_time = min(delay, max_delay)

    time.sleep(sleep_time)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True
        )

def get_api_object_metadata(file_url: str) -> str:
    try:
        api_response = runner(file_url, 'head')
        api_metadata = ApiMetadata(**api_response.headers).etag

        return api_metadata

    except ValidationError as err:
        logger.error(f"Parsing metadata from {file_url} failed, {err.errors()}")
        raise
