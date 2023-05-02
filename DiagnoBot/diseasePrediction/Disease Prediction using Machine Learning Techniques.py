#!/usr/bin/env python
# coding: utf-8

# # Disease Prediction using Machine Learning Techniques

# In[ ]:





# In[1]:


# Importing Libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
# Libraries to clean data
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
# Libraries to perform feature selection
from sklearn.feature_selection import RFE
# Libraries to train models
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
# Libraries to evaluate performance
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score, precision_score


# # Cleaning the Data

# In[2]:


# Reading the Training.csv file
df_train = pd.read_csv("diseasePrediction/Training.csv")


# In[3]:


# Dropping unnecessary columns
df_train = df_train.drop('Unnamed: 133', axis=1)
df_train.head()


# In[4]:


# List of columns names (i.e.symptoms)
df_train.columns.tolist()


# In[5]:


# Check null columns 
null_cols = [col for col in df_train.columns if df_train[col].isnull().sum() > 0]
null_cols


# In[6]:


df_train.head()


# In[7]:


df_train.columns = df_train.columns.str.replace('_', ' ')


# In[8]:


# List of prognosis
df_train['prognosis'].value_counts().sort_index()


# In[9]:


# Splitting data into features and target
X = df_train.drop('prognosis', axis=1)
y = df_train[["prognosis"]]
y = np.ravel(y)


# In[10]:


y


# In[11]:


# label encode the target variable
le = LabelEncoder()
y = le.fit_transform(y)

print(y)


# In[12]:


# Reading the  testing.csv file
df_test = pd.read_csv("diseasePrediction/Testing.csv")

df_test.head()


# In[13]:


# Check null columns 
null_cols = [col for col in df_test.columns if df_test[col].isnull().sum() > 0]
null_cols


# In[14]:


df_test.columns = df_test.columns.str.replace('_', ' ')


# In[15]:


# List of prognosis
df_test['prognosis'].value_counts().sort_index()


# In[16]:


# Splitting data into features and target
X_test_csv= df_test.drop('prognosis', axis=1)
y_test_csv = df_test[["prognosis"]]
y_test_csv = np.ravel(y_test_csv)


# In[17]:


# label encode the target variable
y_test_csv = le.transform(y_test_csv)
print(y_test_csv)


# In[18]:


# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, train_size = 0.70, random_state=42)


# In[19]:


X_train.shape, X_test.shape, y_train.shape, y_test.shape


# # Performing Feature Selection

# **To select the top 95 features, we used RFE with Random Forest as an estimator**

# In[ ]:


rfc = RandomForestClassifier(n_estimators=500, max_leaf_nodes=16, n_jobs=-1)
n_features = 95
rfe = RFE(estimator=rfc, n_features_to_select=n_features)
X_train_rfe = rfe.fit_transform(X_train, y_train)
X_test_rfe = rfe.transform(X_test)
X_test_csv_rfe = rfe.transform(X_test_csv)


# In[ ]:


# Get the names of the selected features
selected_feature_names = df_train.columns[:-1][rfe.support_]
selected_feature_names = list(selected_feature_names)
print("Selected features:", selected_feature_names)


# # Train the Models using Selected Features

# **To build the precision of the model, we utilized three distinctive algorithms which are as per the following**
# * Decision Tree algorithm
# * Random Forest algorithm
# * Gradient Boosting algorithm
# * Support Vector Machines algorithm

# ## Decision Tree Algorithm

# In[ ]:


dtc = DecisionTreeClassifier(max_depth=37) 
dtc = dtc.fit(X_train_rfe,y_train)

y_pred=dtc.predict(X_test_rfe)
print("Decision Tree")
print("Accuracy of Training.csv Split Data")
print("Accuracy score:", accuracy_score(y_test, y_pred))
print("Number of correct predictions:", accuracy_score(y_test, y_pred,normalize=False))
print("Confusion matrix")
conf_matrix=confusion_matrix(y_test,y_pred)
print(conf_matrix)


# In[ ]:


y_pred=dtc.predict(X_test_csv_rfe)
print("Decision Tree")
print("Accuracy of Testing.csv")
print("Accuracy score:", accuracy_score(y_test_csv, y_pred))
print("Number of correct predictions:", accuracy_score(y_test_csv, y_pred, normalize=False))
print("Precision score:", precision_score(y_test_csv, y_pred, average='weighted', zero_division=1))
print("Confusion matrix")
conf_matrix=confusion_matrix(y_test_csv,y_pred)
print(conf_matrix)


# In[ ]:


df_results = pd.DataFrame(le.inverse_transform(y_test_csv), le.inverse_transform(y_pred)).reset_index()
df_results = df_results.rename(columns={'index':'Actual', 0:'Predicted'})
df_results


# ## Random Forest Algorithm

# In[ ]:


rfc = RandomForestClassifier()
rfc = rfc.fit(X_train_rfe,y_train)

# calculating accuracy 
y_pred=rfc.predict(X_test_rfe)
print("Random Forest")
print("Accuracy of Training.csv Split Data")
print("Accuracy score:", accuracy_score(y_test, y_pred))
print("Number of correct predictions:", accuracy_score(y_test, y_pred,normalize=False))
print("Confusion matrix")
conf_matrix=confusion_matrix(y_test,y_pred)
print(conf_matrix)


# In[ ]:


y_pred=rfc.predict(X_test_csv_rfe)
print("Random Forest")
print("Accuracy of Testing.csv")
print("Accuracy score:", accuracy_score(y_test_csv, y_pred))
print("Number of correct predictions:", accuracy_score(y_test_csv, y_pred, normalize=False))
print("Precision score:", precision_score(y_test_csv, y_pred, average='weighted', zero_division=1))
print("Confusion matrix")
conf_matrix=confusion_matrix(y_test_csv,y_pred)
print(conf_matrix)


# In[ ]:


df_results = pd.DataFrame(le.inverse_transform(y_test_csv), le.inverse_transform(y_pred)).reset_index()
df_results = df_results.rename(columns={'index':'Actual', 0:'Predicted'})
df_results


# ## Gradient Boosting

# In[ ]:


gbc = GradientBoostingClassifier()
gbc=gbc.fit(X_train_rfe,y_train)

y_pred=gbc.predict(X_test_rfe)
print("Gradient Boosting")
print("Accuracy of Training.csv Split Data")
print(accuracy_score(y_test, y_pred))
print(accuracy_score(y_test, y_pred,normalize=False))
print("Confusion matrix")
conf_matrix=confusion_matrix(y_test,y_pred)
print(conf_matrix)


# In[ ]:


y_pred=gbc.predict(X_test_csv_rfe)
print("Gradient Boosting")
print("Accuracy of Testing.csv")
print("Accuracy score:", accuracy_score(y_test_csv, y_pred))
print("Number of correct predictions:", accuracy_score(y_test_csv, y_pred, normalize=False))
print("Precision score:", precision_score(y_test_csv, y_pred, average='weighted', zero_division=1))
print("Confusion matrix")
conf_matrix=confusion_matrix(y_test_csv,y_pred)
print(conf_matrix)


# In[ ]:


df_results = pd.DataFrame(le.inverse_transform(y_test_csv), le.inverse_transform(y_pred)).reset_index()
df_results = df_results.rename(columns={'index':'Actual', 0:'Predicted'})
df_results


# ## Support Vector Machine

# In[ ]:


svc = SVC(gamma=100.0, C=1.0)
svc=svc.fit(X_train_rfe,y_train)

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
y_pred=svc.predict(X_test_rfe)
print("Support Vector Machine")
print("Accuracy of Training.csv Split Data")
print("Accuracy score:", accuracy_score(y_test, y_pred))
print("Number of correct predictions:", accuracy_score(y_test, y_pred,normalize=False))
print("Confusion matrix")
conf_matrix=confusion_matrix(y_test,y_pred)
print(conf_matrix)


# In[ ]:


y_pred=svc.predict(X_test_csv_rfe)
print("Support Vector Machine")
print("Accuracy of Testing.csv")
print("Accuracy score:", accuracy_score(y_test_csv, y_pred))
print("Number of correct predictions:", accuracy_score(y_test_csv, y_pred, normalize=False))
print("Precision score:", precision_score(y_test_csv, y_pred, average='weighted', zero_division=1))
print("Confusion matrix")
conf_matrix=confusion_matrix(y_test_csv,y_pred)
print(conf_matrix)


# In[ ]:


df_results = pd.DataFrame(le.inverse_transform(y_test_csv), le.inverse_transform(y_pred)).reset_index()
df_results = df_results.rename(columns={'index':'Actual', 0:'Predicted'})
df_results


# # Pickle the trained models for use in DiagnoBot

# In[ ]:


with open('diseasePrediction/le.pkl', 'wb') as f:
    pickle.dump(le, f)

with open('diseasePrediction/model.pkl', 'wb') as f:
    pickle.dump(svc, f)

with open('diseasePrediction/rfe_model.pickle', 'wb') as f:
    pickle.dump(rfe, f)

