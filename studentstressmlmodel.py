# -*- coding: utf-8 -*-
"""StudentStressMLModel

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hvWI70kLWwkBuJk2-V5CmfW51KWwlzrm

# Setup
"""

import pandas as pd
import numpy
from pandas import Series, DataFrame
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

"""# Read into CSV, Cleaning DataFrame(s)"""

studentlf_data = pd.read_csv('/content/student_lifestyle_dataset.csv')
studentlf_data.head()

# How much data are we working with?
print(len(studentlf_data))
print(len(studentlf_data.columns))

# I want to predict Stress Level based on a Student's Study Hours,
# Sleep Hours, and Extracurricular Hours.
X = studentlf_data[["Study_Hours_Per_Day", "Sleep_Hours_Per_Day", "Extracurricular_Hours_Per_Day"]]
X.head()

y = studentlf_data["Stress_Level"]
y.head()

"""# Creating Model"""

tempmodel = DecisionTreeClassifier()
tempmodel.fit(X,y)

# By loading my model into a file, I no longer need to recreate it. However, for
# the sake of following my process, I have left my previous steps as active
# (rather than comments).
joblib.dump(tempmodel, 'studentlf.joblib')
model = joblib.load('studentlf.joblib')

"""# Testing Model Out"""

#To test my model, input study hours, sleep hours, and extracurricular hours.
predictions = model.predict( [[0, 6, 9]] )
predictions

"""# Accuracy Testing"""

# Now, I want to delegate 20% of my data towards checking
# the accuracy of my model.
X_Train, X_Test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model.fit(X_Train,y_train)
predictiontesting = model.predict(X_Test)
score = accuracy_score(y_test,predictiontesting)
score

"""# Correlation Analysis

We now have an accurate model, however, we can go a further step and find which columns actually correlate.
"""

# First, I'll make a copy of my dataframe.
correl_studentlfdata = studentlf_data.copy()

# I need to replace stress levels with numerical values.
stress_mapping = {'Low': 0, 'Moderate': 1, 'High': 2}
correl_studentlfdata['Stress_Level'] = correl_studentlfdata['Stress_Level'].map(stress_mapping)


correl_studentlfdata.head()

studentdata_correl = correl_studentlfdata.corr()
sns.heatmap(studentdata_correl, annot=True, cmap='coolwarm')
plt.show()

"""Here, we can see that out of all the variables we used to predict stress level, study hours per day had the most positive correlation with stress levels.

# Recreating an Accurate Model
"""

# We will first recreate our binary X dataframe to be based off of factors we
# found to correlate from our matrix. %%
X2 = studentlf_data[["Study_Hours_Per_Day", "Sleep_Hours_Per_Day", "Physical_Activity_Hours_Per_Day"]]
X2.head()

revisedmodel = DecisionTreeClassifier()
#This model will be based on the factors that we found to
# significantly correlate.
revisedmodel.fit(X2,y)

joblib.dump(revisedmodel, 'studentlfrevised.joblib')
revisedmodel = joblib.load('studentlfrevised.joblib')

#Let's try out a prediction. I am inputting study hours,
# sleep hours, and physical activity hours. %%
revisedpredictions = revisedmodel.predict( [[0, 6, 10]] )
revisedpredictions

# Now, let's double-check the accuracy of my revised model by
# allocating 20% towards testing. %%
X2_Train, X2_Test, y_train, y_test = train_test_split(X2, y, test_size=0.2)

revisedmodel.fit(X2_Train,y_train)
predictiontesting2 = revisedmodel.predict(X2_Test)
score2 = accuracy_score(y_test,predictiontesting2)
score

"""# Conclusions

*   Based on my ML model, it seems that the higher the amount of study hours, and the lower the sleep hours, the more a student's stress level increases.
*   However, I noticed that extracurricular hours do not necessarily impact my model's prediction(s) on stress-level
*   This makes sense, as our correlation matrix confirms a .0061, or 0.61% correlation on extracurricular hours.
*   Once I revised and recreated my model based on the factors that correlated, I saw that an increase in physical activity hours helped to decrease stress levels at times.
*  Ultimately, the amount of sleep a student recieved most directly impacted a student's stress-levels, as no increase in physical activity nor decrease in the amount of studying could compensate for 0-5 hours of sleep.
"""
