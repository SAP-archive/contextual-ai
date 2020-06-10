# Contextual AI Compiler tutorials

`contextual-ai` follows simple inversion of control (IoC) programming principle to 
allowing user to customize and create use-case-specific explainability report.

This is to increase the modularity of `contextual-ai` lib and make it easy for extensible.


<span style="font-size:1.5em;font-weight: bold;">Example</span>

The following examples can give you an impression of what the package can do:



<span style="font-size:1.17em;font-weight: bold;">Titanic Dataset</span>

* [Kaggle Overview](https://www.kaggle.com/c/titanic/overview)  
* [Titanic dataset](https://www.kaggle.com/c/titanic/data)
* :ref:doc:`Sample Notebook 1 <tutorials/compiler/tutorial_titanic>`
* :ref:doc:`Sample Notebook 2 <tutorials/compiler/tutorial_titanic2>`



<span style="font-size:1.17em;font-weight: bold;">Automobile Dataset</span>

* [Kaggle Overview](https://www.kaggle.com/toramky/automobile-dataset)
* [Automobile dataset](https://www.kaggle.com/toramky/automobile-dataset)
* :ref:doc:`Sample Notebook 1 <tutorials/compiler/tutorial_automobile>`

 

<span style="font-size:1.5em;font-weight: bold;">Supported Format</span>

The supported `external configuration` format are:
* Json - Javascript Object Notation
* Yaml - Rhymes with Camel (converted to Json when loaded)



<span style="font-size:1.5em;font-weight: bold;">Validation</span>


<span style="font-size:1.17em;font-weight: bold;">Validate with Json Schema</span>

The `external configuration` MUST follow the defined schema bvelow:
```json
      { "definitions": {
            "section": {
                "type": "object",
                "properties": {
                    "title": { "type": "string" },
                    "desc": { "type": "string" },
                    "sections":
                        {
                            "type": "array",
                            "items": { "$ref": "#/definitions/section" },
                            "default": []
                        },
                    "component": { "$ref": "#/definitions/component" }
                },
                "required": ["title"]
            },
            "component": {
                "type": "object",
                "properties": {
                    "package": { "type": "string" },
                    "module": { "type": "string" },
                    "class": { "type": "string" },
                    "attr": {
                        "type": "object"
                    }
                },
                "required": ["class"]
            }
        },

        "type": "object",
        "properties": {
            "name": { "type" : "string" },
            "overview": {" type": "boolean" },
            "content_table": { "type": "boolean" },
            "contents":
                {
                    "type": "array",
                    "items": {"$ref": "#/definitions/section"},
                    "default": []
                },
            "writers":
                {
                    "type": "array",
                    "items": {"$ref": "#/definitions/component"}
                }
        },
        "required": ["name", "content_table", "contents", "writers"]
    }
```


<span style="font-size:1.17em;font-weight: bold;">Example in Json</span>

```json
{
  "name": "Report for Feature Importance Ranking",
  "overview": true,
  "content_table": true,
  "contents": [
    {
      "title": "Feature Importance Ranking",
      "desc": "This section provides the analysis on feature",
      "sections": [
        {
          "title": "Feature Importance Analysis with Breast Cancer data-set",
          "desc": "Model and train data from Breast Cancer",
          "sections": [
            {
              "title": "SHAP analysis with csv (with header)",
              "component": {
                "_comment": "refer to document section xxxx",
                "class": "FeatureImportanceRanking",
                "attr": {
                  "trained_model": "./sample_input/breast_cancer/model.pkl",
                  "train_data": "./sample_input/breast_cancer/train_data.csv",
                  "method": "shap"
                }
              }
            }
          ]
        },
        {
          "title": "Feature Importance Analysis with Titanic data-set",
          "desc": "Model and train data from Titanic",
          "sections": [
            {
              "title": "Default analysis with csv (with header)",
              "component": {
                "_comment": "refer to document section xxxx",
                "class": "FeatureImportanceRanking",
                "attr": {
                  "trained_model": "./sample_input/titanic/model.pkl",
                  "train_data": "./sample_input/titanic/train_data.csv"
                }
              }
            }
          ]
        }
      ]
    }
  ],
  "writers": [
    {
      "class": "Pdf",
      "attr": {
        "name": "feature-importance-report",
        "path": "./sample_output"
      }
    },
    {
      "class": "Html",
      "attr": {
        "name": "feature-importance-report",
        "path": "./sample_output"
      }
    }
  ]
}
```


<span style="font-size:1.17em;font-weight: bold;">Example in Yaml</span>

```yaml
name: Report for Feature Importance Ranking
overview: true
content_table: true
contents: 
  - title: Feature Importance Ranking
    desc: This section provides the analysis on feature
    sections: 
      - title: Feature Importance Analysis with Breast Cancer data-set
        desc: Model and train data from Breast Cancer
        sections: 
          - title: SHAP analysis with csv (with header)
            component:
              _comment: refer to document section xxxx1
              class: FeatureImportanceRanking
              attr:
                trained_model: ./sample_input/breast_cancer/model.pkl
                train_data: ./sample_input/breast_cancer/train_data.csv
                method: shap
          - title: Default analysis with csv (with header)
            component:
              _comment: refer to document section xxxx
              class: FeatureImportanceRanking
              attr:
                trained_model: ./sample_input/breast_cancer/model.pkl
                train_data: ./sample_input/breast_cancer/train_data.csv
          - title: SHAP analysis with numpy input file
            component:
              _comment: refer to document section xxxx2
              class: FeatureImportanceRanking
              attr:
                trained_model: ./sample_input/breast_cancer/model.pkl
                train_data: ./sample_input/breast_cancer/train_data.npy
                feature_names: ./sample_input/breast_cancer/feature_names.npy
                method: shap
      - title: Feature Importance Analysis with Titanic data-set
        desc: Model and train data from Titanic
        sections:
          - title: Default analysis with csv (with header)
            component:
              _comment: refer to document section xxxx
              class: FeatureImportanceRanking
              attr:
                trained_model: ./sample_input/titanic/model.pkl
                train_data: ./sample_input/titanic/train_data.csv
writers:
  - class: Pdf
    attr:
      name: feature-importance-yml-report
      path: ./sample_output
  - class: Html
    attr:
      name: feature-importance-yml-report
      path: ./sample_output
```
