class InvalidExplanationFormat(Exception):
    """
    Raised when an explanation is not of a valid format
    """

    def __init__(self, exp):
        message = 'The following explanation has invalid format! The entire explanation will be ignored. {}'.format(exp)
        Exception.__init__(self, message)
        self.message = message


class MutipleScoresFoundForSameFeature(Exception):
    """
    Raised when multiple scores are found for the same feature in the explanation
    """

    def __init__(self, feature_name, exp):
        message = 'The following explanation has more than one score for feature [{}]! ' \
                  'The entire explanation will be ignored. {}'.format(
            feature_name, exp)
        Exception.__init__(self, message)
        self.message = message


class UnsupportedStatsType(Exception):
    """
    Raised when stats type is not supported.
    """

    def __init__(self, stats_type):
        message = 'The stats type [{}] is currently not supported. '.format(stats_type)
        Exception.__init__(self, message)
        self.message = message


class InvalidArgumentError(Exception):
    """
    Raised when the argument is not valid..
    """

    def __init__(self, arg_name, valid_type):
        message = 'The argument [{}] is not of valid type [{}]. '.format(arg_name, valid_type)
        Exception.__init__(self, message)
        self.message = message
