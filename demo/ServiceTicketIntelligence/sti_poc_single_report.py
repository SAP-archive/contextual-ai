from xai import constants
import os
import shutil
from collections import defaultdict
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score
from xai.util import JsonSerializable
import json
import numpy as np

RESPONSE_KEY_RESULT = 'validation_results'
RESPONSE_KEY_FIELD = 'field'
RESPONSE_KEY_CM = 'confusion_matrix'
RESPONSE_KEY_F1 = 'f1_score'
RESPONSE_KEY_PRECISION = 'precision'
RESPONSE_KEY_RECALL = 'recall'

RESPONSE_KEY_CM_LABEL = 'labels'
RESPONSE_KEY_CM_VALUE = 'values'

RESPONSE_PREFIX_AVE = 'average_'

DATA_FILENAME = 'sti_data.csv'
METADATA_FILENAME = 'sti_data_meta.json'
RESULT_FILENAME = 'result_response.json'
VIS_RESULT_FILENAME = 'vis_result.json'


def get_evaluation_json(field, y_true, y_pred, y_conf):
    labels = list(set(y_true.tolist()))

    acc = accuracy_score(y_true=y_true, y_pred=y_pred)

    pre = precision_score(y_true=y_true, y_pred=y_pred, labels=labels, average=None)
    ave_pre = precision_score(y_true=y_true, y_pred=y_pred, average='weighted')

    rec = recall_score(y_true=y_true, y_pred=y_pred, labels=labels, average=None)
    ave_rec = recall_score(y_true=y_true, y_pred=y_pred, average='weighted')

    f1 = f1_score(y_true=y_true, y_pred=y_pred, labels=labels, average=None)
    ave_f1 = f1_score(y_true=y_true, y_pred=y_pred, average='weighted')

    cm = confusion_matrix(y_true=y_true, y_pred=y_pred, labels=labels)
    cm = cm.tolist()

    evaluation_result = dict()
    evaluation_result[RESPONSE_KEY_F1] = f1
    evaluation_result[RESPONSE_PREFIX_AVE + RESPONSE_KEY_F1] = ave_f1
    evaluation_result[RESPONSE_KEY_RECALL] = rec
    evaluation_result[RESPONSE_PREFIX_AVE + RESPONSE_KEY_RECALL] = ave_rec
    evaluation_result[RESPONSE_KEY_PRECISION] = pre
    evaluation_result[RESPONSE_PREFIX_AVE + RESPONSE_KEY_PRECISION] = ave_pre
    evaluation_result[RESPONSE_KEY_CM] = dict()
    evaluation_result[RESPONSE_KEY_CM][RESPONSE_KEY_CM_LABEL] = labels
    evaluation_result[RESPONSE_KEY_CM][RESPONSE_KEY_CM_VALUE] = cm
    evaluation_result[RESPONSE_KEY_FIELD] = field
    evaluation_result[constants.KEY_VIS_RESULT] = get_swarm_vis_result(y_true, y_pred, y_conf)

    vis_result = {field: get_swarm_vis_result(y_true, y_pred, y_conf)}

    return evaluation_result, vis_result


def get_swarm_vis_result(y_true, y_pred, y_conf):
    vis_result = dict()
    labels = list(set(y_true.tolist()))
    for label in labels:
        bool = y_pred == label
        cat_gt = y_true[bool]
        cat_conf = y_conf[bool]
        vis_result[label] = {constants.KEY_GROUNDTRUTH: cat_gt, constants.KEY_PROBABILITY: cat_conf}
    return vis_result


def convert_result_csv_to_vis_result_dict(csv_file, labels, data_path):
    params = {}
    df = pd.read_csv(os.path.join(data_path,csv_file), index_col=False)
    eva_list = []
    for label in labels:
        eva_item = {}
        eva_item['y_true'] = np.array(df[label])
        eva_item['y_pred'] = np.array(df['%s_pred' % label])
        eva_item['y_conf'] = np.array(df['%s_conf' % label])
        eva_item['field'] = label
        eva_list.append(eva_item)
    eva_result, vis_result = generate_result_json_response(params=params, eva_list=eva_list)
    with open(os.path.join(data_path, RESULT_FILENAME), 'w') as f:
        json.dump(eva_result, f, cls=JsonSerializable)
    with open(os.path.join(data_path, VIS_RESULT_FILENAME), 'w') as f:
        json.dump(eva_result, f, cls=JsonSerializable)

    return eva_result, vis_result


def generate_result_json_response(params: dict, eva_list: list):
    eva_result = dict()
    for k, v in params.items():
        eva_result[k] = v
    eva_result[RESPONSE_KEY_RESULT] = list()
    all_vis_result = dict()
    for eva in eva_list:
        eva_dict, vis_result = get_evaluation_json(**eva)
        eva_result[RESPONSE_KEY_RESULT].append(eva_dict)
        all_vis_result.update(vis_result)
    return eva_result, all_vis_result


def convert_data_csv_to_json(data_folder, csv_files, json_file):
    if os.path.exists(json_file):
        print('%s datajson exist.' % json_file)
        return
    with open(json_file, 'w') as f:
        for file in csv_files:
            csv_path = os.path.join(data_folder, file)
            if not os.path.exists(csv_path):
                print('Error: %s not exist.' % csv_path)
            else:
                print('Converting file:', csv_path)
                df = pd.read_csv(csv_path, index_col=False)
                df.fillna('NAN', inplace=True)
                json_str = df.to_json(orient='records')
                json_obj = json.loads(json_str)

                for k in json_obj:
                    f.write(json.dumps(k))
                    f.write('\n')

    print('Created file:', json_file)


def convert_response_json_to_single_training_meta(response_json_file, meta_json_file, output_folder):
    with open(response_json_file, 'r') as f:
        response = json.load(f)

    with open(meta_json_file, 'r') as f:
        meta_json = json.load(f)

    for k in response.keys():
        if k != RESPONSE_KEY_RESULT:
            meta_json[constants.METADATA_KEY_PARAM_SEC][k] = response[k]
    results = response[RESPONSE_KEY_RESULT]
    training_result = dict()
    for idx, result in enumerate(results):
        individual_training_result = defaultdict(dict)
        label_key = result[RESPONSE_KEY_FIELD]
        meta_json[constants.METADATA_KEY_DATA_SEC][constants.META_KEY_ATTRIBUTE_FEATURE][label_key][
            constants.META_KEY_FIELD_TYPE] = 'Label'
        training_result[label_key] = dict()
        del (result[RESPONSE_KEY_FIELD])
        cm = result[RESPONSE_KEY_CM]
        labels = cm[RESPONSE_KEY_CM_LABEL]
        for metric, metric_value in result.items():
            if metric == RESPONSE_KEY_CM:
                individual_training_result[constants.TRAIN_TEST_CM] = metric_value
            elif metric == constants.KEY_VIS_RESULT:
                individual_training_result[constants.KEY_VIS_RESULT] = metric_value
            elif RESPONSE_PREFIX_AVE in metric:
                _true_metric = metric.replace(RESPONSE_PREFIX_AVE, "")
                individual_training_result[_true_metric]["average"] = metric_value
            else:
                individual_training_result[metric]["class"] = dict()
                assert (len(labels) == len(metric_value))
                label_metric = zip(labels, metric_value)
                for l, v in label_metric:
                    individual_training_result[metric]["class"][l] = v
        training_result[label_key][constants.KEY_DATA_TEST] = individual_training_result

    with open(os.path.join(output_folder, 'eval.json'), 'w') as f:
        json.dump(training_result, f)

    with open(os.path.join(output_folder, 'meta.json'), 'w') as f:
        json.dump(meta_json, f)


def convert_result_csv_to_evaluation_result_json(csv_file, meta_json):
    df = pd.read_csv(csv_file, index_col=False)
    with open(meta_json, 'r') as f:
        meta = json.load(f)
    labels = []
    for fea, fea_values in meta[constants.META_KEY_ATTRIBUTE_FEATURE].items():
        if fea_values[constants.META_KEY_FIELD_TYPE] in constants.FEATURE_DATA_TYPE_LABEL:
            labels.append(fea)
    vis_result_dict = {}
    for label in labels:
        y_true = df[label]
        y_pred = df['%s_pred' % label]
        y_conf = df['%s_conf' % label]
        vis_result_dict[label] = get_swarm_vis_result(y_true, y_pred, y_conf)
    return vis_result_dict


def generate_single_report(data_path,labels):
    temp_path = './__temp'

    output_path = './_xai_output'
    csv_files = ['sti_data.csv']
    test_csv = 'out_df.csv'

    eva_result, vis_result = convert_result_csv_to_vis_result_dict(test_csv, labels, data_path)

    file_check(data_path=data_path)

    for eva in eva_result['validation_results']:
        field = eva[RESPONSE_KEY_FIELD]
        eva['vis_result'] = vis_result[field]

    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.mkdir(output_path)
    shutil.copytree(data_path, temp_path)

    data_json_file = os.path.join(temp_path, constants.ALL_DATA_FILE)
    convert_data_csv_to_json(temp_path, csv_files, data_json_file)

    response_json_file = os.path.join(temp_path, RESULT_FILENAME)
    meta_json_file = os.path.join(temp_path, METADATA_FILENAME)

    convert_response_json_to_single_training_meta(response_json_file, meta_json_file, temp_path)

    ## generate seperate folder and prepare the file for generate report
    rep_output_path = os.path.join(output_path, 'report')
    rep_data_path = os.path.join(temp_path, 'report')
    if not os.path.exists(rep_output_path):
        os.mkdir(rep_output_path)
    if not os.path.exists(rep_data_path):
        os.mkdir(rep_data_path)

    shutil.copyfile(os.path.join(temp_path, 'meta.json'),
                    os.path.join(rep_data_path, constants.TRAIN_META_FILE))

    for f in os.listdir(temp_path):
        if f.endswith('.txt') or f.endswith('.newdata') or f.endswith('.data'):
            shutil.copyfile(os.path.join(temp_path, f), os.path.join(rep_data_path, f))

    with open(os.path.join(temp_path, 'eval.json'), 'r') as f:
        eval_result = json.load(f)
    with open(os.path.join(temp_path, 'meta.json'), 'r') as f:
        meta = json.load(f)
    label_keys = []
    for k, v in meta[constants.METADATA_KEY_DATA_SEC][constants.META_KEY_ATTRIBUTE_FEATURE].items():
        if v[constants.META_KEY_FIELD_TYPE] in constants.FEATURE_DATA_TYPE_LABEL:
            label_keys.append(k)
            label_type = constants.KEY_FEATURE_CATEGORICAL_TYPE

    content_list = [constants.CONTENT_DATA, constants.CONTENT_DEEPLEARNING, constants.CONTENT_TRAINING]

    usecase_name = 'Service Ticket Intelligence'
    usecase_version = '0.0.1'

    # Testing
    training_meta = dict()
    training_meta.update({constants.KEY_EVALUATION_RESULT: eval_result})
    # training_meta.update(training_log)
    # training_meta[constants.KEY_PARAMETERS] = train_parameters
    # training_meta[constants.KEY_TIMING] = timing
    training_meta[constants.KEY_ILLUSTRATION] = os.path.join(data_path,'model_diagram.png')

    report_setup_meta = dict()

    report_setup_meta['data_analysis'] = dict()
    report_setup_meta['data_analysis']['feature_sample_key'] = constants.KEY_DATA_ALL
    report_setup_meta['data_analysis']['sequence_feature_name'] = None
    report_setup_meta['data_analysis']['label_keys'] = label_keys
    report_setup_meta['data_analysis']['label_type'] = label_type
    report_setup_meta['data_analysis']['label_description'] = None

    report_setup_meta['visualize_setup'] = dict()
    report_setup_meta['visualize_setup']['show_sample_classes'] = False
    report_setup_meta['visualize_setup']['force_no_log'] = True
    report_setup_meta['visualize_setup']['x_limit'] = True

    report_setup_meta['overall'] = dict()
    report_setup_meta['overall']['content_list'] = content_list
    report_setup_meta['overall']['usecase_name'] = usecase_name
    report_setup_meta['overall']['usecase_version'] = usecase_version
    report_setup_meta['overall']['usecase_team'] = 'SAP ML-STI'
    report_setup_meta['overall']['is_deeplearning'] = True
    report_setup_meta['overall']['recommendation_metric'] = 'accuracy'

    report_setup_meta['evaluation'] = dict()
    report_setup_meta['evaluation']['key_feature'] = meta[constants.METADATA_KEY_PARAM_SEC]['KeyFeature']

    with open(os.path.join(rep_data_path, 'report_meta.json'), 'w') as f:
        json.dump(report_setup_meta, f)

    from xai.report_generator import generate_report

    generate_report(data_folder=rep_data_path, output_path=rep_output_path, training_meta=training_meta)


def file_check(data_path):
    if not os.path.exists(os.path.join(data_path, DATA_FILENAME)):
        raise FileNotFoundError("Cannot find '%s'" % DATA_FILENAME)
    if not os.path.exists(os.path.join(data_path, METADATA_FILENAME)):
        raise FileNotFoundError("Cannot find '%s'" % METADATA_FILENAME)
    if not os.path.exists(os.path.join(data_path, RESULT_FILENAME)):
        raise FileNotFoundError("Cannot find '%s'" % RESULT_FILENAME)
    print('..pass file check!')


if __name__ == '__main__':
    print('''
To run this demo, you need following files:
    - training data: %s
    - datameta file: %s
    - result response: %s
        ''' % (DATA_FILENAME, METADATA_FILENAME, RESULT_FILENAME))
    data_path = './data'
    labels = ['category','categoryII']
    generate_single_report(data_path=data_path, labels=labels)
