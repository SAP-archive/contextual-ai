from xai.data.constants import DATATYPE


class AttributeNotFound(Exception):
    """
    Raised when an defined attribute name not found in the sample
    """

    def __init__(self, attribute_name, sample):
        message = 'Attribute name "{}" is not found in the sample: {}.'.format(attribute_name, sample)
        Exception.__init__(self, message)
        self.message = message


class InconsistentIteratorSize(Exception):
    """
    Raised when two iterator has different length
    """

    def __init__(self, length_A, length_B):
        message = 'Two iterator has different size: {}, {}.'.format(length_A, length_B)
        Exception.__init__(self, message)
        self.message = message


class AnalyzerDataTypeNotSupported(Exception):
    """
    Raised when two iterator has different length
    """

    def __init__(self, data_type):
        message = 'The data type `{}` is not supported.'.format(data_type)
        Exception.__init__(self, message)
        self.message = message


class ItemDataTypeNotSupported(Exception):
    """
    Raised when two iterator has different length
    """

    def __init__(self, data_type, analyzer_type, supported_types):
        message = 'The data type `{}` is not supported for {}. Please input one of the following supported data type:{}'.format(
            data_type, analyzer_type, supported_types)
        Exception.__init__(self, message)
        self.message = message


class NoItemsError(Exception):
    """
    Raised when no items was passed in the stats
    """

    def __init__(self, stats_type):
        message = 'No items passed to the stats object: {}.'.format(stats_type)
        Exception.__init__(self, message)
        self.message = message
