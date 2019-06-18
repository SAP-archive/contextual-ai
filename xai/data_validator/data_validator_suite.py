from plugin.xai.data_validator.abstract_validator import AbstractValidator


class DataValidatorSuite:
    def __init__(self):
        self.validator_list = []
        self.metadata = {}

    def add_validator(self, validator: AbstractValidator):
        self.validator_list.append(validator)

    def validate_sample(self, sample):
        for validator in self.validator_list:
            validator.validate_sample(sample)

    def get_overall_metadata(self):
        for validator in self.validator_list:
            meta = validator.summarize_info()
            for key, value in meta.items():
                if key in self.metadata:
                    self.metadata[key].update(value)
                else:
                    self.metadata[key] = value
        return self.metadata
