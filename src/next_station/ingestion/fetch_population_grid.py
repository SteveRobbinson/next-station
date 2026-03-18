from .runner import runner
import requests

def fetch_population_grid(api_url: str,
                          is_metadata_same: bool
                          ) -> requests.Response | None:

    if not is_metadata_same:
        return runner(api_url, 'get', stream=True)
