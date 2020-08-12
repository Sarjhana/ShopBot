import csv
import sys
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    '''if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")'''

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data('shopping.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    df = pd.read_csv(filename)
    int_cols =  ['Administrative', 'Informational', 'ProductRelated', 'OperatingSystems',
                    'Browser', 'Region', 'TrafficType']
    float_cols = ['Administrative_Duration', 'Informational_Duration','ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']

    df[int_cols] = df[int_cols].astype(int)
    df[float_cols] = df[float_cols].astype(float)
    
    le = preprocessing.LabelEncoder()
    le.fit(df['Weekend'])
    df.Weekend = le.transform(df['Weekend'])                    

    le = preprocessing.LabelEncoder()
    le.fit(df['Month'])
    df.Month = le.transform(df['Month'])

    le = preprocessing.LabelEncoder()
    le.fit(df['VisitorType'])
    df.VisitorType = le.transform(df['VisitorType'])

    le = preprocessing.LabelEncoder()
    le.fit(df['VisitorType'])
    df.VisitorType = le.transform(df['VisitorType'])

    le = preprocessing.LabelEncoder()
    le.fit(df['Revenue'])
    df.Revenue = le.transform(df['Revenue'])

    labels = df['Revenue'].tolist()

    df = df.drop(['Revenue'], axis = 1)
    evidence = df.to_numpy().tolist()

    return(evidence,labels)  
       
    #raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(evidence, labels)
    return knn
    
    #raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    y_actual = np.array(labels)
    y_predicted = np.array(predictions)
    
    true_pos = np.sum((y_actual == 1) & (y_predicted == 1))
    false_pos = np.sum((y_actual == 0) & (y_predicted ==1))
    true_neg = np.sum((y_actual == 0) & (y_predicted == 0))
    false_neg = np.sum((y_actual == 1) & (y_predicted == 0))

    sens = true_pos / (true_pos + false_neg)
    spec = true_neg / (true_neg + false_pos)

    return (sens, spec)
    #raise NotImplementedError


if __name__ == "__main__":
    main()
