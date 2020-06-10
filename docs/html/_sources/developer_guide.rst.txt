================
Developer Guide
================

Contextual AI libraries consist of multiple modules (data, model, explainer, formatter, and compiler).
Developers of Contextual AI are recommended to follow the same structure and documentation style when extending the library.

---------------------
Structure Guideline
---------------------

- Each module provides a set of closely related classes/functions packed in the same package under xai
  (e.g. xai/explainer/), which aim to address similar types of problems encountered in the same stage of ML piplelines.
- Each module should come with a README.md file in the root of its source package (e.g. xai/explain/README.md),
  describing its main features and capabilities.
- Optionally the module can include its own requirements.txt file stating the dependencies to run the module alone.
- Each module should provide some tutorials demonstrating its typical use case scenarios.
  The tutorials are recommended to be presented in the format of Jupyter notebooks.
  A README.md file should be included to briefly introduce how to run the notebooks and what each notebook does.
- All tutorials related files (including README.md and *.ipynb) should be put under the same folder in tutorials
  (e.g. tutorials/explainer/).


---------------------
Style Guideline
---------------------

- All source codes should be properly documented following Google Python Style
  (http://google.github.io/styleguide/pyguide.html).
- README.md files should be written with proper heading levels:
  a single level 1 heading and multiple level 2 or 3 headings if necessary.
  However, the default heading style (e.g. annotation with #) shall not be used.
  Refer to xai/data/README.md for your reference.
- Jupyter notebooks should follow proper heading levels too:
  a single level 1 heading and more sub-levels if necessary.
  Refer to tutorials/explainer/lime_text_explainer.ipynb for your reference.
- Images in Jupyter notebooks should be inserted using markdown script
  (e.g. `![Report Header](images/sample-report-header.png)`), html `<img>` tag is not supported.
- Due to current library limitations, Juypter notebooks from different tutorials will be extracted to
  the same root folder during intermediate steps. If a notebook has any folder containing referenced images, the folder
  must have a unique name globally across all tutorials.
  Thus it is recommended to prefix your image folder with the module name.



-------------------------
Cross Reference Examples
-------------------------


Readme file reference
----------------------

Many times you need to add cross references between various documentation files.
Here are some examples. The same syntax works for both `md` files and `rst` files.
Click `View page source` on the top right corner to see the code.

* Reference to auto-generated API module example: :py:mod:`~model.interpreter.feature_interpreter`

* Reference to auto-generated API class example: :py:meth:`~model.interpreter.feature_interpreter.FeatureInterpreter`

* Reference to auto-generated API method example: :py:meth:`~model.interpreter.feature_interpreter.FeatureInterpreter.get_feature_importance_ranking`

* Customized API reference example: :py:meth:`my description for feature importance ranking method <model.interpreter.feature_interpreter.FeatureInterpreter.get_feature_importance_ranking>`

* Reference to other doc file example: :ref:doc:`data_module`

* Customized doc file reference example: :ref:doc:`data package API <data/data>`


Jupyter notebook reference
---------------------------


.. toctree::
   :maxdepth: 1

   jupyter_cross_reference.nblink

