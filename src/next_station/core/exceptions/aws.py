from next_station.core.exceptions.base import BaseAppError

class AWSRelatedError(BaseAppError):
    default_message = "An AWS-related error occurred."

class AWSConfigError(AWSRelatedError):
    default_message = "Failed to load or validate AWS configuration."

class AWSResponseError(AWSRelatedError):
    default_message = "Received an invalid or error response from AWS service."
