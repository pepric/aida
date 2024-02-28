#!/usr/bin/python

import json
import cgi, cgitb 
cgitb.enable(display=0, logdir="cgi-logs")   # for troubleshooting
import functions as util
import numpy as np
import csv
import classes
from astropy.io import fits
from astropy.table import Table
from dateutil.parser import parse
from db_io import dbIO

def get_fits_data(filename,cols=None):
	"""Get data from uploaded FITS file. If cols is not defined, columns name are taken, else load data
	Parameters
	-----------
	filename: str,
		full file name with path
	cols : list or None,
		list of column names selected    
        
	Returns
	-----------
		header : list or None,
			list containing the names of file columns. Returned if cols is None.
		error : 0, 1 or 2
			error code: 0 is all ok, 1 if it is impossible to get the header, 2 if returned no header. Returned if cols is None.
		result: dictionary
			dictionary containing data retrieved from data repository. It is structured as follow:
			result={
					'date' : [0,1,...,len(data)-1],
					'x': [<x_parameter_1 as string (or '0' if not required)>, <x_parameter_2>, ... ,<x_parameter_N>]
					'y0': [<y0_parameter_1 as string>, <y0_parameter_2>, ... ,<y0_parameter_N>],
					'y1': [<y1_parameter_1 as string>, <y1_parameter_2>, ... ,<y1_parameter_N>],
					...
					'y<M>': [<yM_parameter_1 as string>, <yM_parameter_2>, ... ,<yM_parameter_N>],
				}
			Records 'y1'...'y<M>' are reported only if they have been required from user. Missing data are replaced by -999. 
			String data are replaced by -999 except for "date" in trend case.
	"""
    # if cols is None, get the header
	if cols is None:  
		try:
			#open fits file
			hdul = fits.open(filename)
			t = Table(hdul[1].data)
			#get header columns names			
			header = t.colnames
			hdul.close()
			#if no data, return error 2
			if len(t) == 0:
				return header, 2
			return header, 0
		except:
			return None, 1
	else:
      	#get data
		result = {}
		#open fits file        
		hdul = fits.open(filename)
		data = Table(hdul[1].data)
		#for each column, get the value used for null values        
		null_list = hdul[1].columns.nulls
		#columns names        
		hdul_cols = hdul[1].columns.names
        #dates are the row index
		result.update({"date" : list(range(len(data)))})
		#if x label is present
		if cols[0] != "None":
			#check if data are string
			if data[cols[0]].dtype.type is np.str_:
              	#if data are dates, it's ok
				for i,d in enumerate(data[cols[0]]):
					if not is_date(d):
						data[cols[0]][i] = -999
				result.update({"x" : data[cols[0]].tolist()})                
			else:          
        	  	#find nans
				pos = hdul_cols.index(cols[0])
				null_val = null_list[pos]
				if null_val != "":
					fnan = np.where(data[cols[0]] == null_val)
					data[cols[0]][fnan] = -999 
                
				result.update({"x" : data[cols[0]].tolist()})
		else:
			#update x result with list of zeros
			result.update({"x" : np.zeros(len(data)).tolist()})
            
		#get y data
		for i, idx in enumerate(cols[1:]):
			#check if data are string
			if data[idx].dtype.type is np.str_:
				res_arr = -999*np.ones(len(data))              
				result.update({"y"+str(i) : res_arr.tolist()})
			else:            
	          	#find nans 
				pos = hdul_cols.index(idx)
				null_val = null_list[pos]
				if null_val != "":
					fnan = np.where(data[idx] == null_val)
					data[idx][fnan] = -999            
				result.update({"y"+str(i) : data[idx].tolist()})
		hdul.close()

		return result
        
def get_csv_data(filename, has_header=False, cols=None):
	"""Get data from uploaded CSV file. If cols is not defined, columns name are taken, else load data
	Parameters
	-----------
	filename: str,
		full file name with path
	has_header : False, "0" or "1",
		value indicating if the file has the header ("1") or not ("0") or not required (False). Default is False
	cols : list or None,
		list of column names selected    
        
	Returns
	-----------
		header : list or None,
			list containing the names of file columns. If has_header="0", column names are defined as col<i>. Returned if cols is None.
		error : 0, 1 or 2
			error code: 0 is all ok, 1 if it is impossible to get the header, 2 if returned no header. Returned if cols is None.
		result: dictionary
			dictionary containing data retrieved from data repository. It is structured as follow:
			result={
					'date' : [0,1,...,len(data)-1],
					'x': [<x_parameter_1 as string (or '0' if not required)>, <x_parameter_2>, ... ,<x_parameter_N>]
					'y0': [<y0_parameter_1 as string>, <y0_parameter_2>, ... ,<y0_parameter_N>],
					'y1': [<y1_parameter_1 as string>, <y1_parameter_2>, ... ,<y1_parameter_N>],
					...
					'y<M>': [<yM_parameter_1 as string>, <yM_parameter_2>, ... ,<yM_parameter_N>],
				}
			Records 'y1'...'y<M>' are reported only if they have been required from user. Missing data are replaced by -999. 
			String data are replaced by -999 except for "date" in trend case.
	"""  
    # if cols is None, get the header  
	if cols is None:  
		try:
			#open file
			with open(filename) as csvfile:
              	#get header
				reader = csv.reader(csvfile)
				i = next(reader)
                #check header
				if has_header == "1":
					header = i
				else:
					header = ["col"+str(x+1) for x in range(len(i))]
				#check there are data
				try:
					i = next(reader)
				except:
					return header, 2
			return header, 0
		except:
			return None, 1
	else:
      	#get data
		result = {}
		#open file        
		with open(filename) as csvfile:
			if has_header == "1":
				skip_header = 1
				reader = csv.reader(csvfile)
    			#get full header
				header = next(reader)
				new_cols = []
                #check if x parameter is defined or None
				for x in cols:
					#get only requested columns header
					if x != "None":
						new_cols.append(header.index(x))
					else:
						new_cols.append("None")
			else:
              	#no header --> use column index
				new_cols= []
				for x in cols:
                  	#check if x parameter is defined or None
					if x == "None":
						new_cols.append(x)
					else:
						new_cols.append(int(x.replace("col",""))-1)
				skip_header = 0        
		#load data        
		data = np.genfromtxt(filename, delimiter=",", skip_header=skip_header, dtype=str)
        #dates are the row index
		result.update({"date" : list(range(len(data)))})

		for (i,j),val in np.ndenumerate(data):
			if j in new_cols:
				#check if it is a number
				try:
					float(val)
				except:
					if new_cols.index(j)==0:
						#check if x is a date
						if not is_date(val.replace('"',"").replace("'","")):
							data[i][j]=-999
						else:
							data[i][j] = val.replace('"',"").replace("'","")
					else:
						data[i][j]=-999        
		data = data.transpose()        
        #collect data
		xlabel = new_cols[0]
		#if x label is present, use data as they are, else set x data to list of zeros
		if xlabel != "None":
			result.update({"x" : list(data[xlabel])})
		else:
			result.update({"x" : list(np.zeros(len(data[0])))})
		#collect y data            
		for i, idx in enumerate(new_cols[1:]):
			result.update({"y"+str(i) : list(data[idx])})
            
		return result

def get_ascii_data(filename,cols=None):
	pass  
  
def get_cols(filename, fmt, header=False, origin=""):
	"""Get columns from uploaded file.
	Parameters
	-----------
	filename: str,
		full file name with path
	fmt : "fits", "csv", "ascii",
    	file format
	header : False, "0" or "1",
		value indicating if the file has the header ("1") or not ("0") or not required (False). Default is False
	origin : "local" or "",
		if local, it indicates that file has been previously uploaded and it is in local DB. Default is "".    
        
	Returns
	-----------
		cols : list,
			list containing the names of file columns.
		error : int
			0 is all ok; 
			1 error, it is impossible to get cols, 
			2 error, if no data
			3 warning, file ok but it is impossible to store info into local DB
			4 warning, file ok but already present into local DB, then updated
	"""
	#call different functions for different file format    
	if fmt == "fits":
		cols, error = get_fits_data(filename)
	elif fmt == "csv":
		cols, error = get_csv_data(filename, has_header=header)
	elif fmt == "ascii":
		cols, error = get_ascii_data(filename)
	#if file format is csv with no header, indicate it in a variabile to store into DB
	if header!="1" and fmt == "csv":
		fmt += "_noheader"
	#if no error and filename is not taken from already uploaded files, add file to local_files table in DB
	if error == 0 and origin != "local":
		try:
			conf = util.repConfig() 	
			dbinst = dbIO(conf.data['local_db'])
			user = filename.split("/")[2]
			fname = filename.split("/")[4]
			#check if filename is already in DB
			counts = dbinst.count_records("local_files", "WHERE filename = '"+fname+"' AND username = '"+user+"' AND data_source='"+fmt+"'", keep_open = True)

			if counts > 0:
				dbinst.close()
				error = 4
			else:
              	#insert into DB
				dbIO(conf.data['local_db']).insert_local_file(fname, fmt , user, ftype="upload")
		except:
			error = 3
	return cols, error
  
def get_uploaded_data(filename, fmt, plot, cols, header = False):
	"""Get data from uploaded file.
	Parameters
	-----------
	filename: str,
		full file name with path
	fmt : "fits", "csv", "ascii",
    	file format
	plot: string,
		analysis to perform
	cols : list,
		list of columns selected        
	header : False, "0" or "1",
		value indicating if the file has the header ("1") or not ("0") or not required (False). Default is False
        
	Returns
	-----------
		result: dictionary
			dictionary containing data retrieved from data repository. It is structured as follow:
			dictionary containing data retrieved from data repository. It is structured as follow:
			result={
					'date' : [<date_parameter_1>, <date_parameter_2>,...,<date_parameter_N>] ([0,1,...,len(data)-1] if not required)
					'x': [<x_parameter_1 as string (or '0' if not required)>, <x_parameter_2>, ... ,<x_parameter_N>]
					'y0': [<y0_parameter_1 as string>, <y0_parameter_2>, ... ,<y0_parameter_N>],
					'y1': [<y1_parameter_1 as string>, <y1_parameter_2>, ... ,<y1_parameter_N>],
					...
					'y<M>': [<yM_parameter_1 as string>, <yM_parameter_2>, ... ,<yM_parameter_N>],
					'errstatus' : 0, 
					'warningstatus':0, 
					'datastatus':0, 
					'infostatus':0
				}
			Records 'y1'...'y<M>' are reported only if they have been required from user. Missing data are replaced by -999. 
			If plot is a trend analysis, then list "x" is moved to "date" and list "x" is replaced by list of zeros.
	"""   
	result = {}
	#call different functions for different file format    
	if fmt == "fits":
		result = get_fits_data(filename, cols)
	elif fmt == "csv":
		result = get_csv_data(filename, header, cols)
	elif fmt == "ascii":
		result = get_ascii_data(filename, cols)

	#modify result moving dates if trend
	if plot != "stats":
		pinst = classes.plot_inst(plot)
		if pinst.vs == "time":
			result['date'] = result['x']
			result['x'] = np.zeros(len(result['date'])).tolist()
	#add errors status flags to compatibily with JS rendering functions        
	result.update({'errstatus' : 0, 'warningstatus':0, 'datastatus':0, 'infostatus':0})        
	return result        

def is_date(string, fuzzy=False):
	"""
	Return whether the string can be interpreted as a date.

	Parameters
	----------
	string: str, string to check for date
	fuzzy: bool, ignore unknown tokens in string if True
    
	Returns
	---------
	True if string can be interpreted as date, False otherwise
	"""
	try: 
		parse(string, fuzzy=fuzzy)
		return True
	except ValueError:
		return False  
	
def main(data):
	"""
	Get data from uploaded file. If cols is not defined, columns name are taken, else load data

	Parameters
	----------
	data: cgi Field Storage object,
		object containing data posted by form
	"""
	#get data from form    
	filename = data['filename'].value
	fmt = data['fmt'].value
	action = data['action'].value
	user = data['user'].value
	header = data['header'].value
	fullfile = "../users/"+user+"/tmp/"+filename
	try:
		cols = data.getlist('cols[]')    
	except:
		cols=[]
	#origin is present if file is taken from the list of already stored tmp files        
	try:
		origin = data['origin'].value
	except:
		origin = ""
	if action == "get_cols":
		res = get_cols(fullfile, fmt, header, origin)
		out = {"cols":res[0], "error":res[1]}
	elif action == "get_data":
		plot = data['plot'].value        
		out = get_uploaded_data(fullfile, fmt, plot, cols, header)
        
	print(json.JSONEncoder().encode(out))        
        
if __name__ == "__main__":
	print("Content-Type: application/json")
	print()
	#the cgi library gets vars from html
	data = cgi.FieldStorage()
	
	main(data)