#!/usr/bin/python
import sys
from sklearn.utils import all_estimators
estimators = all_estimators()

for name, class_ in estimators:
	if name==sys.argv[1]:
		print(help(class_))
    