#!/usr/bin/python

import json
import ast
import numpy as np
import cgi, cgitb 
#cgitb.enable()  # for troubleshooting
import functions as util
from iotstats	import Data

def calc_stat(datain, stats):
	data = Data(datain)	
	res_dict = {}

	for name, curr_conf in stats.items():
		if type(curr_conf) == str:
			if len(datain) == 0:
				res = "-"
			else:
				res = getattr(data,curr_conf)()		
			res_dict.update({name : res})
		elif type(curr_conf) == dict: 
				# get npar
				npar = curr_conf['npar']
				func = curr_conf['func']
				params = curr_conf['params']
				names = list(params.keys())
				
				vals = list(params.values())
				
				for p in range(0, len(vals), npar):
					out_key = name
					exp_par = vals[p:(p+npar)]
					for i in range(len(exp_par)):
						out_key = out_key+" "+names[i]+"="+str(exp_par[i])
					
					exp_p_names_full = names[p:(p+npar)]
					#remove _i for multi configuration of analysis
					exp_p_names = [x.split("_")[0] for x in exp_p_names_full]                    
					final_par = {}
					for idx, el in enumerate(exp_par):
						try:
							el = ast.literal_eval(el)
						except ValueError:
							pass	
						final_par.update({exp_p_names[idx] : el})

					if len(datain) == 0:
						res = "-"
					else:
						res = getattr(data,func)(**final_par)                    
					
					res_dict.update({out_key : res})

	return(res_dict)
  

def get_global_stats(stats):
	conf = util.repConfig()
	connection = util.connect_db(conf.data['local_db'])
	query_globals = util.db_query(connection, "statistics", "stat_name, stat_function", "WHERE stat_type='"+stats+"'")
	stats_config = {}
	for item in query_globals:
		stats_config.update({item['stat_name'] : item['stat_function']})  
	return stats_config
  
def do_calculation(indata, plot, stats_config, ny):
	result = {}
	resultx = {}
	# Calculate statistics
	toremove_x=np.array([])
   	
	# x data if existing
	if plot == "scatter":
		try:      
			datax = np.array(indata["x"], dtype = float)
		except:
			datax = np.array([])
		toremove_x = np.where(datax == -999)[0]
	
	# y0 data
	try:    
		datay0 = np.array(indata["y0"], dtype = float)
	except:
		datay0 = np.array([])

	toremove_y = np.where(datay0 == -999)[0]

	toremove = np.append(toremove_x, toremove_y)
	if len(toremove) > 0:
		toremove = np.int_(toremove)
	if plot == "scatter":
		if len(toremove) > 0:      
			datax0 = np.delete(datax, toremove)
		else:
			datax0 = datax
		stats_x = calc_stat(datax0, stats_config)
		result.update({"x_stats" : stats_x})	
	else:
		result.update({"x_stats" : "None"})
        
	if len(toremove) > 0:
		datay0 = np.delete(datay0, toremove)	       
   
	stats_y0 = calc_stat(datay0, stats_config)
	result.update({"y0_stats" : stats_y0})

	# additional y data
	if ny > 1:
		for i in range(ny-1):
			try:			
				datay = np.array(indata["y"+str(i+1)], dtype = float)
			except:
				datay = np.array([])              
			toremove_y = np.where(datay == -999)[0]
			toremove = np.append(toremove_x, toremove_y)
			if len(toremove) > 0:
				toremove = np.int_(toremove)            
			if plot == "scatter":
				if len(toremove) > 0:              
					dataxi = np.delete(datax, toremove)
				else:
					dataxi = datax
				stats_x = calc_stat(dataxi, stats_config)
				resultx.update({"x_stats"+str(i+1) : stats_x})	
			else:
				result.update({"x_stats" : "None"})
			if len(toremove) > 0:                
				datay = np.delete(datay, toremove)
			stats_y = calc_stat(datay, stats_config)
			result.update({"y"+str(i+1)+"_stats" : stats_y})
	result.update(resultx)
    
	result = str(result).replace("'",'"')
	return result
        
def main(data):
	
	inputdata = json.loads(data['inputdata'].value)
	ny = int(data['ny'].value)
	plot = data["plot_type"].value
	stats = data["stats_type"].value	

	if stats == "global" :
		stats_config = get_global_stats(stats)
	elif stats == "advanced" : 
		stats_config = json.loads(data['stats_config'].value)
       
	result = do_calculation(inputdata, plot, stats_config, ny)
	print(result)

if __name__ == "__main__":
	print("Content-Type: application/json")
	print()

	#the cgi library gets vars from html
	data = cgi.FieldStorage()

	main(data)