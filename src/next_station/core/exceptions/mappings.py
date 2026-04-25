aws_config_errors = {
    # --- 4xx Client Errors ---
    400: "Bad Request. The parameters provided are invalid or malformed.",
    401: "Unauthorized. Authentication is required or has failed. Check your credentials.",
    403: "Forbidden. You do not have permission to access this resource or perform this action.",
    404: "Not Found. The requested resource (file, record, or bucket) could not be located.",
    408: "Request Timeout. The server timed out waiting for the request. Check your connection.",
    409: "Conflict. The resource already exists or there is a state conflict.",
    422: "Unprocessable Entity. Validation failed for the provided data.",
    429: "Too Many Requests. Rate limit exceeded. Please implement a retry with backoff.",

    # --- 5xx Server Errors ---
    500: "Internal Server Error. An unexpected error occurred on the server side.",
    502: "Bad Gateway. The server received an invalid response from the upstream service.",
    503: "Service Unavailable. The server is temporarily overloaded or down for maintenance.",
    504: "Gateway Timeout. The upstream server failed to respond in time.",

    # --- Fallback ---
    0: "Unknown Error. An unmapped error occurred while processing the request."
}

aws_response_errors = {
    # --- 401 Unauthorized ---
    "UnrecognizedClientException": 401,
    "ExpiredToken": 401,
    "InvalidClientTokenId": 401,
    "NotAuthorizedException": 401,

    # --- 403 Forbidden ---
    "AccessDenied": 403,
    "AccessDeniedException": 403,

    # --- 404 Not Found ---
    "NoSuchBucket": 404,
    "NoSuchKey": 404,
    "ResourceNotFoundException": 404,
    "EntityNotFoundException": 404,

    # --- 409 Conflict ---
    "BucketAlreadyExists": 409,
    "BucketAlreadyOwnedByYou": 409,
    "EntityAlreadyExists": 409,
    "ResourceAlreadyExistsException": 409,

    # --- 429 Too Many Requests ---
    "Throttling": 429,
    "ThrottlingException": 429,
    "RequestLimitExceeded": 429,
    "ProvisionedThroughputExceededException": 429,

    # --- 400 Bad Request ---
    "ValidationException": 400,
    "InvalidParameterValue": 400,
    "MissingParameter": 400,

    # --- 5xx Server Errors ---
    "InternalFailure": 500,
    "InternalServerError": 500,
    "ServiceUnavailable": 503
}
