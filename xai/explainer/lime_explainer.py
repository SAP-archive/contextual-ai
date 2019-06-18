import lime.lime_tabular
from xai.explainer.abstract_explainer import AbstractExplainer
import dill


class LimeExplainer(AbstractExplainer):
    def __init__(self, params):
        if 'class_names' in params.keys():
            class_names = params['class_names']
        else:
            print('Error: Fail to initialize explainer. No class_name.')
            return None

        if 'feature_names' in params.keys():
            feature_names = params['feature_names']
        else:
            print('Error: Fail to initialize explainer. No feature_names.')
            return None

        if 'categorical_dict' in params.keys():
            categorical_dict = params['categorical_dict']
        else:
            print('Error: Fail to initialize explainer. No categorical_dict.')
            return None

        super(LimeExplainer, self).__init__(explainer_name='LimeTabular', feature_names=feature_names,
                                            class_names=class_names, categorical_dict=categorical_dict)

    def initialize_explainer(self, predict_fn, train_data=None):
        self.predict_fn = predict_fn
        index = sorted(list(self.categorical_dict.keys()))
        self.explainer = lime.lime_tabular.LimeTabularExplainer(train_data, feature_names=self.feature_names,
                                                                categorical_features=index,
                                                                categorical_names=self.categorical_dict,
                                                                class_names=self.class_names,
                                                                discretize_continuous=True)
        print('Successfully initialize: %s' % self.explainer)
        return self.explainer

    def explain_instance(self, sample, num_features=AbstractExplainer.TOP_EXPLAIN_FEATURES):
        exp = self.explainer.explain_instance(data_row=sample, predict_fn=self.predict_fn,
                                              num_features=num_features).as_list()
        return exp

    def decode_explaination(self, exp, sample, score):
        output_str = ""
        for item in exp:
            output_str += item
            output_str += '\n'
        return output_str

    def save_to_file(self, filename):
        saved_obj = {}
        saved_obj['explainer'] = self.explainer
        saved_obj['explainer_name'] = self.explainer_name
        saved_obj['predict_fn'] = self.predict_fn
        with open(filename, 'wb') as f:
            dill.dump(saved_obj, f)

    def load_from_file(self, filename):
        with open(filename, 'rb') as f:
            saved_obj = dill.loads(f)
        self.explainer = saved_obj['explainer']
        self.explainer_name = saved_obj['explainer_name']
        self.predict_fn = saved_obj['predict_fn']
