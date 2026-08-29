from next_station.core.exceptions.base import BaseAppError

class APIRelatedError(BaseAppError):
    default_message = "An API-related error occurred."

class APIResponseError(APIRelatedError):
    default_message = "Received an error response from the external API."

class APITimeoutError(APIRelatedError):
    default_message = "The request to the external API timed out."
