import xai.constants as constants
from sklearn.metrics.pairwise import cosine_similarity
import math


def get_model_fitting_status(evaluation_result, metric):
    training_performance = evaluation_result[constants.KEY_DATA_TRAIN][metric]
    validation_performance = evaluation_result[constants.KEY_DATA_VALID][metric]

    if training_performance < constants.RECOMMEND_PERFORMANCE_BENCHMARK[metric]:
        return constants.MODEL_STATUS_UNDERFITTING, training_performance, validation_performance

    if training_performance - validation_performance > constants.RECOMMEND_PERFORMANCE_DIFFERENCE_BENCHMARK:
        return constants.MODEL_STATUS_OVERFITTING, training_performance, validation_performance

    return constants.MODEL_STATUS_FITTING, training_performance, validation_performance


def _get_normalized_distribution(distribution, key_names):
    total_count = sum(distribution.values())
    normalized_dist = []
    for label in key_names:
        if label in distribution.keys():
            normalized_dist.append(distribution[label] / total_count)
        else:
            normalized_dist.append(0.0)
    return normalized_dist


def _get_union_keyset(dist_a, dist_b):
    keyset1 = set(dist_a.keys())
    keyset2 = set(dist_b.keys())

    keyset1.update(keyset2)

    return list(keyset1), len(dist_a.keys()), len(dist_b.keys()), \
           len(dist_a.keys()) + len(dist_b.keys()) - len(keyset1)


def get_training_data_distribution_balance_status(data_meta):
    sample_label_key = list(data_meta[constants.KEY_DATA_EXTEND_TRAIN].keys())[0]
    dist = data_meta[constants.KEY_DATA_EXTEND_TRAIN][sample_label_key][constants.KEY_DATA_DISTRIBUTION]
    labels = list(dist.keys())
    max_quan = max(list(dist.values()))

    normalized_values = [dist[x] / max_quan for x in labels]

    unbalanced_labelled = []
    balanced = True
    for idx, value in enumerate(normalized_values):
        if value < constants.RECOMMEND_UNBALANCED_BENCHMARK:
            unbalanced_labelled.append([labels[idx], value])
            balanced = False
        if value == 1:
            max_label = labels[idx]

    return balanced, max_label, unbalanced_labelled


def get_data_distribution_similar_status(data_meta, dataset_a, dataset_b):
    sample_label_key = list(data_meta[dataset_a].keys())[0]
    dist_a = data_meta[dataset_a][sample_label_key][constants.KEY_DATA_DISTRIBUTION]
    dist_b = data_meta[dataset_b][sample_label_key][constants.KEY_DATA_DISTRIBUTION]
    key_names, size_a, size_b, overlap = _get_union_keyset(dist_a, dist_b)
    normalized_dist_a = _get_normalized_distribution(dist_a, key_names)
    normalized_dist_b = _get_normalized_distribution(dist_b, key_names)

    cos_sim = cosine_similarity([normalized_dist_a], [normalized_dist_b])[0, 0]

    if cos_sim < constants.RECOMMEND_DATA_DISTRIBUTION_DISTANCE_BENCHMARK:
        status = False
    else:
        status = True

    return status, key_names, cos_sim, normalized_dist_a, normalized_dist_b


def get_feature_distribution_similar_status(data_meta, feature_name, dataset_a, dataset_b):
    sample_label_key = list(data_meta[dataset_a].keys())[0]
    dist_a = data_meta[dataset_a][sample_label_key][constants.KEY_CATEGORICAL_FEATURE_DISTRIBUTION][feature_name]['all']
    dist_b = data_meta[dataset_b][sample_label_key][constants.KEY_CATEGORICAL_FEATURE_DISTRIBUTION][feature_name]['all']
    key_names, size_a, size_b, overlap = _get_union_keyset(dist_a, dist_b)
    normalized_dist_a = _get_normalized_distribution(dist_a, key_names)
    normalized_dist_b = _get_normalized_distribution(dist_b, key_names)

    cos_sim = cosine_similarity([normalized_dist_a], [normalized_dist_b])[0, 0]

    if cos_sim < constants.RECOMMEND_FEATURE_DISTRIBUTION_DISTANCE_BENCHMARK:
        status = False
    else:
        status = True

    return status, key_names, cos_sim, size_a, size_b, overlap


def get_training_history_suggestion(training_meta, metric):
    if metric == constants.TRAIN_TEST_AUC or metric == constants.TRAIN_TEST_F1:
        return True, None

    f1_scores = []
    auc_scores = []

    best_idx = training_meta[constants.KEY_BEST_INDEX]
    if best_idx not in training_meta[constants.KEY_HISTORY]:
        best_idx = str(best_idx)
    best_idx_f1 = training_meta[constants.KEY_HISTORY][best_idx][constants.KEY_HISTORY_EVALUATION][
        constants.TRAIN_TEST_F1]
    best_idx_auc = training_meta[constants.KEY_HISTORY][best_idx][constants.KEY_HISTORY_EVALUATION][
        constants.TRAIN_TEST_AUC]
    best_metric = training_meta[constants.KEY_HISTORY][best_idx][constants.KEY_HISTORY_EVALUATION][metric]

    if math.isnan(best_idx_f1):
        best_idx_f1 = 0
    recommendation = []
    for iter_num, iter_eval in training_meta[constants.KEY_HISTORY].items():
        f1 = training_meta[constants.KEY_HISTORY][iter_num][constants.KEY_HISTORY_EVALUATION][constants.TRAIN_TEST_F1]
        if math.isnan(f1):
            continue
        diff_f1 = f1 - best_idx_f1
        f1_scores.append(diff_f1)
        auc = training_meta[constants.KEY_HISTORY][iter_num][constants.KEY_HISTORY_EVALUATION][constants.TRAIN_TEST_AUC]
        diff_auc = auc - best_idx_auc
        auc_scores.append(diff_auc)
        diff_metric = best_metric - training_meta[constants.KEY_HISTORY][iter_num][constants.KEY_HISTORY_EVALUATION][
            metric]
        if diff_f1 > constants.RECOMMEND_METRIC_DIFF_BENCHMARK or diff_auc > constants.RECOMMEND_METRIC_DIFF_BENCHMARK:
            recommendation.append((iter_num, diff_f1, diff_auc, diff_metric))

    if len(recommendation) > 0:
        return False, recommendation
    else:
        return True, recommendation
