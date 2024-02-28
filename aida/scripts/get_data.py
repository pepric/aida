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
   
    def __init__(self, db, source):
        self.db = db
        self.s = source
        self.set_tab_par()

    def get_remote_files_list(self, conn, tstart, tstop):
        result = []
        if self.tabname != "":
            #for each db a different statement
            statement = classes.sys_inst(self.s).db_statement_filelist(self.addstatement, tstart, tstop)
            result = util.db_query(conn, self.tabname, self.listcol, statement)
            
        return result        
    
    def set_tab_par(self):
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

    #connect to DB
    connconf = util.repConfig().data['local_db']
    dbio = db_io.dbIO(connconf)
    plotid = dbio.insert_temp_plot(pdata, usecase, plot, username, labels, stats, stat_res, plot_name, ts, te, tokeep)
        
    return plotid        
    
def main(data):
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
            result, e = conf.repclass[usecase].retrieve_plot_data(conf, e, connection, data, source, ts, te, nthreads, prod_id)
            connection.close()          

    else:
        e.confstatus = 1
    status = e.get_status()
    result.update({"errstatus" : status[0], })
    result.update({"warningstatus" : status[1]})
    result.update({"datastatus" : status[2]})
    result.update({"infostatus" : status[3]})
    result.update({"msg" : e.error})
    result.update({"infomsg" : e.info})

    labels = data.getlist('labels[]')    
   
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