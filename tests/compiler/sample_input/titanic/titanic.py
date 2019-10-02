#Libraries
import pickle
# To ignore warnings
import warnings

import numpy as np
import pandas as pd
import re as re
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

################################################################################
### Data Ingestion & Splitting
################################################################################
#Load data
data = pd.read_csv('titanic.csv', index_col=False )

print(data.head())

#Split data
y = data.Survived
X = data.drop('Survived', axis=1)


X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2)
all_data = [X_train, X_test]

################################################################################
### Data & Feature Processing
################################################################################
#Feature 1-2 ready to use, manipulating others
#Feature 3
for data in all_data:
    data['family_size'] = data['SibSp'] + data['Parch'] + 1

#Feature 3.1
for data in all_data:
    data['is_alone'] = 0
    data.loc[data['family_size'] == 1, 'is_alone'] = 1

#Feature 4
for data in all_data:
    data['Embarked'] = data['Embarked'].fillna('S')

#Feature 5
for data in all_data:
    data['Fare'] = data['Fare'].fillna(data['Fare'].median())
X_train['category_fare'] = pd.qcut(X_train['Fare'], 4)

#Feature 6
for data in all_data:
    age_avg  = data['Age'].mean()
    age_std  = data['Age'].std()
    age_null = data['Age'].isnull().sum()

    random_list = np.random.randint(age_avg - age_std, age_avg + age_std , size = age_null)
    data['Age'][np.isnan(data['Age'])] = random_list
    data['Age'] = data['Age'].astype(int)

X_train['category_age'] = pd.cut(X_train['Age'], 5)

#Feature 7
def get_title(name):
    title_search = re.search(' ([A-Za-z]+)\. ', name)
    if title_search:
        return title_search.group(1)
    return ""

for data in all_data:
    data['title'] = data['Name'].apply(get_title)

for data in all_data:
    data['title'] = data['title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'],'Rare')
    data['title'] = data['title'].replace('Mlle','Miss')
    data['title'] = data['title'].replace('Ms','Miss')
    data['title'] = data['title'].replace('Mme','Mrs')

#Map Data
for data in all_data:

    #Mapping Sex
    sex_map = { 'female':0 , 'male':1 }
    data['Sex'] = data['Sex'].map(sex_map).astype(int)

    #Mapping Title
    title_map = {'Mr':1, 'Miss':2, 'Mrs':3, 'Master':4, 'Rare':5}
    data['title'] = data['title'].map(title_map)
    data['title'] = data['title'].fillna(0)

    #Mapping Embarked
    embark_map = {'S':0, 'C':1, 'Q':2}
    data['Embarked'] = data['Embarked'].map(embark_map).astype(int)

    #Mapping Fare
    data.loc[ data['Fare'] <= 7.91, 'Fare']                            = 0
    data.loc[(data['Fare'] > 7.91) & (data['Fare'] <= 14.454), 'Fare'] = 1
    data.loc[(data['Fare'] > 14.454) & (data['Fare'] <= 31), 'Fare']   = 2
    data.loc[ data['Fare'] > 31, 'Fare']                               = 3
    data['Fare'] = data['Fare'].astype(int)

    #Mapping Age
    data.loc[ data['Age'] <= 16, 'Age'] 		      = 0
    data.loc[(data['Age'] > 16) & (data['Age'] <= 32), 'Age'] = 1
    data.loc[(data['Age'] > 32) & (data['Age'] <= 48), 'Age'] = 2
    data.loc[(data['Age'] > 48) & (data['Age'] <= 64), 'Age'] = 3
    data.loc[ data['Age'] > 64, 'Age']                        = 4


#5 Feature Selection
#5.1 Create list of columns to drop
drop_elements = ["Name", "Ticket", "Cabin", "SibSp", "Parch", "family_size"]

#5.3 Drop columns from both data sets
X_train = X_train.drop(drop_elements, axis = 1)
X_train = X_train.drop(['PassengerId','category_fare', 'category_age'], axis = 1)
X_test  = X_test.drop(drop_elements, axis = 1)


#5.4 Double check
print("Training data")
print(X_train.head)
print("Test data")
print(X_test.head)


################################################################################
### Model Training & Persist as pickle
################################################################################
#6 Do training with decision tree
decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, y_train)
pkl = open('model.pkl', 'wb')
pickle.dump(decision_tree, pkl)
decision_tree = None
X_train.to_csv("train_data.csv", index=False)

################################################################################
### Model Loading & Inference
################################################################################
#7.1 Prepare prediction data & Model
model_pkl = open('model.pkl', 'rb')
model = pickle.load(model_pkl)
X_test_predict  = X_test.drop("PassengerId", axis=1).copy()

#7.2 Do predict
accuracy = round(model.score(X_train, y_train) * 100, 2)
print('=========================')
print("Model Accuracy: ",accuracy)
print('=========================')

#7.3 Run prediction on entire test data
Y_pred = model.predict(X_test_predict)
result = pd.DataFrame({
    "PassengerId":X_test["PassengerId"],
    "Survived": Y_pred
})
result.to_csv('result.csv', index = False)