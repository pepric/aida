#!/usr/bin/python

"""
Scikit-Learn Estimator Listing CLI Script.

This command-line script lists all valid scikit-learn estimators implementing 
fit and predict methods.

@package AIDA
@module listMlTrainedModels
"""

from sklearn.utils import all_estimators
import inspect
estimators = all_estimators()

for name, class_ in estimators:
    
	if hasattr(class_, 'predict') and hasattr(class_, 'fit') and name[0]!="_":
		print(name)
    