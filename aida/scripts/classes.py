#!/usr/bin/python

"""
Class Factory and Instantiation Utilities.

This module provides factory functions to dynamically instantiate plot, 
system, and repository classes based on string identifiers, facilitating 
polymorphic operations across different data sources and visualization types.

@package AIDA
@module classes
"""

import systems
import plots
import repos

def plot_inst(pname):
    """Instantiate a plot visualization class based on name.

    Parameters
    ----------
    pname : str
        Name identifier of the plot type.

    Returns
    -------
    pclass : object
        An instance of the requested plot class.
    """ 
    classname = pname.lower().capitalize()
    class_ = getattr(plots, classname)
    pclass = class_()
    return pclass
  
def sys_inst(source):
    """Instantiate a system data source class based on source name.

    Parameters
    ----------
    source : str
        Data system source identifier.

    Returns
    -------
    sysclass : object
        An instance of the requested system class.
    """
    classname = source.lower().capitalize()
    class_ = getattr(systems, classname)
    sysclass = class_()
    return sysclass

def repos_inst(repo):
    """Instantiate a data repository interface class based on repository name.

    Parameters
    ----------
    repo : str
        Data repository identifier.

    Returns
    -------
    repoclass : object
        An instance of the requested repository class.
    """
    classname = repo.upper()
    class_ = getattr(repos, classname)
    repoclass = class_()
    return repoclass    