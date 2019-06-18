def get_table_layout(table_header):
    column = len(table_header) - 1
    width = (180 - 30) / column
    layout = [30]
    layout.extend([width] * column)
    return layout

import json
import numpy

class JsonSerializable(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            if numpy.isnan(obj):
                return 0
            return int(obj)
        elif isinstance(obj, numpy.floating):
            if numpy.isnan(obj):
                return 0.0
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(JsonSerializable, self).default(obj)