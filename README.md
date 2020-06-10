Contextual AI
==============

[![Build Status](https://travis-ci.com/sap-staging/contextual-ai.svg?token=wh5aYpEiVyMyx9ysvFdy&branch=master)](https://travis-ci.com/sap-staging/contextual-ai)
[![Documentation Status](https://readthedocs.org/projects/contextual-ai/badge/?version=latest)](https://contextual-ai.readthedocs.io/en/latest/?badge=latest)


Contextual AI adds explainability to different stages of machine learning pipelines - data, training, and inference - thereby addressing the trust gap between such ML systems and their users.

## 🖥 Installation

Contextual AI has been tested with Python 3.6 and 3.7. You can install it using pip:

```
$ pip install contextual-ai
```

### Building locally

````
$ sh build.sh
$ pip install dist/*.whl
````

## ⚡️ Quickstart

In this simple example, we will attempt to generate explanations for some ML model trained on 20newsgroups, a text classification dataset. In particular, we want to find out which words were important for a particular prediction.

```python
from pprint import pprint
from sklearn import datasets
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

# Main Contextual AI imports
import xai
from xai.explainer import ExplainerFactory

# Train on a subset of the 20newsgroups dataset (text classification)
categories = [
    'rec.sport.baseball',
    'soc.religion.christian',
    'sci.med'
]

# Fetch and preprocess data
raw_train = datasets.fetch_20newsgroups(subset='train', categories=categories)
raw_test = datasets.fetch_20newsgroups(subset='test', categories=categories)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(raw_train.data)
y_train = raw_train.target
X_test = vectorizer.transform(raw_test.data)
y_test = raw_test.target

# Train a model
clf = MultinomialNB(alpha=0.1)
clf.fit(X_train, y_train)

############################
# Main Contextual AI steps #
############################
# Instantiate the text explainer via the ExplainerFactory interface
explainer = ExplainerFactory.get_explainer(domain=xai.DOMAIN.TEXT)

# Build the explainer
def predict_fn(instance):
    vec = vectorizer.transform(instance)
    return clf.predict_proba(vec)

explainer.build_explainer(predict_fn)

# Generate explanations
exp = explainer.explain_instance(
    labels=[0, 1, 2], # which classes to produce explanations for?
    instance=raw_test.data[9],
    num_features=5 # how many words to show?
)

print('Label', raw_train.target_names[raw_test.target[0]], '=>', raw_test.target[0])
pprint(exp)
```

#### Input text:

```
From: creps@lateran.ucs.indiana.edu (Stephen A. Creps)\nSubject: Re: The doctrine of Original Sin\nOrganization: Indiana University\nLines: 63\n\nIn article <May.11.02.39.07.1993.28331@athos.rutgers.edu> Eugene.Bigelow@ebay.sun.com writes:\n>>If babies are not supposed to be baptised then why doesn\'t the Bible\n>>ever say so.  It never comes right and says "Only people that know\n>>right from wrong or who are taught can be baptised."\n>\n>This is not a very sound argument for baptising babies
...
```

#### Output explanations:

```
Label soc.religion.christian => 2
{0: {'confidence': 6.79821e-05,
     'explanation': [{'feature': 'Bible', 'score': -0.0023500809763485468},
                     {'feature': 'Scripture', 'score': -0.0014344577715211986},
                     {'feature': 'Heaven', 'score': -0.001381196356886895},
                     {'feature': 'Sin', 'score': -0.0013723724408794883},
                     {'feature': 'specific', 'score': -0.0013611914394935848}]},
 1: {'confidence': 0.00044,
     'explanation': [{'feature': 'Bible', 'score': -0.007407412195931125},
                     {'feature': 'Scripture', 'score': -0.003658367757678809},
                     {'feature': 'Heaven', 'score': -0.003652181996607397},
                     {'feature': 'immoral', 'score': -0.003469502264458387},
                     {'feature': 'Sin', 'score': -0.003246609821338066}]},
 2: {'confidence': 0.99948,
     'explanation': [{'feature': 'Bible', 'score': 0.009736539971486623},
                     {'feature': 'Scripture', 'score': 0.005124375636024145},
                     {'feature': 'Heaven', 'score': 0.005053514624616295},
                     {'feature': 'immoral', 'score': 0.004781252244149238},
                     {'feature': 'Sin', 'score': 0.004596128058053568}]}}
```



## 🚀 What else can it do?

Contextual AI spans three pillars, or scopes, of explainability, each addressing a different stage of a machine learning solution's lifecycle.

### Pre-training (Data)

* Distributional analysis of data and features
* Data validation
* [Tutorial](https://contextual-ai.readthedocs.io/en/latest/data_module_tutorial.html)

### Training evaluation (Model)

* Training performance
* Feature importance
* Per-class explanations
* [Tutorial](https://contextual-ai.readthedocs.io/en/latest/training_module_tutorial.html)

### Inference (Prediction)

* Explanations per prediction instance
* [Tutorial](https://contextual-ai.readthedocs.io/en/latest/inference_module_tutorial.html)

### Formatter/Compiler

* Produce PDF/HTML reports of outputs from the above using only a few lines of code
* [Tutorial](https://contextual-ai.readthedocs.io/en/latest/compiler_module_tutorial.html)

## 🤝 Contributing

We welcome contributions of all kinds!

- Reporting bugs
- Requesting features
- Creatin pull requests
- Providing discussions/feedback
