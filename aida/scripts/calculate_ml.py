#!/usr/bin/python

import json
import ast
import numpy as np
import sys
import os
import  threading
import cgi, cgitb 
#cgitb.enable()  # for troubleshooting
import functions as util
from iotstats	import Data


def data_to_db(filename, filepath, username, date_exp, ext, filetype, status_exp, comment_exp):
	logFileSql=open("/data/exp/www/aida/logSQL.txt","w")
	logFileSql.write("Open connection\n")
	conf = util.repConfig()
	connection = util.connect_db(conf.data['local_db'])
	logFileSql.write("conn aperta\n")	
	sql = "INSERT INTO user_files (filename, filepath, username, date_exp, ext, filetype, status_exp, comment_exp) VALUES ('"+filename+"', '"+filepath+"', '"+username+"', '"+date_exp+"', '"+ext+"', \""+filetype+"\", \""+status_exp+"\", \""+comment_exp+"\")"
	logFileSql.write(sql+"\n")
	if sql!="":
		with connection.cursor() as cursor:
			cursor.execute(sql)
		connection.commit()
	connection.close()
	logFileSql.write("All done\n")


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
					
					exp_p_names = names[p:(p+npar)]
					final_par = []
					for el in exp_par:
						try:
							el = ast.literal_eval(el)
						except ValueError:
							pass
						final_par.append(el)
					if len(datain) == 0:
						res = "-"
					else:
						res = getattr(data,func)(*final_par)
					
					res_dict.update({out_key : res})

	return(res_dict)

def main(data, nthreads):

	################ ONLY FOR DEBUG
	#inputdata = {"date":["2019-04-02T00:00:00","2019-04-03T00:00:00","2019-04-04T00:00:00","2019-04-05T00:00:00","2019-04-06T00:00:00","2019-04-07T00:00:00","2019-04-08T00:00:00","2019-04-09T00:00:00","2019-04-10T00:00:00","2019-04-11T00:00:00","2019-04-12T00:00:00","2019-04-13T00:00:00","2019-04-14T00:00:00","2019-04-15T00:00:00","2019-04-16T00:00:00","2019-04-17T00:00:00","2019-04-18T00:00:00"],"x":["0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0"],"y0":["69.21638615708184","66.90556109487454","74.86118241313928","71.6018307941061","67.81558432328869","60.09820784655503","57.408907477035314","56.09788043084232","60.74220931535447","58.2045622334014","60.949381362632735","61.733764651602804","73.47909124804964","68.19246446907782","79.29795339446473","79.2173762510978","85.02872002141123"],"y1":["26.19946778456455","24.740152103656357","25.942341677301876","25.01894580068024","25.339957672764275","27.35162662005517","29.627224389818927","30.60641279251202","28.615047863502838","25.91886894195879","24.17286993421325","22.209690482642966","20.98046994535836","19.962610264943457","20.71634789245237","20.512296870267498","20.606760793675477"]}
	
	#ny = 2
	#plot = "stats"
	#stats = "advanced"
	################
	
	
	inputdata = json.loads(data['inputdata'].value)
	ny = int(data['ny'].value)
	plot = data["plot_type"].value
	stats = data["stats_type"].value	

	if stats == "global" :
		conf = util.repConfig()
		connection = util.connect_db(conf.data['local_db'])
		query_globals = util.db_query(connection, "statistics", "stat_name, stat_function", "WHERE stat_type='global'")
		stats_config = {}
		for item in query_globals:
			stats_config.update({item['stat_name'] : item['stat_function']})
	elif stats == "advanced" : 
		################ ONLY FOR DEBUG
		#stats_config= {"Min":"dqc_min","Max":"dqc_max","Percentile":{"func":"dqc_percentile","params":{"q":"50","interpolation":"linear","q_1":"50","interpolation_1":"linear"},"npar":2},"Sigma_Clip":{"func":"dqc_sigma_clip","params":{"sigma":"3","function":"mean"},"npar":2}}
		
		stats_config = json.loads(data['stats_config'].value)

	result = {}
	resultx = {}
	# Calculate statistics
	toremove_x=np.array([])
	
	# x data if existing
	if plot == "scatter":
		datax = np.array(inputdata["x"], dtype = float)
		toremove_x = np.where(datax == -999)[0]

	# y0 data
	datay0 = np.array(inputdata["y0"], dtype = float)
	toremove_y = np.where(datay0 == -999)[0]

	toremove = np.append(toremove_x, toremove_y)
 
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
   
	a=open("infoml.txt", "a")
	a.write(data['stats_config'].value+"\n")
	a.write(data['inputdata'].value+"\n")

	dataFeat=np.zeros((len(inputdata['y0']),ny))
	dataLabel=np.array(inputdata["x"], dtype = float)
 	
	# additional y data
	if ny > 1:
		dataFeat=np.zeros((len(inputdata['y0']),ny))
		for i in range(ny-1):
			
			dataFeat[:,i+1]=np.array(inputdata["y"+str(i+1)], dtype = float)
			datay = np.array(inputdata["y"+str(i+1)], dtype = float)
			toremove_y = np.where(datay == -999)[0]
			toremove = np.append(toremove_x, toremove_y)
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
  
	modelname=data['model'].value

	username=data['username'].value     
	a.write(username+"\n")
	a.write("Boh\n")
  
	from sklearn.utils import all_estimators
	a.write("Boh\n")
	estimators = all_estimators()
	a.write("Boh\n")
     
	def tryeval(val):
		try:
			val = ast.literal_eval(val)
		except ValueError:
			pass
		return val
	a.write("Boh\n")	
	kwargs=json.loads(data['model_param'].value)
	a.write("Boh\n")
	for key in kwargs.keys():
		kwargs[key]=tryeval(kwargs[key])
	try:
		a.write("Boh2\n")
		for name, class_ in estimators:
			if name==modelname:
				modelObj=class_(**kwargs)
				break
		a.write(data['split'].value+' \n')
	    
		splitRate=int(data['split'].value)/100
		a.write(str(splitRate)+'\n')
		try:
			seedSplit=int(data['split'].value)
		except:
			seedSplit=None
		a.write(str(seedSplit)+'\n')
		if splitRate==1:
			a.write('sr=1\n')
			dataFeatTrain=dataFeat
			dataFeatTest=dataFeat
			dataLabelTrain=dataLabel
			dataLabelTest=dataLabel
		else:
			a.write(str(splitRate)+'sr!=1\n')
			from sklearn.model_selection import train_test_split
			dataFeatTrain, dataFeatTest, dataLabelTrain, dataLabelTest=  train_test_split(dataFeat, dataLabel, random_state=seedSplit, train_size=splitRate)
		    
		a.write('datasetsplittato\n')
		a.write(str(dataFeatTrain.shape)+" " +str(dataLabelTrain.shape)+" " +"\n")
		modelObj.fit(dataFeatTrain,dataLabelTrain)
		a.write('trained\n')
	    
		dataOut=np.zeros((dataLabelTest.shape[0],3))
		a.write('outputbase\n')

		dataOut[:,0]=dataLabelTest
		a.write('outputprimacol\n')
		predicted=modelObj.predict(dataFeatTest)
		dataOut[:,1]=predicted
		a.write('\n\n\n'+str(predicted.shape)+" "+str(dataLabelTest.shape)+'\n\n\n')
		dataOut[:,2]=dataLabelTest-predicted
	    
		from joblib import dump, load
		now = util.utc_now()
		a.write("utcnow\n")
		creation = now.strftime("%Y-%m-%d-%H-%M-%S")

	    
		a.write(creation+"\n")
		iodadir=(os.path.dirname(os.path.realpath(__file__)).replace("scripts",""))+'users'+os.sep+username+os.sep
		modelfilename=modelname+"-model-"+creation+'.joblib'
		a.write(modelfilename+"\n")
		outputfilename=modelname+"-output-"+creation+'.csv'
		a.write(outputfilename+"\n")


		np.savetxt(iodadir+outputfilename,dataOut,delimiter=',', header="target,output,difference")
		dump(modelObj, iodadir+modelfilename)
		a.write("db call 1\n")
		data_to_db(outputfilename, username, username, creation, 'csv', 'data', 'ok', 'ok')
		a.write("db call 2\n")
		data_to_db(modelfilename, username, username, creation, 'joblib', 'model', 'ok', str(ny))	    	    
		a.write("db done 1\n")
	except:
		errfile=open(os.path.dirname(os.path.realpath(__file__)).replace("scripts","")+"errlog.txt", "w")
		errfile.write("error!\n")
		errfile.close()

	result.update(resultx)
	result = str(result).replace("'",'"')
	print(result)
	a.write(result)
	a.close()

if __name__ == "__main__":
	print("Content-Type: application/json")
	print()
	nthreads = 4
	#the cgi library gets vars from html
	data = cgi.FieldStorage()
	#data = "debug"
	main(data, nthreads)