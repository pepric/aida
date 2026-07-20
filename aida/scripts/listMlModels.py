#!/usr/bin/python



from sklearn.utils import all_estimators
import inspect
import cgi, cgitb
cgitb.enable(display=0, logdir="cgi-logs")  # for troubleshooting
import json


def main(data):
    ml = data['ml_type'].value
    model_list = []
    error = 0
    estimators = all_estimators(type_filter = ml)
    listExcluded=['VotingClassifier','VotingRegressor','CalibratedClassifierCV','ClassifierChain','GridSearchCV']
    
    for name, class_ in estimators:
        if hasattr(class_, 'predict') and hasattr(class_, 'fit') and name[0]!="_":
            if name not in listExcluded:
                model_list.append(name)
    if len(model_list) == 0:
        model_list = "No model available"
        error = 1
    
    out={"out":model_list, "error":error}
    
    print(json.JSONEncoder().encode(out))


if __name__ == "__main__":
    print("Content-Type: application/json")
    print()
    
    #the cgi library gets vars from html
    data = cgi.FieldStorage()
    
    main(data)