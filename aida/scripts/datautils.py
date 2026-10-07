#!/usr/bin/python

"""
Data Processing and Multi-threading Utilities.

This module provides helper classes and functions for parsing request input 
parameters, managing concurrent multi-threaded file downloads and data parsing, 
and constructing structured dataset payloads for online plot rendering in AIDA.

@package AIDA
@module datautils
"""

import numpy as np
import os
import threading
import functions as util

def get_base_data(data):
    """Extract base plotting parameters and formatted date limits from request data.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Input parameters payload containing source, plot type, parameter count, and time bounds.

    Returns
    -------
    source : str
        Data source identifier.
    plot : str
        Plot type string.
    n_ypar : int
        Number of Y parameters.
    tstartdb : str
        Formatted start datetime string for database queries.
    tenddb : str
        Formatted end datetime string for database queries.
    """
    #Get Data Source
    source = data['source'].value
    #Get plot type
    plot = data['plot_type'].value
    #Get number of y parameters
    n_ypar = int(data['ny'].value)  
    #Get time data
    tstart = data['tstart'].value
    tend = data['tend'].value
    tstartdb = util.format_date(tstart)
    tenddb = util.format_date(tend)

    return source, plot, n_ypar, tstartdb, tenddb

class getFilesThread(threading.Thread):
    """Worker thread class for asynchronously downloading and parsing dataset files.

    Parameters
    ----------
    ThreadID : int
        Numerical identifier for the thread instance.
    name : str
        Thread name identifier.
    params : list
        Parameter bundle containing file lists, system class, parameter names,
        temporary working directory, download queue, repository configuration, 
        ADU flags, detector specifications, repository instance, and metadata.

    Attributes
    ----------
    name : str
        Thread name.
    id : int
        Thread ID.
    sys_cls : object
        Instance of system class responsible for file parsing.
    source : str
        Data source identifier string.
    par : list of str
        List of parameters to read from files.
    todownload : array_like
        Array of files requiring remote retrieval.
    filenames : ndarray
        Concatenated array of existing and download-required filenames.
    conf : object
        Repository system configuration instance.
    temp_dir : str
        Path to temporary working directory.
    filestatus : int
        File reading error flag (0 for success, 1 on error).
    downstatus : int
        File download error flag (0 for success, 1 on error).
    missing : int
        Missing data counter flag.
    na : int
        Not available data counter flag.
    todb : list of str
        List of newly downloaded filenames to register in local database.
    adu : list or str
        ADU calibration settings.
    det : list or str
        Detector layout settings.
    repo : object
        Repository interface instance.
    meta : dict
        Extracted metadata rule mapping.
    res : dict
        Parsed dataset results indexed by date string.
    listfiles : dict
        Mapping of date strings to corresponding source filenames.
    """
    
    def __init__(self, ThreadID, name, params):
        threading.Thread.__init__(self)

        self.name=name
        self.id=ThreadID
        self.sys_cls = params[1]
        self.source = self.sys_cls.source
        self.par = params[2]
        self.todownload = params[4]
        self.filenames = np.concatenate((params[0], self.todownload))
        self.conf = params[5]
        self.temp_dir = "../users/"+params[3]+"/tmp/"
        self.filestatus = 0
        self.downstatus = 0
        self.missing = 0
        self.na = 0
        #list of files for which to store info in local_files
        self.todb = []
        self.adu = params[6]
        self.det = params[7]
        self.repo = params[8]
        self.meta = params[9]


    def run(self):
        """Execute multi-threaded download and dataset file parsing routine."""
        #threadLimiter.acquire()
        self.res = {}
        self.listfiles = {}
        curr_res = {}
        try:
            if len(self.todownload) > 0 and self.repo.method=="ftp":
                #open ftp connection
                ftp = util.open_ftp_connection(self.source, self.conf)
            else:
                ftp = ""

            for name in self.filenames:
                file_ok=True
                if name in self.todownload:
                    if self.conf.wgetdata == "remote":
                        #downloadfile
                        file_ok = self.repo.download_file(name, self.conf, ftp, self.temp_dir, self.source.lower())
                    else:
                        #copy file
                        file_ok = util.copylocal([name], self.conf, self.temp_dir, self.sys_cls, self.repo.use_runid)                        
                    if file_ok:
                        #update local_files list to add
                        self.todb.append(name)
              
                if file_ok:
                    #get data from files
                    try:
                        value = self.sys_cls.read_data_from_file(name, self.temp_dir, self.par, self.conf, adu=self.adu, det=self.det, repo = self.repo, metadata = self.meta, result = {})
                        if self.meta["data"] != {}:
                            if self.meta["fullpar"] == 0:
                                fullparrlist = self.meta["listpars"]
                            else:
                                fullparrlist = self.par                               
                        else:
                            fullparrlist = self.par                         

                        #arrange collected data in usable format for online plot
                        datearr=[]
                        #get all dates
                        for p in value.keys():
                            curr_dates = value[p]['dates']
                            datearr += curr_dates
                        datearr = np.unique(datearr)

                        #for each date, build result as dictionary (date, list of values for all parameters), filled with -999 where missing
                        for d in datearr:
                            vals_arr = -999*np.ones(len(self.par))
                            for i, curr_par in enumerate(fullparrlist):
                                try:
                                    curr_d = np.array(value[curr_par]['dates'])
                                    curr_v = np.array(value[curr_par]['values'])
                                    vpos = np.where(curr_d == d)[0][0]
                                    vals_arr[i] = curr_v[vpos]
                                except:
                                    pass                          
                            curr_res.update({d:list(vals_arr)})
                            self.listfiles.update({d:name})
                        self.res.update(curr_res)
                    except Exception as e:
                        self.filestatus = 1
                else:
                    self.downstatus = 1
        except Exception as e:
            print(str(e))
        finally:
            if ftp != "" and ftp != "unable":
                ftp.close()

    def get_res(self):
        """Retrieve parsed dataset results.

        Returns
        -------
        dict
            Dictionary mapping date strings to extracted parameter value lists.
        """
        return self.res
      
    def get_listfiles(self):
        """Retrieve mapping of timestamps to source data files.

        Returns
        -------
        dict
            Dictionary mapping timestamps to filenames.
        """
        return self.listfiles

    def get_status(self):
        """Get execution status flags for file parsing and downloads.

        Returns
        -------
        filestatus : int
            File reading error flag.
        downstatus : int
            Download error flag.
        missing : int
            Missing data counter.
        na : int
            Not available counter.
        """
        return self.filestatus, self.downstatus, self.missing, self.na
    
class inData():
    """Parser for primary X or Y parameter coordinates and detector configurations.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Raw request input form payload.
    source : str
        Data source identifier name.
    p : str or tuple
        Parameter coordinate prefix (e.g. 'x' or 'y0').

    Attributes
    ----------
    sys : str
        Subsystem or system identifier name.
    par : str
        Parameter name string.
    row : str
        Detector row index string.
    col : str
        Detector column index string.
    det : str
        Detector identifier token.
    val : str
        Parameter value filter string.
    ic : str
        Instrument component identifier string.
    adu : str
        ADU or calibrated flag string.
    coord : str
        Coordinate prefix identifier ('x' or 'y').
    data : cgi.FieldStorage or dict
        Reference to original request payload.
    det_type : list of str
        Detector family specification list.
    """
    
    def __init__(self, data, source, p):
        if len(p)==2:
            p1 = p[0]
            p2 = p[1]
        else:
            p1 = p
            p2 = ""
            
        self.sys = data[p1+'sys'+p2].value
        self.par = data[p1+'par'+p2].value

        try:
            self.row = data[p1+'row'+p2].value
        except:
            self.row = ""
        try:
            self.col = data[p1+'col'+p2].value
        except:
            self.col = ""
        try:
            self.det = data[p1+'det'+p2].value
        except:
            self.det = ""
        try:
            self.val = data[p1+'val'+p2].value
        except:
            self.val = ""
        try:
            self.ic = data[p1+'ic'+p2].value
        except:
            self.ic = ""
        try:
            self.adu = data[p1+'adu'+p2].value
        except:
            self.adu = ""
        
        self.coord = p1 #to define if the coordinate is x or y0
        self.data = data
        self.det_type = self.data.getlist('det_type[]')

    def set_detector(self, connection):
        """Format and construct complete detector token with layer or quadrant information.

        Parameters
        ----------
        connection : PyMySQL object
            Active database connection instance.

        Returns
        -------
        det : str
            Formatted detector string identifier.
        """
        if self.coord == "x":
            idx = 0
        elif self.coord == "y":
            idx = 1
        if self.det_type[idx] == "DET":
            layer = util.db_query(connection, "hktm_detector_layer", "layer", "WHERE detid="+str(self.row)+str(self.col), "one")
            layer = layer.get("layer")
            det = self.det + "["+str(layer)+"]"
        elif self.det_type[idx] == "CCD":
            det = self.det.replace('\"',"")

        return det
        
class yAdditional():
    """Parser for additional Y parameter series inputs from form request data.

    Parameters
    ----------
    data : cgi.FieldStorage or dict
        Raw form request payload.
    source : str
        Data source identifier string.

    Attributes
    ----------
    syss : list of str
        List of system identifiers for additional Y parameters.
    pars : list of str
        List of parameter names for additional Y parameters.
    rows : list of str
        List of detector row indices.
    cols : list of str
        List of detector column indices.
    dets : list of str
        List of detector identifier tokens.
    vals : list of str
        List of parameter value filters.
    ics : list of str
        List of instrument component identifiers.
    tbl : list of str
        List of alternative database table names.
    adu : list of str
        List of ADU or calibrated conversion flags.
    det_type : list of str
        List of detector family types.
    """
    
    def __init__(self, data, source):
        self.syss = data.getlist('additional_y_sys[]')
        self.pars = data.getlist('additional_y_par[]')
        try:
            self.rows = data.getlist('additional_y_row[]')
        except:
            self.rows = ""
        try:
            self.cols = data.getlist('additional_y_col[]')
        except:
            self.cols = ""
        try:
            self.dets = data.getlist('additional_y_det[]')
        except:
            self.dets = ""  
        try:
            self.vals = data.getlist('additional_y_val[]')
        except:
            self.vals = ""
        try:
            self.ics = data.getlist('additional_y_ic[]')
        except:
            self.ics = ""
        try:
            self.tbl= data.getlist('additional_y_tbl[]')
        except:
            self.tbl = ""    
        try:
            self.adu= data.getlist('additional_y_adu[]')
        except:
            self.adu = ""       
        self.det_type = data.getlist('det_type[]')
        
    def set_detector(self, connection, idx):
        """Format complete detector identifier string for a specific additional Y parameter.

        Parameters
        ----------
        connection : PyMySQL object
            Active database connection instance.
        idx : int
            Index of target additional Y parameter in parameter array.

        Returns
        -------
        det : str
            Formatted detector string identifier.
        """
        if self.det_type[idx+2] == "DET":
            layer = util.db_query(connection, "hktm_detector_layer", "layer", "WHERE detid="+str(self.rows[idx])+str(self.cols[idx]), "one")
            layer = layer.get("layer")
            det = self.dets[idx] + "["+str(layer)+"]"
        elif self.det_type[idx+2] == "CCD":
            det = self.dets[idx].replace('\"',"")

        return det

def create_result(dates, data, ny):
    """Structure time series timestamps and parameter arrays into output result payload.

    Parameters
    ----------
    dates : list of str
        List of timestamp strings.
    data : list of array_like
        Sequence of parameter arrays (X, Y0, Y1, ...).
    ny : int
        Number of Y parameters.

    Returns
    -------
    out : dict
        Structured dictionary containing 'date', 'x', 'y0', and additional 'y<i>' series.
    """
    out = {'date':dates, 'x':list(data[0]), 'y0':list(data[1])} 
    #Append additonal y data to result
    if ny > 1:
        for i in range(ny-1):
            out.update({"y"+str(i+1) : list(data[i+2])})

    return out

def start_multithread(threads, thread_id, params):
    """Instantiate and start a file processing thread if files exist in queue.

    Parameters
    ----------
    threads : list of getFilesThread
        List of active thread workers.
    thread_id : int
        Numerical index for the new worker thread.
    params : list
        Parameter configuration bundle for thread instantiation.

    Returns
    -------
    threads : list of getFilesThread
        Updated list of active worker thread instances.
    """
    if len(params[0])+len(params[4])>0:
        session = getFilesThread(thread_id, "Thread_"+str(thread_id), params)
        threads = threads+[session]
        threads[thread_id].start()
    return threads

def retrieve_data(nthreads, filenames, system_cls, listparams, tmp_dir, todownload, conf, listadu=None, listdet = None, repo = None, metadata = {}):
    """Partition file lists and spawn worker threads to process files concurrently.

    Parameters
    ----------
    nthreads : int
        Maximum number of concurrent worker threads.
    filenames : array_like
        List of existing local data files to read.
    system_cls : object
        System class instance implementing data parsing routines.
    listparams : list of str
        List of parameter names to extract.
    tmp_dir : str
        Path to temporary working directory.
    todownload : array_like
        List of files needing remote download.
    conf : object
        Repository system configuration instance.
    listadu : list of str, optional
        ADU conversion flags per parameter.
    listdet : list of str, optional
        Detector configuration flags per parameter.
    repo : object, optional
        Repository interface instance.
    metadata : dict, optional
        Additional metadata configuration rules.

    Returns
    -------
    threads : list of getFilesThread
        List of initialized and started thread instances.
    """
    #semaphore
    util.set_threadlimiter(nthreads)    
    
    threads = []
    filesarray = []
    files2down = []
    
    #split lists of files for multi-threading
    filesarray = np.array_split(np.array(filenames), nthreads)
    files2down = np.array_split(np.array(todownload), nthreads)

    #if files to download exist, create temporary download directory if needed
    if len(todownload)>0:
        new_tmp = "../users/"+tmp_dir+"/tmp"
        if (os.path.exists(new_tmp)==False):
            os.mkdir(new_tmp)
        sourcetmp = new_tmp+"/"+system_cls.name
        if (os.path.exists(sourcetmp)==False):
            os.mkdir(sourcetmp)
            
    #run multi-threading code to get data from files
    for thread_id in range(nthreads):
     
        params = [filesarray[thread_id], system_cls, listparams, tmp_dir, files2down[thread_id], conf, listadu, listdet, repo, metadata]
        if len(filesarray[thread_id])+len(files2down[thread_id])>0:
            session = getFilesThread(thread_id, "Thread_"+str(thread_id), params)
            threads = threads+[session]
            threads[thread_id].start()
       
    return threads      
