#!/usr/bin/python

"""
Image Analysis Execution Engine.

This module handles image processing operations on FITS images, including 
image subtraction, stacking, statistical calculation, database tracking, 
and email notification dispatching.

@package AIDA
@module run_img_analysis
"""

import cgi, cgitb 
cgitb.enable()  # for troubleshooting
from    os              import system, getpid, path, sep, mkdir, remove,sep
import datetime
import sys
import functions as util
from datetime import datetime
from shutil import copyfile, rmtree
import  threading
import repos
import numpy as np
import iotstats
import db_io
from send_mail import Email
from astropy.io import fits

global e
e = util.statusMsg()


def subtract_images(img1,img2,outputUrl, imagesAlligned=True):
    """Subtract pixel data of the second FITS image from the first and save to file.

    Parameters
    ----------
    img1 : str
        File path to the primary FITS image.
    img2 : str
        File path to the FITS image to subtract.
    outputUrl : str
        Output file path for the subtracted FITS image.
    imagesAlligned : bool, optional
        Flag indicating if input images are pre-aligned (default is True).
    """
    fits1=fits.open(img1)
    fits2=fits.open(img2)
    dastaStruct=fits1.info(False)
    for ind in range(1,len(dastaStruct)):
        fits1[ind].data=fits1[ind].data-fits2[ind].data
    fits2.close()
    fits1.writeto(outputUrl, overwrite=True)

def stack_images(imgList,outputUrl, imagesAlligned=True):
    """Stack and average pixel data across a sequence of FITS images.

    Parameters
    ----------
    imgList : list of str
        List of file paths to FITS images to stack.
    outputUrl : str
        Output file path for the stacked FITS image.
    imagesAlligned : bool, optional
        Flag indicating if input images are pre-aligned (default is True).
    """
    fits1=fits.open(imgList[0])
    dastaStruct=fits1.info(False)
    for img in range(1,len(imgList)):
        fits2=fits.open(imgList[img])
        for ind in range(1,len(dastaStruct)):
            fits1[ind].data=fits1[ind].data+fits2[ind].data
            if img==len(imgList)-1:
                fits1[ind].data=fits1[ind].data/len(imgList)
        fits2.close()
    fits1.writeto(outputUrl, overwrite=True)
    
def stats_image(img1, imagesAlligned=True):
    """Compute statistical metrics across FITS image data extensions.

    Parameters
    ----------
    img1 : str
        File path to the target FITS image.
    imagesAlligned : bool, optional
        Flag indicating if image is aligned (default is True).

    Returns
    -------
    dictStat : dict
        Dictionary containing calculated statistical metrics per HDU extension and overall.
    """
    fits1=fits.open(img1)
    dastaStruct=fits1.info(False)
    dictStat={}
    allinone=np.zeros(0)
    #for ind in range(1,len(dastaStruct)):
    for ind in range(1,3):
        dictStat[dastaStruct[ind][1]]=iotstats.calculateGlobal(fits1[ind].data)
        allinone=np.append(allinone,fits1[ind].data)
    dictStat["overall"]=(iotstats.calculateGlobal(allinone))    
    return dictStat  

def stat_to_db(pdata, usecase, plot, username, labels, stats, stat_res, operation, ts, te, tokeep=0):
    """Insert temporary image analysis plot record into the database.

    Parameters
    ----------
    pdata : dict or str
        Image analysis data payload.
    usecase : str
        Data origin classification string.
    plot : str
        Plot or analysis operation type name.
    username : str
        Username initiating the analysis.
    labels : list of str
        List of parameter or file labels.
    stats : str
        Statistical mode identifier.
    stat_res : dict or str
        Statistical calculation results dictionary or JSON string.
    operation : str
        Name of performed operation.
    ts : str
        Data range start datetime string.
    te : str
        Data range end datetime string.
    tokeep : int, optional
        Persistence flag (0 for temporary, 1 for permanent, default is 0).

    Returns
    -------
    plotid : int or None
        Inserted database record ID, or None if insertion failed.
    """
    #connect to DB
    connconf = util.repConfig().data['local_db']
    dbio = db_io.dbIO(connconf)
    plotid = dbio.insert_temp_plot(pdata, usecase, plot, username, labels, stats, stat_res, operation, ts, te, tokeep)
        
    return plotid   

def do_calculation(indata, operation, user, filepath,dt):
    """Perform requested image processing operation and calculate image statistics.

    Parameters
    ----------
    indata : list of str
        List of input image file paths.
    operation : str
        Image operation identifier name (e.g. 'difference').
    user : str
        Username requesting the calculation.
    filepath : str
        Target output directory path.
    dt : str
        Timestamp string for output naming.

    Returns
    -------
    result : dict
        Calculated image statistics dictionary.
    """
    result = {}
    # Calculate statistics
    try:
        if operation == "difference":
            fileA = indata[0]
            fileB = indata[1]
            outputUrl = filepath+sep+"difference_"+dt.replace(" ","T").replace(":","")+".fits"
            subtract_images(fileA,fileB, outputUrl=outputUrl)
            result=stats_image(outputUrl)

    except:
        e.datastatus = 1
        e.datamsg = "ERROR! Impossible to calculate statistics for selected images. Please contact AIDA team."

    return result

class getFiles(threading.Thread):
    """Worker thread for multi-threaded image file downloading or copying.

    Parameters
    ----------
    ThreadID : int
        Thread numerical identifier.
    name : str
        Thread name identifier.
    params : list
        Parameter bundle containing configuration, source, target temporary directory,
        filenames list, copy queue list, and username.

    Attributes
    ----------
    name : str
        Thread name.
    id : int
        Thread ID.
    conf : repConfig
        Repository configuration object.
    source : str
        Target system source name.
    tmpdir : str
        Temporary working directory path.
    filenames : list of str
        Files assigned to this worker thread.
    tocopy : list of str
        Local files list to copy instead of downloading.
    user : str
        Username.
    repo : object
        Instantiated repository handler object.
    """
    def __init__(self, ThreadID, name, params):
        threading.Thread.__init__(self)
        self.name=name
        self.id=ThreadID
        self.conf = params[0]
        self.source = params[1]
        self.tmpdir = params[2]
        self.filenames = params[3]
        self.tocopy = params[4]
        self.user = params[5]
        self.repo = self.conf.repclass['image']        
        
    def run(self):
        """Execute multi-threaded file copy or remote FTP download operations."""
        try:
            if self.repo.method=="ftp":

                #open ftp connection
                ftp = util.open_ftp_connection(self.source, self.conf)

            else:
                ftp = ""

            for name in self.filenames:
                fullname = "../users/"+self.user+"/tmp/"+self.source.lower()+"/"+name
                file_ok=True

                if fullname in self.tocopy:
                    try:
                        copyfile(fullname, self.tmpdir+sep+name)
                    except:
                        file_ok = False
                else:
                    file_ok = self.repo.download_file(name, self.conf, ftp, self.tmpdir, self.source.lower(),False)
        except Exception as e:
            print(str(e))
        finally:
            if ftp != "" and ftp != "unable":
                ftp.close()            
        
def main(data):
    """CGI main entry point for running image processing and analysis jobs.

    Parameters
    ----------
    data : cgi.FieldStorage
        HTTP POST request payload containing user, operation type, source system,
        file list, and application URL.
    """
    user = data['user'].value
    op = data['op'].value
    source = data['source'].value
    listfiles = data.getlist('files[]')        
    
    #create experiment dir
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)
    filepath = "../users/report/img_"+user+"_"+str(ts)
    if not path.isdir(filepath):    
        mkdir(filepath)
    tocopy = []
    for f in listfiles:
        fullname = "../users/"+user+"/tmp/"+source.lower()+"/"+f
        if path.isfile(fullname) and not path.isfile(filepath+sep+f):    
            tocopy.append(fullname)

    #get config info
    conf = util.repConfig(source, 'image')
    #get files
    nproc = min(conf.sourcedata['nprocs'], len(listfiles))
    #split lists of files for multi-threading
    filesarray = np.array_split(np.array(listfiles), nproc)
    threads = []
    #run multi-threading code to get files
    for thread_id in range(nproc):
        params = [conf, source, filepath, filesarray[thread_id], tocopy, user]
        session = getFiles(thread_id, "Thread_"+str(thread_id), params)
        threads = threads+[session]
        threads[thread_id].start()
    for th in threads:
        th.join()
    #make operations
    files2db = ",".join(listfiles)  
    path2save = "../users/"+user+"/stored"
    if op == "difference":
        file_A = filepath+sep+listfiles[0]
        file_B = filepath+sep+listfiles[1]
        if path.isfile(file_A) and path.isfile(file_B):
            files2db +=","+path2save+sep+"difference_"+str(dt).replace(" ","T").replace(":","")+".fits"
        else:
            e.remotemsg = "ERROR!\nOne or more files cannot be downloaded. Analysis can not be performed"
            e.remotestatus = 1            
        flist = [file_A, file_B]
        hist_name = "Statistics on Difference Image"
    else:
        flist = []
        hist_name = ""
                   
    result = {}    
    if e.remotestatus == 0:
        result = do_calculation(flist, op, user, path2save, str(dt))
    labels = list(result.keys())
    
    status = e.get_status()        
    result.update({"errstatus" : status[0]})
    result.update({"warningstatus" : status[1]})
    result.update({"datastatus" : status[2]})
    result.update({"infostatus" : status[3]})
    result.update({"msg" : e.error})
    result.update({"infomsg" : e.info})
    #Replace \n with _RETCHAR_ to avoid errors when parsing in result page
    msg = result['msg']
    msg = msg.replace("\n", "_RETCHAR_")
    result.update({"msg" : msg})
    
    msg = result['infomsg']
    msg = msg.replace("\n", "_RETCHAR_")		
    result.update({"infomsg" : msg})	   
    #store results into DB
    connconf = conf.data['local_db']
    dbio = db_io.dbIO(connconf)
    plotid = dbio.insert_temp_plot(result, "image analysis", op, user, labels, source, files2db, "Image Analysis", "NULL", "NULL", 0)    
    #copy or move downloaded files to tmp
    #TODO
    
    rmtree(filepath)

    connconfig = conf.data['local_db']
    connection = util.connect_db(connconfig) 
    # #update history
    if plotid is not None:
        try:
            res = {"Source" : source}
            for i,f in enumerate(flist):
                fname = f.split("/")[-1]
                res.update({'File '+str(i+1) : fname})  
            util.update_history(connection, user, hist_name, input="NA", output=str(res).replace("'","\""), config="NA")  
        except Exception as err:
            pass

    #send email
    mailconfig = Email("../smtp.json")  
    #get user email 
    email = util.get_email(connection, user)
    connection.close()
    #set email text
    url = data['iodaurl'].value
    maildata = [op, source, dt, result, url, str(listfiles)]

    if plotid is not None:
        subject = "New Image Analysis generated"       
        text = mailconfig.ok_img_text(maildata, plotid, source)
    else:
        subject = "ATTENTION: Failed Image Analysis generation"        
        text = mailconfig.error_img_text(maildata, "Impossible to store data in local DB")
    #send mail  
    fromuser = "AIDA"
    to = email
    msg = mailconfig.set_message(subject,fromuser,to,text)
    mailconfig.send_mail(msg)

if __name__ == "__main__":
    print("Content-Type: application/json")
    print()

    data = cgi.FieldStorage()
    main(data)
      
    