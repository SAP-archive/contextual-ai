class DomainNotSupported(Exception):
    def __init__(self, domain):
        message = 'Domain {} is currently not supported.'.format(domain)
        Exception.__init__(self, message)
        self.message = message


class AlgorithmNotFoundInDomain(Exception):
    def __init__(self, domain, algorithm):
        message = 'Algorithm {} is not found in domain {}.'.format(algorithm, domain)
        Exception.__init__(self, message)
        self.message = message


class ExplainerUninitializedError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message

class UnsupportedModeError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message
