from xai.data.constants import DATATYPE
from xai.data.explorer.categorical import categorical_analyzer
from xai.data.explorer.datetime import datetime_analyzer
from xai.data.explorer.numerical import numerical_analyzer
from xai.data.explorer.text import text_analyzer

DICT_DATATYPE_TO_ANALYZER = {
    DATATYPE.CATEGORY: categorical_analyzer,
    DATATYPE.NUMBER: numerical_analyzer,
    DATATYPE.FREETEXT: text_analyzer,
    DATATYPE.DATETIME: datetime_analyzer
}


DICT_ANALYZER_TO_DATATYPE = {
    categorical_analyzer: DATATYPE.CATEGORY,
    numerical_analyzer: DATATYPE.NUMBER,
    text_analyzer: DATATYPE.FREETEXT,
    datetime_analyzer: DATATYPE.DATETIME
}
