from .runner import runner
from schemas.worldpop import GetFileUrl, FileUrl

def get_file_url(api_url: str,
                 index: int
                 ) -> str:

    response = runner(api_url, 'get')
    response = response.json()

    result = GetFileUrl(**response)

    return result[index]
