#!/usr/bin/python

import systems
import plots
import repos

def plot_inst(pname):
	"""Instantiate a plot class.
	Parameters
	----------
	pname : str,
		name of the plot
	Returns
	---------
	pclass : class,
		instance of the class
	"""  
	classname = pname.lower().capitalize()
	class_ = getattr(plots, classname)
	pclass = class_()
	return pclass
  
def sys_inst(source):
	"""Instantiate a system class.
	Parameters
	----------
	source : str,
		data source
	Returns
	---------
	sysclass : class,
		instance of the class
	"""
	classname = source.lower().capitalize()
	class_ = getattr(systems, classname)
	sysclass = class_()
	return sysclass

def repos_inst(repo):
	"""Instantiate a repository class.
	Parameters
	----------
	repo : str,
		repository source 
	Returns
	---------
	repoclass : class,
		instance of the class
	"""
	classname = repo.upper()
	class_ = getattr(repos, classname)
	repoclass = class_()
	return repoclass    