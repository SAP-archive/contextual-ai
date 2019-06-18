from xai.data_validator.abstract_validator import AbstractValidator
from typing import Dict, Iterator
from xai import constants

class MissingValueValidator(AbstractValidator):

    def __init__(self, schema_meta: Dict = None, feature_type_list: Dict = None):
        '''

        :param schema_meta: dict: for each feature, list of values which are considered as missing
        '''
        if schema_meta is None:  # use default type-based validator
            if feature_type_list is None:
                raise Exception('Not feature type defined, cannot use type-based validator.')
            else:
                schema_meta = dict()
                for type, features in feature_type_list.items():
                    for defined_type, default_values in constants.DEFAULT_VALUE.items():
                        if type == defined_type:
                            for feature in features:
                                schema_meta[feature] = default_values
        super(MissingValueValidator, self).__init__(schema_meta=schema_meta)

    def update_info(self, feature_name, feature_value):
        if feature_name not in self.schema_meta:
            self.schema_meta[feature_name] = []
        if feature_value in self.schema_meta[feature_name]:
            if feature_name in self.info_summary.keys():
                self.info_summary[feature_name] += 1
            else:
                self.info_summary[feature_name] = 1

    def validate_sample(self, sample: dict):
        ## TODO: consider other expections in value type
        for feature_name, feature_value in sample.items():
            if type(feature_value) == list:  ## consider each item if it's a list
                for item in feature_value:
                    self.update_info(feature_name, item)
            else:
                self.update_info(feature_name, feature_value)

    def validate_set(self, sample_list: Iterator[dict]):
        for item in sample_list:
            self.validate_sample(item)

    def summarize_info(self):
        return {constants.KEY_MISSING_VALUE_COUNTER: self.info_summary}
