import os
from xai.graphs import graph_generator as gg
from xai.graphs import format_contants as graph_constants
from xai import constants


def visualize_feature_for_similar_classes(dataset, label_key, feature_name, base_class, similar_class,
                                          sub_confusion_matrix):
    # TODO: if figure not exist, regenerate

    image_path_a = os.path.join(constants.FIGURE_PATH,
                                ('%s_%s_%s_%s.png' % (dataset, label_key, feature_name, base_class)).replace('/', '-'))
    if not os.path.exists(image_path_a):
        image_path_a = os.path.join(constants.FIGURE_PATH,
                                    ('%s_%s_%s_%s.png' % (
                                    constants.KEY_DATA_ALL, label_key, feature_name, base_class)).replace('/',
                                                                                                          '-'))
    image_path_b = os.path.join(constants.FIGURE_PATH,
                                ('%s_%s_%s_%s.png' % (dataset, label_key, feature_name, similar_class)).replace('/',
                                                                                                                '-'))
    if not os.path.exists(image_path_b):
        image_path_b = os.path.join(constants.FIGURE_PATH,
                                    ('%s_%s_%s_%s.png' % (
                                    constants.KEY_DATA_ALL, label_key, feature_name, similar_class)).replace('/',
                                                                                                             '-'))

    image_cm = gg.HeatMap(sub_confusion_matrix, 'cm_%s_%s_%s' % (label_key, base_class, similar_class), 'Predicted',
                          'True').draw(x_tick=[base_class, similar_class], y_tick=[base_class, similar_class], color_bar=False, grey_scale=True)

    return {'image_set': [image_cm, image_path_a, image_path_b],
            'grid_spec': graph_constants.ABSOLUTE_3_COMPARISON_2_GRID_SPEC}
