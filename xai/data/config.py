from xai.data.constants import DATATYPE
from xai.data.explorer.categorical import categorical_analyzer, labelled_categorical_analyzer
from xai.data.explorer.datetime import datetime_analyzer, labelled_datetime_analyzer
from xai.data.explorer.numerical import numerical_analyzer, labelled_numerical_analyzer
from xai.data.explorer.text import text_analyzer, labelled_text_analyzer

DICT_DATATYPE_TO_ANALYZER = {
    DATATYPE.CATEGORY: categorical_analyzer,
    DATATYPE.NUMBER: numerical_analyzer,
    DATATYPE.FREETEXT: text_analyzer,
    DATATYPE.DATETIME: datetime_analyzer
}



DICT_ANALYZER_TO_DATATYPE = {
    labelled_categorical_analyzer: DATATYPE.CATEGORY,
    labelled_numerical_analyzer: DATATYPE.NUMBER,
    labelled_text_analyzer: DATATYPE.FREETEXT,
    labelled_datetime_analyzer: DATATYPE.DATETIME
}
