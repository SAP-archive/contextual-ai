# Explainer Module

This module houses all algorithms which are used to generate explanations for model predictions.


<span style="font-size:1.5em;font-weight: bold;">A simple example</span>


```python
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Main Contextual-AI imports
import xai
from xai.explainer import ExplainerFactory

# Load the dataset and prepare training and test sets
raw_data = datasets.load_breast_cancer()
X, y = raw_data['data'], raw_data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Instantiate a classifier, train, and evaluate on test set
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
clf.score(X_test, y_test)

# Instantiate LimeTabularExplainer via the ExplainerFactory interface
explainer = ExplainerFactory.get_explainer(domain=xai.DOMAIN.TABULAR, algorithm=xai.ALG.LIME)

# Build the explainer
explainer.build_explainer(
    training_data=X_train,
    training_labels=y_train,
    mode=xai.MODE.CLASSIFICATION,
    predict_fn=clf.predict_proba,
    column_names=raw_data['feature_names'],
    class_names=list(raw_data['target_names'])
)

# Explain an instance
explainer.explain_instance(
    instance=X_test[0],
    top_labels=2,
    num_features=10)

```

Output:

```
{0: {'confidence': 0.0,
     'explanation': [{'feature': 'worst perimeter <= 83.79',
                      'score': -0.10193695487658752},
                     {'feature': 'worst area <= 509.25',
                      'score': -0.09601666088375639},
                     {'feature': 'worst radius <= 12.93',
                      'score': -0.06025582708518221},
                     {'feature': 'mean area <= 419.25',
                      'score': -0.056302517885391166},
                     {'feature': 'worst texture <= 21.41',
                      'score': -0.05509499962470648}]},
 1: {'confidence': 1.0,
     'explanation': [{'feature': 'worst perimeter <= 83.79',
                      'score': 0.10193695487658752},
                     {'feature': 'worst area <= 509.25',
                      'score': 0.0960166608837564},
                     {'feature': 'worst radius <= 12.93',
                      'score': 0.06025582708518222},
                     {'feature': 'mean area <= 419.25',
                      'score': 0.05630251788539119},
                     {'feature': 'worst texture <= 21.41',
                      'score': 0.05509499962470641}]}}
```

<span style="font-size:1.17em;font-weight: bold;">Development</span>

If you are developing your own Contextual AI compatible explanation algorithm, you should do the following:
* Extend the :py:meth:`AbstractExplainer <explainer.abstract_explainer.AbstractExplainer>` and implement
all the abstract methods.
* Assign a particular domain to your explanation algorithm as well as a unique name. Place the module
in the appropriate directory (e.g. `xai/explainer/tabular`) and create constants accordingly in
:py:meth:`constants.py <explainer.constants>`.
* Map the domain to your algorithm in 
:py:meth:`config.py <explainer.config>`.
* Create unittests in the `tests` directory.
