#!/usr/bin/python

"""
System Backup and Data Management Module.

This module provides functionalities for exporting, importing, and flushing 
system data and user configurations. It handles the creation and extraction 
of compressed archives (.tar.gz), database table dumps, restoration of public 
and private stored files, system settings, and SMTP configuration management.

@package AIDA
@module backup
"""
 
import cgi, cgitb 
cgitb.enable(display=0, logdir="cgi-logs")  # for troubleshooting
import json
import functions as util
#import pymysql
#import pymysql.cursors
from datetime import datetime
import zipfile
import glob,os
import tarfile
#import traceback
#import sys
import csv
import sys
from shutil import copyfile, rmtree
from distutils.dir_util import copy_tree
import db_io
import traceback
#maxInt = sys.maxsize
import smtplib

def maketar(zipf, d):
    """Add a file or directory to a tar archive.

    Parameters
    ----------
    zipf : tarfile.TarFile
        Target tar archive object.
    d : str
        File or directory path to add.

    Returns
    -------
    isdone : int
        1 if successfully added, 0 otherwise.
    """    
    isdone = 1
    try:
        zipf.add(d, arcname=d)
    except:
        isdone = 0
        
    return isdone

def addemptydir(zipf, d):
    """Add an empty directory entry to a tar archive.

    Parameters
    ----------
    zipf : tarfile.TarFile
        Target tar archive object.
    d : str
        Directory path to create in the archive.

    Returns
    -------
    isdone : int
        1 if successfully added, 0 otherwise.
    """
    isdone = 1
    try:    
        t = tarfile.TarInfo(d)
        t.type = tarfile.DIRTYPE
        t.mode = 0o777        
        zipf.addfile(t)
    except:
        isdone = 0
    return isdone        

def addtbldump(tbl, zipf,keep_tmp=True):
    """Export database table contents to SQL insert file and add it to archive.

    Parameters
    ----------
    tbl : str
        Database table name.
    zipf : tarfile.TarFile
        Target tar archive object.
    keep_tmp : bool, optional
        If False, exports only permanently stored records (tokeep > 0) (default is True).

    Returns
    -------
    isdone : int
        1 if table dump was successfully added, 0 otherwise.
    """
    isdone = 1  
    os.chdir("scripts")
    try:
        conn_conf = util.repConfig().data['local_db']
        conn = util.connect_db(conn_conf)
        stat=""
        if not keep_tmp:
            stat = " WHERE tokeep>0"
        result = util.db_query(conn, tbl, "*", stat, res_type="all")
        
        conn.close()
        hasid = 0
        if len(result) > 0:
            tblfile = '../tmp/'+tbl+'.csv'              
            colnames = list(result[0].keys())
            if colnames[0]=="id":
                hasid = 1
                colnames = colnames[1:]
            colnames = ",".join(colnames)   
            sql = "INSERT INTO "+tbl+" ("+colnames+") VALUES "

            for row in result:
                r = ""
                vals = []
                if hasid :
                    lvals = list(row.values())[1:]
                else:
                    lvals = list(row.values())
                for v in lvals:
                    #print(v,type(v))
                    if v is not None:
                        if isinstance(v,str):
                            r += "'"+v.replace('"',r'"')+"',"
                        elif isinstance(v, datetime):
                            r += "'"+str(v)+"',"
                        else:
                            r += str(v)+","
                    else:
                        r += "NULL,"
                r = r[:-1]
                sql += "("+r+"),"
            sql = sql[:-1]+";"              
            with open(tblfile, 'w', newline='') as csvfile:
                csvfile.write(sql)

            zipf.add(tblfile, arcname=tbl+'.tbl')
    
            os.remove(tblfile)                        

    except Exception as e:
        isdone = 0        
    os.chdir("..")
    return isdone    


def data_export(data):
    """Generate a compressed archive backup containing selected system data and tables.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Form parameters specifying components to include in export.

    Returns
    -------
    filename : str
        Generated archive filename.
    error : int
        Error status code (0: success, 1: total failure, 2: partial success).
    listerr : str
        Detailed newline-separated log of failed or skipped components.
    """
    error = 0
    now = datetime.utcnow()
    now = now.strftime("%Y%m%d%H%M%S")
    username = data["username"].value   
    file = "tmp/"+username+"_aida_backup_"+ now + ".tar.gz"  
    users = int(data["users"].value)
    reports = int(data["reports"].value)
    configs = int(data["repconf"].value)
    stored = int(data["stored"].value)    
    systems = int(data["systems"].value)
    history = int(data["hist"].value)
    smtp = int(data["smtp"].value)
    ml = int(data["ml"].value)

    os.chdir("..")

    tar = tarfile.open(file, "w:gz")
    
    listerr = ""    
    errflag = []    
    #init users dir
    udiradded = 0    
    if users or reports or configs or stored:
        udiradded = addemptydir(tar,"users")
        if not udiradded:
            errflag.append(udiradded)          
            listerr += "Users data\n"

    if udiradded:        
        #users
        if users:
            #save folders & files
            userdir = os.listdir("users")
            for ud in userdir:
                d="users/"+ud          
                if os.path.isdir(d) and ud not in ["stored","report","config", "ml"]:     #COPIARE ANCHE I FILE DA ML (NON ANCORA SISTEMATI) TODO             
                    addemptydir(tar,d) 
                    addemptydir(tar,d+"/tmp")        
                    maketar(tar, d+"/index.html")
                    if stored:
                        list_stored_err = []
                        
                        for el in os.listdir(d+"/stored"):
                            if not el.endswith('.fits'):
                                ustoredadd = maketar(tar, d+"/stored/"+el)
                                list_stored_err.append(ustoredadd)
                        err_sum = sum(list_stored_err)
                        if err_sum == 0:
                            listerr += "All private stored data for user: "+d+"\n"
                        elif err_sum != len(list_stored_err):
                            listerr += "Some private stored data for user: "+d+"\n"                        
                    
                    
                        # ustoredadd = maketar(tar, d+"/stored")
                        # errflag.append(ustoredadd)
                        # if not ustoredadd:
                            # listerr += "Private stored data for user: "+d+"\n"
                    else:
                        addemptydir(tar,d+"/stored")
                        maketar(tar, d+"/stored/index.html")
                        maketar(tar, d+"/stored/listfiles.html")
                #store user history txt
                if history:
                    maketar(tar,d+"/history_"+ud+".txt")
            #dump DB tables members and user files
            utblerr = addtbldump("members", tar)
            errflag.append(utblerr)
            if not utblerr:
                listerr += "Members table\n"
            #dump private stored files
            if stored:
                ustoredtbladd = addtbldump("user_files", tar)
                errflag.append(ustoredtbladd)                
                if not ustoredtbladd:
                    listerr += "Private stored data table\n"
            #store notification email
            try:
                # get repository data from json
                fileobj = open("config.json", "r")
                jsonstr = fileobj.read()
                fileobj.close()
                #change slashes
                jsonstr = jsonstr.replace("\\","/")
                #convert input string to json object
                confdata = json.loads(jsonstr)  
                #confdata = util.repConfig().get_config_data()[0]
                
                notiemail = confdata["admin_email"]
                notifile = 'notification.txt'
                with open(notifile,'w') as nf:
                    nf.write(notiemail)
                maketar(tar, notifile)
                os.remove('notification.txt')
                errflag.append(1)
            except Exception as e:
                errflag.append(0)
                listerr += "Notification Email\n"
                #listerr += str(e)
                
        
        #se reports --> cartella reports, tbl report_files
        if reports:
            list_err = []
            for el in os.listdir("users/report"):
                if os.path.isfile("users/report/"+el):
                    repadd = maketar(tar, "users/report/"+el)
                    list_err.append(repadd)
            err_sum = sum(list_err)
            if err_sum == 0:
                listerr += "All Report files\n"
            elif err_sum != len(list_err):
                listerr += "Some Report files\n"
            # repadd = maketar(tar, "users/report")
            # errflag.append(repadd)                
            # if not repadd:
                # listerr += "Report files\n"

            #dump DB table
            reptblerr = addtbldump("report_files", tar)
            errflag.append(reptblerr)                
            if not reptblerr:
                listerr += "Report table\n"
    
        #se configs --> cartella config, tbl config_files
        if configs:
            confadd = maketar(tar, "users/config")
            errflag.append(confadd)                
            if not confadd:
                listerr += "Report configuration files\n"
#           isdone = dir2zip(file, "users/config")
            #dump DB table
            conftblerr = addtbldump("config_files", tar)
            errflag.append(conftblerr)                
            if not conftblerr:
                listerr += "Report config table\n"
    
    
        #se stored --> cartella stored, tbl stored_files, tbl stored_plots (tokeep=1)
        if stored:
            isdone = maketar(tar, "users/stored")
#           isdone = dir2zip(file, "users/stored")
            storedtblerr = addtbldump("stored_files", tar)
            errflag.append(storedtblerr)                
            if not storedtblerr:
                listerr += "Public stored data table\n"
            plotstblerr = addtbldump("stored_plots", tar, keep_tmp=False)
            errflag.append(plotstblerr)                
            if not plotstblerr:
                listerr += "Stored plots data table\n"

        #se ml --> cartella ml, tbl stored_ml
        if ml:
            confadd = maketar(tar, "users/ml")
            errflag.append(confadd)                
            if not confadd:
                listerr += "ML experiments files\n"
            #dump DB table
            mltblerr = addtbldump("stored_ml", tar)
            errflag.append(mltblerr)                
            if not mltblerr:
                listerr += "ML experiments table\n"
    
    #se history --> tbl history
    if history:
        histtblerr = addtbldump("history", tar)
        errflag.append(histtblerr)                
        if not histtblerr:
            listerr += "History table\n"
        maketar(tar,"users/history.txt")
    
    #systems settings
    if systems:
        for fconf in glob.glob("*.conf"):
            fconfadd = maketar(tar, fconf)
            errflag.append(fconfadd)                
            if not fconfadd:
                listerr += "Settings file : "+fconf+"\n"
        setadd = maketar(tar, "settings")
        errflag.append(setadd)                
        if not setadd:
            listerr += "Settings folder\n"
#       isdone = dir2zip(file, "settings")
    
    #smtp    
    if smtp:
        smtpadd = maketar(tar,"smtp.json")
#       isdone = file2zip(file,"smtp.json")      
        errflag.append(smtpadd)                
        if not smtpadd:
            listerr += "SMTP settings\n"

    #export config.json
    mainconf = maketar(tar,"config.json")
    errflag.append(mainconf)                
    if not mainconf:
        listerr += "General settings\n"    


    #export running_reports table
    runerr = addtbldump("running_reports", tar)
    errflag.append(runerr)
    if not runerr:
        listerr += "Running Reports table\n"



    if all(errflag):
        error = 0
    elif not any(errflag):
        error = 1
        #remove tar file if exists
        if os.path.isfile(file):
            os.remove(file)          
    else :
        error = 2
    tar.close()
    os.chdir("scripts")       
    return file.split("/")[-1], error, listerr


def data_import(data):
    """Import system data, configurations, and database records from an extracted archive.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Input parameters containing uploaded backup details and flags.

    Returns
    -------
    filename : str
        Name of the imported file archive.
    error : int
        Error status code (0: success, 1: total failure, 2: partial error).
    listout : str
        Detailed log of error messages or processed items.
    """
    error = 0
    listout = ""
    username = data["username"].value   
    users = int(data["users"].value)
    reports = int(data["reports"].value)
    configs = int(data["repconf"].value)
    stored = int(data["stored"].value)    
    systems = int(data["systems"].value)
    history = int(data["hist"].value)
    smtp = int(data["smtp"].value)
    ml = int(data["ml"].value)
    filename = data["file"].value
    datapath = "../tmp/"+os.path.splitext(filename)[0]

    errorlist = []
    connconfig = util.repConfig().data['local_db']
     
            
    uerr = None
    if users:
        uerr = copy_el(datapath+"/users", "../users")
        if not uerr:
            #import members table
            uerr = import_tbl(["members"], datapath)     
        
        if uerr:
            errorlist.append(1)
            listout += "Users Data\n"        
        
        #set notification email
        try:
            with open(datapath+"/notification.txt","r") as nf:
                notif = nf.readline()
            confdata = util.repConfig().get_config_data()[0]
            confdata["admin_email"] = notif
            with open('../config.json', 'w') as f:
                json.dump(confdata, f, indent="\t")
            
        except Exception as e:
            listout += "Notification Email\n"
        

    if reports:
        reperr = 0
        if uerr != 0:
            reperr = copy_el(datapath+"/users/report", "../users/report")
        if not reperr:
            #import report table
            reperr = import_tbl(["report_files"], datapath)

        if reperr:
            errorlist.append(1)
            listout += "Report files\n"
        #clean from failed reports directories
        for el in os.listdir("../users/report"):
            if os.path.isdir("../users/report/"+el):
                try:
                    rmtree("../users/report/"+el)
                except:
                    pass
            
    if configs:
        conferr = 0
        if uerr != 0:
            conferr = copy_el(datapath+"/users/config", "../users/config")
        if not conferr:
            #import config table
            conferr = import_tbl(['config_files'], datapath)
        if conferr:
            errorlist.append(1)
            listout += "Report configuration files\n"
        else:
            #set isrunning = 0 for each config_files record
            sql = "UPDATE config_files SET isrunning = 0"
            #connconfig = util.repConfig().data['local_db']
            dbio = db_io.dbIO(connconfig)
            dbio._commit_query(sql)
    
    if stored:
        private = 1
        sterr = 0
        if uerr != 0:
            private = 0
            sterr = copy_el(datapath+"/users/stored", "../users/stored")
        if not sterr:
            #import stored table
            if uerr == 0:
                liststored = ["stored_files","stored_plots","user_files"]
            else:
                liststored = ["stored_files","stored_plots"]              
            sterr = import_tbl(liststored, datapath)
        if sterr:
            errorlist.append(1)
            listout += "Stored files\n"
            
    #preserve webapp.json
    webapperr = copy_el("../settings/webapp.json", "../tmp/webapp.json")   

    if systems:
        syserr = 0
        #copy .conf files
        files = os.listdir(datapath)
        for file in files:
            if os.path.splitext(file)[1] == ".conf":
                currerr = copy_el(datapath+"/"+file, "../"+file)
                if currerr == 1:
                    syserr = 1


        #copy elements in "settings" folder
        # seterr = copy_el(datapath+"/settings", "../settings")
        settings_to_copy = ["ingestion.json"]
        seterr = 0
        for el in os.listdir(datapath+"/settings"):
            if el in settings_to_copy:
                seterr += copy_el(datapath+"/settings/"+el, "../settings/"+el)
                    
        #if syserr or seterr:
        if syserr or seterr>0:
            errorlist.append(1)
            listout += "Systems settings\n"
            
    #copy webapp.json
    if(webapperr==0):
        webapperr = copy_el("../tmp/webapp.json","../settings/webapp.json")
        # #remove webapp.json backup
        # os.remove("../tmp/webapp.json") 
            
    if history:
        herr = 0
        #import config table
        herr = import_tbl(['history'], datapath)

        if herr:
            errorlist.append(1)
            listout += "History\n"
        #import history.txt
        if os.path.isfile(datapath+"/users/history.txt"):
            copy_el(datapath+"/users/history.txt", "../users/history.txt")        
            
    else:
        if os.path.isfile("../users/history.txt"):
            os.unlink("../users/history.txt")
        #remove all users history files
        userfiles = os.listdir("../users/")
        for el in userfiles:
            if(os.path.isdir("../users/"+el)):
                if(os.path.isfile("../users/"+el+"/history_"+el+".txt")):
                    os.unlink("../users/"+el+"/history_"+el+".txt")
        
        
    if smtp:
#       smtperr = replace_file(datapath+"/smtp.json", "../smtp.json")
        smtperr = copy_el(datapath+"/smtp.json", "../smtp.json")
        if smtperr:
            errorlist.append(1)
            listout += "SMTP settings\n"

    if ml:
        mlerr = 0
        if uerr != 0:
            mlerr = copy_el(datapath+"/users/ml", "../users/ml")
        if not mlerr:
            #import ml table
            mlerr = import_tbl(['stored_ml'], datapath)
        if mlerr:
            errorlist.append(1)
            listout += "ML Experiment files\n"

    # errsum = sum(errorlist)
    # if errsum == 7:
        # error = 1
    # elif errsum > 0 and errsum < 7:
        # error = 2

    if os.path.isfile(datapath+"/config.json"):
        mainerr = copy_el(datapath+"/config.json", "../config.json")
    else:
        errorlist.append(1)
        listout += "General settings\n"

        
    errsum = sum(errorlist)
    if errsum == 8:
        error = 1
    elif errsum > 0 and errsum < 8:
        error = 2        
        

    if "Notification Email\n" in listout:
        error = 2
#   if error == 0:
#       #remove tmp files
#       os.remove(datapath+".gz")
#       rmtree(datapath)
        
#   if not users:
#       error = 3


    #Import running_reports table 
    # if users or reports or configs:           DECIDERE SE USARE LA CONDIZIONE O MENO
    if os.path.isfile(datapath+"/running_reports.tbl"):
        runerr = 0
        runerr = import_tbl(["running_reports"], datapath)
        if runerr:
            errorlist.append(1)
            listout += "Running Reports table\n"
        else:
            #get all running reports
            dbio = db_io.dbIO(connconfig)
            runnings = dbio.get_running_reports(keep_open=True)        
            for rep in runnings:
                cfile = rep["config_file"]
                if rep["start_date"] is not None:
                    tstart = rep["start_date"].strftime("%m-%d-%Y %H:%M:%S")
                else:
                    tstart = None
                exp_status = float(rep["exp_status"])
                #put running and scheduled to pause
                isrunning = 3
                if exp_status > 0 or exp_status == -102.0:
                    exp_status = -100.0
                elif exp_status == -101.0:
                    isrunning = 4
                #update running reports
                sql = "UPDATE running_reports SET exp_status="+str(exp_status)+" WHERE config_file='"+cfile+"'"
                dbio._commit_query(sql, keep_open=True)
                
                sql = "UPDATE config_files SET isrunning="+str(isrunning)+" WHERE filename='"+cfile+"'"
                dbio._commit_query(sql, keep_open=True)            

            
            dbio.close()
    
    return filename, error, listout



def copy_el(src, dst):
    """Copy a file or directory tree to a target destination.

    Parameters
    ----------
    src : str
        Source file or directory path.
    dst : str
        Destination path.

    Returns
    -------
    error : int
        0 if successful, 1 on failure.
    """
    error = 0
    try:
        if os.path.isfile(src):      
            copyfile(src, dst)
        elif os.path.isdir(src):
            copy_tree(src, dst)
        
    except:
        error = 1
    return error

def import_tbl(tbl_list, datapath) :
    """Import SQL insert statements from dumped table files into database.

    Parameters
    ----------
    tbl_list : list of str
        List of table names to import.
    datapath : str
        Directory path where `.tbl` files are stored.

    Returns
    -------
    error : int
        0 if all tables imported successfully, 1 if any import failed.
    """
    error = 0  
    for tbl in tbl_list:
        if error == 0:
            #arg=tbl+"_test"
            arg=tbl
            fname = datapath+"/"+tbl+".tbl"            
            try:            
                #import csv from tbl file
                if os.path.isfile(fname):
                    connconfig = util.repConfig().data['local_db']
#                   connection = util.connect_db(connconfig)                    
                    with open(fname,"r") as f:
                        sql = f.readline()
                        dbio = db_io.dbIO(connconfig)
                        dbio._commit_query(sql)
                else:
                    error = 1

            except Exception as e:
                # with open("err.log","w") as f:
                    # f.write(str(e)+"\n")
                    # f.write(str(tbl)+"\n")
                    # f.write(str(tbl_list)+"\n")
                    # f.write(str(connconfig))
                error = 1
    return error
 
    
def replace_file(src, dst):
    """Replace target destination file with source file.

    Parameters
    ----------
    src : str
        Source file path.
    dst : str
        Destination file path.

    Returns
    -------
    error : int
        0 if successful, 1 on failure.
    """
    error = 0
    try:
        copyfile(src, dst)
    except:
        error = 1
    return error

def copydir(src, dst):
    """Copy directory structure recursively to destination.

    Parameters
    ----------
    src : str
        Source directory path.
    dst : str
        Destination directory path.

    Returns
    -------
    error : int
        0 if successful, 1 on failure.
    """
    error = 0
    try:
        copy_tree(src, dst)
    except:
        error = 1
    return error 

def check_exist(files=[], dirs=[], ext=""):
    """Check existence of specific files, directories, or extension matches.

    Parameters
    ----------
    files : list of str, optional
        List of file paths to check.
    dirs : list of str, optional
        List of directory paths to check.
    ext : str, optional
        File extension to check for matching files.

    Returns
    -------
    out : str
        "block" if all requested checks pass, otherwise "none".
    """

    if len(files) > 0:
        chkfile = False
        for elem in files:
            if os.path.isfile(elem):
                chkfile = True
    else:
        chkfile = True
        
    if len(dirs) > 0:
        chkdir = False
        for elem in dirs:
            if os.path.isdir(elem):
                chkdir = True
    else:
        chkdir = True
        
    if ext != "":
        chkext = False  
        if len(glob.glob("*."+ext)) > 0:
            chkext = True
    else:
        chkext = True
        
        
    if chkfile and chkdir and chkext:
        out = "block"
    else:
        out = "none"
        
    return out
        
    
def upload(data):
    """Decompress uploaded tar.gz backup file and check its constituent contents.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Contains uploaded file details and user details.

    Returns
    -------
    file : str
        Path to processed archive file.
    error : int
        0 on success, 1 on decompression failure, 2 if user data check fails.
    listout : list or str
        List of component status strings or error message.
    """
    error = 0
    user = data["user"].value
    file = "../tmp/"+data["filename"].value
    #try to decompress file
    try:
        listout = []    
        tar = tarfile.open(file, "r:gz")
        tar.extractall(path=os.path.splitext(file)[0])
        tar.close()
        #change working directory
        os.chdir(os.path.splitext(file)[0])

        #check users
        listout.append(check_exist(["members.tbl"], ["users"]))
        #check reports
        listout.append(check_exist(["report_files.tbl"], ["users/report"]))
        #check report config files
        listout.append(check_exist(["config_files.tbl"], ["users/config"]))
        #check stored
        listout.append(check_exist(["stored_plots.tbl","stored_files.tbl"], ["users/stored"]))
        #check systems
        listout.append(check_exist([], ["settings"], "conf"))
        #check history
        listout.append(check_exist(["history.tbl"], []))
        #check smtp
        listout.append(check_exist(["smtp.json"], []))

        if check_exist(["members.tbl"], ["users"]) == "none":
            error = 2
    except:
        error = 1
        listout = "ERROR! Uploaded file is not a valid tar.gz\n"


    return file, error, listout

def store_smtp(data):
    """Save SMTP server settings to configuration file and test connection.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Contains host, port, user, and password fields.

    Returns
    -------
    error : int
        0 on success, 1 on write error, 2 on SMTP connection failure.
    """
    error = 0
    host = data['host'].value
    port = data['port'].value
    user = data['user'].value
    try:
        pwd = data['pwd'].value
    except:
        pwd = ""
    
    out = {"host" : host, "port" : port, "user" : user, "password" : pwd}
    
    try:
        with open('../smtp.json', 'w') as f:
            json.dump(out, f, indent="\t")
    except:
        error = 1

    #check smtp connection
    if error == 0:
        try:
            server = smtplib.SMTP(host, port)
            server.ehlo()
            server.starttls()
            if pwd != "":        
                server.login(user, pwd)
            server.quit()
        except:
            error = 2

    return error

def flush_data(isfull = True, remove_stored = False, keep_config = False):
    """Purge database tables, user folders, logs, and temporary files.

    Parameters
    ----------
    isfull : bool, optional
        If True, purges all user accounts and default settings (default is True).
    remove_stored : bool, optional
        If True, removes stored files in user directories (default is False).
    keep_config : bool, optional
        If True, preserves report configuration files (default is False).
    """
    #flush db
    #tbl2del = ["history", "report_files", "stored_files", "stored_plots", "user_files"]
    tbl2del = ["history", "report_files", "stored_files", "stored_plots", "user_files", "running_reports","stored_ml"]
    dir2purge = ["report","stored","ml"]
    f2skip=["index.html","listfiles.html","analyze_benchmark.py"]    
    if isfull:
        tbl2del.append("members")
    if not keep_config:
        tbl2del.append("config_files")
        dir2purge.append("config")
        
    connconfig = util.repConfig().data['local_db']
    dbio = db_io.dbIO(connconfig)
    for tbl in tbl2del:
        #fake tbl
        #tbl = tbl+"_test"
        sql = "TRUNCATE TABLE "+tbl
        dbio._commit_query(sql) 
    
    
    #flush folders & files
    #stored files folders
    for d in dir2purge:
        workdir = "../users/"+d
        for el in os.listdir(workdir):
            if el not in f2skip:
                if os.path.isdir(workdir+"/"+el):
                    rmtree(workdir+"/"+el)
                else:
                    os.remove(workdir+"/"+el)

    if isfull:
        #users folders
        for el in os.listdir("../users"):
                if el not in dir2purge:
                    try:
                        rmtree("../users/"+el)
                    except:
                        pass    
        #restore default settings
        for el in os.listdir("../defaults"):
            copy_el("../defaults/"+el, "../"+el)
    else:
        #users folders
        for el in os.listdir("../users"):
            dir2purge.append("config")
            if el not in dir2purge:       
                try:
                    curr_dir = "../users/"+el
                    for f in os.listdir(curr_dir):
                            if os.path.isfile(curr_dir+"/"+f) or os.path.islink(curr_dir+"/"+f):
                               if remove_stored and f not in f2skip:
                                    os.unlink(curr_dir+"/"+f)
                            elif f=="tmp":
                                #clean tmp dir
                                for tmpf in os.listdir(curr_dir+"/tmp"):
                                    if tmpf not in f2skip:
                                        os.unlink(curr_dir+"/tmp/"+tmpf)
                            elif f=="stored":
                                #clean stored dir
                                for sf in os.listdir(curr_dir+"/stored"):
                                    if remove_stored and sf not in f2skip:
                                        os.unlink(curr_dir+"/stored/"+sf)
                    #restore history_<user>.txt
                    #open("../users/"+el+"/history_"+el+".txt", 'w').close()                    
                except:
                    pass
        #remove "waiting" running reports
        sql = "DELETE FROM running_reports WHERE (exp_status=-99.0 AND pid<0)"
        dbio._commit_query(sql)
    #restore history.txt
    #open("../users/history.txt", 'w').close()
    #remove existing history.txt
    if os.path.isfile("../users/history.txt"):
        os.unlink("../users/history.txt")

    #flush cgi-logs, profiling and logs directories
    aux_dir = ["cgi-logs", "profiling", "logs"]
    
    for d in aux_dir:
        for el in os.listdir(d):
            if el not in f2skip:
                if os.path.isdir(d+"/"+el):
                    rmtree(d+"/"+el)
                else:
                    os.remove(d+"/"+el)        

        
        
def clean_install():
    """Clean temporary directory and log system installation readiness status."""
    #clean tmp dir
    for el in os.listdir("../tmp"):
        if el != "index.html":
            if os.path.isfile("../tmp/"+el):      
                os.remove("../tmp/"+el)
            elif os.path.isdir("../tmp/"+el):
                rmtree("../tmp/"+el)
    #remove .install
    with open("../users/ready.log","w") as f:
        f.write("OK")

def set_super_email(data):
    """Update system administrator notification email address in global configuration.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Contains the new admin email value.

    Returns
    -------
    error : int
        0 on success, 1 on configuration update failure.
    """
    error = 0
    email = data['email'].value
    try:
        confdata = util.repConfig().get_config_data()[0]
        confdata["admin_email"] = email
        with open('../config.json', 'w') as f:
            json.dump(confdata, f, indent="\t")     
    except:
        error = 1

    return error

def check_connection():
    """Verify local database connection status.

    Returns
    -------
    err : int
        0 if connection succeeded, non-zero error code otherwise.
    """
    #get IODA DB connection data from config.json
    connconfig = util.repConfig().data['local_db']
    dbio = db_io.dbIO(connconfig)
    err, conn = dbio.check_connection(connconfig)
    return err

def main(data):
    """CGI main entry point for backup management operations.

    Parameters
    ----------
    data : cgi.FieldStorage
        HTTP request payload containing action parameter and relevant settings.
    """
    error = 0
    file = ""
    listerr = ""    
    action = data['action'].value
    if action == "export":
        file, error, listerr = data_export(data)
    elif action == "import":

        flush_data()
    
        file, error, listerr = data_import(data)
        #remove .install file
#       if error != 1 and error != 3:
#           if os.path.isfile("../.install"):
#               os.remove("../.install")        #se non importa tutto cosa succede???? Se mancano gli users deve creare primo utente
            # vedi se c'è nel backup USERS
                #se c'è 
                #   controlla che non c'è errore
                #   se errore
                #       ritorna 3
                #else 
                #   ritorna error=3         
    elif action == "upload" : 
        file, error, listerr = upload(data)
    elif action == "savesmtp":
        error = store_smtp(data)
    elif action == "flush":
        error = check_connection()
        if error == 0:
            flush_data()

    elif action == "clean":
        clean_install()
    elif action == "notification":
        error = set_super_email(data)


    print(json.JSONEncoder().encode({'error' : error, 'file' : file, "msg" : listerr}))












if __name__ == "__main__":
    print("Content-Type: application/json")
    print()

    #the cgi library gets vars from html
    data = cgi.FieldStorage()


    main(data)