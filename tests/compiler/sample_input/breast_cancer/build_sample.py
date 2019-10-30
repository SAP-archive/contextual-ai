import sys
import random
import numpy as np
import pandas as pd

from pprint import pprint
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

raw_data = datasets.load_breast_cancer()
X, y = raw_data['data'], raw_data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# print(X_train)
# np.savetxt("train_data.csv", X_train, delimiter=",")
#
# x = np.loadtxt("train_data.csv",delimiter=",")
# print(x)

from xai.data.constants import DATATYPE
feature_names = raw_data['feature_names']
feature_types = [DATATYPE.NUMBER]*len(feature_names)

# print(feature_names.dtype)
print(type(feature_names))
print(feature_names)
#np.savetxt("feature_names.csv", feature_names, delimiter=",")
feature_names.tofile("feature_names2.csv", sep=",")

# x = np.loadtxt("feature_names.csv",delimiter=",", dtype='str')
# print(x)

df = pd.read_csv(str("feature_names2.csv"))
print(df.columns)


