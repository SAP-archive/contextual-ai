CONTENT_SUMMARY = 'Summary'
CONTENT_DATA = 'Data Analysis'
CONTENT_FEATURE = 'Feature Analysis'
CONTENT_HYPEROPT = 'Hyperparameter Tuning'
CONTENT_TRAINING = 'Training Result'
CONTENT_RECOMMENDATION = 'Recommendations'
CONTENT_DEEPLEARNING = 'Deep Learning Training'

TEXT_TRAININGMODE_DEFAULT = 'Default training'
TEXT_TRAININGMODE_HYPEROPT_BENCHMARK = 'Hyperparameter tuning with benchmarking test'
TEXT_TRAININGMODE_HYPEROPT = 'Hyperparameter tuning without benchmarking test'

USECASE_CR = 'Customer Retention'
USECASE_LS = 'Lead Scoring'

COLOR_PALLETES = ["Blues_d", "Reds_d", "Greens_d", "Purples_d", "Oranges_d"]
COLORS = ["b", "r", "g"]

MAXIMUM_NUM_ENUM_DISPLAY = 20

KEY_DATA_META = 'data_meta'
KEY_TRAINING_META = 'training_meta'
KEY_MODEL_META = 'model_meta'

KEY_DATA_ALL = 'all'
KEY_DATA_TRAIN = 'train'
KEY_DATA_VALID = 'validation'
KEY_DATA_TEST = 'test'
KEY_DATA_EXTEND_TRAIN = 'extend_train'
KEY_DATA_EXTEND_VALID = 'extend_valid'
KEY_DATA_EXTEND_TEST = 'extend_test'

FEATURE_DATA_TYPE_NOMINAL = ['Nominal', 0, '0']
FEATURE_DATA_TYPE_ORDINAL = ['Ordinal', 1, '1']
FEATURE_DATA_TYPE_TEXT = ['Text', 'Free Text', 2, '2']
FEATURE_DATA_TYPE_CONTINUOUS = ['Continuous', 3, '3']
FEATURE_DATA_TYPE_DATETIME = ['DateTime', 4, '4']
FEATURE_DATA_TYPE_LABEL = ['Label', 5, '5']
FEATURE_DATA_TYPE_KEY = ['Key', 6, '6']

VALID_DATATYPE = FEATURE_DATA_TYPE_NOMINAL + FEATURE_DATA_TYPE_ORDINAL + FEATURE_DATA_TYPE_TEXT \
                 + FEATURE_DATA_TYPE_CONTINUOUS + FEATURE_DATA_TYPE_DATETIME \
                 + FEATURE_DATA_TYPE_LABEL + FEATURE_DATA_TYPE_KEY

## file names
TRAIN_DATA_FILE = 'train_data.txt'
TEST_DATA_FILE = 'test_data.txt'
VALIDATION_DATE_FILE = 'valid_data.txt'
ALL_DATA_FILE = 'all_data.txt'
EXTEND_TRAIN_DATA_FILE = 'extend_train_data.newdata'
EXTEND_TEST_DATA_FILE = 'extend_test_data.newdata'
EXTEND_VALID_DATA_FILE = 'extend_valid_data.newdata'

## metric
METRIC_BATCH_NUM = 'batch_num'
METRIC_LOSS = 'loss'
METRIC_ACCURACY = 'accuracy'
METRIC_PRECISION = 'precision'
METRIC_RECALL = 'recall'
METRIC_F1 = 'f1'
METRIC_AUC = 'auc'
METRIC_CM = 'confusion matrix'

METRIC_MAPPING = {METRIC_ACCURACY: [0, '0', METRIC_ACCURACY],
                  METRIC_PRECISION: [1, '1', METRIC_PRECISION],
                  METRIC_RECALL: [2, '2', METRIC_RECALL],
                  METRIC_F1: [3, '3', METRIC_F1],
                  METRIC_AUC: [4, '4', METRIC_AUC],
                  METRIC_CM: [5, '5', METRIC_CM],
                  }

TRAIN_META_FILE = 'meta.json'

## metadata key
METADATA_KEY_DATA_SEC = 'Data'
METADATA_KEY_MAPPING_SEC = 'Mapping'
METADATA_KEY_PARAM_SEC = 'Parameter'
METADATA_PREDICTIVE_SCENARIO = 'PredictiveScenario'
METADATA_MODEL_UUID = 'ModelUUID'
METADATA_DELETE_SOURCE_DATA = 'DeleteSourceData'

META_KEY_FIELD_TYPE = 'type'
META_KEY_FIELD_KEY = 'KEY'
META_KEY_FIELD_IA_TYPE = 'IA_TYPE'
META_KEY_FIELD_LABEL = 'LABEL'
META_KEY_FIELD_TIMESTAMP = 'IA_TIMESTAMP'
META_KEY_FIELD_START_DATE = 'START_DATE'
META_KEY_FIELD_END_DATE = 'END_DATE'
META_KEY_FIELD_CUTOFF_DATE = 'CUTOFF_DATE'
META_KEY_TIMESTAMP_PATTERN = 'TIMESTAMP_PATTERN'
META_KEY_ATTRIBUTE_FEATURE = 'AttributeFeature'
META_KEY_SEQUENCE_FEATURE = 'SequenceFeature'
META_KEY_SCORE = 'Score'
META_KEY_TRAINING_MODE = 'TrainingMode'

KEY_PROBABILITY = "probability"
KEY_GROUNDTRUTH = "gt"
KEY_VIS_RESULT = "vis_result"

KEY_PARAMETERS = 'parameters'
KEY_EVALUATION_RESULT = 'evaluation_result'
KEY_TRAINING_LOG = 'training_log'
KEY_FEATURE_RANKING = 'feature_ranking'
KEY_HISTORY = 'history'
KEY_HISTORY_PARAMETERS = 'params'
KEY_HISTORY_EVALUATION = 'val_scores'
KEY_BEST_INDEX = 'best_idx'
KEY_BENCHMARK_SCORE = 'benchmark_score'
KEY_TRAINING_MODE = 'training_mode'
KEY_VIS_LAYERS = 'vis_layers'

KEY_TIMING = 'timing'
KEY_ILLUSTRATION = 'illustration'
KEY_TIMING_FEATURE = 'feature extraction'
KEY_TIMING_DATAPROCESSING = 'data processing'
KEY_TIMING_TRAINING = 'training'
KEY_TIMING_EVALUATION = 'evaluation'
KEY_TIMING_DATAVALIDATION = 'data validation'

KEY_FILENAME = 'filename'
KEY_CATEGORICAL_FEATURE_DISTRIBUTION = 'categorical_feature_distribution'
KEY_NUMERIC_FEATURE_DISTRIBUTION = 'numeric_feature_distribution'
KEY_TEXT_FEATURE_DISTRIBUTION = 'text_feature_distribution'
KEY_LENGTH_FEATURE_DISTRIBUTION = 'length_feature_distribution'

KEY_DATA_DISTRIBUTION = 'data_distribution'
KEY_TOTAL_COUNT = 'total_count'

KEY_FEATURE_CATEGORICAL_TYPE = 'categorical'
KEY_FEATURE_NUMERIC_TYPE = 'numeric'
KEY_FEATURE_TEXT_TYPE = 'text'
KEY_FEATURE_LABLE_TYPE = 'label'
KEY_FEATURE_SEQUENCE_TYPE = 'sequence'

DATA_ANALYSIS_TYPES = [KEY_FEATURE_CATEGORICAL_TYPE, KEY_FEATURE_NUMERIC_TYPE, KEY_FEATURE_TEXT_TYPE]

KEY_MISSING_VALUE_COUNTER = 'missing_value'
KEY_FIELD_COUNTER = 'field_count'

PLOT_LINE_COLORS = ['mediumslateblue', 'cornflowerblue', 'orchid', 'thistle', 'lightpink', 'crimson', 'lightskyblue']

IMPORTANCE_THRESHOLD = 0.01

FIGURE_PATH = 'figures'

DATASET_LABEL = [(ALL_DATA_FILE, KEY_DATA_ALL, 'All Data (before splitting)'),
                 (TRAIN_DATA_FILE, KEY_DATA_TRAIN, 'Train Set'),
                 (VALIDATION_DATE_FILE, KEY_DATA_VALID, 'Validation Set'),
                 (TEST_DATA_FILE, KEY_DATA_TEST, 'Test Set'),
                 (EXTEND_TRAIN_DATA_FILE, KEY_DATA_EXTEND_TRAIN, 'Training (Extended)'),
                 (EXTEND_VALID_DATA_FILE, KEY_DATA_EXTEND_VALID, 'Validation (Extended)'),
                 (EXTEND_TEST_DATA_FILE, KEY_DATA_EXTEND_TEST, 'Testing (Extended)')]

PDF_NAME = 'training_report.pdf'

MODEL_STATUS_OVERFITTING = 2
MODEL_STATUS_UNDERFITTING = 1
MODEL_STATUS_FITTING = 0

RECOMMEND_PERFORMANCE_BENCHMARK = {METRIC_ACCURACY: 0.8,
                                   METRIC_F1: 0.8,
                                   METRIC_PRECISION: 0.8,
                                   METRIC_RECALL: 0.8,
                                   METRIC_AUC: 0.8}

RECOMMEND_PERFORMANCE_DIFFERENCE_BENCHMARK = 0.15
RECOMMEND_DATA_DISTRIBUTION_DISTANCE_BENCHMARK = 0.999
RECOMMEND_FEATURE_DISTRIBUTION_DISTANCE_BENCHMARK = 0.9

RECOMMEND_UNBALANCED_BENCHMARK = 0.2

RECOMMEND_METRIC_DIFF_BENCHMARK = 0.1

FEATURE_DATA_TYPE = {
    "Nominal": ['Nominal', 'Categorical', 0, '0'],
    "Ordinal": ['Ordinal', 1, '1'],
    "Free Text": ['Text', 'Free Text', 2, '2'],
    "Numeric": ['Continuous', 'Numeric', 3, '3'],
    "DateTime": ['DateTime', 'Timestamp', 4, '4'],
    "Label": ['Label', 5, '5'],
    "Key": ['Key', 6, '6']
}

DEFAULT_VALUE = {
    KEY_FEATURE_CATEGORICAL_TYPE: ["", "-", "*"],
    KEY_FEATURE_NUMERIC_TYPE: [0, ""],
    KEY_FEATURE_TEXT_TYPE: ["", "N.A.", "null", "NAN"],
    KEY_FEATURE_LABLE_TYPE: [""]
}

RELIABILITY_BINSIZE = 15
DEFAULT_LIMIT_SIZE = 1000

LAYER_NAME_LOGITS = 'logits'
LAYER_NAME_RNN = 'rnn_outputs'
LAYER_NAME_MERGED = 'merged_outputs'

# LS_VIS_LAYERS = [LAYER_NAME_LOGITS, LAYER_NAME_RNN, LAYER_NAME_MERGED]
## TODO: set to empty list before solving potential memory issue when storing data in numpy array
LS_VIS_LAYERS = []
