import requests
from requests.exceptions import HTTPError
import time

def check_server(api_url: str,
                 query: str | None = None,
                 max_retries: int = 3
                 ) -> bool:

    for i in range(max_retries):
        
        try: 

            response = requests.head(
                url = api_url,
                params = query,
                allow_redirects = True
            )
            
            response.raise_for_status()

            return True
            

        except HTTPError:
            
            if response.status_code == 400:
                print(f"Failed!: \n{response.text}")

                return False

            if response.status_code in (429, 500, 501, 502, 503, 504):
                   
                time.sleep((i + 1) * 4)
                print(f"Status code: {response.status_code}, retrying...")
                continue


        except Exception as err:

            print(f"Other error occurred: {err}")

            return False

        return False
