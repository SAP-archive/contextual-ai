from xai.data.validator.abstract_validator import AbstractValidator
from xai.data.validator.enum_validation_stats import EnumValidationStats

from typing import Dict
from xai.data.exceptions import AttributeNotFound


class EnumValidator(AbstractValidator):

    def __init__(self, schema: Dict):
        super(EnumValidator).__init__(schema=schema)
        self._column_count = dict()
        self._total_count = 0

    def validate(self, sample: Dict):
        keys_not_found = list()
        validate_result = dict()
        for feature_name, enum_values in self.schema.items():
            if feature_name not in sample:
                keys_not_found.append(feature_name)
            else:
                if sample[feature_name] in enum_values:
                    validate_result[feature_name] = True
                    self._column_count[feature_name] += 1
                else:
                    validate_result[feature_name] = False
        if len(keys_not_found) > 0:
            raise AttributeNotFound(attribute_name=keys_not_found, sample=sample)
        else:
            return validate_result

    def get_statistics(self) -> Dict:
        stats = EnumValidationStats()
        stats.update_stats(column_stats=self._column_count, total_count=self._total_count)
        return stats.to_json()
