import os
import json
from xai import constants
from collections import defaultdict


class Params:
    def __init__(self, path):
        self.folder_path = path
        self.seq_fea = None
        self.att_fea = None
        self.label_type = None
        self.label_key = None

        report_metadata_path = os.path.join(self.folder_path, 'report_meta.json')
        if not os.path.exists(report_metadata_path):
            raise FileNotFoundError("'report_meta.json' is not found!")

        with open(report_metadata_path, 'r') as f:
            report_setup_meta = json.load(f)

        label_keys = report_setup_meta['data_analysis']['label_keys']
        label_type = report_setup_meta['data_analysis']['label_type']
        self.vis_params = dict()
        if 'show_sample_classes' in report_setup_meta['visualize_setup']:
            self.vis_params['show_sample_classes'] = report_setup_meta['visualize_setup']['show_sample_classes']
        else:
            self.vis_params['show_sample_classes'] = True

        if 'force_no_log' in report_setup_meta['visualize_setup']:
            self.vis_params['force_no_log'] = report_setup_meta['visualize_setup']['force_no_log']
        else:
            self.vis_params['force_no_log'] = False

        if 'x_limit' in report_setup_meta['visualize_setup']:
            self.vis_params['x_limit'] = report_setup_meta['visualize_setup']['x_limit']
        else:
            self.vis_params['x_limit'] = False


        att_fea, seq_fea, all_fea = self.load_feature_list()
        print('all_fea',all_fea)

        self.file_params = dict()
        for dataset_file, dataset_key, dataset_label in constants.DATASET_LABEL:
            self.file_params[dataset_key] = {'data_file': dataset_file,
                                             'att_fea': att_fea,
                                             'seq_fea': seq_fea,
                                             'all_fea': all_fea,
                                             'metafile_name': dataset_key,
                                             'label_keys': label_keys,
                                             'label_type': label_type}

        self.recommendation_metric = report_setup_meta['overall']['recommendation_metric']
        self.is_deeplearning = report_setup_meta['overall']['is_deeplearning']
        self.content_list = report_setup_meta['overall']['content_list']
        self.usecase_name = report_setup_meta['overall']['usecase_name']
        self.usecase_version = report_setup_meta['overall']['usecase_version']
        self.usecase_team = report_setup_meta['overall']['usecase_team']

        self.label_description = report_setup_meta['data_analysis']['label_description']
        self.feature_sample_key = report_setup_meta['data_analysis']['feature_sample_key']
        self.sequence_feature_name = report_setup_meta['data_analysis']['sequence_feature_name']
        self.key_feature = report_setup_meta['evaluation']['key_feature']

    def load_feature_list(self):
        ml_metadata_path = os.path.join(self.folder_path, 'meta.json')

        if not os.path.exists(ml_metadata_path):
            raise FileNotFoundError("'meta.json' is not found!")

        with open(ml_metadata_path, 'r') as f:
            meta = json.load(f)

        all_valid_field = []
        att_fea = defaultdict(list)

        for k, v in meta[constants.METADATA_KEY_DATA_SEC][constants.META_KEY_ATTRIBUTE_FEATURE].items():
            feature_type = v[constants.META_KEY_FIELD_TYPE]
            if feature_type in constants.FEATURE_DATA_TYPE_NOMINAL + constants.FEATURE_DATA_TYPE_ORDINAL:
                att_fea['categorical'].append(k)
            elif feature_type in constants.FEATURE_DATA_TYPE_CONTINUOUS:
                att_fea['numeric'].append(k)
            elif feature_type in constants.FEATURE_DATA_TYPE_TEXT:
                att_fea['text'].append(k)
            if feature_type in constants.VALID_DATATYPE:
                all_valid_field.append(k)

        seq_fea = defaultdict(list)
        for k, v in meta[constants.METADATA_KEY_DATA_SEC][constants.META_KEY_SEQUENCE_FEATURE].items():
            feature_type = v[constants.META_KEY_FIELD_TYPE]
            if feature_type in constants.FEATURE_DATA_TYPE_NOMINAL + constants.FEATURE_DATA_TYPE_ORDINAL:
                seq_fea['categorical'].append(k)
            elif feature_type in constants.FEATURE_DATA_TYPE_CONTINUOUS:
                seq_fea['numeric'].append(k)
            elif feature_type in constants.FEATURE_DATA_TYPE_TEXT:
                seq_fea['text'].append(k)
            if feature_type in constants.VALID_DATATYPE:
                all_valid_field.append(k)

        return att_fea, seq_fea, all_valid_field
