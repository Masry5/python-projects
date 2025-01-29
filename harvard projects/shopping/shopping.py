import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
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
        - Weekend, an integer 0 (if false) or 1 (if true)"""
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        
        
        evidence = []
        labels=[]
        for row in reader:
            evidence0 = []
            mnumber=month(row[10])
            evidence0 += [convert_to_number(cell) for cell in row[:10]] 
            evidence0.append(mnumber)
            evidence0 += [convert_to_number(cell) for cell in row[11:15]]
            visitor=1
            if row[15]!='Returning_Visitor':
                visitor=0
            evidence0.append(visitor)
            weekend=0
            if row[16]=='TRUE':
                weekend=1
            evidence0.append(weekend)
            evidence.append(evidence0[:])
            
            label=0
            if row [17]=='TRUE':
                label=1    
            labels.append(
                label
            )
    return (evidence,labels)



def month(m):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months.index(m)

def convert_to_number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    num_label0=0
    num_label1=0
    num_prediction0=0
    num_prediction1=0
    for label in range(len(labels)):
        if labels[label]==1:
            num_label1+=1
            if predictions[label]==1:
                num_prediction1+=1
        if labels[label]==0:
            num_label0+=1
            if predictions[label]==0:
                num_prediction0+=1
    
    sensitivity=num_prediction1/num_label1
    specificity=num_prediction0/num_label0
    
    return (sensitivity,specificity)



if __name__ == "__main__":
    main()
