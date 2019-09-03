class AttributeNotFound(Exception):
    """
    Raised when an defined attribute name not found in the sample
    """

    def __init__(self, attribute_name, sample):
        message = 'Attribute name "{}" is not found in the sample: {}.'.format(attribute_name, sample)
        Exception.__init__(self, message)
        self.message = message


class ColumnNotFound(Exception):
    """
    Raised when an defined column name not found in the dataframe
    """

    def __init__(self, column_name, columns):
        message = 'Column name "{}" is not found in the dataframe: {}.'.format(column_name, columns)
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


class InconsistentSize(Exception):
    """
    Raised when two lists have different lengths
    """

    def __init__(self, column_A, column_B, length_A, length_B):
        message = '"{}" is different from "{}" has different size: {}, {}.'.format(column_A, column_B, length_A,
                                                                                   length_B)
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


class InvalidTypeError(Exception):
    """
    Raised when object type is invalid
    """

    def __init__(self, att_name, obj_type, supported_types):
        message = "The '{}' type [{}] is invalid, should be {} .".format(att_name, obj_type, supported_types)
        Exception.__init__(self, message)
        self.message = message


class InvalidSizeError(Exception):
    """
    Raised when object type is invalid
    """

    def __init__(self, att_name, obj_size, supported_sizes):
        message = "The '{}' has invalid size: {}, should be {} .".format(att_name, obj_size, supported_sizes)
        Exception.__init__(self, message)
        self.message = message
