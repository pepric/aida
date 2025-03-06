#!/usr/bin/python
import functions as util
import numpy as np
from get_data import listRemoteFiles
import classes
from astropy.io import fits
from astropy.table import Table
from datetime import datetime
import xml.etree.ElementTree as etree
from os import remove, path, mkdir, sep
import cgi, cgitb 
cgitb.enable(display=0, logdir="cgi-logs")   # for troubleshooting
import traceback
import db_io
import ssl
import socket


class FAKE():
    def __init__(self):
        self.slug = "fake"
        self.method = "ftp"
        self.use_runid = True
        self.metadata = None

    def download_file(self,fname, conf, ftp, tmp_dir, source):
        """ Download files from remote repository to temporary directory

        Parameters
        --------
            fname: string
                file to download
            conf: class
                main AIDA configuration (from functions.repConfig())
            ftp: class
                ftp connection previously opened
            tmp_dir: string
                temporary directory,
            source: string
                lowercase system source

        Returns
        -------
            completed: boolean
                True if the file have been successfully downloaded, False otherwise

        """
        completed = False
        if source=="fake":
            #set complete path for downloading file
            remotedir = util.set_path(conf.wgetd)
            #different folder structures for files
            if conf.usecase == "hktm" or conf.usecase == "report":
                runid = util.extract_runid(fname)
                full_path = remotedir + str(runid)
            elif conf.usecase == "science":
                datestr = fname.split("_")[-4]
                full_path = remotedir + datestr
            filein = sep + full_path + sep + fname
            #change separator for UNIX IWS machine
            filein = filein.replace(sep, "/")
            filepath = tmp_dir+source
            fileout = filepath+sep+fname
            try:
                with open(fileout, "wb") as h:
                    #download file in fileout
                    ftp.retrbinary('RETR %s' % filein, h.write)
                completed = True
            except :
                remove(fileout)
                completed = False

        return completed        
        
    def retrieve_plot_data(self, conf, e, connection, data, source, ts, te, nthreads, prod_id = None):
        result={}
        #remote db configuration
        dbconfig = conf.dbconfig
        #if data must be retrieved from files
        sysclass = classes.sys_inst(source)            
        if conf.sourcedata['source']=="file":
            try:
                remconn = util.connect_db(dbconfig)
                rf = listRemoteFiles(dbconfig, source)
                remotelist = rf.get_remote_files_list(remconn, ts, te)
                remconn.close()
            except:
                e.remotestatus = 1

            #Run specific function to get data for each system
            if not (e.confstatus or e.localstatus or e.remotestatus):
                result = sysclass.get_plot_data(connection, data, nthreads, remotelist, conf, e, repo = self)

        elif conf.sourcedata['source']=="db":
            #connect to data db
            result = sysclass.get_data_from_db(data, dbconfig, e)        

        return result, e
      
    def retrieve_report_data(self, conf, sub, thClass, t0, tf, report_conf, e, dt, i=0):
        conndata = conf.dbconfig[sub]

        conf.wgetdata = conf.wgetdata_dict[sub]
        if conf.wgetdata == "remote":
            conf.wgeta = conf.wgeta_dict[sub]
            conf.wgetu = conf.wgetu_dict[sub]
            conf.wgetp = conf.wgetp_dict[sub]
            conf.wgetd = conf.wgetd_dict[sub]
        else:
            conf.path = conf.path_dict[sub]

            #parameters to analyze
        try:
            thClass.basepars = report_conf.pars[thClass.source][sub]["keys"]
            thClass.addpars = report_conf.pars[thClass.source][sub]["add"]
        except:
            thClass.addpars = []
            thClass.basepars = []
        thClass.exppars=np.unique(thClass.basepars+thClass.addpars) 

        res = {}
        if conf.repsource[sub]=="file":
            #connection to remote db to download the list of files for experiment
            ############################ BENCHMARK ##################
            with open(report_conf.bm_tfile, "a") as f:
                lfts, ltfs_ts = util.get_time()       
                report_conf.bm_last_cadence_t = (lfts, ltfs_ts)                       
                f.write(thClass.name+" --- LIST_REMOTE_FILES START FOR STEP "+str(dt)+" :\t" + str(lfts)+"\n")
            ############################################################
            remotelist = []

            try:
                #get_remote_files_list
                remconn = util.connect_db(conndata)
                rf = listRemoteFiles(conndata, thClass.source)
                remlist = rf.get_remote_files_list(remconn, t0, tf)
                remotelist = [f['filename'] for f in remlist]
                remconn.close()
            except:
                remotelist=[]
                e.remotestatus = 1
                thClass.th_error.append({"type": "Connection error",
                                       "msg" : "Impossible to download file list from remote DB for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                       "sub" : "",
                                       "level" : "serious"})
    
            f2use = thClass.cls.get_files2use(report_conf, sub, thClass.exppars, remotelist)

            ############################ BENCHMARK ##################
            with open(report_conf.bm_tfile, "a") as f:
                lfte, ltfe_ts = util.get_time()                       
                f.write(thClass.name+" --- LIST_REMOTE_FILES END FOR STEP "+str(dt)+" :\t" + str(lfte)+"\n")
                f.write(thClass.name+" --- LIST_REMOTE_FILES FOR STEP "+str(dt)+" DURATION :\t"+str(util.pretty_time(ltfe_ts - ltfs_ts))+"\n")

            #########################################################                        
                        
            #Run specific function to get data for each system
            if not (e.confstatus or e.localstatus or e.remotestatus):
    
                if len(thClass.exppars)>0:
                    ############################ BENCHMARK ##################
                    with open(report_conf.bm_tfile, "a") as f:
                        gdts, gdts_ts = util.get_time()                              
                        f.write(thClass.name+" --- GET DATA START FOR STEP "+str(dt)+"\t" + str(gdts)+"\n")
                    ############################################################

                    params_chunk = thClass.collect_data(i, report_conf, sub, f2use, conf, t0, tf, dt, self)

                    ############################ BENCHMARK ##################
                    with open(report_conf.bm_tfile, "a") as f:
                        gdte, gdte_ts = util.get_time()
                        f.write(thClass.name+" --- GET DATA END FOR STEP "+str(dt)+" :\t" + str(gdte)+"\n")
                        f.write(thClass.name+" --- GET DATA END FOR STEP "+str(dt)+" DURATION :\t"+str(util.pretty_time(gdte_ts - gdts_ts))+"\n")
                    ##########################################################
            else:
                e.remotestatus = 1
                params_chunk = [] 
        else:
            f2use=None                      
            #case data from db
            try:
                #check connection to remote db
                remconn = util.connect_db(conndata)
                remconn.close()
            except:
                e.remotestatus = 1
                thClass.th_error.append({"type": "Connection error",
                                        "msg" : "Impossible to connect to remote DB for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                        "sub" : "",
                                        "level" : "serious"})                      
         
            if not (e.confstatus or e.localstatus or e.remotestatus):                        
                    if len(thClass.exppars)>0:
                         
                    ############################ BENCHMARK ##################
                        with open(report_conf.bm_tfile, "a") as f:
                            gdts, gdts_ts = util.get_time()                              
                            f.write(thClass.name+" --- GET DATA START FOR STEP "+str(dt)+"\t" + str(gdts)+"\n")
                        ############################################################

                        params_chunk = thClass.collect_data(i, report_conf, sub, f2use, conf, t0, tf, dt, self)
                            
                        ############################ BENCHMARK ##################
                        with open(report_conf.bm_tfile, "a") as f:
                            gdte, gdte_ts = util.get_time()
                            f.write(thClass.name+" --- GET DATA END FOR STEP "+str(dt)+" :\t" + str(gdte)+"\n")
                            f.write(thClass.name+" --- GET DATA END FOR STEP "+str(dt)+" DURATION :\t"+str(util.pretty_time(gdte_ts - gdts_ts))+"\n")
                        ##########################################################
            else:
                e.remotestatus = 1                        
                params_chunk = []      
      
        return params_chunk, e
        
        
class USDF():
    def __init__(self):
        self.slug = "efd"
        self.method = "ftp"
        self.use_runid = True
        self.metadata = None
    
    def retrieve_plot_data(self, conf, e, connection, data, source, ts, te, nthreads, prod_id = None):
        result={}
        
        sysclass = classes.sys_inst(source)
        if not (e.confstatus or e.localstatus or e.remotestatus):
            result = sysclass.get_plot_data(connection, data, nthreads, [], conf, e, repo = self)

        return result, e
        
    def retrieve_report_data(self, conf, sub, thClass, t0, tf, report_conf, e, dt, i=0):

        #print(conf, sub, thClass, t0, tf, report_conf, e, dt, i)
    # QUELLO CHE GENERO QUA DEVE ANDARE IN QUESTA FUNZIONE
    # async def get_data_from_efd(self, par, fields, t_start, t_end, client="usdf_efd", prefix ="lsst.sal"):
        # # The EFD Python client for the USDF environment
        # efd_client = EfdClient(efd_name=client)
        # par2get = prefix+"."+par
        # #print(client, par2get,fields)
        # result = await efd_client.select_time_series(par2get,fields=fields,start=t_start,end=t_end)
        # return result

#for l,f in input_dict.items():
#            result = asyncio.run(self.get_data_from_efd(l, f, t_start, t_end))

    
        # conndata = conf.dbconfig[sub]
        # #metadata host
        # meta_host = conf.sourcedata[sub]['files repository']
        # file_host = conndata['host']        

        #parameters to analyze
        try:
            thClass.basepars = report_conf.pars[thClass.source][sub]["keys"]
            thClass.addpars = report_conf.pars[thClass.source][sub]["add"]
        except:
            thClass.addpars = []
            thClass.basepars = []
        thClass.exppars=np.unique(thClass.basepars+thClass.addpars) 

        pardict={}
        for p in thClass.exppars:
            p_arr = p.rsplit(".",1)
            topic = p_arr[0]
            field = p_arr[1]
            
            if topic in pardict.keys():
                fields = pardict[topic]
                fields.append(field)
            else:
                fields = [field]
           
            pardict.update({topic : fields})
        
        #sysclass = classes.sys_inst(thClass.source)
        if len(thClass.exppars)>0:
            #metadata.update({"fullpar" : 0})
            #self.metadata = metadata
            #get data
            params_chunk = thClass.collect_data(i, report_conf, sub, None, conf, t0, tf, dt, self)
        else:
            params_chunk = []           
        #print(params_chunk)

        # d, error = sysclass.get_report_data(pardict, t0, tf)
        # print("DATA"+str(d))
        # if error:
            # thClass.th_error.append({"type": "No data error",
            # "msg" : "No data available for on archive for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
            # "sub" : "EFD",
            # "level" : "warning"})  
        
        #ret={<parameter> : {"dates" : [datetime string in the form 'YYYY-MM-DD HH:mm:ss'], "values" : [values]}
        
        
        
        # rep_error = self._setrepoconf(thClass.source.lower(), conf.opmode, sub)

        # if rep_error :         
            # e.remotestatus = 1
            # #Il tipo di errore non è questo: _setrepoconf legge il nostro system conf. Modificare
            # thClass.th_error.append({"type": "Connection error",
                                    # "msg" : "Impossible to connect to remote archive",
                                    # "sub" : "",
                                    # "level" : "serious"})
            # return [],e                                    
        # res = {}

        # #metadata = {}        
        # metadata = {"data" : {}}
        # # query_datetag = db_io.dbIO(conf.data['local_db']).get_date_tag(thClass.source,sub)  
        # # self.datetag = query_datetag['date_tag']        
        # self._set_datetag(conf, thClass.source, usecase=sub)

        # if sub == "hktm" : 
           
            # # query = self._query_maker(t0, tf, 'DpdHKTMProduct')            
            # # xmlfile, error = eu.getMetadataXml(self.BASE_EAS_URL, query)
            # fitsfield = "Data.HKTMContainer.File.FileName"
            # #fromdatefield = "Data.DateTimeRange.FromDate"
            # fromdatefield = self.dtag_start
            # #todatefield = "Data.DateTimeRange.ToDate"
            # todatefield = self.dtag_stop
            # dsrfield = "Header.DataSetRelease"
            # #tmp_dir = data['user'].value
            # fields = [fitsfield,fromdatefield,todatefield,dsrfield]
           
            # #workaround to solve "\r" issue in results
            # fields.append("Header.ProductType")
            # query = self._query_maker(t0, tf, 'DpdHKTMProduct', fields=fields)
            # # print(query)
            # # exit()            
            # #OLD: products, error = eu.NEW_getMetadataXml(self.BASE_EAS_URL, query)   
            # products, error = eu.NEW_getMetadataXml(self.BASE_EAS_URL, query, username=self.user, password=self.pwd)  

            # if error > 0:
                # if error == 1:
                    # e.remotestatus = 0
                    # errtype = "No data error"
                    # errlvl = "warning"
                    # errmsg = "No data products available for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]"                    
                # elif error == 2:
                    # e.remotestatus = 1
                    # errtype = "Connection error"
                    # errlvl = "serious"                  
                    # errmsg = "Impossible to query remote archive to get metadata for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]"
                # thClass.th_error.append({"type": errtype,
                                     # "msg" : errmsg,
                                      # "sub" : "HKTM",
                                      # "level" : errlvl})
            # else :
                # e.remotestatus = 0
            # params_chunk = []
 
            # if not (e.confstatus or e.localstatus or e.remotestatus):

                # if len(thClass.exppars)>0:             
                    # remotelist = []
                    
                    # #get file list for specific source
                    # filefield = products[fitsfield]
                    # for idx,el in enumerate(filefield):
                        # filearr = el.split(";")
                        # toappend=""
                        # for fname in filearr:
                            # if thClass.source in fname:
                                # toappend = fname
                                # break

                        # #remotelist.append(toappend)
                        # #create metadata["data"]
                        # if toappend != "":
                            # remotelist.append(toappend)
                            # metadata["data"].update({toappend : {"from" : products[fromdatefield][idx], "to" : products[todatefield][idx], "release" : products[dsrfield][idx]}})                    
                        
                    # metadata.update({"fullpar" : 1})

                    # self.metadata = metadata
                    # conf.usecase = "hktm"   

                    # #get data

                    # params_chunk = thClass.collect_data(i, report_conf, sub, remotelist, conf, t0, tf, dt, self)                      
          
        # elif sub == "science" : 
            # if thClass.source == "NISP":
                # #get intr_conf, exp_conf from parameters labels
                # try:
                    # extrafilters = []
                    # for el in thClass.exppars:
                        # curr = el.split(".")
                        # extrafilters.append((curr[0],curr[1]))
                    # extrafilters_unique = list(set(extrafilters))

                    # #get metadata
                    # metadata_mini = []
                    # errflag = []
                    # for el in extrafilters_unique:
                        # meta, error = self._get_metadata(el[0], el[1], t0, tf, thClass.source, e)
                        # errflag.append(error)           #FORSE DA SISTEMARE IL CHECK DELL'ERROR

                        # if error == 0:
                            # metadata_mini.append(meta)
                        # elif error == 1:
                            # metadata_mini.append(meta)
                            # thClass.th_error.append({"type": "No data error",
                                                # "msg" : "No data products available with configuration '"+el[0]+"."+el[1]+"' on archive for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                                # "sub" : "SCIENCE",
                                                # "level" : "warning"})
                            # e.remotestatus = 0                    
                        # elif error == 2:
                            # thClass.th_error.append({"type": "Connection error",
                                                # "msg" : "Impossible to download file list from EAS with configuration '"+el[0]+"."+el[1]+"' for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                                # "sub" : "SCIENCE",
                                                # "level" : "serious"})
   
                    # remotelist = []
                    # for el in metadata_mini:
                        # try:
                            # remotelist += el['hkfitsfile']
                        # except:
                            # thClass.th_error.append({"type": "No data error",
                                                # "msg" : "Some data products have not linked HKFitsFile",
                                                # "sub" : "SCIENCE",
                                                # "level" : "warning"})                           
                        
                    # remotelist = np.unique(remotelist)

                # except:
                    # remotelist=[]
                    # e.remotestatus = 1
                    # thClass.th_error.append({"type": "Connection error",
                                         # "msg" : "Impossible to download file list from EAS for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                          # "sub" : "SCIENCE",
                                          # "level" : "serious"})                   
                
                # #AGGIUNGERE e.remotestatus quando tutti 2
                
                # #FARE UN TEST A CAVALLO DELLE DATE
                # #alla fine rimuovere il print che è in giro
                

                # if not (e.confstatus or e.localstatus or e.remotestatus):              
                    # if len(thClass.exppars)>0:
                        # #build metadata with structure like the one for plots. Add metadata as repo attribute
                        # for imm, efm in enumerate(extrafilters_unique):
                            # el_pos=[idx for idx,t in enumerate(extrafilters) if t==efm]  

                            # for j in el_pos:
                                # if len(metadata_mini) > 0:
                                    # meta2store = metadata_mini[imm]
                                # else:
                                    # meta2store = []
                                # metadata["data"].update({thClass.exppars[j] : meta2store})

                        # connection = util.connect_db(conf.data['local_db'])
                        # listcalib = self._get_science_calibrated_flags(thClass.exppars, connection)
                        # connection.close()
                        # metadata["conversion"]=listcalib
                        # self.metadata = metadata
  
                        # conf.usecase = "science"
                        
                        # #get data
                        # params_chunk = thClass.collect_data(i, report_conf, sub, remotelist, conf, t0, tf, dt, self)
                    # else:
                        # params_chunk = []                      
                # else:
                    # e.remotestatus = 1
                    # params_chunk = []
                                
            # elif thClass.source == "VIS":
                # #fitsfield = "Data.DataStorage.DataContainer.FileName"
                # csvfield = "Data.AnalysisResults.AnalysisFiles.TextFiles.FileName"
                # datefield = "Data.AnalysisID"          
                # #fields = [fitsfield,datefield,csvfield]            
                # fields = [datefield,csvfield]            

                # #workaround to solve "\r" issue in results
                # fields.append("Header.ProductType")

                # #dp_list = []
                # fields_dict = {}
                # remotelist = []
                # conf.usecase = "science"

                # # for el in thClass.exppars:
                    # # dp = el.split(".")[0]
                    # # if dp not in dp_list:
                        # # dp_list.append(dp)            
                # metadp = {}
                # meta, error = self._get_metadata("", "", t0, tf, thClass.source, e, fields)

                # if error == 0:
                    # if not path.isdir(thClass.tempdir+"vis"):
                        # mkdir(thClass.tempdir+"vis")
                    # if len(meta) > 0:
                        # for csvf in meta['results'][csvfield]:
                            # remotelist.append(csvf)

                        # #metadp.update({el : meta})
                    # elif error == 1:
                    
                        # thClass.th_error.append({"type": "No data error",
                                            # "msg" : "No data products available for '"+el+"' on archive for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # "sub" : "SCIENCE",
                                            # "level" : "warning"})                       
                    # elif error == 2:
                        # thClass.th_error.append({"type": "Connection error",
                                            # "msg" : "Impossible to download file list from EAS for '"+el+"' for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # "sub" : "SCIENCE",
                                            # "level" : "serious"})                        

                # datadict = {}
                # tsdb = str(util.format_date(t0))
                # tedb = str(util.format_date(tf))
                # metadata.update({"time" : [tsdb,tedb]})                
                # if len(thClass.exppars)>0:
                    # metadata.update({"fullpar" : 0})
                    # metadata.update({"listpars" : thClass.exppars})

                    # for p in thClass.exppars:
                        # curr_csv = []
                        # #curr_fits = []
                        # curr_dates = []
                        # #curr_dp = p.split(".")[0]
                        # #curr_data = metadp.get(curr_dp)
                        # #if curr_data is not None:
                        # if len(meta['results']) > 0:
                            # curr_csv_list = meta['results'][csvfield]
                            # for icsv,csvf in enumerate(curr_csv_list):
                                # if csvf not in curr_csv:
                                    # curr_csv.append(csvf)
                                    # #curr_fits.append(curr_data['results'][fitsfield][icsv])
                                    # curr_dates.append(meta['results'][datefield][icsv])
                            # #datadict.update({p:{"results":{"csvfiles" : curr_csv, "fitsfiles":curr_fits, "dates" : curr_dates}}})        
                            # datadict.update({p:{"results":{"csvfiles" : curr_csv, "dates" : curr_dates}}})        
                        # else:
                            # #datadict.update({p:{"results":{"csvfiles" : [], "fitsfiles":[], "dates":[]}}})
                            # datadict.update({p:{"results":{"csvfiles" : [], "dates":[]}}})

                    # metadata["data"] = datadict
                    # self.metadata = metadata
                    # #get data
                    # params_chunk = thClass.collect_data(i, report_conf, sub, remotelist, conf, t0, tf, dt, self)
                # else:
                    # params_chunk = []                                             
      
            # elif thClass.source == "QLA":
            
                # remotelist = []
                # #NEW PART#
                # ts_stamp = int(util.format_date(t0))
                # te_stamp = int(util.format_date(tf))

                # qlafilefield = "Data.File.FileName"
                # obtdatefield = "Header.CreationDate"
                # dsrfield = "Header.DataSetRelease"
                # keysfield = "Parameters.Parameter.Key"
                # stringfield = "Parameters.Parameter.StringValue"
                # #intfield = "Parameters.Parameter.IntValue"
                # intfield = self.dtag_start
                # #tmp_dir = data['user'].value
                # #fields = [obtdatefield,qlafilefield,dsrfield,keysfield,stringfield,intfield]
                # fields = [qlafilefield,dsrfield,keysfield,stringfield,intfield]
                # #workaround to solve "\r" issue in results
                # fields.append("Header.ProductType")                  
                # #fields = [qlafilefield,intfield]
                # query = self._query_maker(ts_stamp, te_stamp, thClass.source, fields=fields)
                # # print(query)
                # instr_list = []
                # for el in thClass.exppars:
                    # curr_instr = el.split("-")[0]
                    # if curr_instr not in instr_list:
                        # instr_list.append(curr_instr)
                # # if len(instr_list)==1:
                    # # query+="&Parameters.Parameter.StringValue=like"+instr_list[0]+"*"

                # #OLD: products, error = eu.NEW_getMetadataXml(self.BASE_EAS_URL, query)
                # products, error = eu.NEW_getMetadataXml(self.BASE_EAS_URL, query, username=self.user, password=self.pwd)
                # # with open("qla_results2.txt","w") as xx:
                    # # xx.write(str(products))
                # if error > 0:
                    # if error == 1:
                        # e.remotestatus = 0
                        # errtype = "No data error"
                        # errlvl = "warning"
                        # errmsg = "No data products available for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]"                    
                    # elif error == 2:
                        # e.remotestatus = 1
                        # errtype = "Connection error"
                        # errlvl = "serious"                  
                        # errmsg = "Impossible to query remote archive to get metadata for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]"
                    # thClass.th_error.append({"type": errtype,
                                         # "msg" : errmsg,
                                          # "sub" : "QLA",
                                          # "level" : errlvl})
                # else :
                    # e.remotestatus = 0
                    # keys=products[keysfield]
                    # allints=products[intfield]
                    # allfiles=products[qlafilefield]
                    # alldsr = products[dsrfield]
                    # allstr = products[stringfield]
                    # good_pos=[]
                    # img_type_pos = []
                    # for idx,x in enumerate(keys):
                        # if allfiles[idx].split("-")[0].split("_")[-1] in instr_list: #filter not selected channels                
                            # if x=="OBT_START":
                                # good_pos.append(idx)
                            # if x=="IMG_TYPE":
                                # img_type_pos.append(idx)


                    # img_t_dict={}
                    # for n in img_type_pos:
                        # curr_file = allfiles[n]
                        # curr_imgt = allstr[n]
                        # if curr_file not in img_t_dict.keys():
                            # img_t_dict.update({curr_file : curr_imgt})

                    # datadict = {}
                    # # good_dates=[]
                    # #good_files=[]
                    # # good_dsr = []

                    # for idx in good_pos:
                        # if(int(allints[idx])>=ts_stamp and int(allints[idx])<=te_stamp):
                            # curr_file = allfiles[idx]
                            # curr_imgt = img_t_dict[curr_file]
                            # curr_date = int(allints[idx])
                            # curr_dsr = alldsr[idx]
                            # for l in thClass.exppars:
                                # if l!="None":
                                    # s_and_type = l.split(".")[0]
                                    # curr_source = s_and_type.split("-")[0]
                                    # curr_type = s_and_type.split("-")[1]
                                    
                                    
                                    # if curr_source == "NISP":
                                        # curr_type_arr = curr_type.split("_")
                                        # if len(curr_type_arr) > 1 and curr_type_arr[0] == "DARK":
                                            # curr_type = curr_type_arr[0]                                     
                                    # #print(curr_source,curr_type,curr_file,curr_imgt)
                                    # # if curr_type=="DARK_SPEC":
                                        # # curr_type="DARK"
                                        # # curr_channel = "NISP-S"
                                    # # else:
                                        # # curr_channel = None
                                    # try:
                                        # curr_dict = datadict[l]
                                    # except:
                                        # curr_dict = {}
                                    # if (curr_source in curr_file) and (curr_type==curr_imgt):
                                        # if curr_dict!={}:
                                            # obt_list = curr_dict['obt']
                                            # file_list = curr_dict['fitsfile']
                                            # obt_list.append(datetime.utcfromtimestamp(curr_date).strftime('%Y-%m-%d %H:%M:%S'))
                                            # file_list.append(curr_file)
                                            # datadict[l].update({'obt' : obt_list, 'fitsfile' : file_list})
                                        # else:
                                            # obt_list = [datetime.utcfromtimestamp(curr_date).strftime('%Y-%m-%d %H:%M:%S')]
                                            # file_list = [curr_file]
                                            # datadict.update({l:{'obt' : obt_list, 'fitsfile' : file_list}})
                                        # remotelist.append(curr_file)
                    # remotelist = np.unique(remotelist)
                      
                # params_chunk = []
                # #print(remotelist) 
                # if not (e.confstatus or e.localstatus or e.remotestatus):
                    # if len(thClass.exppars)>0:             
                        # metadata.update({"fullpar" : 0})
                        # metadata.update({"listpars" : thClass.exppars})
                        # metadata.update({"data" : datadict}) 
                        # conf.usecase = "science"   
                        # #get data
                        # params_chunk = thClass.collect_data(i, report_conf, sub, remotelist, conf, t0, tf, dt, self)                    
                # else:
                    # e.remotestatus = 1
                      
                    # #OLD WORKING NO METADATA
                    # # meta_reduced = {}
                    # # #QUI DIVENTA UN FOR NEL CASO VENGA AGGIUNTO NEL DM L'IMAGE TYPE
                    # # meta, error = self._get_metadata("", "", t0, tf, thClass.source, e)

                    # # metadata_mini = []
                    # # errflag = []
                    # # errflag.append(error)

                    # # if error == 2:
                        # # e.remotestatus = 1
                        # # thClass.th_error.append({"type": "Connection error",
                                            # # "msg" : "Impossible to download file list from EAS for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # # "sub" : "SCIENCE",
                                            # # "level" : "serious"})
                    # # else:
                        # # # metadata_mini.append(meta)
                        # # remotelist = []
                        # # e.remotestatus = 0
                        # # for p in thClass.exppars: 
                            # # if error == 0:                
                                # # curr_sub = p.split(".")[0].split("-")[0]
                                # # obt = meta['obt']
                                # # metafiles = meta['fitsfile']
                                # # new_obt = []
                                # # new_files = []
                                # # for idx, fname in enumerate(metafiles):
                                    # # if curr_sub in fname:
                                        # # new_files.append(fname)
                                        # # new_obt.append(obt[idx])
                                        # # remotelist.append(fname)
                                # # meta_reduced.update({p : {'obt' : new_obt, 'fitsfile' : new_files}})
                            # # else:
                                # # meta_reduced.update({p : {'obt' : [], 'fitsfile' : []}})
                        # # remotelist = np.unique(remotelist)


                # # except:
                    # # remotelist=[]
                    # # traceback.print_exc()                    
                    # # e.remotestatus = 1
                    # # thClass.th_error.append({"type": "Connection error",
                                         # # "msg" : "Impossible to download file list from EAS for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                          # # "sub" : "SCIENCE",
                                          # # "level" : "serious"})

                # # if not (e.confstatus or e.localstatus or e.remotestatus):              
                    # # if len(thClass.exppars)>0:              
                        # # #build metadata with structure like the one for plots. Add metadata as repo attribute
                        # #  for el in thClass.exppars:
                        # #      metadata.update({el : metadata_mini})                          
                        # # conf.usecase = "science"
                        # # self.metadata = meta_reduced
                        # # #get data
                        # # params_chunk = thClass.collect_data(i, report_conf, sub, remotelist, conf, t0, tf, dt, self)
                    # # else:
                        # # params_chunk = []                      
                # # else:
                    # # e.remotestatus = 1
                    # # params_chunk = []               

        # elif sub == "calibration":
            # params_chunk = []
            # conf.usecase = "calibration"
            # if thClass.source == "NIR":
                # full_dp_list = []
                # dp_list = []
                # fields_dict = {}
                # metadata_mini = []
                # remotelist = []
                
                # for el in thClass.exppars:
                    # dp = el.split(".")[0]
                    # full_dp_list.append(dp)
                    # #dp_branch = el.replace(dp+".","")
                    # if dp not in dp_list:
                        # dp_list.append(dp)
                        # # fields_dict.update({dp:[dp_branch]})
                    # # else:
                        # # list_fields = fields_dict[dp]
                        # # if dp_branch not in list_fields:
                            # # list_fields.append(dp_branch)
                            # # fields_dict.update({dp:list_fields})
                            
                # for el in dp_list:
                    # meta, error = self._get_metadata(el, "", t0, tf, thClass.source, e)                    
                    # #print(meta,error)                    

                    # if error == 0:
                        # #metadata_mini.append(meta)
                        # #store metadata xml into files
                        # if not path.isdir(thClass.tempdir+"nir"):
                            # mkdir(thClass.tempdir+"nir")
                        # if len(meta) > 0:
                            # for xfile in meta['results']:
                                # root = etree.XML(xfile)
                                # ptype = root.find(".//ProductType").text
                                # pid = root.find(".//ProductId").text
                                # pfile = ptype[0].upper() + ptype[1:] + '__' + pid + ".xml"
                                # with open(thClass.tempdir+"nir/"+pfile,'w') as xf:
                                    # xf.write(xfile)                        
                                # remotelist.append(pfile)
                            
                            # metadata['data'].update({el : remotelist})

                    # elif error == 1:
                    
                        # thClass.th_error.append({"type": "No data error",
                                            # "msg" : "No data products available for '"+el+"' on archive for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # "sub" : "CALIBRATION",
                                            # "level" : "warning"})                       
                    # elif error == 2:
                        # thClass.th_error.append({"type": "Connection error",
                                            # "msg" : "Impossible to download file list from EAS for '"+el+"' for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # "sub" : "CALIBRATION",
                                            # "level" : "serious"})
                    
                    
                    
                # if len(thClass.exppars)>0:
                    # metadata.update({"fullpar" : 0})
                    # self.metadata = metadata
                    # #print(metadata)                    
                    # #build metadata with structure like the one for plots. Add metadata as repo attribute

                    # # for imm, efm in enumerate(dp_list):
                        # # el_pos=[idx for idx,t in enumerate(full_dp_list) if t==efm]  
                        # # for j in el_pos:
                            # # metadata["data"].update({thClass.exppars[j] : metadata_mini[imm]})
  
                    # # self.metadata = metadata
                    # # print(metadata)
                    # # conf.usecase = "science"
                    
                    # #get data
                    # params_chunk = thClass.collect_data(i, report_conf, sub, remotelist, conf, t0, tf, dt, self)
                # else:
                    # params_chunk = []                    

            # elif thClass.source == "SIR":
                # #full_dp_list = []
                # dp_list = []
                # # fields_dict = {}
                # # metadata_mini = []
                # remotelist = []            
                # for el in thClass.exppars:
                    # dp = el.split(".")[0]
                    # #full_dp_list.append(dp)
                    # if dp not in dp_list:
                        # dp_list.append(dp)
                            
                # for el in dp_list:
                    # meta, error = self._get_metadata(el, "", t0, tf, thClass.source, e)
                    # #print(len(meta['results']))     #DATI OK
                    # if error == 0:
                        # #store metadata xml into files
                        # if not path.isdir(thClass.tempdir+"sir"):
                            # mkdir(thClass.tempdir+"sir")
                        # if len(meta) > 0:
                            # for xfile in meta['results']:
                                # root = etree.XML(xfile)
                                # ptype = root.find(".//ProductType").text
                                # pid = root.find(".//ProductId").text
                                # pfile = ptype[0].upper() + ptype[1:] + '__' + pid + ".xml"
                                # with open(thClass.tempdir+"sir/"+pfile,'w') as xf:
                                    # xf.write(xfile)                        
                                # remotelist.append(pfile)
                            
                            # metadata['data'].update({el : remotelist})

                    # elif error == 1:
                        # thClass.th_error.append({"type": "No data error",
                                            # "msg" : "No data products available for '"+el+"' on archive for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # "sub" : "CALIBRATION",
                                            # "level" : "warning"})                       
                    # elif error == 2:
                        # thClass.th_error.append({"type": "Connection error",
                                            # "msg" : "Impossible to download file list from EAS for '"+el+"' for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # "sub" : "CALIBRATION",
                                            # "level" : "serious"})
                                            
                # #CHECK E MODIFICARE DA QUI                            
                # if len(thClass.exppars)>0:
                    # metadata.update({"fullpar" : 0})
                    # self.metadata = metadata
                    # #get data
                    # params_chunk = thClass.collect_data(i, report_conf, sub, remotelist, conf, t0, tf, dt, self)
                # else:
                    # params_chunk = [] 
                # #exit()

            # elif thClass.source == "VIS":
                # fitsfield = "Data.DataStorage.DataContainer.FileName"
                # csvfield = "Data.QualityParameterStorage.DataContainer.FileName"
                # #datefield = "Header.CreationDate"
                # datefield = self.dtag_start            
                
                # fields = [fitsfield,datefield,csvfield]            
            
                # #workaround to solve "\r" issue in results
                # fields.append("Header.ProductType")      
                
                # #full_dp_list = []
                # dp_list = []
                # fields_dict = {}
                # remotelist = []


                # for el in thClass.exppars:
                    # dp = el.split(".")[0]
                    # # full_dp_list.append(dp)
                    # if dp not in dp_list:
                        # dp_list.append(dp)            

                # metadp = {}

                # for el in dp_list:
                    # meta, error = self._get_metadata(el, "", t0, tf, thClass.source, e,fields)

                    # #print(meta,error)
                    # if error == 0:
                        # if not path.isdir(thClass.tempdir+"vis"):
                            # mkdir(thClass.tempdir+"vis")
                        # if len(meta) > 0:
                            # for csvf in meta['results'][csvfield]:
                                # remotelist.append(csvf)

                            # metadp.update({el : meta})                            


                    # elif error == 1:
                    
                        # thClass.th_error.append({"type": "No data error",
                                            # "msg" : "No data products available for '"+el+"' on archive for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # "sub" : "CALIBRATION",
                                            # "level" : "warning"})                       
                    # elif error == 2:
                        # thClass.th_error.append({"type": "Connection error",
                                            # "msg" : "Impossible to download file list from EAS for '"+el+"' for dates in ["+t0.replace(" ","T")+", "+tf.replace(" ","T")+"]",
                                            # "sub" : "CALIBRATION",
                                            # "level" : "serious"})
                # datadict = {}
                # #print(report_conf.tstart,report_conf.tstop)
                # full_ts = str(util.format_date(report_conf.tstart))
                # full_te = str(util.format_date(report_conf.tstop))
                # # print(t0,tf,tsdb,tedb)
               
                # metadata.update({"time" : [full_ts,full_te]})                  
                # if len(thClass.exppars)>0:
                    # metadata.update({"fullpar" : 0})
                    # metadata.update({"listpars" : thClass.exppars})

                    # for p in thClass.exppars:
                        # curr_csv = []
                        # curr_fits = []
                        # curr_dates = []
                        # curr_dp = p.split(".")[0]
                        # curr_data = metadp.get(curr_dp)

                        # if curr_data is not None:
                            # if len(curr_data) > 0:
                                # curr_csv_list = curr_data['results'][csvfield]
                                # for icsv,csvf in enumerate(curr_csv_list):
                                    # if csvf not in curr_csv:
                                        # curr_csv.append(csvf)
                                        # curr_fits.append(curr_data['results'][fitsfield][icsv])
                                        # curr_dates.append(curr_data['results'][datefield][icsv])
                                # datadict.update({p:{"results":{"csvfiles" : curr_csv, "fitsfiles":curr_fits, "dates" : curr_dates}}})        
                        # else:
                            # datadict.update({p:{"results":{"csvfiles" : [], "fitsfiles":[], "dates":[]}}})
                    # metadata["data"] = datadict


                    # self.metadata = metadata
                    # #get data
                    # params_chunk = thClass.collect_data(i, report_conf, sub, remotelist, conf, t0, tf, dt, self)
                # else:
                    # params_chunk = []                                             

        return params_chunk, e
        
        
    
        
        
        
                        