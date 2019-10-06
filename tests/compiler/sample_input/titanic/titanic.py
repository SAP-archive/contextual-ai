#Libraries
import pickle
# To ignore warnings
import warnings

import numpy as np
import pandas as pd
import re as re
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

################################################################################
### Data Ingestion & Splitting
################################################################################
#Load data
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')
all_data = [train_data, test_data]

data = pd.concat([train_data, test_data], sort=False)
data.to_csv('titanic.csv', index=False)

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
train_data['category_fare'] = pd.qcut(train_data['Fare'], 4)

#Feature 6
for data in all_data:
    age_avg  = data['Age'].mean()
    age_std  = data['Age'].std()
    age_null = data['Age'].isnull().sum()

    random_list = np.random.randint(age_avg - age_std, age_avg + age_std , size = age_null)
    data['Age'][np.isnan(data['Age'])] = random_list
    data['Age'] = data['Age'].astype(int)

train_data['category_age'] = pd.cut(train_data['Age'], 5)

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
train_data = train_data.drop(drop_elements, axis = 1)
train_data = train_data.drop(['PassengerId','category_fare', 'category_age'], axis = 1)
test_data  = test_data.drop(drop_elements, axis = 1)


#5.4 Double check
print("Training data")
print(train_data.head)
print("Test data")
print(test_data.head)


################################################################################
### Model Training & Persist as pickle
################################################################################
#6 Do training with decision tree
X_train = train_data.drop("Survived", axis=1)
Y_train = train_data["Survived"]

decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, Y_train)
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

X_test  = test_data.drop("PassengerId", axis=1).copy()

#7.2 Do predict
accuracy = round(model.score(X_train, Y_train) * 100, 2)
print('=========================')
print("Model Accuracy: ",accuracy)
print('=========================')

#7.3 Run prediction on entire test data
Y_pred = model.predict(X_test)
result = pd.DataFrame({
    "PassengerId":test_data["PassengerId"],
    "Survived": Y_pred
})
result.to_csv('result.csv', index = False)