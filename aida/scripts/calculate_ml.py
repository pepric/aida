#!/usr/bin/python
"""
Machine Learning Execution Engine.

This module manages the execution of Machine Learning experiments, including 
clustering, regression, and classification tasks. It interfaces with scikit-learn 
to split datasets, train models, and generate predictions. It also calculates 
statistical metrics on the datasets and exports the results, models (.joblib), 
and summary reports for the end user.

@package AIDA
@module calculate_ml
"""


import json
import ast
import numpy as np
import sys
import os
import  threading
import cgi, cgitb 
#cgitb.enable()  # for troubleshooting
import functions as util
from iotstats   import Data
from datetime import datetime
import traceback
import pandas as pd

def calc_stat(datain, stats):
    """Compute statistical metrics on numerical dataset according to configuration.

    Parameters
    ----------
    datain : array_like
        Input array or sequence of data values[cite: 8].
    stats : dict
        Dictionary mapping metric names to function names or parameter configurations[cite: 8].

    Returns
    -------
    res_dict : dict
        Dictionary mapping metric names to calculated statistical values.
    """
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

def do_calculation(data, inputdata, plot, stats_config, ny):
    """Execute machine learning workflow including training, prediction, and output generation.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Request parameters containing ML model name, parameters, split rate, and user metadata.
    inputdata : dict
        Dataset structure containing date, x, and y parameter series.
    plot : str
        Target operation or model type ("cluster", "regressor", etc.).
    stats_config : dict
        Global statistical configuration mapping.
    ny : int
        Number of Y feature parameters.

    Returns
    -------
    result : str
        JSON string containing statistical results, generated file paths, and execution status.
    """
    ################ ONLY FOR DEBUG
    #inputdata = {"date":["2019-04-02T00:00:00","2019-04-03T00:00:00","2019-04-04T00:00:00","2019-04-05T00:00:00","2019-04-06T00:00:00","2019-04-07T00:00:00","2019-04-08T00:00:00","2019-04-09T00:00:00","2019-04-10T00:00:00","2019-04-11T00:00:00","2019-04-12T00:00:00","2019-04-13T00:00:00","2019-04-14T00:00:00","2019-04-15T00:00:00","2019-04-16T00:00:00","2019-04-17T00:00:00","2019-04-18T00:00:00"],"x":["0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0"],"y0":["69.21638615708184","66.90556109487454","74.86118241313928","71.6018307941061","67.81558432328869","60.09820784655503","57.408907477035314","56.09788043084232","60.74220931535447","58.2045622334014","60.949381362632735","61.733764651602804","73.47909124804964","68.19246446907782","79.29795339446473","79.2173762510978","85.02872002141123"],"y1":["26.19946778456455","24.740152103656357","25.942341677301876","25.01894580068024","25.339957672764275","27.35162662005517","29.627224389818927","30.60641279251202","28.615047863502838","25.91886894195879","24.17286993421325","22.209690482642966","20.98046994535836","19.962610264943457","20.71634789245237","20.512296870267498","20.606760793675477"]}
    
    #ny = 2
    #plot = "stats"
    #stats = "advanced"
    ################
    # with open("prova.txt","w") as xx:
        # xx.write(str(data))    

    result = {}
    resultx = {}
    # Calculate statistics
    toremove_x=np.array([], dtype=int)
    dataDate = np.array(inputdata["date"])
    
    # x data if existing
    if plot != "cluster":
        datax = np.array(inputdata["x"], dtype = float)
        toremove_x = np.where(datax == -999)[0]
        

    # y0 data
    datay0 = np.array(inputdata["y0"], dtype = float)
    toremove_y = np.where(datay0 == -999)[0]

    toremove = np.append(toremove_x, toremove_y)

    datay_full = np.zeros((len(datay0),ny))
    datay_full[:,0] = datay0

    # append toremove_yi to toremove for additional y data
    if ny > 1:
        for i in range(ny-1):
            datay = np.array(inputdata["y"+str(i+1)], dtype = float)
            datay_full[:,i+1] = datay
            toremove_yi = np.where(datay == -999)[0]
            toremove = np.append(toremove, toremove_yi)
    toremove = np.unique(toremove)
    # toremove = np.asarray(toremove, dtype="int")    

    if len(toremove) > 0:
        if plot != "cluster":
            datax_clean = np.delete(datax, toremove)
            stats_x = calc_stat(datax_clean, stats_config)
            result.update({"x_stats" : stats_x})
        datay_clean = np.delete(datay_full, toremove, axis=0)
        datadate_clean = np.delete(dataDate, toremove)
    else:
        if plot != "cluster":
            datax_clean = datax
        datay_clean = datay_full
        datadate_clean = dataDate         
        
    #calculate stats
    if plot != "cluster":
        stats_x = calc_stat(datax_clean, stats_config)
        result.update({"x_stats" : stats_x})
        dataLabel = datax_clean
    else:
        dataLabel = np.zeros(len(datay_clean))
        result.update({"x_stats" : "None"})        
        
    for i in range(ny):    
        stats_y = calc_stat(datay_clean[:,i], stats_config)
        result.update({"y"+str(i)+"_stats" : stats_y})
    
    if ny > 1:
        dataFeat = datay_clean
    else:
        dataFeat = datay_clean[:,0]
  
    modelname=data['model'].value
    # a.write(modelname+"\n")
    username=data['username'].value     
    # a.write(username+"\n")

  
    from sklearn.utils import all_estimators
    estimators = all_estimators()
     
    def tryeval(val):
        try:
            val = ast.literal_eval(val)
        except ValueError:
            pass
        except SyntaxError:
            val = str(val)
        return val
 
    kwargs=json.loads(data['model_param'].value)
    # a.write(str(kwargs)+"\n")  
    for key in kwargs.keys():
        # a.write(str(key)+"----------")
        kwargs[key]=tryeval(kwargs[key])
        # a.write(str(kwargs[key])+"\n")  
    try:
        for name, class_ in estimators:
            if name==modelname:
                modelObj=class_(**kwargs)
                break
        # a.write(data['split'].value+' \n')
        splitRate=int(data['split'].value)/100
        # a.write(str(splitRate)+'\n')
        try:
            seedSplit=int(data['split'].value)
        except:
            seedSplit=None
        # a.write(str(seedSplit)+'\n')
        if splitRate==1:
            # a.write('sr=1\n')
            dataFeatTrain=dataFeat
            dataFeatTest=dataFeat
            dataLabelTrain=dataLabel
            dataLabelTest=dataLabel
            dataDateTrain = datadate_clean
            dataDateTest = datadate_clean
        else:
            # a.write(str(splitRate)+'sr!=1\n')
            from sklearn.model_selection import train_test_split
            dataFeatTrain, dataFeatTest, dataLabelTrain, dataLabelTest,dataDateTrain, dataDateTest=  train_test_split(dataFeat, dataLabel, datadate_clean, random_state=seedSplit, train_size=splitRate)
        
        # a.write('datasetsplittato\n')
        # a.write(str(dataFeatTrain.shape)+" " +str(dataLabelTrain.shape)+" " +"\n")
        try:
            modelObj.fit(dataFeatTrain,dataLabelTrain)
            # a.write('trained\n')
        except Exception as err:
            pass
            # a.write(str(err))

        #create output file
        #utcdates = [int(datetime.utcfromtimestamp(el).strftime('%Y%m%d%H%M%S')) for el in dataDateTest]        
        utcdates = dataDateTest   
        
        if plot != "cluster":
            predicted=modelObj.predict(dataFeatTest)
            df = pd.DataFrame({
                'dateID' : utcdates,
                'target' : dataLabelTest,
                'output' : predicted,
                'difference' : dataLabelTest-predicted
            })
        else:
            df = pd.DataFrame({
                'dateID' : utcdates,
                'cluster' : dataLabelTest.astype(np.int64)
            })
        
 
        from joblib import dump, load
        now = util.utc_now()
        # a.write("utcnow\n")
        creation = now.strftime("%Y-%m-%d-%H-%M-%S")
        
        # a.write(creation+"\n")
        iodadir=(os.path.dirname(os.path.realpath(__file__)).replace("scripts",""))+'users'+os.sep+"ml"+os.sep
        modelfilename=modelname+"-model-"+creation+'.joblib'
        # a.write(modelfilename+"\n")
        outputfilename=modelname+"-output-"+creation+'.csv'
        
        # a.write(outputfilename+"\n")
        #np.savetxt(iodadir+"test.csv",dataFeat,delimiter=',')
        recapfilename=modelname+"-recap-"+creation+'.txt'

        #np.savetxt(iodadir+outputfilename,dataOut,delimiter=',', header=h, fmt=outformat)
        df.to_csv(iodadir+outputfilename, index=False)
        dump(modelObj, iodadir+modelfilename)
        
        # a.write("db call 1\n")
# #        data_to_db(outputfilename, username, username, creation, 'csv', 'data', 'ok', 'ok')
        # a.write("db call 2\n")
# #        data_to_db(modelfilename, username, username, creation, 'joblib', 'model', 'ok', str(ny))               
        # a.write("db done 1\n")
        webdir = iodadir.replace("var/www/html/","")
        result.update({"outputfilename" : webdir+outputfilename})
        result.update({"modelfilename" : webdir+modelfilename})
        result.update({"recapfilename" : webdir+recapfilename})
        result.update({"mlerror" : 0})
        result.update({"model" : modelname})
        

        
        
    except Exception as err:
        result.update({"mlerror" : 1})
        # errfile=open(os.path.dirname(os.path.realpath(__file__)).replace("scripts","")+"errlog.txt", "w")
        
        # errfile.write("error!" + str(traceback.format_exc())+"\n")
        
        # errfile.close()

    result.update(resultx)
    result = str(result).replace("'",'"')
    

    
    return result
    # a.write(result)
    # a.close()
    
def main(data, nthreads):
    """Start machine learning model evaluation and dataset processing job.

    Parameters
    ----------
    data : cgi.FieldStorage
        HTTP POST payload containing input parameters, model config, and feature settings.
    nthreads : int
        Number of concurrent execution threads allowed.
    """
    #read data
    inputdata = json.loads(data['inputdata'].value)
    ny = int(data['ny'].value)
    plot = data["plot_type"].value
#    stats = data["stats_type"].value    

    #load list of advanced analysis to perform if configured
    conf = util.repConfig()
    connection = util.connect_db(conf.data['local_db'])
    query_globals = util.db_query(connection, "statistics", "stat_name, stat_function", "WHERE stat_type='global'")
    stats_config = {}
    for item in query_globals:
        stats_config.update({item['stat_name'] : item['stat_function']})    
        
    #calculate
    result = do_calculation(data, inputdata, plot, stats_config, ny)
    print(result)

if __name__ == "__main__":
    print("Content-Type: application/json")
    print()
    nthreads = 4
    #the cgi library gets vars from html
    data = cgi.FieldStorage()
    #data = "debug"
    main(data, nthreads)