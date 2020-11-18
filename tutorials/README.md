### Contextual AI tutorials

#### Pre-requisite
Before running any tutorials, make sure you have done the following steps:
- Pull the latest code from the `master` branch:
```
git clone https://github.com/sap/contextual-ai
git checkout master
git pull 
``` 
- Go to the root directory and install the required packages:
```
pip install -r requirements.txt
```
- Install nltk data stopwords corpus following the steps at https://www.nltk.org/data.html  
  eg. From Python interpreter, invoke the interactive NLTK Downloader and select popular packages for download.  
  Alternatively run the command line installation or manual installation
```
>>> import nltk
>>> nltk.download()
```

- Set your jupyter notebook kernel correctly to the environment with all required packages.
