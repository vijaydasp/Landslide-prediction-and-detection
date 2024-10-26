import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

def load_data(tem,hum,rain,moi):

    landslide_dataset = pd.read_csv('dataset.csv')

    X = landslide_dataset.drop(columns='Landslide', axis=1)
    Y = landslide_dataset['Landslide']

    scaler = StandardScaler()
    scaler.fit(X)
    standardized_data = scaler.transform(X)

    X = standardized_data

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)
    print(X.shape, X_train.shape, X_test.shape)

    classifier = svm.SVC(kernel='linear')
    classifier.fit(X_train, Y_train)

    X_train_prediction = classifier.predict(X_train)
    training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
    print('Accuracy score of the training data : ', training_data_accuracy)

    X_test_prediction = classifier.predict(X_test)
    test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
    print('Accuracy score of the test data : ', test_data_accuracy)

    input_data = (tem,hum,rain,moi)
    print(input_data)

    input_data_df = pd.DataFrame([input_data], columns=landslide_dataset.drop(columns='Landslide').columns)

    std_data = scaler.transform(input_data_df)

    prediction = classifier.predict(std_data)

    if prediction[0] == 0:
        return 'No Landslide'
    else:
        return 'Landslide'

# load_data(19.93899667,64.19237333,51195.41667,47.00263333)

