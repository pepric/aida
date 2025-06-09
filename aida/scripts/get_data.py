#!/usr/bin/python

import json
import cgi, cgitb 
cgitb.enable(display=0, logdir="cgi-logs")   # for troubleshooting
import functions as util
import datautils as du
import classes
from calculate_statistics import get_global_stats, do_calculation
import db_io
from send_mail import Email

class listRemoteFiles():
    """ Class implementing methods and utilities to retrieve list of data files remotely stored"""
    def __init__(self, db, source):
        """listRemoteFiles init
        Parameters
        ---------
        db : dict,
            dictionary containing connection parameters as instantiated by class functions.repConfig
        source : str,
            system source under analysis
            
        Attributes
        ---------
        db : dict,
            dictionary containing connection parameters
        s : str,
            system source under analysis,
        tabname : str,
            name of DB table to use
        addstatement : str,
            additional statement for DB query
        """        
        self.db = db
        self.s = source
        self.tabname = ""
        self.addstatement = ""
        self.set_tab_par()

    def get_remote_files_list(self, conn, tstart, tstop):
        """Retrieve the list of remote files to get data from.
        
        Parameters
        ---------
        conn : PyMySQL object,
            instance of a PyMySQL connection to the MySQL database
        tstart : str,
            start datetime of experiment data,
        tstop : str,
            end datetime of experiment data

        Returns
        ---------
        result : PyMySQL Cursor object,
                instance of a cursor object containing the results of the query
        """         
        result = []
        if self.tabname != "":
            #for each db a different statement
            statement = classes.sys_inst(self.s).db_statement_filelist(self.addstatement, tstart, tstop)
            result = util.db_query(conn, self.tabname, self.listcol, statement)
            
        return result        
    
    def set_tab_par(self):
        """Set DB table name and additional statement to query the specific DB.""" 
        db = self.db
        s = self.s
        sys_class = classes.sys_inst(s)
        self.listcol = sys_class.db_cols

        try:
            self.tabname = db['dbname']+"."+db['tabname']
        except:
            self.tabname = ""
            
        try:
            self.addstatement = "and " + db['condition']
        except : 
            self.addstatement = ""
        
def plot_to_db(pdata, usecase, plot, username, labels, stats, stat_res, plot_name, ts, te, tokeep=0):
    """Store plot data into local DB.
    
    Parameters
    ----------
    pdata : str,
            dictionary as string, containing data retrieved from data repository
    usecase :str, 
            data origin
    plot : str,
           type of plot to which the data refers 
    username : str,
              user who generated the plot 
    labels : list,
            list of plotted parameters
    stats : "global" or "advanced", str
            type of statistical analysis requested
    stat_res : dict,
            results of statistical analysis
    plot_name : str,
            displayed name of plot
    ts : str,
        start datetime of experiment data
    te : str,
        end datetime of experiment data
    tokeep : 0 or 1,
        0 if data are temporary stored, 1 if data are permanently stored
        
    Returns
    -------
    plotid : int,
        row id of stored record in DB
    """
    #connect to DB
    connconf = util.repConfig().data['local_db']
    dbio = db_io.dbIO(connconf)
    plotid = dbio.insert_temp_plot(pdata, usecase, plot, username, labels, stats, stat_res, plot_name, ts, te, tokeep)
        
    return plotid        
    
def main(data):
    """Retrieve data to display on a new plot.
    
    Parameters
    ----------
    data : cgi.FieldStorage,
        Contains all data coming from client side script: source, datetime intervals or pid, usecase, online/offline plot flag, username, plot type, statistics, bins configuration, parameters labels
        
    Returns
    -------
    result : dict,
           dictionary containing data retrieved from data repository. It is returned only if isonline = 1, else it is stored into the local DB.
           It is structured as follow:
                result={
                    'date' : [<datetime_1 ('YYYY-MM-DD HH:mm:ss')>, <datetime_2>, ... ,<datetime_N>],
                    'x': [<x_parameter_1 as string (or '0' if not required)>, <x_parameter_2>, ... ,<x_parameter_N>]
                    'y0': [<y0_parameter_1 as string>, <y0_parameter_2>, ... ,<y0_parameter_N>],
                    'y1': [<y1_parameter_1 as string>, <y1_parameter_2>, ... ,<y1_parameter_N>],
                    ...
                    'y<M>': [<yM_parameter_1 as string>, <yM_parameter_2>, ... ,<yM_parameter_N>],
                    "errstatus" : <flag for error>,
                    "warningstatus" : <flag for general warning>,
                    "datastatus" : <flag for data warning>,
                    "infostatus" : <flag for data data>,
                    "msg" : text describing error/warning,
                    "infomsg" : text reporting info
                    }
                Records 'y1'...'y<M>' are reported only if they have been required from user.
    """     
    global e
    e = util.statusMsg()

    #Get Data Source
    source = data['source'].value
    try:
        ts = data['tstart'].value
        te = data['tend'].value
        prod_id = None
    except:
        prod_id = data['pid'].value
        ts = None
        te = None
    usecase = data['usecase'].value
    isonline = data['isonline'].value
    
    #get repository info
    conf = util.repConfig(source,usecase)
    
    connmsg={}
    result = {}
    if conf.error == 0:
       # print(ts,te)
        lmain = len(conf.main)
        curr_main = util.set_path(conf.root[-lmain:-1])
        #set number of threads to use
        try:
            nthreads = int(conf.sourcedata['nprocs'])
        except:
            nthreads = 1

        if curr_main != conf.main:
            e.mainstatus = 1

        try:
            connection = util.connect_db(conf.data['local_db'])
            locerr = 0
        except:
            locerr = 1
            e.localstatus = 1
     
        if locerr == 0:
            #directory to store downloaded files
            tmp_dir = data['user'].value
            #get data
            result, e = conf.repclass[usecase].retrieve_plot_data(conf, e, connection, data, source, ts, te, nthreads, prod_id)
            connection.close()          

    else:
        e.confstatus = 1
    #update errors list
    status = e.get_status()
    result.update({"errstatus" : status[0], })
    result.update({"warningstatus" : status[1]})
    result.update({"datastatus" : status[2]})
    result.update({"infostatus" : status[3]})
    result.update({"msg" : e.error})
    result.update({"infomsg" : e.info})

    labels = data.getlist('labels[]')    
   
    # if plot is online, return result, else collect additional info and store experiment into the DB
    if isonline == "1":
        print(json.JSONEncoder().encode(result))
    else:
        #get additional data to store
        try:
            binsize = data['binsize'].value
            bintype = data['bintype'].value
            result.update({"bins" : [binsize, bintype]})
        except:
            binsize = None
            bintype = None
        plot = data['plot_type'].value
        stats = data['stats'].value
        if stats == "advanced":  
            try:
                stats_list = json.loads(data['stats_list'].value)
            except:
                stats_list = {}
        else:
            stats_list = get_global_stats(stats)
        username = data['user'].value

        stat_res = ""
        if result['errstatus'] == 0 and result['datastatus'] == 0:
            stat_res = do_calculation(result, plot, stats_list, len(labels)-1)

        #set plot name  
        try:
            pclass = classes.plot_inst(plot)
            plot_name = pclass.name
        except:
            plot_name = "Statistical Analysis"
            
        #change \n into another format to be stored in db
        msg = result['msg']
        msg = msg.replace("\n", "_RETCHAR_")
        result.update({"msg" : msg})
        msg = result['infomsg']
        msg = msg.replace("\n", "_RETCHAR_")        
        result.update({"infomsg" : msg})        
        #save data to DB
        plotid = plot_to_db(str(result), usecase, plot, username, labels, stats, stat_res, plot_name, ts, te)
        connconfig = util.repConfig().data['local_db']
        connection = util.connect_db(connconfig)        
        #update history
        if plotid is not None:
            data2store = '{"source" : "'+source+'", "dates range" : "['+str(ts)+', '+str(te)+']"}'
            l = str(labels)[1:-1].replace("'","").replace("None,","")
            settings = {"usecase" : usecase.upper(), "parameters" : l}         
            if labels[0] is not None:
                settings.update({"X" : labels[0]})
            if binsize is not None:
                if bintype=="binnumber":
                    bin2hist = "Number of Bins"
                else:
                    bin2hist = "Bin Size"
                settings.update({bin2hist : binsize})
            if len(stats_list)>0:
                stats2hist = ",".join([k for k in stats_list.keys()])
                settings.update({"Stats" : stats2hist})                
            settings = str(settings).replace("'","\"")                               
            util.update_history(connection, username, plot_name, input="NA", output=data2store, config=settings)  
        else:
            pass
        
        #SEND EMAIL
        mailconfig = Email("../smtp.json")    
        #get user email    
        email = util.get_email(connection, username)
        connection.close()
        #set email text
        url = data['url'].value
        maildata = [plot_name, usecase, source, labels, ts, te, stats_list, url]
        
        if plotid is not None:
            subject = "New "+plot_name+" generated"          
            text = mailconfig.ok_plot_text(maildata, plotid, source)
        else:
            subject = "ATTENTION: Failed "+plot_name+" generation"          
            text = mailconfig.error_plot_text(maildata, "Impossible to store data in local DB")
        #send mail    
        fromuser = "AIDA"
        to = email
        msg = mailconfig.set_message(subject,fromuser,to,text)
        mailconfig.send_mail(msg)
        
if __name__ == "__main__":
    print("Content-Type: application/json")
    print()
    #the cgi library gets vars from html
    data = cgi.FieldStorage()
    
    main(data)