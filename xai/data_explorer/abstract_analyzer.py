from abc import abstractmethod, ABC


class AbstractAnalyzer(ABC):
    def __init__(self,feature_list):
        self.feature_list=feature_list

    @abstractmethod
    def analyze_sample(self):
        raise NotImplementedError('The derived helper needs to implement it.')

    @abstractmethod
    def aggregate(self):
        raise NotImplementedError('The derived helper needs to implement it.')

    @abstractmethod
    def summarize_info(self):
        raise NotImplementedError('The derived helper needs to implement it.')

