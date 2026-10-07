#!/usr/bin/python

"""
Machine Learning Model Help Inspector.

This command-line script retrieves and prints the official docstring/help
documentation for a specified scikit-learn estimator class name.

@package AIDA
@module helpMlModel
"""

import sys
from sklearn.utils import all_estimators
estimators = all_estimators()

for name, class_ in estimators:
    if name==sys.argv[1]:
        print(help(class_))
    