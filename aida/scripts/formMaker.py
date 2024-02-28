#!/usr/bin/python
import inspect
import sys
from sklearn.utils import all_estimators

estimators = all_estimators()

for name, class_ in estimators:
	if name==sys.argv[1]:
		sig=(inspect.signature(class_))
		parList=sig.parameters
		for parameter in parList:
			if parameter !='kwargs':
				print(parameter,sig.parameters[parameter].default)
		exit()