#!/usr/bin/python

import numpy as np
import json
from os import sep, path, mkdir, remove
import sys
import csv
import functions as util
import datautils as du
import reportutils as ru
from calculate_statistics import calc_stat
from collections import defaultdict
from shutil import copyfile
from astropy.io import fits
from astropy.table import Table
from datetime import datetime, timezone
import multiprocessing
import pymysql.cursors
import xml.etree.ElementTree as ET
import db_io
import traceback

class Efd():
    def __init__(self):
        #data origin (housekeeping/scientific)
        self.allowed_origin = ["HKTM","SCIENCE"]
        #columns to get from metadata db
        self.db_cols = "filename, startdate, enddate, basepath"
        #extra parameters for analysis
        self.exp_par_info = {}
        #name as used for AIDA db tables
        self.name = "efd"
        #source as defined in AIDA forms/json
        self.source = "EFD"
        self.parstruct = {"hktm" : ["par"], "science" : ["ic.ec","det","par"]}
        self.br_depth = {"hktm" : 1, "science" : 3}
        self.hasorig = True
        self.parallel = True
        self.runid_to_dir = {"hktm" : True, "science" : True}

    def __build_params_dict(self, sub):
        """Private method to extract all the report parameters for the system, divided by role (main keys or additional). Called by self.get_report_params()

        Parameters
        --------
            sub: string
                second level key ("HKTM"/"SCIENCE") as defined in the report configuration file.

        Returns
        -------
            pars: dictionary
                all the report parameters for the system, divided by role (main keys or additional)
                It is structured as follow:
                {
                    'keys': [<par1>, <par2>,...,<parN>],
                    'add': [<par1>, <par2>,...,<parN>]
                }

        """

        #AUTOMATIC PLOTS LIST FROM DB TODO
        graphops = ["scatter", "trend", "histogram"]
        addpars = []
        if sub=="HKTM":
            pars = ru.get_pars(self.report_tree[sub])
            addpars = ru.get_add(self.report_tree, ["Additional Parameters", "X"])
            addpars = list(np.unique(addpars))
        pars = {"keys" : pars, "add" : addpars}

        return pars
         
    def __build_science_query(self, var, tbl, t0, t1, extra, colfile = ""):  
    
        t0 = int(util.format_date(t0))
        t1 = int(util.format_date(t1))
        sql = "SELECT "+ var[2]+",timestamp FROM " + tbl + " WHERE timestamp >= " + str(t0) + " AND timestamp <= " + str(t1)        
        
        return sql

    def check_report_tree(self, check):
        """ Check if the configuration tree for a system in the configuration file has been  correctly compiled.

        Parameters
        --------
            check: class
                class containing methods to check the report tree, as defined by config_validation.configCheck()

        Returns
        -------
            dictionary
                dictionary containing the result of check in the following structure:
                {
                    'isvalid' : <True if the check is ok, False otherwise>,
                    'msg' : <message to display in the web application (or "" is check is ok)>
                }

        """
    
        isvalid = True
        msg = ""
        s=self.source

        plots = check.allowed_plots
        stats = check.allowed_stats

        #check subsystems
        subsk, checksub = check.check_subsystems(mainsys=s, allowed=self.allowed_origin)
        
        if not checksub['isvalid']:
            return checksub
        
        #check parameters name
        for k in subsk:
            if k=="HKTM":
              #  define structure for additional parameters
                add_tpl = "sub.par"     
                subsystems_dict = util.get_subsystems_from_file("hktm", self.name, check.connection) 
                #get required filters
                required_allowed = []
                for sk,v in subsystems_dict.items():
                    required_allowed.append(v['values'])
                    if sk=="subsystem":
                        check.allowed_subs=v['values']
                try:
                    req_str = check.get_keys(check.text[s][k])
                except:
                    msg = 'ERROR! Invalid branch structure in '+s+"/"+k
                    return {"isvalid" : False, "msg" : msg} 
                if len(req_str)==0:
                    msg = "ERROR! Branch "+k+" for system "+s+" is empty. Please, remove it from configuration file.\n"
                    return {'isvalid':False, 'msg':msg}
                
                for req in req_str:
                    req_arr = req.split(".")
                    #check syntax of required filters (A.B.C)
                    if len(req_arr) != len(required_allowed):
                        return {'isvalid':False, 'msg':"Invalid format for subsystem "+req+" in "+s+"/"+k+"\n"}
                    #check allowed filters
                    for i, r in enumerate(req_arr):
                        if r not in required_allowed[i]:
                            return {'isvalid':False, 'msg':"Unrecognized subsystem "+r+" in "+s+"/"+k+"/"+req+"\n"}
                    if not isinstance(check.text[s][k][req],dict):
                        msg = 'ERROR! Invalid branch structure for subsystem "'+req+'" in '+s+'/'+k+"\n"
                        return {'isvalid':False, 'msg':msg}                        

                    listpar, listval = self.get_params_list(k, check.connection, "WHERE subsystem='"+req+"'")
                    pars, checkpar = check.check_params(s,k,req,listpar=listpar) #pars : parameters to check, listpar : list of all available parameters
                    if not checkpar['isvalid']:
                        return checkpar
                    for p in pars:
                        #check operation
                        nops, checkop = check.check_op(s,k,req,p)
                        if not checkop['isvalid']:
                            return checkop
                        for i in range(nops):
                            currop = "Operation_"+str(i+1)                  
                            checkf =  check.check_exp(s,k,req,p,currop, listpar=listpar, extra_tpl=add_tpl)
                            if not checkf['isvalid']:
                                return checkf
            else:
                add_tpl = "par"
                pars, checkpar = check.check_params(s,k,listpar=listpar) #pars : parameters to check, listpar : list of all available parameters
                if not checkpar['isvalid']:
                    return checkpar
                for p in pars:
                    #check operation
                    nops, checkop = check.check_op(s,k,p)
                    if not checkop['isvalid']:
                        return checkop
                    for i in range(nops):
                        currop = "Operation_"+str(i+1)
                        checkf =  check.check_exp(s,k,p,currop, listpar=listpar, extra_tpl=add_tpl)
                        if not checkf['isvalid']:
                            return checkf                

        return {'isvalid':isvalid, 'msg':msg}

    def copylocal(self, f2use, orig_path, final_path, usecase = "report"):
        """ Copy files from local repository to temporary directory

        Parameters
        --------
            f2use: list
                list of files to copy
            orig_path: string
                path of local repository (from configuration)
            final_path: string
                path of destination (temporary path)
            usecase : string, optional
                experiment from which the call is done ("report", "plot"...), Deafult is "report"

        Returns
        -------
            file_ok: boolean
                True if all the files in the list f2use have been successfully copied, False otherwise

        """
        orig_path = orig_path.replace("/", sep)
        file_ok_arr = []
        fullpath = final_path+sep+self.name
        for f in f2use:
            runid = util.extract_runid(f)
            fullname = orig_path + sep+runid + sep + f
            if path.isfile(fullname):
                copyfile(fullname, fullpath+sep+f)
            #check if copy has been completed correctly
            if path.isfile(fullpath+sep+f):
                file_ok_arr.append(True)
            else:
                file_ok_arr.append(False)
        file_ok = all(file_ok_arr)

        return file_ok

    def count_params(self, conf, sub):
        """ Return the number of main parameters for the selected sub.

        Parameters
        --------
            conf: class
                class generate_report.reportConfig() containing report configuration from configuration file
            sub : string
                second level key ("HKTM"/"SCIENCE") as defined in the report configuration file.

        Returns
        -------
            npar : int
                number of parameters
        """

        npar = 0
        sub_params = conf.repdata[self.source][sub].keys()
        npar += len(sub_params)
        return npar

    def db_statement_filelist(self, addstatement, tstart, tstop):
        """Set the MYSQL WHERE statement to get the list of files to download from the metadata archive

        Parameters
        --------
            addstatement : string
                "condition" defined in the system configuration file
            tstart : string
                start datetime in the form compliant to the metadata db format (YYYY-MM-DD HH:mm:ss)
            tstop : string
                end datetime in the form compliant to the metadata db format (YYYY-MM-DD HH:mm:ss)

        Returns
        -------
            statement: string
                MYSQL WHERE statement

        """

        statement = "WHERE startdate <= '"+tstop+"' AND enddate >= '"+tstart+"' "+addstatement+" AND swcomponentid <> 1"
        return statement

    def download_file(self, fname, conf, ftp, tmp_dir, repo):
        tmppath = tmp_dir+self.name+sep
        completed = repo.download_file(fname, tmppath)
         
        return completed
        
    def get_data_from_db(self, data, conf, e):
        #Import data parameters
        source, plot, n_ypar, tstartdb, tenddb = du.get_base_data(data)
        try:
            extraf = json.loads(data['extra'].value)
        except:
            extraf = {}

        t0 = data['tstart'].value#.replace(" ","T")
        t1 = data['tend'].value#.replace(" ","T")
        
        #import y0 parameter data
        y0 = du.inData(data,source,"y0")
        y0_data = ["y0", y0.sys, y0.par ,y0.row+y0.col,y0.ic]
        
        sql = self.__build_science_query(y0_data, conf["tabname"], t0, t1, extraf, colfile = "FILENAME") 

        connection = util.connect_db(conf)
        with connection.cursor() as cursor:
            # Execute query.
            cursor.execute(sql)
            out_y0 = cursor.fetchall()        
        
        dates=[]
        y0_vals = []
        flist = []
        for item in out_y0:
            dates.append(item['timestamp'])
            try:            
                y0_vals.append(item[y0.par])
            except:
                y0_vals.append(item[y0.par+"_phys"])

        # If scatter plot, x param exists
        if plot == "scatter":
            #Import x parameter data
            x = du.inData(data,source,"x")
            x_data = ["x", x.sys, x.par,x.row+x.col,x.ic]
            out_x_dict = {}
            sql = self.__build_science_query(x_data, conf["tabname"], t0, t1, extraf, colfile = "FILENAME") 
            with connection.cursor() as cursor:
                # Execute query.
                cursor.execute(sql)
                out_x = cursor.fetchall() 

            for item in out_x:
                curr_d = item['timestamp']
                try:            
                    curr_val = item[x.par]
                except:
                    curr_val = item[x.par+"_phys"]
                out_x_dict.update({curr_d:curr_val})                                
                if curr_d not in dates:
                    dates.append(curr_d)
                    y0_vals.append(-999)            
        #Import additional y data
        if n_ypar > 1:
            yadd = du.yAdditional(data,source)
            yadd_out={}
            for i in range(n_ypar-1):
                y_add_dates = []
                out_yadd_dict = {}
                yadd_data = ["y"+str(i+1), yadd.syss[i], yadd.pars[i],"",""]

                sql = self.__build_science_query(yadd_data, conf["tabname"], t0, t1, extraf, colfile = "FILENAME") 
                with connection.cursor() as cursor:
                # Execute query.
                    cursor.execute(sql)
                    curr_out = cursor.fetchall()                 

                for item in curr_out:
                    curr_d = item['timestamp']
                    try:            
                        curr_val = item[yadd.pars[i]]
                    except:
                        curr_val = item[yadd.pars[i]+"_phys"]      
                    out_yadd_dict.update({curr_d:curr_val})
                    if curr_d not in dates:
                        dates.append(curr_d)
                        y0_vals.append(-999)
                yadd_out.update({"y"+str(i+1) : out_yadd_dict})
        connection.close()
        if len(dates) > 0:
            final_files = []
            final_dates, final_y0 = (list(t) for t in zip(*sorted(zip(dates, y0_vals))))
        else:
            final_dates = []
            final_y0 = []
            final_files = []
        # If scatter plot, x param exists
        if plot == "scatter":
            x_vals = []
            for d in final_dates:
                try:
                    x_vals.append(out_x_dict[d])
                except:
                    x_vals.append(-999)             
        else:
            x_vals = [0]*len(final_dates)
            
        not_valid = [final_y0.count(-999) == len(final_y0)]
        if len(final_dates) > 0 and x_vals.count(-999) != len(x_vals):
            result = {"date" : final_dates, "x" : x_vals, "y0" : final_y0}
            if n_ypar > 1:
                for y, v in yadd_out.items():
                    curr_y = []
                    for d in final_dates:
                        try:
                            curr_y.append(v[d])
                        except:
                            curr_y.append(-999)
                    not_valid.append(curr_y.count(-999) == len(curr_y))
                    result.update({y : curr_y})
            if all(not_valid):
                e.datastatus = 1
                result = {}
        else:
            e.datastatus = 1
            result = {}

        return result      
    
    def get_files2use(self,report_conf, origin, pars, remotelist):
        """ Select useful files from the list of all files in the selected period taken from the metadata archive

        Parameters
        --------
            report_conf: class
                class generate_report.reportConfig() containing report configuration from configuration file
            origin: string
                second level key ("hktm"/"science") as defined in the system configuration file .conf
            pars: list
                list of parameters to analyze for the selected system/origin
            remotelist: list
                list of files to consider in the defined period, obtained from metadata archive

        Returns
        -------
            f2use: list
                list of files to use for the analysis, after cleaning

        """
        f2use = []
        fwithf = []        
        f2use_plf = util.get_plf(report_conf.root+sep+origin+"_plf.dat", pars, remotelist)
        for f in f2use_plf:
            flag_f = f.split("_")[1]
            if flag_f == "f":
                fwithf.append(f)
            else:
                f2use.append(f)
        for f in fwithf:
            f0 = f.replace("_f_","_0_")
            pos = np.where(np.array(f2use) == f0)[0]
            if len(pos)>0:
                i=pos[0]
                f2use[i] = f
              
        return f2use
    
    def get_par_info(self, listpar, conn, sub):
        """ Retrieve parameters info from AIDA db

        Parameters
        --------
            listpar: list
                list of main keys parameters for which getting info
            conn: class
                opened connection to AIDA db
            sub: string
                second level key ("HKTM"/"SCIENCE") as defined in the report configuration file.

        Returns
        -------
            infopar: list of dictionaries
                list of dictionaries containing all parameters info directly from AIDA db table "<sub.lower()>_<self.name>_params" (for instance "hktm_nisp_params")

        """

        infopar = []
        statement = "WHERE "
        for i in range(len(listpar)):
            if i == 0:
                statement += "param = '"+listpar[i]+"'"
            else:
                statement += " OR param = '"+listpar[i]+"'"
        #get parameters info from DB
        infopar = util.db_query(conn, sub.lower()+"_"+self.name+"_params", "*", statement, "all")

        return infopar

    def get_params_list(self, subsys, connection, stat=""):
        """ Retrieve the list of all available parameters and (optionally) the related list of values for the selected subsystem from AIDA db

        Parameters
        --------
            subsys: string
                second level key ("HKTM"/"SCIENCE") as defined in the report configuration file.
            connection: class
                opened connection to AIDA db

        Returns
        -------
            listpar: list
                list of all available parameters
            listval: list of lists
                list containing the lists of available values for each available parameter. For each element listpar[i], the corresponding values list is listval[i]. For this system, listval = [].

        """

        try:
            sys = self.name
            ss = subsys.lower()

            table = ss+"_"+sys+"_params"


            res_query = util.db_query(connection, table, '*', statement = stat, res_type = "all")
            #res to list of allowed params
            listpar = []
            for item in res_query:
                #list of all available parameters
                listpar.append(item['param'])
        except:
            listpar = []

        listval = []

        return listpar, listval

    def get_plot_data(self, connection, data, nthreads, remlist, conf, e, repo = "", metadata={"data" : {}}):
        """Collect data to plot in online web application from data repository.

        Parameters
        --------
            connection : class
                opened connection to AIDA db
            data : class
                cgi.FieldStorage class containing data collected from web application form
            nthreads : int
                maximum number of parallel threads to run
            remlist : list of dictionaries
                list containing retrieved info about files to use. For each file, info are collected as dictionary as retrieved by the query to metadata archive
            conf : class
                main AIDA configuration (from functions.repConfig())
            e : class
                class to handle with errors

        Returns
        -------
            result: dictionary
                dictionary containing data retrieved from data repository. It is structured as follow:
                    result={
                        'date' : [<datetime_1 ('YYYY-MM-DD HH:mm:ss')>, <datetime_2>, ... ,<datetime_N>],
                        'x': [<x_parameter_1 as string (or '0' if not required)>, <x_parameter_2>, ... ,<x_parameter_N>]
                        'y0': [<y0_parameter_1 as string>, <y0_parameter_2>, ... ,<y0_parameter_N>],
                        'y1': [<y1_parameter_1 as string>, <y1_parameter_2>, ... ,<y1_parameter_N>],
                        ...
                        'y<M>': [<yM_parameter_1 as string>, <yM_parameter_2>, ... ,<yM_parameter_N>],
                    }
                Records 'y1'...'y<M>' are reported only if they have been required from user.

        """

        #Import data parameters
        source, plot, n_ypar, tstartdb, tenddb = du.get_base_data(data)
        tmp_dir = data['user'].value
        #hktm/science
        sub = data['usecase'].value

        # If scatter plot, x param exists
        if plot == "scatter":
            #Import x parameter data
            x = du.inData(data,source,"x")

        #Import y0 parameter data
        y0 = du.inData(data,source,"y0")

        listdet = None     
        
        if plot == "scatter":
            listsys = [x.sys, y0.sys]       #list of systems for each variable
            listparams = [x.par, y0.par]    #list of params for each variable
            listadu = [x.adu, y0.adu]
            if sub == "science":
                listdet = [x.det, y0.det]            
        else:
            listsys = [y0.sys]
            listparams = [y0.par]
            listadu = [y0.adu]
            if sub == "science":
                listdet = [y0.det]            
        #Import additional y data
        if n_ypar > 1:
            yadd = du.yAdditional(data,source)
            for i in range(n_ypar-1):
                curr_sys = yadd.syss[i]
                listsys.append(curr_sys)
                listparams.append(yadd.pars[i])
                listadu.append(yadd.adu[i])
                if sub == "science":
                    listdet.append(yadd.dets[i])                

        todownload = []         #files to download/copy
        filenames=[]            #files already in user local path
        ftp = ""
        ftpmsg = {}

        # list of files stored in temporary local DB
        local_files = []        #list of all files in local_files structured as query result
        local_files = util.db_query(connection, "local_files",
                            #"filename, data_time",
                            "filename",
                            "WHERE (date_start <= '"+str(tenddb)+"' AND date_stop >= '"+str(tstartdb)+"' AND data_source = '"+source+"' AND username  = '"+tmp_dir+"')",
                            "all")
        #create list with all files
        try:
            allfiles = [f.get('filename') for f in remlist]
        except:
            allfiles = remlist
            
        #list of required files
        reqfiles = allfiles

        #create list of all locafile
        locfiles = [f.get('filename') for f in local_files]
        #split required files in files to download and already downloaded
        for f in reqfiles:
            if f in locfiles:
                filenames.append(f)
            else:
                todownload.append(f)
 
        nfiles = len(filenames)
        n2download = len(todownload)
        if nfiles + n2download > 0:
            if nthreads == 0:
                nthreads = 1

            self.exp_par_info.update({"tstart" : tstartdb, "tstop" : tenddb})
            threads = du.retrieve_data(nthreads, filenames, self, listparams, tmp_dir, todownload, conf, listadu, listdet, repo = repo, metadata = metadata)
            #collect output from threads
            filedict = {}
            filestatus = []
            downstatus = []
            nastatus = []
            file2db = []
            listfiles={}
            files = []
            for th in threads:
                th.join()
                filedict.update(th.get_res())
                filestatus.append(th.get_status()[0])
                downstatus.append(th.get_status()[1])
                nastatus.append(th.get_status()[3])
                file2db.append(th.todb)
                curr_fl = th.get_listfiles()
                listfiles = {**listfiles,**th.get_listfiles()}
            file2db = [item for sublist in file2db for item in sublist]
            
            #store file info into local_files db
            if metadata["data"] != {}:
                if conf.usecase == "science":              
                    filedate = []
                    for k, par_meta in metadata["data"].items():
                        for parfile in par_meta['hkfitsfile']:
                            #build dict for db storing
                            if parfile in file2db:
                                #index of input in file list
                                idx = par_meta['hkfitsfile'].index(parfile)                                
                                #set date
                                obtdate = par_meta['obt'][idx]
                                filedate.append({'filename':parfile, 'startdate' : obtdate})
                    remlist = filedate
                elif conf.usecase == "hktm":
                    remlist = []
                    for f in metadata["data"].keys():
                        name_noext = f.split(".")[0]
                        date_str = name_noext.split("_")[-1].split("-")
                        startd = datetime.strptime(date_str[0], '%Y%m%dT%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
                        endd = datetime.strptime(date_str[1], '%Y%m%dT%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
                        remlist.append({'filename' : f, 'startdate' : startd, 'enddate' : endd})
            for fname in file2db:
                a = []
                #find fname in remlist & get tstart, tstop                
                for x in remlist:
                    if x['filename'] == fname:
                        curr_start = x['startdate']
                        try:
                            curr_end = x['enddate']
                        except:
                            curr_end = x['startdate']
                        a.append([curr_start,curr_end])
                #convert tstart, tstop
                tstart = int(util.format_date(str(a[0][0])))
                tstop = int(util.format_date(str(a[0][1])))
                util.update_local_files(connection, fname, source, None, tstart,tstop, tmp_dir)

            if any(downstatus):
                e.downstatus = 1
            if any(filestatus):
                e.filestatus = 1
            if any(nastatus):
                e.nastatus = 1

            if filedict != {}:
                #add output to numpy array
                finaldata = []
                dates = []
                for k,v in filedict.items():
                    tmp_row = []
                    if not isinstance(k,str):
                        dates.append(datetime.utcfromtimestamp(k).strftime('%Y-%m-%d %H:%M:%S'))                     
                    else:
                        dates.append(k)
                    if plot!="scatter":
                        tmp_row.append("0")
                    for i in v:
                        tmp_row.append(str(i))
                    finaldata.append(tmp_row)

                # sort array if plot is trend to avoid weird connection lines in plot
                if plot == "trend":
                    if len(dates)>0:
                        dates, finaldata = (list(t) for t in zip(*sorted(zip(dates, finaldata))))
                finaldata = np.array(finaldata).transpose()
                #create result dictionary
                result = du.create_result(dates, finaldata, n_ypar)
                if conf.usecase == "science": 
                    #add filelist
                    for d in dates:
                        files.append(listfiles[d])
                    result.update({"files" : {"HKFitsFile" : files}})                   
            else:
                e.datastatus = 1
                result = {}
        else:
            e.datastatus = 1
            result = {}

        return result      
    
    def get_report_params(self, report_data):
        """ Update self.params with all the report parameters for the system, divided by role (main keys or additional)

        Parameters
        --------
            report_data: dictionary
                dictionary containing configuration data as defined in reportConfig().repdata

        Returns
        -------
            self.params: dictionary
                all the report parameters for the system, divided by role (main keys or additional)
                It is structured as follow:
                {
                    <sub name 1("hktm"/"science")> : {
                        'keys': [<par1>, <par2>,...,<parN>],
                        'add': [<par1>, <par2>,...,<parN>]
                    },
                    <sub name 2> : ...
                }

        """
        self.params = {}
        self.report_tree = report_data[self.source]
        subs = ru.get_keys(self.report_tree)[0]
        for k in subs:
            curr_params = self.__build_params_dict(k)
            self.params.update({k.lower() : curr_params})

        return self.params    
    
    def report_data_from_db(self, par, sub, conf, tstart = None, tstop = None, result={}):
        """ Read data by querying remote DB

        Parameters
        --------
            par : list
                list of all parameters to query, indipendently from being main or additional parameters
            sub: string
                second level key ("hktm"/"science") as defined in the report configuration file in lowercase format.                
            conf : class
                main AIDA configuration (from functions.repConfig())
            tstart : int
                timestamp of start date/time (UTC)
            tstop : int
                timestamp of end date/time (UTC)
            result : dictionary, optional
                results dictionary to update. Default : {}

        Returns
        -------
            result: dictionary
                results dictionary updated with extracted values. Its structure is:
                    ret={<parameter> : {"dates" : [datetime string in the form 'YYYY-MM-DD HH:mm:ss'], "values" : [values]}
        """

        conndata = conf.dbconfig[sub]
        connlocal = conf.data['local_db']
        #convert dates
        if tstart is None:      
            t0 = self.exp_par_info['tstart']
        else:
            t0 = datetime.utcfromtimestamp(tstart).strftime('%Y-%m-%d %H:%M:%S')
        if tstop is None:       #????
            tf = self.exp_par_info['tstop']
        else:
            tf = datetime.utcfromtimestamp(tstop).strftime('%Y-%m-%d %H:%M:%S')
            
        tbl = conndata["tabname"]            
        extra = {}
        for p in par:
            #get subsystem and param name
            psplit = p.split(".")
            subsys = psplit[0]
            parname = psplit[1]
            pdata = ["", "", parname]
            
            sql = self.__build_science_query(pdata, tbl, t0, tf, extra)
            connection = util.connect_db(conndata)
            with connection.cursor() as cursor:
                # Execute query.
                cursor.execute(sql)
                out_data = cursor.fetchall()      
            connection.close()        
            dates=[]
            vals = []
            for item in out_data:
                print(item)
                dates.append(item['timestamp'])
                curr = item[parname]
                if isinstance(curr, str):
                    try:
                        curr = int(curr)
                    except ValueError:
                        try:
                            curr = float(curr)
                        except:
                            pass
                vals.append(curr)
            result.update({p:{"dates":dates, "values":vals}})

        return result       
    
    def read_data_from_file(self, input, temp_dir, par, conf, tstart = None, tstop = None, adu=None, det=None, repo = None, metadata={}, result = {}):
        """ Read useful data from files in the temporary report directory

        Parameters
        --------
            input : string
                file to open
            tmp_dir : string
                temporary report directory
            par : list
                list of all parameters to get from file, indipendently from being main or additional parameters
            conf : class
                main AIDA configuration (from functions.repConfig())
            tstart : int
                timestamp of start date/time (UTC)
            tstop : int
                timestamp of end date/time (UTC)
            result : dictionary, optional
                results dictionary to update. Default : {}

        Returns
        -------
            result: dictionary
                results dictionary updated with extracted values. Its structure is:
                    ret={<parameter> : {"dates" : [datetime string in the form 'YYYY-MM-DD HH:mm:ss'], "values" : [values]}
        """

        if repo.metadata is not None:
            metadata = repo.metadata
        result = self.read_eas_file(input, temp_dir, par, conf, tstart, tstop, adu, det, metadata, result)
        
        return result        

    def read_eas_file(self, input, temp_dir, par, conf, tstart, tstop, adu, det, metadata, result):       
        f2open = temp_dir+self.name+sep+input

        if tstart is None:
            tstart = self.exp_par_info['tstart']
        if tstop is None:
            tstop = self.exp_par_info['tstop']        

        if conf.usecase == "science":
            for k,par_meta in metadata["data"].items():
                values = []
                dates=[]
                det = k.split(".")[-2]
                p = k.split(".")[-1]
                if input in par_meta['hkfitsfile']:
                    #index of input in file list
                    idx = par_meta['hkfitsfile'].index(input)
                    #set date
                    curr_date = par_meta['obt'][idx]
                    tbl = det.replace("_","")+".RAW"
                    
                    #search for parameter in the table header
                    try:
                        data = Table.read(f2open, hdu=tbl)                    
                        data_par = data.meta[p]
                        dates.append(curr_date)
                        values.append(data_par)                        
                    except:
                        pass
                    try:
                        stored_d = result[k]["dates"]
                        stored_v = result[k]["values"]
                        new_dates = stored_d+dates
                        new_values = stored_v+values
                        result.update({k:{"dates":new_dates, "values":new_values}})
                    except:
                        result.update({k:{"dates":dates, "values":values}})
        elif conf.usecase == "hktm":
            hdus = metadata["data"][input]
            for h in hdus:
                dates = []
                values = []
                data = Table.read(f2open, hdu=h)
                par = data.colnames[1]
                datelist = data['timestamp']
                for i,d in enumerate(datelist):
                    if int(str(d)[:-6]) >= tstart and int(str(d)[:-6])<= tstop :
                        dates.append(datetime.utcfromtimestamp(d/1000000).strftime('%Y-%m-%d %H:%M:%S.%f'))     #POSSIBILE BUG TIMESTAMP FILE SOC HKTM
                        values.append(data[par][i])
                try:
                    stored_d = result[par]["dates"]
                    stored_v = result[par]["values"]
                    new_dates = stored_d+dates
                    new_values = stored_v+values
                    result.update({par:{"dates":new_dates, "values":new_values}})
                except:
                    result.update({par:{"dates":dates, "values":values}})
                   
        return result                
    
    def set_par_summary(self, par, info):
        """Set dictionary containing parameters info to be stored in PDF report summary table

        Parameters
        --------
            par: string
                name of parameter
            info: list of dictionaries
                list of dictionaries obtained by self.get_par_info

        Returns
        -------
            out: dictionary
                dictionary containing parameter data to be summarized into PDF report table

        """
        out = {"Parameter" : par}
        for item in info:
            if item['param'] == par:
                #get subsystem
                sub = item['subsystem'].strip()
                #get description
                descr = item['description']
                if (descr is None) or (len(descr)==0):
                    descr = "-"
                #get rangeval
                try :
                    minval = item['minval']
                    if int(minval) == -999:
                        minval ="ND"
                except:
                    minval = "ND"
                try :
                    maxval = item['maxval']
                    if int(maxval) == -999:
                        maxval ="ND"
                except:
                    maxval = "ND"
                if minval != "ND" and maxval != "ND":
                    rangeval = "["+str(minval)+", "+str(maxval)+"]"
                else:
                    rangeval = "ND"
                #set detector
                det = ""
                break
        out.update({"Subsystem" : sub, "Description" : descr, "Allowed Range" : rangeval, "Detector" : det})

        return out

    def set_pdf_params_items(self, p, conn, tbl, usecase = "hktm"):
        """Retrieve description data for paramaters from AIDA db

        Parameters
        --------
            p: string
                name of parameter
            conn: class
                opened connection to AIDA db
            tbl: string
                table containing 'description' column,
            usecase : "hktm" or "science"
                origin of data. Default is "hktm"

        Returns
        -------
            list
                list containing name, subsystem and description of the input parameter

        """

        par_arr = p.split(".")
        if usecase == "hktm":
            par = par_arr[1]
            subs = par_arr[0]
            add = {}
        elif usecase == "science":
            par = par_arr[-1]
            subs = None
            add = {"INTR_CONF" : par_arr[0], "EXP_CONF" : par_arr[1]}
        sql = "SELECT description FROM "+tbl+" WHERE param = '"+par+"'"
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            d = result['description']
            if d == "":
                d = "-"

        return [par,subs, d, add]