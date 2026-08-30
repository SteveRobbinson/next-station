import logging
import sys

from pydantic import ValidationError

from next_station.infrastructure.runner import runner
from next_station.schemas.worldpop import ApiMetadata

logger = logging.getLogger(__name__)


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
