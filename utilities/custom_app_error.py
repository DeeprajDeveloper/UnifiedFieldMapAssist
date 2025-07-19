from .base import ErrorClass


class RegExMismatch(ErrorClass):
    """Regex Pattern Mismatch"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="REGEX_MISMATCH")


class NoContent(ErrorClass):
    """No Content retrieved from the database"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="NO_CONTENT")


class DBDataExtract(ErrorClass):
    """Error occurred while extracting data from the database"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DATABASE_EXTRACT_ERROR")


class IndexOutOfRange(ErrorClass):
    """ID is out of the defined range"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INDEX_OUT_OF_BOUND")


class MissingInput(ErrorClass):
    """No Input request provided"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INPUT_MISSING")


class MissingOldValue(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="OLV_VALUE_MISSING")


class MissingMandatoryKeys(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="MANDATORY_KEY_MISSING")


class InvalidAction(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_ACTION")


class InvalidOperation(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_OPERATION")


class InvalidReturnType(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_RETURN_TYPE")


class InvalidPayload(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_PAYLOAD")


class InvalidData(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_DATA")


class InvalidRequest(ErrorClass):
    """Input JSON Request doesn't contain the required parameters"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_REQUEST")


class InvalidInputValues(ErrorClass):
    """Input values doesn't match the standards"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_INPUT")


class InvalidSearchParameter(ErrorClass):
    """Input values doesn't match the standards"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="INVALID_SEARCH_PARAM")


class DataExists(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DATA_EXISTS")


class PageNumberOutOfRange(ErrorClass):
    """Provided old value does not match the original value"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="PAGE_NUMBER_OUT_OF_RANGE")


class PandasGenericAppError(ErrorClass):
    def __init__(self, message):
        super().__init__(error_message=message, error_code="PANDA_GENERIC_ERROR")


class PandasDataframeAppError(ErrorClass):
    def __init__(self, message):
        super().__init__(error_message=message, error_code="PANDA_DATAFRAME_ERROR")


class ValueMismatch(ErrorClass):
    def __init__(self, message):
        super().__init__(error_message=message, error_code="VALUE_MISMATCH")
