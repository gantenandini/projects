# -*- coding: utf-8 -*-
"""bagging assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N9V9tqXXKWQBEgZ0OxlVmXuNzAK27NKh
"""

# Commented out IPython magic to ensure Python compatibility.
# Importing the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

# To ignore warnings
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv('/content/credit-card-default.csv')
df.head()

df.info()

# Importing test_train_split from sklearn library
from sklearn.model_selection import train_test_split

# Putting feature variable to X
X = df.drop('defaulted', axis=1)

# Putting response variable to y
y = df['defaulted']

# Splitting the data into train and test with test size as 30% and random state as 101
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3, random_state=101)

# import StandardScaler, DecisionTreeClassifier and make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline

# Pipeline Estimator
pipeline = make_pipeline(StandardScaler(), DecisionTreeClassifier(random_state=1))

# fit model on training data
pipeline.fit(X_train, y_train)

# Model scores on test and training data
print("Model test score: %.3f, " %pipeline.score(X_test, y_test),
      "Model training score: %.3f, " %pipeline.score(X_train, y_train))

# import BaggingClassifier
from sklearn.ensemble import BaggingClassifier

# Instantiate the bagging classifier
bgclassifier = BaggingClassifier(base_estimator=pipeline, random_state=1)

# fitting above model on training data
bgclassifier.fit(X_train, y_train)

# Model scores on test and training data
print("Model test score: %.3f, " %bgclassifier.score(X_test, y_test),
      "Model training score: %.3f, " %bgclassifier.score(X_train, y_train))

# import GridSearchCV
from sklearn.model_selection import GridSearchCV

'''A dictionary with base_estimator__max_depth from 1 to 20 with step size as 5
A max_samples with [0.05, 0.1, 0.2, 0.5] and max_features form 1 to 20 with step size as 5'''


param_grid = {
    'base_estimator__max_depth' : [1, 5, 10, 15, 20],
    'max_samples' : [0.05, 0.1, 0.2, 0.5],
    'max_features' : [1, 5, 10, 15, 20]
}

# Instantiate gridsearch with BaggingClassifier with base estimator DecisionTreeClassifier
gs = GridSearchCV(BaggingClassifier(DecisionTreeClassifier(), random_state=1),
                  param_grid, scoring='accuracy')

# fit grid search on training data
gs.fit(X_train, y_train)

# print best paramaters selected by gridsearch
print("Optimal hyperparameter combination: ", gs.best_params_)

# print mean accuracy score on final tuned  BaggingClassifier
print("Mean cross-validated training accuracy score:", gs.best_score_)

# Instantiate the bagging classifier with optimized parameter by grid search
bgclassifier = BaggingClassifier(DecisionTreeClassifier(max_depth=5), max_features=20, max_samples=0.5)

# fitting above model on training data
bgclassifier.fit(X_train, y_train)

# Model scores on test and training data
print("Model test score: %.3f, " %bgclassifier.score(X_test, y_test),
      "Model training score: %.3f, " %bgclassifier.score(X_train, y_train))

# Importing random forest classifier from sklearn library
from sklearn.ensemble import RandomForestClassifier

# Running the random forest with default parameters.
rfc = RandomForestClassifier(random_state=1)

# fit model on training data
rfc.fit(X_train, y_train)

# Making predictions
predictions = rfc.predict(X_test)

# Importing classification report and confusion matrix from sklearn metrics
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# Let's check the report of our default model
print(classification_report(y_test, predictions))

# Printing confusion matrix
print(confusion_matrix(y_test, predictions))

# Printing accuracy
print(accuracy_score(y_test, predictions))

# import Kfold
from sklearn.model_selection import KFold

# specify number of folds for k-fold CV which is 5
n_folds = 5

# parameters to build the model on here max_depth with range(2, 20, 5)
parameters = {'max_depth': range(2,20,5)}

# instantiate the model
rf = RandomForestClassifier(random_state=1)


# Instantiate GridSearchCVwith rf, parameter, cv and scoring as accuracy and return_train_score=True
rf = GridSearchCV(rf, parameters, cv=n_folds, scoring='accuracy', return_train_score=True)

# fit tree on training data
rf.fit(X_train, y_train)

# scores of GridSearch CV
scores = rf.cv_results_
pd.DataFrame(scores).head()

# plotting accuracies with max_depth
plt.figure()
plt.plot(scores["param_max_depth"], scores["mean_train_score"], label=["training accuracy"])
plt.plot(scores["param_max_depth"], scores["mean_test_score"], label=["test accuracy"])
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

# parameters to build the model on (here n_estimators with range(100, 1500, 400))
parameters = {'n_estimators' : range(100, 1500, 400)}

# instantiate the model (note we are specifying a max_depth as 4)
rf = RandomForestClassifier(max_depth=4, random_state=1)

# Instantiate GridSearchCVwith rf, parameter, cv and scoring as accuracy and return_train_score as True
rf = GridSearchCV(rf, parameters, cv=n_folds, scoring='accuracy', return_train_score=True)

# fit tree on training data
rf.fit(X_train, y_train)

# scores of GridSearch CV
scores = rf.cv_results_
pd.DataFrame(scores).head()

# plotting accuracies with n_estimators
plt.figure()
plt.plot(scores["param_n_estimators"], scores["mean_train_score"], label="training accuracy")
plt.plot(scores["param_n_estimators"], scores["mean_test_score"], label="test accuracy")
plt.xlabel("n_estimators")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

# parameters to build the model on max_features with [4, 8, 14, 20, 24]
parameters = {'max_features' : [4, 8, 14, 20, 24]}

# instantiate the model (note we are specifying a max_depth as 4)
rf = RandomForestClassifier(max_depth=4, random_state=1)

# Instantiate GridSearchCVwith rf, parameter, cv and scoring as accuracy and return_train_score as True
rf = GridSearchCV(rf, parameters, cv=n_folds, scoring='accuracy', return_train_score=True)

# fit tree on training data
rf.fit(X_train, y_train)

# scores of GridSearch CV
scores = rf.cv_results_
pd.DataFrame(scores).head()

# plotting accuracies with max_features
plt.figure()
plt.plot(scores["param_max_features"], scores["mean_train_score"], label="training accuracy")
plt.plot(scores["param_max_features"], scores["mean_test_score"], label="test accuracy")
plt.xlabel("max_features")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

# parameters to build the model on min_samples_leaf of range(100, 400, 50)
parameters = {'min_samples_leaf' : range(100, 400, 50)}

# instantiate the model (not specifying any max_depth)
rf = RandomForestClassifier(random_state=1)

# Instantiate GridSearchCVwith rf, parameter, cv and scoring as accuracy and return_train_score as True
rf = GridSearchCV(rf, parameters, cv=n_folds, scoring='accuracy', return_train_score=True)

# fit tree on training data
rf.fit(X_train, y_train)

# scores of GridSearch CV
scores = rf.cv_results_
pd.DataFrame(scores).head()

# plotting accuracies with min_samples_leaf
plt.figure()
plt.plot(scores["param_min_samples_leaf"], scores["mean_train_score"], label="training accuracy")
plt.plot(scores["param_min_samples_leaf"], scores["mean_test_score"], label="test accuracy")
plt.xlabel("min_samples_leaf")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

# parameters to build the model on (min_samples_split with range(200, 500, 50))
parameters = {'min_samples_split' : range(200, 500, 50)}

# instantiate the model
rf = RandomForestClassifier(random_state=1)


# Instantiate GridSearchCVwith rf, parameter, cv and scoring as accuracy and return_train_score as True
rf = GridSearchCV(rf, parameters, cv=n_folds, scoring='accuracy', return_train_score=True)

# fitting model on training data
rf.fit(X_train, y_train)

# scores of GridSearch CV
scores = rf.cv_results_
pd.DataFrame(scores).head()

# plotting accuracies with min_samples_split
plt.figure()
plt.plot(scores["param_min_samples_split"], scores["mean_train_score"], label="training accuracy")
plt.plot(scores["param_min_samples_split"], scores["mean_test_score"], label="test accuracy")
plt.xlabel("min_samples_split")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

from sklearn.model_selection import RandomizedSearchCV

# Create the parameter grid based on the results of random search
param_grid = {
    'max_depth': [4,8,10],
    'min_samples_leaf': range(100, 400, 200),
    'min_samples_split': range(200, 500, 200),
    'n_estimators': [100,200, 300],
    'max_features': [5, 10]
}

# Create a based model (i.e RF)
rf = RandomForestClassifier(random_state=1)

# Instantiate the radom search model with estimator, param_grid, and random_state as 0
rs = RandomizedSearchCV(rf, param_grid, random_state=1)

# Fit the grid search to the data
rs.fit(X_train, y_train)

# printing the optimal accuracy score and hyperparameters
print("we can get accuracy of", rs.best_score_, 'using', rs.best_params_)

# Instantiate RF model with the best hyperparameters
rfc = RandomForestClassifier(max_depth=8,
                             min_samples_leaf=100,
                             min_samples_split=400,
                             max_features=10,
                             n_estimators=100,
                             random_state=1)

# fit rfc on training data
rfc.fit(X_train, y_train)

# predict
predictions = rfc.predict(X_test)

# evaluation metrics using classification_report
print(classification_report(y_test, predictions))

# print confusion_matrix and
print(confusion_matrix(y_test, predictions))

# print accuracy
print(accuracy_score(y_test, predictions))

# import ExtraTreesClassifier
from sklearn.ensemble import ExtraTreesClassifier

# Instantiate ExtraTreesClassifier with default parameters
et = ExtraTreesClassifier(random_state=1)

# fitting model on training data
et.fit(X_train, y_train)

# Making predictions
predictions = et.predict(X_test)

# Let's check the report of our default model
print(classification_report(y_test, predictions))

# Printing confusion matrix
print(confusion_matrix(y_test, predictions))

# printing accuracy_score
print(accuracy_score(y_test, predictions))

# Create the parameter grid similar to random forest
param_grid = {
    'max_depth': [4,8,10],
    'min_samples_leaf': range(100, 400, 200),
    'min_samples_split': range(200, 500, 200),
    'n_estimators': [100,200, 300],
    'max_features': [5, 10]
}


# Instantiate RandomizedSearchCV with et , param_grid and random state=0
rs = RandomizedSearchCV(et, param_grid, random_state=1)

# Fit the random search to the training data
rs.fit(X_train, y_train)

# printing the optimal accuracy score and hyperparameters
print("we can get accuracy of", rs.best_score_, 'using', rs.best_params_)

# Instantiate ExtraTreesClassifier with default parameters
et = ExtraTreesClassifier(n_estimators=100, min_samples_split=400, min_samples_leaf=100, max_features=10, max_depth=8)

# fitting model on training data
et.fit(X_train, y_train)

# Making predictions
predictions = et.predict(X_test)

# printing accuracy_score
print(accuracy_score(y_test, predictions))

