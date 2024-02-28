#!/usr/bin/python



from sklearn.utils import all_estimators
import inspect
estimators = all_estimators()
listExcluded=['VotingClassifier','VotingRegressor','CalibratedClassifierCV','ClassifierChain','GridSearchCV']
for name, class_ in estimators:
    
	if hasattr(class_, 'predict') and hasattr(class_, 'fit') and name[0]!="_":
		if name not in listExcluded:
			print(name)
    