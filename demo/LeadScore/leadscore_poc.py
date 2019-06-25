import os
import json
from xai import constants
from xai.report_generator import generate_report
import shutil


def generate_training_report(data_path, model_path, output_path, eval_result, training_log, train_parameters, timing):
    key_feature = None
    with open(os.path.join(model_path, 'meta.json'), 'r') as f:
        meta = json.load(f)

    with open(os.path.join(data_path, constants.ALL_DATA_FILE), 'w') as f:
        for data_file in os.listdir(data_path):
            if data_file.endswith('.newdata'):
                with open(os.path.join(data_path, data_file), 'r') as data_f:
                    for line in data_f:
                        f.write(line)
    for k, v in meta[constants.METADATA_KEY_DATA_SEC][constants.META_KEY_ATTRIBUTE_FEATURE].items():
        if v[constants.META_KEY_FIELD_TYPE] in constants.FEATURE_DATA_TYPE_LABEL:
            key_feature = k
            break
    label_key = constants.META_KEY_FIELD_LABEL
    label_type = constants.KEY_FEATURE_CATEGORICAL_TYPE
    fea_sample_key = constants.KEY_DATA_EXTEND_TRAIN
    content_list = [constants.CONTENT_DATA, constants.CONTENT_DEEPLEARNING, constants.CONTENT_TRAINING,
                    constants.CONTENT_RECOMMENDATION]

    usecase_name = constants.USECASE_LS
    is_deeplearning = True
    recommendation_metric = constants.TRAIN_TEST_ACCURACY
    label_description = "0 (Not Opportunity), 1 (Opportunity)"

    sequence_feature_name = None
    with open(os.path.join(model_path, constants.TRAIN_META_FILE), 'r') as f:
        meta = json.load(f)
    for k, v in meta[constants.METADATA_KEY_DATA_SEC][constants.META_KEY_SEQUENCE_FEATURE].items():
        if v[
            constants.META_KEY_FIELD_TYPE] in constants.FEATURE_DATA_TYPE_NOMINAL + constants.FEATURE_DATA_TYPE_ORDINAL:
            sequence_feature_name = k
            break

    usecase_version = 'DI 0.0.1'

    # Testing
    training_meta = dict()
    training_meta[constants.KEY_EVALUATION_RESULT] = eval_result
    training_meta[constants.KEY_TRAINING_LOG] = training_log
    training_meta[constants.KEY_PARAMETERS] = train_parameters
    training_meta[constants.KEY_TIMING] = timing

    report_setup_meta = dict()

    report_setup_meta['data_analysis'] = dict()
    report_setup_meta['data_analysis']['feature_sample_key'] = fea_sample_key
    report_setup_meta['data_analysis']['sequence_feature_name'] = sequence_feature_name
    report_setup_meta['data_analysis']['label_key'] = label_key
    report_setup_meta['data_analysis']['label_type'] = label_type
    report_setup_meta['data_analysis']['label_description'] = label_description

    report_setup_meta['overall'] = dict()
    report_setup_meta['overall']['content_list'] = content_list
    report_setup_meta['overall']['usecase_name'] = usecase_name
    report_setup_meta['overall']['usecase_version'] = usecase_version
    report_setup_meta['overall']['usecase_team'] = 'SAP ML-MKT'
    report_setup_meta['overall']['is_deeplearning'] = is_deeplearning
    report_setup_meta['overall']['recommendation_metric'] = recommendation_metric

    report_setup_meta['visualize_setup'] = dict()

    report_setup_meta['evaluation'] = dict()
    report_setup_meta['evaluation']['key_feature'] = key_feature

    with open(os.path.join(data_path, 'report_meta.json'), 'w') as f:
        json.dump(report_setup_meta, f)

    generate_report(data_path, output_path=output_path, training_meta=training_meta)


if __name__ == '__main__':

    # create temp folder for data
    temp_path = './__temp'

    data_path = './data'
    model_path = os.path.join(temp_path, 'SavedModel')
    output_path = './_xai_output'

    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.mkdir(output_path)
    shutil.copytree(data_path, temp_path)

    with open(os.path.join(data_path, 'training_log.json'), 'r') as f:
        training_log = json.load(f)
    with open(os.path.join(data_path, 'evaluation_result.json'), 'r') as f:
        evaluation_result = json.load(f)
    with open(os.path.join(data_path, 'train_parameters.json'), 'r') as f:
        train_parameters = json.load(f)
    with open(os.path.join(data_path, 'timing.json'), 'r') as f:
        timing = json.load(f)
    generate_training_report(data_path=temp_path,
                             model_path=model_path,
                             output_path=output_path,
                             eval_result=evaluation_result,
                             training_log=training_log,
                             train_parameters=train_parameters,
                             timing=timing)

    shutil.rmtree(temp_path)
