import sys
import json
import numpy as np
import pandas as pd
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#loading data from sklearn
breast_cancer_data = sklearn.datasets.load_breast_cancer()
# print(breast_cancer_data)
#loading data to data frame
data_frame=pd.DataFrame(breast_cancer_data.data , columns = breast_cancer_data.feature_names)

# print(data_frame.head())

# adding target to dataframe
data_frame['label'] =  breast_cancer_data.target

# print(data_frame.shape)

# cleaning data
X = data_frame.drop(columns='label', axis=1)
Y = data_frame['label']

# splitting data
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, random_state=2)

model = LogisticRegression()

# training model
model.fit(X_train,Y_train)

# evaluation 
X_train_prediction = model.predict(X_train)
training_accuracy = accuracy_score(Y_train, X_train_prediction)
# print("accuracy on  training is ", training_accuracy)

X_test_prediction = model.predict(X_test)
test_accuracy = accuracy_score(Y_test, X_test_prediction)
# print("accuracy on test is ", test_accuracy)

# building predictive system
# Read data from stdin
input_data = sys.stdin.read()
# print('running')
received_data = json.loads(input_data)

# Print the received data (for debugging)
# print("Received data:" ,received_data)

numeric_data = [float(value) for value in received_data]
columns = [
        'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 
        'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 
        'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 
        'area error', 'smoothness error', 'compactness error', 'concavity error', 
        'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 
        'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 
        'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 
        'worst fractal dimension'
    ]
input_df = pd.DataFrame([numeric_data], columns=columns)

    # Make prediction
prediction = model.predict(input_df)[0]
probability = model.predict_proba(input_df)[0].tolist()

    # Respond with the prediction and probabilities
response = {
        "message": "Prediction successful",
        "prediction": int(prediction),  # Assuming binary classification (0 or 1)
        "probability": probability
    }
sys.stdout.write(json.dumps(response))


# Respond back to Node.js
# sys.stdout.write(json.dumps({"message": "Data received", "data": numeric_data}))