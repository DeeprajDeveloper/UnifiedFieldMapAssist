class CustomError(Exception):
    def __init__(self, error_message, error_code):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(error_message)


class RegexMismatch(CustomError):
    """Regex Pattern Mismatch"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="REGEX_MISMATCH")


class NoContent(CustomError):
    """No Content retrieved from the database"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="NO_CONTENT")


class DBDataExtraction(CustomError):
    """Error occurred while extracting data from the database"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DATABASE_EXTRACT_ERROR")


class InputIdOutOfRange(CustomError):
    """Verse ID is out of the defined range"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INDEX_OUT_OF_BOUND")


class InputMissing(CustomError):
    """No Input request provided"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INPUT_MISSING")


class OldValueMismatch(CustomError):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="OLV_VALUE_MISSING")


class InvalidAction(CustomError):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_ACTION")


class InvalidOperation(CustomError):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_OPERATION")


class InvalidReturnType(CustomError):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_RETURN_TYPE")


class InvalidPayload(CustomError):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_PAYLOAD")


class InvalidData(CustomError):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_DATA")


class InvalidRequest(CustomError):
    """Input JSON Request doesn't contain the required parameters"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_REQUEST")


class InvalidInputValues(CustomError):
    """Input values doesn't match the standards"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_INPUT")


class InvalidSearchParameter(CustomError):
    """Input values doesn't match the standards"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_SEARCH_PARAM")


class DataExists(CustomError):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DATA_EXISTS")

