from src.next_station.core.exceptions.mappings import api_errors

class UnifiedAPIError(Exception):
    error_map: dict[int, str] = api_errors
    
    def __init__(self, source: str, status_code: int, details: str = 'No additional details'):
        self.source = source
        self.status_code = status_code
        self.message = self.error_map.get(self.status_code, self.error_map[0])
        self.details = details
        
        title = f"{source} - Status code: {status_code}\nDetails: {details}\nMessage: {self.message}"

        super().__init__(title)
