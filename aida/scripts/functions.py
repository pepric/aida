#!/usr/bin/python

import json
import time         #useless?
import numpy as np
import sys          #useless?
from os import sep, remove, path,mkdir            #remove useless?
import threading
import pymysql.cursors
import ftplib
import socket           #useless?
import repos
import inspect
import classes
from shutil import copyfile
from datetime import datetime, timezone, timedelta
import filecmp
import traceback

class repConfig():
    def __init__(self, source = None, usecase = "config"):

        self.root = path.dirname(path.abspath(__file__)).replace("scripts","")
        self.usecase = usecase
        self.data, data_read_error = self.get_config_data()
        self.repclass = {}
        self.wgetdata_dict = {}
        self.path_dict = {}        
        if data_read_error==0:
            self.tmp_dir = "../users/"

        #operation mode
        self.opmode, opmode_error = self.get_opmode() #DA CAMBIARE A REGIME         #SE USECASE REPORT, L'OPMODE DEVE ESSERE PRESO DALLA TBL DEI CONFIG FILES TODO
      
        #data offset
        self.offset = self.get_offset()

        main_err = self.set_main()
        self.path_dict = {}
        self.wgeta_dict = {}
        self.wgetu_dict = {}
        self.wgetp_dict = {}
        self.wgetd_dict = {}
        self.dbconfig = ""
        self.nth_dict = {}
        repsource_error = 0
        data_rep_error = 0
        db_error = 0        

        if not source is None:
            s = source.lower()
            sourcedata, sourcedata_read_error = self.get_config_data(s+".conf")
            if sourcedata_read_error == 0:
                if self.usecase == "report":
                    self.sourcedata = sourcedata[self.opmode]
                else:
                    self.sourcedata = sourcedata[self.opmode][self.usecase]
                    
                self.get_nthreads()             
                repsource_error = self.set_rep_source()
                if repsource_error == 0:
                    db_error = self.set_db()
                    data_rep_error = self.set_data_rep()

        self.error = main_err or data_read_error or repsource_error or db_error or data_rep_error or opmode_error

    def get_config_data(self, cfile = "config.json"):
        error = 0
        data = None
        try:
            # get repository data from json
            fileobj = open("../"+cfile, "r")
            jsonstr = fileobj.read()
            fileobj.close()
            #change slashes
            jsonstr = jsonstr.replace("\\","/")
            #convert input string to json object
            data = json.loads(jsonstr)
        except:
            error = 1
        return data, error

    def get_nthreads(self):
        for sub, data in self.sourcedata.items():
            try:
                ftp_th = data["nprocs"]
            except:
                ftp_th = 1
            self.nth_dict.update({sub : ftp_th})

    def get_offset(self):
        try:
            offset = int(self.data['offset'])
        except:
            offset = 0

        return offset      
      
    def get_opmode(self):
        error = 0
        opmode = None
        try:
            conn_conf = self.data['local_db']
            conn = connect_db(conn_conf)
            result = db_query(conn, "operation_modes", "mode", "WHERE enable = 1", res_type="one")
            opmode = result['mode']
            conn.close()
        except:
            error = 1

        return opmode, error

    def set_db(self):
        error = 0
        try:
            if self.usecase == "report":
                self.dbconfig = {}
                for s in self.sourcedata:
                    self.dbconfig.update({s : self.sourcedata[s]['db']})
            else:
                self.dbconfig = self.sourcedata["db"]
        except:
            error = 1

        return error

    def set_data_rep(self):
        error = 0

        for sub,repsys in self.repsource.items():
            if self.usecase == "report":
                curr_sd = self.sourcedata[sub]
            else:
                curr_sd = self.sourcedata

            try:
                w = curr_sd["files repository"]
                method = self.repclass[sub].method
                if method == "ftp":
                    if isinstance(w,dict):
                        self.wgetdata_dict.update({sub : "remote"})
                        try:
                            self.wgeta_dict.update({sub : w["host"]})
                            self.wgetu_dict.update({sub : w["user"]})
                            self.wgetp_dict.update({sub : w["password"]})
                            self.wgetd_dict.update({sub : w["dir"]})
                        except:
                            error = 1
                    else:
                        self.wgetdata_dict.update({sub : "local"})
                        try:
                            self.path_dict.update({sub : w})
                        except:
                            error = 1

                    if self.usecase != "report":
                        self.wgetdata = self.wgetdata_dict[sub]
                        if self.wgetdata == "remote":
                            self.wgeta = self.wgeta_dict[sub]
                            self.wgetu = self.wgetu_dict[sub]
                            self.wgetp = self.wgetp_dict[sub]
                            self.wgetd = self.wgetd_dict[sub]
                        else:
                            self.path = self.path_dict[sub]
                elif method == "uri":
                    if w.startswith("http"):
                        self.wgetdata = "remote"
                    else:
                        self.wgetdata = "local"
                        self.path = w
                else:
                    error = 1
            except:
                self.wgetdata_dict.update({sub : ""})
                error = 1

        return error

    def set_main(self):
        error = 0
        try:
            self.main = set_path(self.data['webapp_dir'])
            if self.main[0] == sep:
                self.main = self.main[1:]
        except:
            error = 1

        return error

    def set_rep_source(self):
        error = 0
        try:
            list_repos = [m[0] for m in inspect.getmembers(repos, inspect.isclass) if m[1].__module__ == 'repos']
            self.repsource = {}
            if self.usecase == "report":
                for s in self.sourcedata:
                    repo = self.sourcedata[s]['repository']
                    if not self.sourcedata[s]['source'] in ['file','db']:
                        error=1
                    self.repsource.update({s : self.sourcedata[s]['source']})
                    #set repository class
                    if repo.upper() in list_repos:
                        repcls = classes.repos_inst(repo)
                        self.repclass.update({s : repcls}) 
                    else:
                        error = 1
            else:
                if not self.sourcedata['source'] in ['file','db']:
                    error=1
                self.repsource.update({self.usecase : self.sourcedata['source']})
                repo = self.sourcedata['repository']
                if repo.upper() in list_repos:
                    repcls = classes.repos_inst(repo)                  
                    self.repclass.update({self.usecase : repcls}) 
                else:
                    error = 1                
        except Exception as xx:
            error = 1

        return error

class statusMsg():
    def __init__(self):
        #Configuration file status
        self.confmsg = "ERROR!\nUnable to read configuration file.\nPlease check config.json"
        self.confstatus = 0
        #Main dir status
        self.mainmsg = "ERROR!\nMain directory not properly set.\nPlease check config.json"
        self.mainstatus = 0
        #FTP status
        self.ftpmsg = "WARNING!\nUnable to download files by FTP.\nAnalysis could be incomplete.\nPlease, check connection parameters or contact AIDA admin."
        self.ftpstatus = 0
        #Downloaded file check
        self.downmsg = "WARNING!\nOne or more files cannot be downloaded. Analysis could be incomplete"
        self.downstatus = 0
        #File status
        self.filemsg = "WARNING!\nOne or more files cannot be opened. Analysis could be incomplete"
        self.filestatus = 0
        #Local DB status
        self.localmsg = "ERROR!\nUnable to connect to AIDA local database.\nPlease retry or contact AIDA admin"
        self.localstatus = 0
        #Remote DB status
        self.remotemsg = "ERROR!\nUnable to connect to remote database.\nPlease retry or contact AIDA admin"
        self.remotestatus = 0
        #Check if there are data
        self.datamsg = "No available data for requested period"
        self.datastatus = 0
        #Check if there are missing parameters
        #self.missingmsg = "INFO!\nOne or more parameters are missing. Analysis could be incomplete"
        #self.missingstatus = 0
        #Check if some parameters are not plotable
        self.namsg = "INFO!\nOne or more parameters cannot be plotted. Analysis could be incomplete"
        self.nastatus = 0

        self.error = ""
        self.info = ""

    def get_confstatus(self):
        return self.confmsg
    def get_ftpstatus(self):
        return self.ftpmsg
    def get_downloadstatus(self):
        return self.downmsg
    def get_filestatus(self):
        return self.filemsg
    def get_locdbstatus(self):
        return self.localmsg
    def get_remdbstatus(self):
        return self.remotemsg

    def get_status(self):
        errorstatus = self.confstatus or self.localstatus or self.remotestatus or self.mainstatus
        warningstatus = self.ftpstatus or self.downstatus or self.filestatus
        datastatus = self.datastatus
        infostatus = self.nastatus
        self.set_errormsg()
        self.set_warningmsg()
        self.set_datamsg()
        self.set_infomsg()
        return errorstatus, warningstatus, datastatus, infostatus

    def set_errormsg(self):
        if self.confstatus == 1:
            self.error += self.confmsg + "\n"
        if self.mainstatus == 1:
            self.error += self.mainmsg + "\n"
        if self.localstatus == 1:
            self.error += self.localmsg + "\n"
        if self.remotestatus == 1:
            self.error += self.remotemsg + "\n"

    def set_warningmsg(self):
        if self.ftpstatus == 1:
            self.error += self.ftpmsg + "\n"
        if self.downstatus == 1:
            self.error += self.downmsg + "\n"
        if self.filestatus == 1:
            self.error += self.filemsg + "\n"

    def set_datamsg(self):
        if self.datastatus == 1:
            self.error += self.datamsg + "\n"

    def set_infomsg(self):
        if self.nastatus == 1:
            self.info += self.namsg + "\n"

def add_detector_layer(connection, det_type, det, row, col):
    if det_type == "DET":
        layer = db_query(connection, "hktm_detector_layer", "layer", "WHERE detid="+str(row)+str(col), "one")
        layer = layer.get("layer")
        det = det + "["+str(layer)+"]"
    return det

def concat_keys(dictionary):
    result = []
    for key, value in dictionary.items():
        if type(value) is dict:
            new_keys = concat_keys(value)
            for innerkey in new_keys:
                result.append(f'{key}.{innerkey}')
        else:
            result.append(key)
    return result

def connect_db(config):

    host=config['host']
    port=int(config['port'])
    socket=config['socket']
    user=config['user']
    password=config['password']
    dbname=config['dbname']

    # Connect to the database.
    connection = pymysql.connect(host=host, port = port,
                             user=user,
                             password=password,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    return connection

def db_query(connection, table, column, statement = "", res_type = "all"):
    allowed = ["one", "all"]
    if not res_type in allowed:
        raise TypeError("Invalid result type")

    with connection.cursor() as cursor:
        # SQL
        sql = "SELECT " +column+" FROM "+ table +" "+statement
        # Execute query.
        cursor.execute(sql)
        if res_type == "one":
            result = cursor.fetchone()
        elif res_type == "all":
            result = cursor.fetchall()

        return result  
  
def extract_runid(fname):
    x = fname.split("_")[0]
    if len(x) > 4:
        runid = int(int(x[3:])/10)
        n0 = 4-len(str(runid))
        s = ""
        for i in range(n0):
            s += "0"
        dir = s+str(runid)
    else:
        dir = str(fname.split("_")[3])      

    return dir
    
def flatten(mydict):
    new_dict = {}
    for key,value in mydict.items():
      if type(value) == dict and not key.startswith("Operation"):
        _dict = {'.'.join([key, _key]):_value for _key, _value in flatten(value).items()}
        new_dict.update(_dict)
      else:
        new_dict[key]=value
    return new_dict

def format_date(t):
    #CASE from YYYY-mm-dd HH:mm:ss to TIMESTAMP UTC
    #remove Z from utc time string
    if t[-1] == "Z":
        t=t[:-1]
    else:
        #remove +timezone from utc time string
        t = t.split("+")[0]
    try:    
        dt = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    except:
        dt = datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')       
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return timestamp  
  
def get_detector_layers(config):
    con = connect_db(config)
    layerdict = db_query(con, "hktm_detector_layer", "*", "", "all")
    layers = {}
    for i in range(len(layerdict)):
        detid = str(layerdict[i]['detid'])
        layerid = layerdict[i]['layer']
        layers.update({detid : layerid})
    con.close()
    return layers

def get_email(connection, user):
    sql = "SELECT email FROM members WHERE username = '"+user+"'"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        email = result['email']
    connection.commit()
    return email  

def get_localdb_info():
    confdata = repConfig().data
    conndata = confdata['local_db']
    return conndata  

def get_par_info(obj, conn, origin, system):
    infopar = []
    statement = "WHERE "
    if system == "QLA":
        listpar = []
        listsys = []
        for par in obj:
            listpar.append(par.split(".")[2])
            listsys.append(par.split(".")[0])
        for i in range(len(listpar)):
            if i == 0:
                statement += "(param = '"+listpar[i]+"' AND subsystem = '"+listsys[i]+"')"
            else:
                statement += " OR (param = '"+listpar[i]+"' AND subsystem = '"+listsys[i]+"')"
    else:
        listpar = list(obj[system][origin].keys())
        listpar = sorted(listpar)

        for i in range(len(listpar)):
            if i == 0:
                statement += "param = '"+listpar[i]+"'"
            else:
                statement += " OR param = '"+listpar[i]+"'"
    #get parameters info from DB
    infopar = db_query(conn, origin.lower()+"_"+system.lower()+"_params", "*", statement, "all")

    return infopar  
  
def get_param_list(repdata, conn, origin, system):
    try:
        infopar = get_par_info(repdata, conn, origin, system)
        tolist = []
        for item in infopar:
            tolist.append([item['param'], item['subsystem'], item['description']])
    except:
        infopar = []
        tolist = []

    return infopar, tolist  

def get_plf(plffile, params, fulllist):
    f2use = []
    try:
        #get info from PLF file to download only useful files
        plf = np.genfromtxt(plffile, dtype=str).transpose()
        par_list = plf[0]
        par_id = plf[1]

        allinplf =  all(elem in par_list for elem in params)
        if allinplf:
            useful = np.array([])
            if len(params)>0:
                for par in params:
                    el = np.where(par_list == par)
                    useful = np.append(useful, par_id[el])
                useful = np.unique(useful)
                #from fulllist get only useful files
                for i in range(len(fulllist)):
                    filename = fulllist[i]
                    curr_id = filename.split('_')[2]
                    if curr_id in useful:
                        f2use = f2use + [filename]
        else:
            f2use = fulllist
    except:
        f2use = fulllist

    return f2use  
  
def get_subs_files(flist, subs):
    out=[]
    for fname in flist:
        curr_sub = fname.split("_")[1]
        if curr_sub in subs:
            out.append(fname)
    return out

def get_subsystems(origin, system, connection):
    subs_dict = db_query(connection, origin+"_"+system, '*', res_type = "all")
    return subs_dict
  
def get_subsystems_from_file(origin, system, connection, t="required"):
    opmode = db_query(connection, "operation_modes", 'mode', "WHERE enable=1", "one")['mode']
    repo_json = get_json_data("../"+system+".conf")
    repo = repo_json[opmode][origin]["repository"]
    repo_json = get_json_data("../settings/forms.json")
    try:
        subs = repo_json[system][repo][origin][t]
    except Exception as e:
        subs = {}

    return subs

def get_json_data(path):
    # get repository data from json
    fileobj = open(path, "r")
    jsonstr = fileobj.read()
    fileobj.close()
    #change slashes
    jsonstr = jsonstr.replace("\\","/")
    #convert input string to json object
    data = json.loads(jsonstr)  
    return data  
  
def get_time(t=None):
    """Function to get current time as string and timestamp"""
    if t is None:
        t = utc_now()

    t_str = t.strftime("%Y-%m-%d %H:%M:%S") #current UTC datetime
    t_ts = format_date(t_str)
    return t_str, t_ts  
  
def join_by_date(D):
    X = np.array(D)
    masked = np.ma.masked_where(X == None, X, True).mask
    noneindex = np.where(np.all(masked,axis=0) == True)[0]
    X[masked] = 0
    x = []
    res = [sum(x) for x in zip(*X)]
    for i in noneindex:
        res[i] = -999

    return res  
  
def open_ftp_connection(source, conf):
    try:
        ftp = ftplib.FTP(conf.wgeta, conf.wgetu, conf.wgetp)
    except:
        ftp = "unable"
    return ftp

def pretty_time(t):
    """Change time format from seconds to a pretty visualization (H:m:s)"""
    return timedelta(seconds=t)  
  
def read_db_config(configfile):
    config={}
    try:
        f = open(configfile, "r")
        lines = f.readlines()
        lines = lines[1:-1]
        for row in lines:
            row = row.replace(";\n","")
            row = row.replace("\n","")
            row = row.replace('"','')
            row = row.replace(' ','')
            conn_name = row.split("=")[0][1:]
            conn_data = row.split("=")[1]
            config[conn_name] = conn_data
    finally:
        f.close()
    return config

def remove_nan_data(X,Y):
    final_y = []
    final_x = []
    toremove = []
    npX = np.array(X)
    npY = np.array(Y)
    toremove_x = np.where(npX == -999)[0]
    toremove_y = np.where(npY == -999)[0]
    toremove = np.append(toremove_x, toremove_y)
    final_x = np.delete(npX, toremove)
    final_y = np.delete(npY, toremove)

    return final_x, final_y  
  
def set_path(s):
    s = s.replace("/",sep).replace("\\",sep)
    if s[-1]==sep:
        path = s
    else:
        path = s+sep
    return path

def set_running_flag(connection, configfile, flag):
    sql = "UPDATE config_files SET isrunning = "+str(flag)+" WHERE filename = '"+configfile+"'"
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()  

def set_threadlimiter(n):
    global threadLimiter
    threadLimiter=threading.BoundedSemaphore(n)
    
def update_history(connection, user, op, input="NA", output="NA", config="NA"):
    #limit number of records 
    lr = db_query(connection, "history", "MIN(date_time), COUNT(*)", statement = "WHERE username = '"+user+"'", res_type = "one")  
    l = lr['COUNT(*)'];
    conf = get_json_data("../config.json")
    try:
        hist_num = conf["history"]
    except:
        hist_num = 100
    if l>=hist_num:
        #remove oldest record
        diff = l-hist_num+1
        sql = "DELETE FROM history WHERE username = '"+user+"' ORDER BY date_time ASC LIMIT "+str(diff)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    #date-time
    dt = utc_now()
    dt = datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    #build query
    sql="INSERT INTO history (date_time, username, operation, input, output, configuration) VALUES ('"+dt+"', '"+user+"', '"+op+"', '"+str(input)+"', '"+str(output)+"', '"+str(config)+"')"
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()  

    #update history text files
    user_str = "["+dt+"] : "+op
    glob_str = "["+dt+"]["+user+"] : "+op
    if output != "NA" or config != "NA":
        user_str += " --- "
        glob_str += " --- "
    outstr = []
    if output != "NA":
        outstr.append(str(output).replace("{","").replace("}",""))
    if config != "NA":
        outstr.append(str(config).replace("{","").replace("}",""))
    user_str += ",".join(outstr)
    glob_str += ",".join(outstr)
    with open("../users/"+user+"/history_"+user+".txt","a") as hf:
        hf.write(user_str+"\n")
    with open("../users/history.txt","a") as hf:
        hf.write(glob_str+"\n")

        
def update_local_files(connection, fname, source, subsystem, tstart, tstop, user):
  
    cols = "filename, data_source, date_start, username"
    values = "'"+fname+"', '"+source+"', '"+str(tstart)+"', '"+user+"'"

    if not subsystem is None:
        cols += ", subsystem"
        values += ", '"+subsystem+"'"
    if not tstop is None:
        cols += ", date_stop"
        values += ", '"+str(tstop)+"'"

    sql = "INSERT INTO local_files ("+cols+") VALUES ("+values+")"

    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()

def update_stored(connection, fname,user, date, ext, ftype, status="nd", filepath = "stored", tbl = "stored", comment="", pars = "{}", tstart = "NULL", tstop = "NULL", plot_id = None, source="NA"):
    
    if tstart != "NULL" and tstart != "undefined":
        exptstart = datetime.strptime(tstart, '%Y-%m-%d %H:%M:%S')
    else:
        exptstart = None
    if tstop != "NULL" and tstop != "undefined": 
        exptstop = datetime.strptime(tstop, '%Y-%m-%d %H:%M:%S')   
    else:
        exptstop = None
    if plot_id is None:  
        sql="INSERT INTO "+tbl+"_files (filename, filepath, username, date_exp, ext, filetype, status_exp, comment_exp, parinfo, sourcename, exp_tstart, exp_tstop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            # Create a new record
            if ftype == "report":
                final_file = fname
            else:
                final_file = fname+".pdf"
            cursor.execute(sql, (final_file, filepath,user,date,ext,ftype,status,comment, pars, source, exptstart, exptstop))
        connection.commit()        
    else:
        sql="INSERT INTO "+tbl+"_files (filename, filepath, username, date_exp, ext, filetype, status_exp, comment_exp, parinfo, sourcename, exp_tstart, exp_tstop, plot_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql, (fname+".pdf", filepath,user,date,ext,ftype,status,comment, pars, source, exptstart, exptstop, plot_id))
        connection.commit()

def utc_now():
    now = datetime.utcnow()
    return now
  
def units_to_label(label, struct, partags, connection, tbl):
  
    if len(struct) > 1:
        xl_splitted = label.split(".")
        parid = partags.index("par")
        xlname = xl_splitted[parid]
    else:
        xlname = label
    try:
        sql = "SELECT units FROM "+tbl+" WHERE param='"+xlname+"'"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            xl_units = cursor.fetchone()['units']
            if xl_units is not None:
                new_l = label +" ("+xl_units+")"
            else:
                new_l = label
    except:
        new_l = label
    return new_l  
  
def copylocal(f2use, conf, final_path, sysclass, userunid="False", usecase = "hktm"):
    """ Copy files from local repository to temporary directory

    Parameters      DA RISCRIVERE
    --------
        f2use: list
        list of files to copy
        orig_path: string
            path of local repository (from configuration)
        final_path: string
            path of destination (temporary path)
        usecase : string, optional
            experiment from which the call is done ("report", "plot"...), Default is "hktm"

    Returns
    -------
        file_ok: boolean
            True if all the files in the list f2use have been successfully copied, False otherwise

    """
   
    orig_path = conf.path.replace("/", sep)
    file_ok_arr = []
    fullpath = final_path+sep+sysclass.name
    if userunid:
        runid2dir = sysclass.runid_to_dir[conf.usecase]
    else:
        runid2dir = False      
    for f in f2use:
        if runid2dir:
            runid = extract_runid(f)
            fullname = orig_path + sep + runid + sep + f
        else:
            fullname = orig_path + sep + f
        if path.isfile(fullname):
            copyfile(fullname, fullpath+sep+f)
        #check if copy has been completed correctly
        if path.isfile(fullpath+sep+f) and filecmp.cmp(fullpath+sep+f, fullname):
            file_ok_arr.append(True)
        else:
            file_ok_arr.append(False)
    file_ok = all(file_ok_arr)
    return file_ok
  
def get_subsystems_from_json(source, usecase, key = "subsystem"):
    #get current operation mode
    conf = repConfig(source,usecase)
    reponame = conf.repclass[usecase].slug
    
    subs = get_json_data("../settings/forms.json")[source.lower()][reponame][usecase]["required"][key]["values"]    

    return subs
    
def create_temp_dir(usr_tmp_dir, source_slug):
    if (path.exists(usr_tmp_dir)==False):
        mkdir(usr_tmp_dir)
    sourcetmp = usr_tmp_dir+"/"+source_slug
    if (path.exists(sourcetmp)==False):
        mkdir(sourcetmp)    
    
def get_configured_origin(opmode, source):
    sys_json = get_json_data("../"+source+".conf")
    keys = [x.upper() for x in sys_json[opmode].keys()]

    return keys
    
def finddepth(dictA):
   if isinstance(dictA, dict):
      return 1 + (max(map(finddepth, dictA.values()))
         if dictA else 0)

   return 0    
    
def change_timestring(t):
    if t!="":
        date = t.replace("-",",").replace(":",",").replace(" ",",")
        date = date.split(".")[0]
    else:
        date = t
    return date