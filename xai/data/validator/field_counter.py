from xai.data_validator.abstract_validator import AbstractValidator
from typing import Iterator
from xai import constants


class FieldCounter(AbstractValidator):

    def __init__(self,feature_list):
        '''

        :param schema_meta: dict: for each feature, list of values which are considered as missing
        '''
        schema_meta = {}
        for fea in feature_list:
            schema_meta[fea] = None
        super(FieldCounter, self).__init__(schema_meta=schema_meta)

    def update_info(self, feature_name, value):
        if feature_name in self.info_summary.keys():
            self.info_summary[feature_name] += value
        else:
            self.info_summary[feature_name] = value

    def validate_sample(self, sample: dict):
        ## TODO: consider other expections in value type
        for feature_name, feature_value in sample.items():
            if feature_name not in self.schema_meta.keys():
                continue
            if type(feature_value) == str:
                self.update_info(feature_name, 1)
            elif type(feature_value) == list:
                self.update_info(feature_name, len(feature_value))
            else:
                self.update_info(feature_name, 1)

    def validate_set(self, sample_list: Iterator[dict]):
        for item in sample_list:
            self.validate_sample(item)

    def summarize_info(self):
        return {constants.KEY_FIELD_COUNTER: self.info_summary}
