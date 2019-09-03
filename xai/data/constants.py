class DATATYPE:
    """
    Predefined data type for data analyzer
    """

    CATEGORY = 'categorical'
    NUMBER = 'numerical'
    FREETEXT = 'text'
    DATETIME = 'datetime'


class STATSCONSTANTS:
    """
    constants for stats generation
    """
    DEFAULT_BIN_SIZE = 20
    KDE_BAND_WIDTH = 0.2
    KDE_XGRID_RESOLUTION = 100


class STATSKEY:
    """
    constants for key used in stats json object
    """
    TOTAL_COUNT = 'total_count'
    DATA_TYPE = 'data_type'
    DATA_COLUMN_NAME = 'attribute_name'

    DISTRIBUTION = 'frequency'
    FIELDS = 'fields'

    class DISTRIBUTION_KEY:
        ATTRIBUTE_NAME = 'value'
        ATTRIBUTE_COUNT = 'count'

    HISTOGRAM = 'distribution'

    class HISTOGRAM_KEY:
        X_LEFT = 'bin_left_edge'
        X_RIGHT = 'bin_right_edge'
        BIN_COUNT = 'bin_count'

    KDE = 'kernel_density_estimation'

    class KDE_KEY:
        X = 'x'
        Y = 'y'

    MIN = 'minimum'
    MAX = 'maximum'
    MEAN = 'mean'
    MEDIAN = 'median'
    STDDEV = 'standard_deviation'

    TFIDF = 'tfidf'
    TF = 'term_frequency'
    DF = 'document_frequency'
    PATTERN = 'pattern'

    class PATTERN:
        PATTERN_NAME = 'pattern_name'
        PATTERN_TF = 'occurrence'
        PATTERN_DF = 'doc_with_pattern'
