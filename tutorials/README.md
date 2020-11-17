### Contextual AI tutorials

#### Pre-requisite
Before running any tutorials, make sure you have done the following steps:
- pull the latest code from the `master` branch:
```
git clone https://github.com/sap/contextual-ai
git checkout master
git pull 
``` 
- go to the root directory and install the required packages:
```
pip install -r requirements.txt
```
- install nltk data stopwords corpus following the steps at https://www.nltk.org/data.html. eg. From Python interpreter, invoke the interactive NLTK Downloader and select popular packages for download
```
>>> import nltk
>>> nltk.download()
```

- set your jupyter notebook kernel correctly to the environment with all required packages.
