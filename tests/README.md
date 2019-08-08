### Demos for XAI

Before running any demo, make sure you have done the following steps:
- pull the latest code from the `master` branch:
```
git clone https://github.wdf.sap.corp/ML-Leonardo/Explainable_AI.git
git checkout master
git pull 
``` 
- go to the root directory and install the required packages:
```
pip install -t requirements.txt
```
- set your jupyter notebook kernel correctly to the environment with all required packages.


The following notebooks demostrate different functionality of XAI packages:
- `Training Report Generation.ipynb`: demos for `xai.formatter` package. It shows how you can format your own PDF report based on the information generated from the other packages. The demo generates a `training_report.pdf` in the `tests` folder based on the data in `sample_data`. 
