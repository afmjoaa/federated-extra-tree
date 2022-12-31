import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing

# READ FROM CSV
df = pd.read_csv('ds_all.csv')
X = df.drop(columns=['Loan_Status', 'Loan_ID'], axis=1)
y = df['Loan_Status']

# ENCODE THE INPUT
encoder = OneHotEncoder()
encoder.fit(X)
X_encoded = encoder.transform(X)

# ENCODE THE OUTPUT
label_encoder = preprocessing.LabelEncoder()
label_encoder.fit(y)
y_encoded = label_encoder.transform(y)

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.3)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

predictions = rf.predict(X_test)

# PRINT PREDICTION RESULT
print(confusion_matrix(y_test, predictions))
print('\n')
print(classification_report(y_test, predictions))
