import csv
import sys
import shopping

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
        - Month, an index from 0 (January) to 11 (December)(9)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)"""
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        
        evidence0 = []
        evidence = []
        labels=[]
        for row in reader:
            mnumber=shopping.month(row[10])
            evidence0.append(
                cell for cell in row[:10]
            ) 
            evidence0.append(mnumber)
            evidence0.append(
                cell for cell in row[10:15]
            )
            visitor=1
            if row[15]!='Returning_Visitor':
                visitor=0
            evidence0.append(visitor)
            weekend=0
            if row[16]=='True':
                weekend=1
            evidence0.append(weekend)
            evidence.append(evidence0)
            
            label=0
            if row [17]=='True':
                label=1    
            labels.append(
                label
            )   
    print(labels)
load_data("shopping.csv")

