#!/usr/bin/python

import json
import numpy as np
import  argparse
import sys
from    os          import path, sep, mkdir, remove, getpid
from datetime import datetime
import  threading
import functions as util
from reportutils import get_keys, update_progress, analysis, send_report_mail, dbThread, get_add, get_operation_branches
from get_data import listRemoteFiles
import pymysql
import pymysql.cursors
import classes
from shutil import copyfile, rmtree
import multiprocessing
from time import sleep
import benchmark as bm
from report_io import create_xml_report, create_pdf_report, xml_error_pdf
try:
    from DBUtils.PooledDB import PooledDB
except:
    from dbutils.pooled_db import PooledDB
import db_io
import h5py
import repos
import traceback

class reportConfig():
    """Class to get configuration data for current report"""
    
    def __init__(self, configfile, period, conndata, user = "auto", tresume = None, runid = 0):
        """ reportConfig init.
        Parameters
        ----------
        configfile : str,
            name of report configuration file
        period : "ondemand", "daily", "weekly", "monthly" or "custom"
            report periodicity
        user : str,
            name of the user who launched report generation
        """
        
        ############### FOR BENCHMARK ###############
        #BENCHMARK CONFIGURATION LINES FOR FILENAME
        try:
            with open("current_dir.txt", "r") as f:
                self.bm_dir = f.read()
        except:
            bm_config = bm.read_config()
            self.start_exp = util.utc_now().strftime("%Y%m%d_%H%M%S")
            descr = ""
            for item in bm_config['description']:
                descr+=item+"-"
            descr = descr[:-1]
            #create benchmark directory
            self.bm_dir = "profiling/"+self.start_exp+"_"+descr+"_"+str(bm_config['n'])+"_"+period

        if not path.isdir(self.bm_dir):
            mkdir(self.bm_dir)
        #file name for time record
        self.bm_tfile = "logs/timing_"+str(runid)+".log"
        #start time for last cadence step
        self.bm_last_cadence_t = None        
        ##############################################################
        
        general_error = 0
        config_read_error = 0
        systems_error = 0

        #set AIDA main directory
        self.root = path.dirname(path.abspath(__file__)).replace("scripts","").replace("\\",sep).replace("/",sep)
        configroot = self.root + "users"+sep+"config"+sep

        self.configfile = configfile
        # set config file with complete path
        self.cfile = configroot + configfile

        #import data from config
        self.repdata, config_read_error = self.get_report_config()
        
        #get general info
        general_error = self.get_general_info(period)

        if general_error == 0 and config_read_error == 0:
            self.period = period
            self.user = user

            #set useful dates
            #tstart as timestamp            
            if tresume is not None:
                self.tstart = str(datetime.utcfromtimestamp(tresume))

            self.ts_stamp = util.format_date(self.tstart)
            deltat = self.t_window*3600.0
            #tstop
            self.tstop_stamp = self.ts_stamp+deltat
            self.tstop = str(datetime.utcfromtimestamp(self.tstop_stamp))
            #create array with all (tstart, tstop) for usecase with number of acquisitions > 1
            if self.period == "ondemand":
                self.tsarr = []
                self.tearr = []
                for n in range(self.nacq):
                    t0_stamp = self.ts_stamp + n*self.tacq*3600
                    tf_stamp = t0_stamp + deltat
                    t0 = str(datetime.utcfromtimestamp(t0_stamp))
                    tf = str(datetime.utcfromtimestamp(tf_stamp))
                    self.tsarr.append(t0)
                    self.tearr.append(tf)
            else:
                self.tsarr = [self.tstart]
                self.tearr = [self.tstop]

            #define data download cadence (hours)
            cadence_map = {"ondemand" : 0, "daily" : 2, "weekly" : 12, "monthly" : 24, "custom" : 0}
            #set cadence for ondemand report and periodic with custom period
            if self.t_window >= 12 and self.t_window < 24:
                cadence_map["ondemand"] = 4
                cadence_map["custom"] = 4
            elif self.t_window >= 24 and self.t_window < 168:
                cadence_map["ondemand"] = 12
                cadence_map["custom"] = 12
            elif self.t_window >= 168:
                cadence_map["ondemand"] = 24
                cadence_map["custom"] = 24
            self.cadence = cadence_map[self.period]

            #get list of systems to analyze
            try:
                allowed_systems = db_io.dbIO(conndata).get_systems()
                self.systems, systems_error = get_keys(self.repdata, allowed_systems, ["General Info"])
                
                #get list of parameters to analyze            
                if systems_error == 0:
                    self.pars = {}
                    self.sysclasses = []
                    for s in self.systems:
                        sys_class = classes.sys_inst(s)
                         
                        self.sysclasses.append(sys_class)
                        sys_params = sys_class.get_report_params(self.repdata)
                        self.pars.update({s : sys_params})
            except Exception as e:

                systems_error = 1              

        #check errors
        self.error = config_read_error or systems_error or general_error

    def get_add(self,s,keys):
        """Pull all values of specified key from nested JSON."""
        obj = self.repdata[s]
        arr = []
        try:
            def extract(obj, arr, keys):
                """Recursively search for values of key in JSON tree."""
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if k in keys:
                            arr.append(v)
                        if isinstance(v, (dict, list)):
                            extract(v, arr, keys)
                elif isinstance(obj, list):
                    for item in obj:
                        extract(item, arr, keys)
                return arr

            y = extract(obj, arr, keys)
        except:
            y = []
        results = []
        if y!=[]:
            for n in y:
                if isinstance(n, list):
                    for el in n:
                        results.append(el)
                else:
                    results.append(n)
        return results

    def get_general_info(self, period):
        """Get general info from JSON data
        Parameters
        ----------
        period : "ondemand", "daily", "weekly", "monthly" or "custom"
            report periodicity
        """
        general_error = 0
        try:
            #Get start time
            tstart = self.repdata["General Info"]["Start Time"]
            self.tstart = tstart.replace("T", " ")
            #Get window
            self.t_window = self.repdata["General Info"]["Time Window"]
            #Get sampling type
            self.sampling = self.repdata["General Info"]["Sampling"]
            #Get sampling period
            if self.sampling != "full":
                self.ts = self.repdata["General Info"]["Sampling period"]
            else:
                self.ts = 0
            if self.sampling == "by function":
                self.sfunc = self.repdata["General Info"]["Sampling function"]
            else:
                self.sfunc = None
            #Get number of acquisitions and acquisition time step
            if period == "ondemand":
                #Get number of acquisitions
                self.nacq = self.repdata["General Info"]["Number of acquisitions"]
                #Get acquisition time step
                if self.nacq > 1:
                    self.tacq = self.repdata["General Info"]["Acquisition time step"]
                else:
                    self.tacq = 0
            else:
                self.nacq = 1
                self.tacq = 0
        except:
            general_error = 1
        #get parameter to set if to save time (create plots in memory) or memory (create plots in files). Default is save memory
        self.plotfromfile = True        
        try:
            priority = self.repdata["General Info"]["Resource priority"]
            if priority == "time":
                self.plotfromfile = False
        except:
            pass
            
        return general_error

    def get_report_config(self):
        """ Read report data from JSON configuration file."""
        error = 0
        repdata = {}
        try:
            # get report config data from json
            fileobj = open(self.cfile, "r")
            jsonstr = fileobj.read()
            fileobj.close()
            #change slashes
            jsonstr = jsonstr.replace("\\","/")
            #convert input string to json object
            repdata = json.loads(jsonstr)
        except:
            error = 1
        return repdata, error

    def set_workdir(self, runid):
        """Set working directory for current experiment
        Parameters
        ---------
        runid : int or str,
            id of the current experiment
        """
        dirname = self.root+"users/report/temp_id"+str(runid)+sep
        self.workdir = dirname.replace("\\",sep).replace("/",sep)
        if not path.isdir(self.workdir):
            mkdir(self.workdir)

        return self.workdir

class reportData():

    def __init__(self, iodaconf, f2use, sysclass, tempdir, nthreads, ts, te, params, repo, sub=None):
        self.tempdir = tempdir
        self.source = sysclass.source
        self.f2use = f2use
        self.iodaconf = iodaconf
        self.nthreads = nthreads
        self.tstart = util.format_date(ts)
        self.tstop = util.format_date(te)
        self.params = params
        self.cls = sysclass
        self.download_error = False
        self.readfile_error = False
        self.query_error = False        
        self.sub = sub
        self.repo = repo

    def get_files(self):
        #get data from local (by copying files in temp directory) or remote repository (by downloading files)
        #create tmp report directory        
        filepath = self.tempdir+self.cls.name
        if not path.isdir(filepath):
            mkdir(filepath) 
            
        #split array of file names to use into threads
        filesarray = np.array_split(np.array(self.f2use), self.nthreads)
        jobs = []
        for chunk in filesarray:
            #check which files have been already downloaded for the current experiment
            todownload = []
            for f in chunk:
                if not path.isfile(self.tempdir+self.source.lower()+sep+f):
                    todownload.append(f)

            if self.iodaconf.wgetdata == "local":
                #copy files in report temporary directory
                localpath = self.iodaconf.path
                j = multiprocessing.Process(target=util.copylocal, args=(todownload, self.iodaconf, self.tempdir, self.cls,self.repo.use_runid,))                
            else:
                #download files in report temporary directory
                j = multiprocessing.Process(target=self.multidownload, args=(todownload, ))
            jobs.append(j)
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

        return filesarray                       

    def read_data(self, filesarray=[]):
        result_dict = {}  
        if self.f2use is not None:                
            #open files and get data
            with multiprocessing.Pool(self.nthreads) as p:
                multi_data = p.map(self.get_data_from_file, filesarray) #list of dictionaries from multiprocess contaning extracted data (len(multi_data)=number of files)
            
            for p in self.params:
                for elem in multi_data:
                    data = elem[0]
                    data_k = list(data.keys())
                    dataok = True
                    if p in data_k:
                        p2find = p
                    else:
                        p2find = p.replace("['","[\"").replace("']","\"]")
                        if p2find not in data_k:
                            p2find = p.replace("[\"","['").replace("\"]","']")
                            if p2find not in data_k:
                                dataok = False

                    if dataok:
                        curr_date = data[p2find]['dates']
                        curr_val = data[p2find]['values']
                    else:
                        curr_date = []
                        curr_val = []                        
                    try:
                        stored_d = result_dict[p2find]['dates']
                        stored_v = result_dict[p2find]['values']
                        new_d = stored_d+curr_date
                        new_v = stored_v+curr_val
                        result_dict.update({p:{"dates":new_d, "values":new_v}})
                    except:
                        result_dict.update({p:{"dates":curr_date, "values":curr_val}})

            for elem in multi_data:
                curr_de = elem[1]
                curr_fe = elem[2]
                if curr_de == 1:
                    self.download_error = True
                if curr_fe == 1:
                    self.readfile_error = True
        else:
            #get data from DB
            #split params to use in multiprocess
            parray = np.array_split(np.array(self.params), self.nthreads)
            
            #get data
            with multiprocessing.Pool(self.nthreads) as p:
                multi_data = p.map(self.get_data_from_db, parray)

            for tup in multi_data:
                #store data in result_dict
                result_dict.update(tup[0])              
                #check if at least one query has given an error
                if tup[1] == 1:
                    self.query_error = True

        return result_dict


    def get_data_from_db(self, parray):
        ret = {}
        errorquery = 0 
        try:
            ret = self.cls.report_data_from_db(parray, self.sub, self.iodaconf, self.tstart, self.tstop, ret)
        except:
            #error querying data
            errorquery = 1

        return ret, errorquery
      
    def get_data_from_file(self, f2use):

        #OPEN FILE AND GET DATA
        ret = {}
        dirname = self.tempdir+sep
        source = self.cls
        sysname = self.cls.name+sep
        #for each file in the input array
        errordownstatus = 0
        errorfilestatus = 0
        for f in f2use:
            #check if file is present in the temporary directory
            file_ok = path.isfile(dirname+sysname+f)
            if file_ok:
                #Open file and get data, then update output dictionary
                try:
                    ret = self.cls.read_data_from_file(f, dirname, self.params, self.iodaconf, self.tstart, self.tstop, repo=self.repo, result=ret)     #AGGIUNGERE ADU LIST (VEDI GET_DATA) PER UTILIZZARE ADU/CALIB
                except Exception as e:
                    #error opening file
                    errorfilestatus = 1
            else:
                #error downloading/copy file
                errordownstatus = 1

        return ret, errordownstatus, errorfilestatus

    def multidownload(self, f2use):
        ftp=""
        self.res = {}
        errorfilestatus = 0
        errordownstatus = 1 

        if self.repo.method == "ftp":
            #get files from remote DB
            try:
                ftp = util.open_ftp_connection(self.source, self.iodaconf)
                for name in f2use:
                    self.cls.download_file(name, self.iodaconf, ftp, self.tempdir, self.repo)
            finally:
                if ftp != "" and ftp != "unable":
                    ftp.close()
        elif self.repo.method == "uri":
            for name in f2use:
                self.repo.download_file(name, self.iodaconf, None, self.tempdir, self.cls.name)

class threadSys(threading.Thread):
    def __init__(self, ThreadID, name, params, nthreads, runid, start_time = None):
        threading.Thread.__init__(self)
        self.name=name
        self.id=ThreadID
        self.source = name.split("_")[1]
        self.params = params
        self.tempdir = params.workdir
        self.nth = nthreads
        self.indata = {}
        self.exppars = []
        self.hktm_res = {}
        self.science_res = {}
        self.cls = params.sysclasses[ThreadID]
        self.runid = runid
        self.th_error = []
        self.start_time = start_time
        self.nsys = len(params.systems)
        self.nacq = len(params.tsarr)
        self.par_pos = {}        

    def run(self):

        threadLimiter.acquire()
        self.res = {}
      
        # GET DATA FOR EACH SYSTEM
        #get repository configuration from file
        conf = util.repConfig(self.source, "report")

        #report configuration
        report_conf = self.params
        if self.start_time is not None:
            report_conf.tstart = self.start_time
            report_conf.ts_stamp = util.format_date(report_conf.tstart)
            report_conf.tstop_stamp = report_conf.ts_stamp+report_conf.t_window*3600.0
            report_conf.tstop = str(datetime.utcfromtimestamp(report_conf.tstop_stamp))            

        connmsg={}
        #if no errors in configuration
        if conf.error == 0:
            lmain = len(conf.main)
            curr_main = util.set_path(conf.root[-lmain:-1])

            if curr_main != conf.main:
                e.mainstatus = 1

            #check connection to local db
            try:
                connection = util.connect_db(conf.data['local_db'])
                locerr = 0
                connection.close()
            except:
                locerr = 1
                e.localstatus = 1

            if locerr == 0:
                if report_conf.period == "ondemand":
                    #ondemand report
                    self.ondemand_pipe(report_conf, conf, e)                        
                else:
                    #periodic report
                    self.periodic_pipe(report_conf, conf, e)              
            else:
                self.th_error.append({"type": "Connection error", "msg" : "Impossible to connect to local DB", "sub" : "", "level" : "serious"})
                self.hktm_res.update({})
        else:
            self.th_error.append({"type": "Configuration error", "msg" : "Impossible to read system configuration file", "sub" : "", "level" : "serious"})
            self.hktm_res.update({})

        threadLimiter.release()

    def ondemand_pipe(self, report_conf, conf, e):

        s = self.cls
        nthreads = self.nth

        connconfig = conf.data['local_db']
        dbio = db_io.dbIO(connconfig)        
        ############################ BENCHMARK ##################        
        retrievets, retrievets_ts = util.get_time() 
        #########################################################  
      
        #array with tstart and tstop for each acquisition
        tsarr = report_conf.tsarr
        tearr = report_conf.tearr
        cadence = report_conf.cadence

        #acquisitions
        for i, (ts,te) in enumerate(zip(tsarr,tearr)):
            self.par_pos = {}
            t_stamp = util.format_date(ts)
            tstop_stamp = util.format_date(te)
            times_arr = [t_stamp]
            if cadence != 0:
                #create time array
                while t_stamp+cadence*3600<tstop_stamp:
                    t_stamp += cadence*3600
                    times_arr.append(t_stamp)
            if times_arr[-1] != tstop_stamp:
                times_arr.append(tstop_stamp)
            
            nsteps = len(times_arr)-1
            if len(times_arr) > 1:
                nsteps = len(times_arr)-1
            else:                
                nsteps = 1              
            update_perc = 81.0/(self.nsys*self.nacq*nsteps)
            #cadence
            for dt in range(1, len(times_arr)):
                if dt>1:
                    t0 = str(datetime.utcfromtimestamp(times_arr[dt-1]+1))
                else:
                    t0 = str(datetime.utcfromtimestamp(times_arr[0]))
                tf = str(datetime.utcfromtimestamp(times_arr[dt]))
                for sub in report_conf.pars[self.source].keys():
                    repoClass = conf.repclass[sub]

                    params_chunk, e = repoClass.retrieve_report_data(conf, sub, self, t0, tf, report_conf, e, dt, i)                  
                    #return params_chunk list
                    if len(params_chunk) > 0:
                        self.par_pos.update({sub : params_chunk})                               
                #update progress
                dbio.update_progress(self.runid, update_perc)                
                
        ############################ BENCHMARK ##################        
        retrievete, retrievete_ts = util.get_time()
        with open(report_conf.bm_tfile, "a") as f:
            f.write(self.name+" --- FULL DATA RETRIEVE DURATION :\t"+str(util.pretty_time(retrievete_ts - retrievets_ts))+"\n")
        print(self.name+" --- FULL DATA RETRIEVE DURATION : ", util.pretty_time(retrievete_ts - retrievets_ts))
        ##########################################################        
    
        #update progress
        dbio.update_progress(self.runid, 6.0/self.nsys)             

    def periodic_pipe(self, report_conf, conf, e):      
        s = self.cls
        nthreads = self.nth
        
        connconfig = conf.data['local_db']
        dbio = db_io.dbIO(connconfig)
        
        cadence = report_conf.cadence*3600
        offset = conf.offset*3600
        t0 = report_conf.tstart
        t0_stamp = report_conf.ts_stamp
        tf_stamp = report_conf.ts_stamp + cadence
        tf = str(datetime.utcfromtimestamp(tf_stamp))
        tstop = report_conf.tstop
        tstop_stamp = report_conf.tstop_stamp

        if tf_stamp > tstop_stamp or cadence == 0:
            tf_stamp = tstop_stamp
            tf = tstop            

        completed = False
        dt = 1
        if cadence > 0:        
            steps = int((tstop_stamp - t0_stamp)/cadence)
            if steps == 0:
                steps = 1
        else:
            steps = 1

        update_perc = 80/(self.nsys*steps)        
        while not completed:
            print("T0",t0)
            print("TF",tf)
            print("TSTOP",tstop)
            for sub in report_conf.pars[self.source].keys():
                repoClass = conf.repclass[sub]
                params_chunk, e = repoClass.retrieve_report_data(conf, sub, self, t0, tf, report_conf, e, dt, 0)    
                #return params_chunk list
                if len(params_chunk) > 0:
                    self.par_pos.update({sub : params_chunk})               
    
            if tf_stamp == tstop_stamp:
                completed = True
                #update progress
                dbio.update_progress(self.runid, update_perc)  
            else:
                t0_stamp = tf_stamp+1
                t0 = str(datetime.utcfromtimestamp(t0_stamp))

                #update progress
                dbio.update_progress(self.runid, update_perc)                 

                wait_time = tf_stamp + offset - util.utc_now().timestamp()
                print("WAIT : ", util.pretty_time(wait_time))                
                if wait_time > 0:
                    sleep(wait_time)
                tf_stamp += cadence
                if tf_stamp > tstop_stamp:
                    tf_stamp = tstop_stamp
                    tf = tstop                  
                tf = str(datetime.utcfromtimestamp(tf_stamp))                
                dt += 1                    
            
        #update progress
        dbio.update_progress(self.runid, 6.0/self.nsys)             

    def get_hktm_result(self):
        return self.hktm_res

    def get_science_result(self):
        return self.science_res

    def get_errors(self):
        return self.th_error

    def get_parameters_pos(self):
        return self.par_pos      
        
    def collect_data(self, acquid, report_conf, s, f2use, ioda_conf, ts, te, runstep, repo):        #EX GET_RESULTS
        #number of threads for ftp connections
        ftp_th = ioda_conf.nth_dict[s]
        #number of threads for AIDA machine
        nthreads = self.nth
        indata = {}

        if f2use is not None:
            #get data from files
            if len(f2use)>0:
                #change number of ftp connections if files are few
                if ftp_th > len(f2use):     
                    nprocfile = len(f2use)
                else:
                    nprocfile = ftp_th

                #Multiprocess to download files
                repdata = reportData(ioda_conf, f2use, self.cls, self.tempdir, nprocfile, ts, te, self.exppars, repo)
                
                ############################ BENCHMARK ##################        
                with open(report_conf.bm_tfile, "a") as f:
                    downt0, downt0_ts = util.get_time()    
                    f.write(self.name+" --- DOWNLOAD/COPY FILES START FOR STEP "+str(runstep)+" :\t" + str(downt0)+"\n")
                ##########################################################                  
                farray = repdata.get_files()

                ############################ BENCHMARK ##################
                with open(report_conf.bm_tfile, "a") as f:
                    downte, downte_ts = util.get_time()                       
                    f.write(self.name+" --- DOWNLOAD/COPY FILES END FOR STEP "+str(runstep)+" :\t" + str(downte)+"\n")
                    f.write(self.name+" --- DOWNLOAD/COPY FILES FOR STEP "+str(runstep)+" DURATION :\t"+str(util.pretty_time(downte_ts - downt0_ts))+"\n")
                #########################################################
                indata = repdata.read_data(farray)
                err_down = repdata.download_error
                file_err = repdata.readfile_error

                if err_down:
                    self.th_error.append({"type": "Download error",
                                          "msg" : "Impossible to download one or more files from data DB. Analysis could be incomplete.",
                                          "sub" : "",
                                          "level" : "warning"})
                if file_err:
                    self.th_error.append({"type": "File read error",
                                          "msg" : "Impossible to read one or more data files. Analysis could be incomplete.",
                                          "sub" : "",
                                          "level" : "warning"})
        else:
            #get data from db
            #change number of ftp connections if files are few
            if ftp_th > len(self.exppars):      
                nprocfile = len(self.exppars)
            else:
                nprocfile = ftp_th 

            repdata = reportData(ioda_conf, None, self.cls, self.tempdir, nprocfile, ts, te, self.exppars, repo, s)
            indata = repdata.read_data()

            query_err = repdata.query_error
            if query_err:
                self.th_error.append({"type": "Data read error",
                                     "msg" : "Impossible to read data from remote DB. Analysis could be incomplete.",
                                     "sub" : "",
                                     "level" : "warning"})             

        if nthreads > len(self.basepars):
            nproc = len(self.basepars)
        else:
            nproc = nthreads

        basepar_chunk = np.array_split(np.array(self.basepars), nproc)
        jobs=[]
        sysclass = classes.sys_inst(self.source)        

        for i in range(nproc):
            data_dict = {}
            if len(indata) > 0:              
                for k in basepar_chunk[i]:
                    data_dict.update({k: indata[k]})
                    #get additional parameters for params in chunk
                    #if s == "science": parstruct[s] = parstruct["hktm"]  
                    opbranch = get_operation_branches(k, report_conf.repdata, self.source, s.upper(), sysclass.hasorig)

                    add = np.unique(get_add(opbranch, ["Additional Parameters", "X"]))
                    for a in add:
                        #get data and put it in data_dict
                        if a not in basepar_chunk[i]:
                            data_dict.update({a : indata[a]})
            else:
                for k in basepar_chunk[i]:
                    data_dict.update({k: {'dates': [], 'values':[]}})
                    opbranch = get_operation_branches(k, report_conf.repdata, self.source, s.upper(), sysclass.hasorig)
                    add = np.unique(get_add(opbranch, ["Additional Parameters", "X"]))
                for a in add:
                    #get data and put it in data_dict
                    if a not in basepar_chunk[i]:
                        data_dict.update({a : {'dates': [], 'values':[]}})                 
            j = multiprocessing.Process(target=data_to_hdf5, args=(data_dict, self.source.lower(), s.lower(), acquid, i, basepar_chunk[i], self.addpars, self.tempdir, ))  
            jobs.append(j)
            j.start()
        for j in jobs:
            j.join()  
  
        return basepar_chunk    

def data_to_hdf5(data, source, sub, acquid, procid, params, addpars, tempdir):
    addpars = np.unique(addpars)  
    h5file_main = tempdir+source+"_"+sub+"_"+str(procid)+".h5"
    hf = h5py.File(h5file_main,"a")

    for p in params:    
        if len(data[p]['dates']) > 0 and isinstance(data[p]['dates'][0], str):
            d = [util.format_date(x.replace("T"," ")) for x in data[p]['dates']]
        else:
            d = data[p]['dates']
        #create hdf5 items
        #param group
        if p not in hf.keys():
            g = hf.create_group(p)
        else:
            g = hf[p]
        if "acquisition_"+str(acquid) not in g.keys():
            #acquisition group
            acq = g.create_group("acquisition_"+str(acquid))
            #add values to items
            acq.create_dataset("dates", data=d, maxshape = (None,), chunks = True)
            #acq.create_dataset("vals", data=data[p]['values'], maxshape = (None,), chunks = True)    
            acq.create_dataset("vals", data=[float(i) for i in data[p]['values']], maxshape = (None,), chunks = True)    
        else:
            if len(d) > 0:
                acq = g["acquisition_"+str(acquid)]
                dates = acq['dates']
                vals = acq['vals']
                #change lists length
                dates.resize(dates.shape[0]+len(d), axis=0)
                vals.resize(vals.shape[0]+len(data[p]['values']), axis=0)
                #add new values
                dates[-len(d):] = d
                vals[-len(data[p]['values']):] = [float(i) for i in data[p]['values']]    
    
    hf.close()
      
    h5file_add = tempdir+source+"_"+sub+"_"+str(procid)+"_add.h5"
    hf = h5py.File(h5file_add,"a")    
    for p in addpars:
        if p in data.keys():
            if len(data[p]['dates']) > 0 and isinstance(data[p]['dates'][0], str):
                d = [util.format_date(x.replace("T"," ")) for x in data[p]['dates']]
            else:
                d = data[p]['dates']

            #create hdf5 items
            #param group
            if p not in hf.keys():
                g = hf.create_group(p)
            else:
                g = hf[p]
            
            if "acquisition_"+str(acquid) not in g.keys():
                #acquisition group
                acq = g.create_group("acquisition_"+str(acquid))
                 #add values to items
                acq.create_dataset("dates", data=d, maxshape = (None,), chunks = True)
                acq.create_dataset("vals", data=data[p]['values'], maxshape = (None,), chunks = True)    
            else:
                if len(d) > 0:
                    acq = g["acquisition_"+str(acquid)]
                    dates = acq['dates']
                    vals = acq['vals']
                    dates.resize(dates.shape[0]+len(d), axis=0)
                    vals.resize(vals.shape[0]+len(data[p]['values']), axis=0)
                    #add new values
                    dates[-len(d):] = d
                    vals[-len(data[p]['values']):] = data[p]['values']    
    hf.close()      

def ondemand_report(confreport, connconfig, nthreads, runid, url, dirname, pid, email):

    #Init threadLimiter
    global threadLimiter
    threadLimiter=threading.BoundedSemaphore(nthreads)
    dbio = db_io.dbIO(connconfig)
    #Update running reports
    dbio.update_running_reports(pid, runid, tstart = confreport.tstart)     
    dbio.update_config_files(configfile, 1)    
    #Thread for each system
    threads =[]
    for i in range(len(confreport.systems)):
        source = confreport.systems[i]      #source (NIST, VIS, QLA...)
        thread_id = i
        session = threadSys(thread_id, "Thread_"+source, confreport, nthreads, runid)
        threads = threads+[session]
        threads[thread_id].start()

    errors = {}
    par_pos = {}    
    for th in threads:
        th.join()
        #get analysis results
        hres = th.get_hktm_result()
        err = th.get_errors()
        pp = th.get_parameters_pos()        
        errors.update({th.source:err})
        par_pos.update({th.source:pp})

    ############################ BENCHMARK ##################        
    with open(confreport.bm_tfile, "a") as f:
        xmlts, xmlts_ts = util.get_time()
        f.write("XML CREATION START :\t" + str(xmlts) +"\n")        
    ##########################################################          
        
    #OUTPUT CREATION
    xml_ok, creationdate, fname = create_xml_report(confreport, runid, connconfig, nthreads, errors, par_pos)    
    #update progress
    dbio.update_progress(runid, 6.0)    
    ############################ BENCHMARK ##################        
    with open(confreport.bm_tfile, "a") as f:
        xmlte, xmlte_ts = util.get_time()
        f.write("XML CREATION END   :\t" + str(xmlte) +"\n")
        f.write("XML CREATION DURATION :\t"+str(util.pretty_time(xmlte_ts - xmlts_ts))+"\n")
    print("XML CREATION DURATION : ", util.pretty_time(xmlte_ts - xmlts_ts))            
    ##########################################################    
   
    if xml_ok:
    #Create PDF report
        ############################ BENCHMARK ##################        
        with open(confreport.bm_tfile, "a") as f:
            pdfts, pdfts_ts = util.get_time()
            f.write("PDF CREATION START :\t" + str(pdfts) +"\n")        
        ##########################################################     

        try:
            pdf_ok = create_pdf_report(fname, confreport.plotfromfile)
        except Exception as e:
            xml_error_pdf(confreport, fname)
            pdf_ok = False
            print(traceback.format_exc())
                
        ############################ BENCHMARK ##################        
        with open(confreport.bm_tfile, "a") as f:
            pdfte, pdfte_ts = util.get_time()
            f.write("PDF CREATION END   :\t" + str(pdfte) +"\n")
            f.write("PDF CREATION DURATION :\t"+str(util.pretty_time(pdfte_ts - pdfts_ts))+"\n")
        print("PDF CREATION DURATION : ", util.pretty_time(pdfte_ts - pdfts_ts))            
        ##########################################################                  
        
        ############################ BENCHMARK ##################        
        with open(confreport.bm_tfile, "a") as f:
            finalts, finalts_ts = util.get_time()
            f.write("CLOSING (db updates, temp removal, mail sending) START :\t" + str(finalts) +"\n")        
        ##########################################################              
        
        #Update reports table in AIDA DB
        dbio.insert_report_file(fname, user, creationdate, period, configfile, confreport.tstart, confreport.tearr[-1]) 

        maildata = [fname, user, creationdate, period, confreport.tstart, confreport.tearr[-1], runid, url, pdf_ok]
        errortype = ""        
    else:
        finalts, finalts_ts = util.get_time()      
        #config for FAILURE mail to user/admin      
        maildata = [configfile, confreport.tstart, confreport.tearr[-1],period, runid]
        errortype = "noxml"        
    #update progress
    dbio.update_progress(runid, "final")        
    #send SUCCESS or FAILURE email to user/admin
    ok_send = send_report_mail(email, util.repConfig().data["admin_email"], xml_ok, maildata, errortype)     

    #remove tmp file
    rmtree(dirname)
       
    #sleep to allow the visualization of "100%" on webapp    
    sleep(5)    
    dbio.remove_running_report(runid, keep_open=True)
    dbio.update_config_files(configfile, 0)         

    ############################ BENCHMARK ##################        
    with open(confreport.bm_tfile, "a") as f:
        finalte, finalte_ts = util.get_time()
        f.write("CLOSING (db updates, temp removal, mail sending) END   :\t" + str(finalte) +"\n")
        f.write("CLOSING (db updates, temp removal, mail sending) DURATION :\t"+str(util.pretty_time(finalte_ts - finalts_ts))+"\n")
    print("CLOSING (db updates, temp removal, mail sending) DURATION : ", util.pretty_time(finalte_ts - finalts_ts))            
    ########################################################## 

def periodic_report(confreport, connconfig, nthreads, runid, url, dirname, pid, email):
    #Init threadLimiter
    global threadLimiter
    threadLimiter=threading.BoundedSemaphore(nthreads)  
    dbio = db_io.dbIO(connconfig)   
    start_time = None    
    #infinite loop
    while True:
        #UPDATE RUNNING REPORT
        if start_time is None:
            db_start_time = confreport.tstart
        else:
            db_start_time = start_time
        #Update running reports
        dbio.update_running_reports(pid, runid, tstart = db_start_time)
        #update config file status
        dbio.update_config_files(configfile, 1)            
     
        #Thread for each system
        threads =[]
        for i in range(len(confreport.systems)):
            source = confreport.systems[i]      #source
            thread_id = i
            session = threadSys(thread_id, "Thread_"+source, confreport, nthreads, runid, start_time)
            threads = threads+[session]
            threads[thread_id].start()
            
        errors = {}
        par_pos = {}  
        for th in threads:
            th.join()
            #get analysis results
            hres = th.get_hktm_result()
            err = th.get_errors()
            pp = th.get_parameters_pos()
            errors.update({th.source:err})
            par_pos.update({th.source:pp})  

        #OUTPUT CREATION
        print("ACQUISITION END")
        xml_ok, creationdate, fname = create_xml_report(confreport, runid, connconfig, nthreads, errors, par_pos)        
        #update progress
        dbio.update_progress(runid, 6.0)    
        if xml_ok:
        #Create PDF report
            try:
                pdf_ok = create_pdf_report(fname, confreport.plotfromfile)
            except:
                xml_error_pdf(confreport, fname)
                pdf_ok = False           
            #Update reports table in AIDA DB
            dbio.insert_report_file(fname, user, creationdate, period, configfile, confreport.tstart, confreport.tstop)           
          
            #config for SUCCESS mail to user/admin
            maildata = [fname, user, creationdate, period, confreport.tstart, confreport.tstop, runid, url, pdf_ok]
            errortype = ""      
        else:
            #config for FAILURE mail to user/admin
            maildata = [configfile, confreport.tstart, confreport.tstop,period, runid]
            errortype = "noxml"          
        #update progress
        dbio.update_progress(runid, "final")
        #send SUCCESS or FAILURE email to user/admin          
        ok_send = send_report_mail(email, util.repConfig().data["admin_email"], xml_ok, maildata, errortype)

        #sleep to allow the visualization of "100%" on webapp    
        sleep(5)
        dbio.update_running_reports(pid, runid, tstart = confreport.tstop, status=-99, keep_open=True)    
        dbio.update_config_files(configfile, isrunning=2, start_date=confreport.tstop)   
        #remove tmp file
        rmtree(dirname)
        mkdir(dirname)       
        start_time = confreport.tstop

        #empty memory
        del errors        
    
def main(configfile, nthreads, period, user, url, runid, email, t0):

    ############################ BENCHMARK ##################
    t0_bench_str, t0_bench_timestamp = util.get_time()   
    print("START PROGRAM:", t0_bench_str)     
    #########################################################
    #error class
    global e
    e = util.statusMsg()
    #get AIDA DB connection data from config.json
    connconfig = util.repConfig().data['local_db']
    #number of processes
    try:
        nthreads = util.repConfig().data['nprocs']
    except:
        pass

    dbio = db_io.dbIO(connconfig)
    #check connection to AIDA DB
    locerr, connection = dbio.connect()

    if locerr == 0:
        dbio.close()
    #if not connected to local DB, send error mail and exit  
    else:
        e.localstatus = 1
        maildata = [configfile, "", "", period, runid]
        ok_send = send_report_mail(email, "", False, maildata,"locerr")            
        exit(1)    
    #get data from experiment configuration file
    confreport = reportConfig(configfile, period, connconfig, user, tresume=t0, runid=runid)

    #get pid
    global pid
    pid = getpid()
    #Update running reports
    dbio = db_io.dbIO(connconfig)
    status = dbio.get_report_status(runid)
    dbio.update_running_reports(pid, runid, status=status)

    ############################ BENCHMARK ##################   
    tend_config_str, tend_configtimestamp = util.get_time()    
    with open(confreport.bm_tfile, "w") as f:
        f.write("RUNID : " +str(runid)+"\n")
        f.write("Period : " +period+"\n")
        f.write("Experiment interval : " +str(confreport.tsarr[0])+" - " +str(confreport.tearr[-1])+"\n\n")
        f.write("START ANALYSIS: " + t0_bench_str+"\n")
        f.write("READ CONFIG DURATION : "+str(util.pretty_time(tend_configtimestamp - t0_bench_timestamp))+"\n\n")
    print("READ CONFIG DURATION :", util.pretty_time(tend_configtimestamp - t0_bench_timestamp))           
    ##########################################################
    #sleep to allow the visualization of "waiting" on webapp    
    sleep(3)
    
    #if no errors in experiment configuration file
    if confreport.error == 0:
        #create current report temporary directory
        dirname = confreport.set_workdir(runid)
        #connection = util.connect_db(connconfig)
        if period == "ondemand":
            ondemand_report(confreport, connconfig, nthreads, runid, url, dirname, pid, email)
            ############################ BENCHMARK ##################
            t_branch_end, t_branch_end_timestamp = util.get_time()                      
            with open(confreport.bm_tfile, "a") as f:
                f.write("END ONDEMAND BRANCH : "+str(t_branch_end)+"\n")
                f.write("DURATION ONDEMAND BRANCH: " + str(util.pretty_time(t_branch_end_timestamp-tend_configtimestamp))+"\n")
            print("DURATION ONDEMAND BRANCH", util.pretty_time(t_branch_end_timestamp-tend_configtimestamp))
            ############################################################ 
        else:
            #wait until start date is reached and data are available (start_date + cadence + offset)
            #time to wait for available data            
            offset = util.repConfig().offset*3600
            #data acquisition step            
            cadence = confreport.cadence*3600
            #time to run report generation pipeline            
            t_pipe_start = confreport.ts_stamp + cadence + offset
            t_pipe_start_dt = datetime.utcfromtimestamp(t_pipe_start)
            #time to wait from report config submission to run
            wait_time = t_pipe_start - util.utc_now().timestamp()
            if wait_time > 0:
                dbio.update_config_files(configfile, 2)              
                sleep(wait_time)
            periodic_report(confreport, connconfig, nthreads, runid, url, dirname, pid, email)

        ############################ BENCHMARK ##################
        now, now_timestamp = util.get_time()                        
        with open(confreport.bm_tfile, "a") as f:
            f.write("END PROGRAM : "+str(now)+"\n")
            f.write("TOTAL DURATION : " + str(util.pretty_time(now_timestamp-t0_bench_timestamp)))
        try:
            remove("current_dir.txt")
        except:
            pass
        print("END PROGRAM:", now)
        print("DURATION", util.pretty_time(now_timestamp-t0_bench_timestamp))
        ############################################################
    else:
        #send email for configuration file error
        #config for FAILURE mail to user/admin      
        maildata = [configfile, "", "", period, runid]
        ok_send = send_report_mail(email, "", False, maildata,"conferr")

if __name__ == "__main__":

    #nthreads to set automatically depending on the number of cores of the machine
    nthreads = multiprocessing.cpu_count()-1        #-1 leave 1 processor available for other purposes
    parser = argparse.ArgumentParser(prog = sys.executable +' generate_report.py')

    allowed = ["daily", "weekly", "monthly", "custom", "ondemand"]

    parser.add_argument('-c', '--config', metavar="FILE", help='Configuration file name')
    parser.add_argument('-p', '--period', metavar="PERIOD", help='Report periodicity '+str(allowed))
    parser.add_argument('-u', '--user', metavar="USER", help='Username launching script')
    parser.add_argument('-w', '--www', metavar="URL", help='Url of AIDA app')
    parser.add_argument('-r', '--rid', metavar="RUNID", help='Experiment ID in AIDA DB')
    parser.add_argument('-e', '--email', metavar="EMAIL", help='User email address')
    parser.add_argument('-t', '--tresume', metavar="START TIME", help='Starting date overwriting config file')
    args = parser.parse_args()

    period = vars(args)['period']
    if not period in allowed:
        print("\nError! Period not allowed\n")
        parser.print_help()
        exit(1)

    try:
        t0 = float(vars(args)['tresume'])
    except:
        t0 = None

    configfile = vars(args)['config']
    user = vars(args)['user']
    url = vars(args)['www']
    runid = vars(args)['rid']
    email = vars(args)['email']

    main(configfile, nthreads, period, user, url, runid, email, t0)