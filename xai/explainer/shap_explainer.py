import shap
import dill
from xai.explainer.abstract_explainer import AbstractExplainer


class ShapExplainer(AbstractExplainer):
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

        super(ShapExplainer, self).__init__(explainer_name='ShapKernal', feature_names=feature_names,
                                            class_names=class_names, categorical_dict=categorical_dict)

    def initialize_explainer(self, predict_fn, train_data):
        self.explainer = shap.KernelExplainer(predict_fn, train_data, link="identity")
        print('Successfully initialize: %s' % self.explainer)
        return self.explainer

    def explain_instance(self, sample, num_features=AbstractExplainer.TOP_EXPLAIN_FEATURES):
        exp = self.explainer.shap_values(sample, nsamples=100,
                                         l1_reg='num_features(%s)' % num_features)
        return exp

    def decode_explaination(self, exp, sample, output):
        output_str = ''
        expected_values = self.explainer.expected_value
        output_str += "expected_value: %s\n" % expected_values
        exp_list = []
        for c_idx, class_name in enumerate(self.class_names):
            output_value = expected_values[c_idx]
            class_explaination = {}
            class_explaination['class name'] = class_name
            class_explaination['output value'] = output[c_idx]
            class_explaination['expected value'] = expected_values[c_idx]
            class_explaination['explainations'] = []
            assert (len(exp[c_idx] == len(self.feature_names)))
            for f_idx, fea in enumerate(self.feature_names):
                shap_value = exp[c_idx][f_idx]
                output_value += shap_value
                if exp[c_idx][f_idx] != 0:
                    x = sample[f_idx]
                    if f_idx in self.categorical_dict.keys():
                        x = int(x)
                        x = self.categorical_dict[f_idx][x]
                    class_explaination['explainations'].append((fea, x, shap_value))

            exp_list.append(class_explaination)

        ## print the explanations
        for item in exp_list:
            output_str += '=========================\n'
            for k, v in item.items():
                output_str += '---------------\n'
                output_str += '%s\n' % k
                if type(v) == list:
                    for iv in v:
                        output_str += '\t%s\n' % iv
                else:
                    output_str += '\t%s\n' % v
        return output_str

    def save_to_file(self, filename):
        saved_obj = dict()
        saved_obj['explainer'] = self.explainer
        saved_obj['explainer_name'] = self.explainer_name
        saved_obj['class_names'] = self.class_names
        saved_obj['feature_names'] = self.feature_names
        saved_obj['categorical_dict'] = self.categorical_dict

        with open(filename, 'wb') as f:
            dill.dump(saved_obj, f)

    def load_from_file(self, filename):
        with open(filename, 'rb') as f:
            saved_obj = dill.loads(f)
        self.explainer = saved_obj['explainer']
        self.explainer_name = saved_obj['explainer_name']
        self.feature_names = saved_obj['feature_names']
        self.categorical_dict = saved_obj['categorical_dict']
        self.class_names = saved_obj['class_names']
