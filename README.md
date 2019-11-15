Explainable AI (XAI)
==============

[![Build Status](https://jenkins.ml.only.sap/buildStatus/icon?job=Explainable_AI%2Fmaster)](https://jenkins.ml.only.sap/job/Explainable_AI/job/master/)
[![Generic badge](https://img.shields.io/badge/docs-passing-<GREEN>.svg)](https://github.wdf.sap.corp/pages/ML-Leonardo/Explainable_AI/)



XAI is a Python package that addresses the trust gap between machine learning systems and their developers and users.



## Installation ##

XAI has been tested with Python 3.5+. You can install it using pip:

### Building locally

````
$ git clone https://github.wdf.sap.corp/ML-Leonardo/Explainable_AI
$ cd Explainable_AI
$ sh build.sh
$ pip install dist/*.whl
````

### Installing from Nexus

_Coming soon_

## Quickstart

In this simple example, we will attempt to generate explanations for some ML model trained on 20newsgroups, a text classification dataset. In particular, we want to find out which words were important for a particular prediction.

```python
import random
import numpy as np
from pprint import pprint
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

# Main XAI imports
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

# Instantiate the text explainer via the ExplainerFactory interfact
explainer = ExplainerFactory.get_explainer(domain=xai.DOMAIN.TEXT)

# Build the explainer
def predict_fn(instance):
    vec = vectorizer.transform(instance)
    return clf.predict_proba(vec)

explainer.build_explainer(predict_fn)

# Generate explanations
exp = explainer.explain_instance(
    labels=[0, 1, 2],
    instance=raw_test.data[9],
    num_features=5
)

print('Label', raw_train.target_names[raw_test.target[0]], '=>', raw_test.target[0])
pprint(exp)
```

Output:

```
Label soc.religion.christian => 2
{0: {'confidence': 6.798212345437472e-05,
     'explanation': [{'feature': 'Bible', 'score': -0.0023500809763485468},
                     {'feature': 'Scripture', 'score': -0.0014344577715211986},
                     {'feature': 'Heaven', 'score': -0.001381196356886895},
                     {'feature': 'Sin', 'score': -0.0013723724408794883},
                     {'feature': 'specific', 'score': -0.0013611914394935848}]},
 1: {'confidence': 0.00044272540371258136,
     'explanation': [{'feature': 'Bible', 'score': -0.007407412195931125},
                     {'feature': 'Scripture', 'score': -0.003658367757678809},
                     {'feature': 'Heaven', 'score': -0.003652181996607397},
                     {'feature': 'immoral', 'score': -0.003469502264458387},
                     {'feature': 'Sin', 'score': -0.003246609821338066}]},
 2: {'confidence': 0.9994892924728337,
     'explanation': [{'feature': 'Bible', 'score': 0.009736539971486623},
                     {'feature': 'Scripture', 'score': 0.005124375636024145},
                     {'feature': 'Heaven', 'score': 0.005053514624616295},
                     {'feature': 'immoral', 'score': 0.004781252244149238},
                     {'feature': 'Sin', 'score': 0.004596128058053568}]}}
```



## The Three Pillars of Explainable AI







## Resources

* [Wiki](https://wiki.wdf.sap.corp/wiki/pages/viewpage.action?pageId=2098642718)
* [Slack (#xai)](https://sap-ml.slack.com/messages/CHJMDJB17)
* [Fiori UX4AI design guidelines](https://ux.wdf.sap.corp/fiori-design-web/explainable-ai/)

## Contact Us

DL_5CE39E1B960F84027F4937EE@global.corp.sap (DL ML Explainable AI)
