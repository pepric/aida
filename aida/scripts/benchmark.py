#!/usr/bin/python

import cgi, cgitb 
#cgitb.enable()  # for troubleshooting
import numpy as np
from    os              import system, mkdir
import json
import datetime
import sys
import functions as util
import multiprocessing
import subprocess
import pymysql
import pymysql.cursors
from time import sleep

def read_config():
	fileobj = open("benchmark_config.json", "r")
	jsonstr = fileobj.read()
	fileobj.close()
	#convert input string to json object
	config = json.loads(jsonstr)
	return config
