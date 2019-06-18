import json
import os
import xai.constants as Const
import logging
from xai.data_explorer.text_analyzer import TextAnalyzer
from xai.data_explorer.categorical_analyzer import CategoricalAnalyzer
from xai.data_explorer.numeric_analyzer import NumericAnalyzer
from xai.data_explorer.sequence_length_analyzer import SequenceLengthAnalyzer
from xai.data_explorer.data_analyzer_suite import DataAnalyzerSuite

from xai.data_validator.data_validator_suite import DataValidatorSuite
from xai.data_validator.field_counter import FieldCounter
from xai.data_validator.missing_value_validator import MissingValueValidator

LOGGER = logging.getLogger(__name__)


class DataAnalysis:
    def __init__(self, att_fea, seq_fea, label_key, label_type):
        self.data_file = None
        self.label_analyzer = None

        if label_type == Const.KEY_FEATURE_CATEGORICAL_TYPE:
            self.label_analyzer = CategoricalAnalyzer(feature_list=[label_key])
        elif label_type == Const.KEY_FEATURE_NUMERIC_TYPE:
            self.label_analyzer = NumericAnalyzer(feature_list=[label_key])

        self.feature_type_list = {}
        for type in Const.DATA_ANALYSIS_TYPES:
            self.feature_type_list[type] = att_fea[type] + seq_fea[type]

        self.att_fea = att_fea
        self.seq_fea = seq_fea

        flatten_seq_fea = []
        for features in self.seq_fea.values():
            flatten_seq_fea.extend(features)

        self.total_count = 0
        self.label_key = label_key
        self.label_type = label_type

        # initialize validator suite

        self.validator_suite = DataValidatorSuite()
        self.validator_suite.add_validator(MissingValueValidator(feature_type_list=self.feature_type_list))
        self.validator_suite.add_validator(FieldCounter())

        # initialize analyzer suite

        self.analyzer_suite = DataAnalyzerSuite()
        self.analyzer_suite.add_analyzer(self.label_analyzer)
        self.analyzer_suite.add_analyzer(CategoricalAnalyzer(
            feature_list=self.feature_type_list[Const.KEY_FEATURE_CATEGORICAL_TYPE]))
        self.analyzer_suite.add_analyzer(NumericAnalyzer(feature_list=self.feature_type_list[Const.KEY_FEATURE_NUMERIC_TYPE]))
        self.analyzer_suite.add_analyzer(TextAnalyzer(feature_list=self.feature_type_list[Const.KEY_FEATURE_TEXT_TYPE]))
        self.analyzer_suite.add_analyzer(SequenceLengthAnalyzer(feature_list=flatten_seq_fea))

    def input_data(self, file_name):
        self.data_file = file_name
        self.update_metadata({Const.KEY_FILENAME: self.data_file})

    def _get_sample_iter(self):
        with open(self.data_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                yield data

    def feature_distribution(self):
        if self.data_file is None:
            LOGGER.info('Please input a data file.')
            return

        for idx, sample in enumerate(self._get_sample_iter()):
            self.total_count += 1

            # validate sample
            self.validator_suite.validate_sample(sample)

            if self.label_key in sample:
                if self.label_type == Const.KEY_FEATURE_CATEGORICAL_TYPE:
                    label_value = sample[self.label_key]
                elif self.label_type == Const.KEY_FEATURE_NUMERIC_TYPE:
                    label_value = 'all'  # set back to None if numeric
            else:
                label_value = 'all'

            # analyze distribution for sample
            self.analyzer_suite.analyze_sample(sample=sample, class_value=label_value)

            # logging count
            if (idx + 1) % 1000 == 0:
                print('Processed %s samples.' % (idx + 1))

        # aggregate distribution information

        self.analyzer_suite.aggregate()

        # update overall metadata
        self.update_metadata(self.analyzer_suite.get_overall_metadata())
        self.update_metadata(self.validator_suite.get_overall_metadata())


    def update_metadata(self, updated_meta):
        if not hasattr(self, 'meta_json'):
            self.meta_json = {}
        for k in updated_meta.keys():
            if k not in self.meta_json.keys():
                self.meta_json.update(updated_meta)
            else:
                self.meta_json[k].update(updated_meta[k])

    def data_distribution(self):
        if self.data_file is None:
            LOGGER.info('Please input a data file.')
            return
        if self.label_analyzer is None:
            LOGGER.info('Label distribution is not analyzed')
            return
        self.meta_json[Const.KEY_DATA_DISTRIBUTION] = self.label_analyzer.summary_info[self.label_key]['all']
        return self.meta_json[Const.KEY_DATA_DISTRIBUTION]

    def generate_meta_data(self, meta_data_name):
        self.meta_json['total_count'] = self.total_count
        with open(meta_data_name, 'w') as f:
            json.dump(self.meta_json, f)
        return self.meta_json


def prepare_data_metafile(data_folder, file_params={}):
    LOGGER.info('Start preparing metadata for raw data...')

    all_meta = {}

    for data_key, data_params in file_params.items():
        if os.path.exists(os.path.join(data_folder, data_params['data_file'])):
            LOGGER.info('Prepare for dataset %s' % data_key)
            all_meta[data_key] = generate_datavis_meta(data_folder=data_folder, data_file=data_params['data_file'],
                                                       metafile_name=data_params['metafile_name'],
                                                       att_fea=data_params['att_fea'],
                                                       seq_fea=data_params['seq_fea'],
                                                       label_type=data_params['label_type'],
                                                       label_key=data_params['label_key'])
        else:
            print('Cannot find %s' % os.path.join(data_folder, data_params['data_file']))
        LOGGER.info('Finish preparing metadata for raw data!')

    return all_meta


def generate_datavis_meta(data_folder, data_file, metafile_name, att_fea, seq_fea, label_key, label_type):
    metadata_fpath = os.path.join(data_folder, 'meta_%s.json' % metafile_name)
    if os.path.exists(metadata_fpath):
        with open(metadata_fpath, 'r') as f:
            meta_json = json.load(f)
            return meta_json
    print('Start generated meta file for:', data_file)

    data_analysis = DataAnalysis(att_fea, seq_fea, label_key, label_type)
    LOGGER.info('=============================================')
    LOGGER.info('Start analysis for data: %s' % metafile_name)
    data_analysis.input_data(os.path.join(data_folder, data_file))

    LOGGER.info('Get feature distribution...')
    data_analysis.feature_distribution()

    LOGGER.info('Get data distribution...')
    data_analysis.data_distribution()

    LOGGER.info('Generate meta file...')

    meta_json = data_analysis.generate_meta_data(metadata_fpath)
    print('Generated meta file:', metadata_fpath)
    return meta_json
