#!/usr/bin/python

"""
Data Repository Interface Modules.

This module provides repository classes (such as FAKE and USDF) implementing 
data download, plot data retrieval, and report data extraction methods for 
various backend archives and systems.

@package AIDA
@module repos
"""

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
    """Repository interface implementation for fake or local mock data archives.

    Attributes
    ----------
    slug : str
        Repository slug identifier ("fake").
    method : str
        Data transfer protocol method ("ftp").
    use_runid : bool
        Flag indicating if directory structure uses run IDs (True).
    metadata : dict or None
        Metadata container.
    """
    def __init__(self):
        self.slug = "fake"
        self.method = "ftp"
        self.use_runid = True
        self.metadata = None

    def download_file(self,fname, conf, ftp, tmp_dir, source):
        """Download files from remote FTP repository to local temporary directory.

        Parameters
        ----------
        fname : str
            Filename to download.
        conf : repConfig
            Main AIDA operational configuration object.
        ftp : ftplib.FTP
            Active FTP connection handle.
        tmp_dir : str
            Temporary working directory path.
        source : str
            Lowercase system source name.

        Returns
        -------
        completed : bool
            True if file was downloaded successfully, False otherwise.
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
        """Retrieve dataset series for plot generation from file repository or database.

        Parameters
        ----------
        conf : repConfig
            Repository configuration object.
        e : statusMsg
            Status and diagnostic message handler object.
        connection : pymysql.connections.Connection
            Active local database connection.
        data : cgi.FieldStorage or dict
            CGI request payload.
        source : str
            System source identifier name.
        ts : str
            Start datetime string.
        te : str
            End datetime string.
        nthreads : int
            Parallel thread allocation count.
        prod_id : str or None, optional
            Product ID filter (default is None).

        Returns
        -------
        result : dict
            Extracted plot data dictionary.
        e : statusMsg
            Updated status message object.
        """
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
        """Retrieve dataset series for report generation from remote repository.

        Parameters
        ----------
        conf : repConfig
            Repository configuration object.
        sub : str
            Subsystem or origin identifier string.
        thClass : threadSys
            Worker thread handling report data collection.
        t0 : str
            Data range start datetime string.
        tf : str
            Data range stop datetime string.
        report_conf : reportConfig
            Report configuration instance.
        e : statusMsg
            Status message handler object.
        dt : int
            Cadence step index.
        i : int, optional
            Acquisition step index (default is 0).

        Returns
        -------
        params_chunk : list
            Extracted data chunks list.
        e : statusMsg
            Updated status message object.
        """
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
    """Repository interface implementation for the USDF (EFD) archive.

    Attributes
    ----------
    slug : str
        Repository slug identifier ("efd").
    method : str
        Data transfer protocol method ("ftp").
    use_runid : bool
        Flag indicating if directory structure uses run IDs (True).
    metadata : dict or None
        Metadata container.
    """
    def __init__(self):
        self.slug = "efd"
        self.method = "ftp"
        self.use_runid = True
        self.metadata = None
    
    def retrieve_plot_data(self, conf, e, connection, data, source, ts, te, nthreads, prod_id = None):
        """Retrieve dataset series for plot generation from the USDF archive.

        Parameters
        ----------
        conf : repConfig
            Repository configuration object.
        e : statusMsg
            Status and diagnostic message handler object.
        connection : pymysql.connections.Connection
            Active local database connection.
        data : cgi.FieldStorage or dict
            CGI request payload.
        source : str
            System source identifier name.
        ts : str
            Start datetime string.
        te : str
            End datetime string.
        nthreads : int
            Parallel thread allocation count.
        prod_id : str or None, optional
            Product ID filter (default is None).

        Returns
        -------
        result : dict
            Extracted plot data dictionary.
        e : statusMsg
            Updated status message object.
        """
        result={}
        
        sysclass = classes.sys_inst(source)
        if not (e.confstatus or e.localstatus or e.remotestatus):
            result = sysclass.get_plot_data(connection, data, nthreads, [], conf, e, repo = self)

        return result, e
        
    def retrieve_report_data(self, conf, sub, thClass, t0, tf, report_conf, e, dt, i=0):
        """Retrieve dataset series for report generation from the USDF archive.

        Parameters
        ----------
        conf : repConfig
            Repository configuration object.
        sub : str
            Subsystem or origin identifier string.
        thClass : threadSys
            Worker thread handling report data collection.
        t0 : str
            Data range start datetime string.
        tf : str
            Data range stop datetime string.
        report_conf : reportConfig
            Report configuration instance.
        e : statusMsg
            Status message handler object.
        dt : int
            Cadence step index.
        i : int, optional
            Acquisition step index (default is 0).

        Returns
        -------
        params_chunk : list
            Extracted data chunks list.
        e : statusMsg
            Updated status message object.
        """

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

        return params_chunk, e
        
        
    
        
        
        
                        