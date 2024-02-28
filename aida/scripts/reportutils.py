#!/usr/bin/python

# import json
import ast
import numpy as np
from    os          import environ
from datetime import datetime
import  threading
import multiprocessing
import functions as util
import pymysql.cursors
from send_mail import Email
import socket
from calculate_statistics import calc_stat
from math import ceil
environ['HOME'] = '/'
environ['MPLCONFIGDIR'] = './tmp/'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class dbThread(threading.Thread):
    def __init__(self, ThreadID, name, th_pars):
        threading.Thread.__init__(self)
        self.name=name
        self.id=ThreadID
        self.data = th_pars[0]
        self.runid = th_pars[1]
        self.source = th_pars[2]
        self.sub = th_pars[3]
        self.acquid = th_pars[4]
        self.runstep = th_pars[5]
        self.procid = th_pars[6]
        self.params = th_pars[7]
        self.conf = th_pars[8]
        self.dbconnection_in = th_pars[9]
        self.dberror = 0

    def run(self):
        use_runstep = False
        for p in self.params:
            if not use_runstep:
                stored = util.db_query(self.dbconnection_in, self.source+"_reports_data", "*" ,
                                       statement = "WHERE param = '"+p+"' AND runID = "+str(self.runid)+" AND acqID = "+str(self.acquid)+" AND subsystem = '"+self.sub+"'", res_type = "one")
                #check if data related to p and runid are already stored
                #if previous data exist, update them, else insert new record
                if stored is not None:
                    #update
                    stored_id = stored['id']
                    v = stored['vals']
                    d = stored['dates']
                    if len(self.data[p]['dates'])>0:
                        if len(d)>1:
                            new_v = v+","+str(self.data[p]['values'])[1:-1].replace(" '","'")
                            new_d = d+","+str(self.data[p]['dates'])[1:-1].replace(" '","'")
                        else:
                            new_v = str(self.data[p]['values'])[1:-1].replace(" '","'")
                            new_d = str(self.data[p]['dates'])[1:-1].replace(" '","'")
                        sql = "UPDATE "+self.source+"_reports_data SET dates=\""+new_d+"\", vals=\""+new_v+"\" WHERE id = "+str(stored_id)
                    else:
                        sql = ""
                else:
                    #insert
                    if len(self.data[p]['dates'])>0:
                        sql = "INSERT INTO "+self.source+"_reports_data (runID, subsystem, acqID, runstep, param, dates, vals) VALUES ('"+str(self.runid)+"', '"+self.sub+"', '"+str(self.acquid)+"', '"+str(self.runstep)+"', '"+p+"', \""+str(self.data[p]['dates'])[1:-1]+"\", \""+str(self.data[p]['values'])[1:-1]+"\")"
                    else:
                        sql=""
            else:
                #insert
                if len(data[p]['dates'])>0:
                    sql = "INSERT INTO "+self.source+"_reports_data (runID, subsystem, acqID, runstep, param, dates, vals) VALUES ('"+str(self.runid)+"', '"+self.sub+"', '"+str(self.acquid)+"', '"+str(self.runstep)+"', '"+p+"', \""+str(self.data[p]['dates'])[1:-1]+"\", \""+str(self.data[p]['values'])[1:-1]+"\")"
                else:
                    sql=""

            if sql!="":
                try:
                    # Obtain a cursor object
                    mySQLCursor = self.dbconnection_in.cursor()
                    # Execute the SQL stament
                    mySQLCursor.execute(sql)
                    # Close the cursor and connection objects
                    mySQLCursor.close()
                except:
                    self.dberror = 1

        self.dbconnection_in.close()

    def get_error(self):
        return self.dberror

def analysis(conf,jsonconf,syscls,nproc,runid,origin="",acquid = 1):
    result = {}
    error = 0
    source = syscls.source
    #get list of available statistical functions
    try:
        connection = util.connect_db(conf.data['local_db'])
        query_stats = util.db_query(connection, "statistics", "stat_name, stat_slug, stat_function, parameters", "")
        connection.close()
    except:
        return {}, 1
    #get params to analyze
    try:
        params = jsonconf.pars[source][origin]['keys']
    except:
        params = []
  
    if syscls.parallel:
        #set number of parallel processes
        if len(params) < nproc:
            nproc = len(params)
        if len(params) == 0:
            nproc = 1
        if len(params)>0:
            #do analysis
            params_chunk = np.array_split(np.array(params), nproc)
            manager = multiprocessing.Manager()
            result = manager.dict()
            jobs = []
            for i in range(len(params_chunk)):
                j = multiprocessing.Process(target=parallel_analysis, args=(params_chunk[i], source, origin.upper(), runid, acquid, jsonconf.repdata, conf, query_stats,syscls.parstruct[origin],syscls.hasorig,result))
                jobs.append(j)
                j.start()
            for j in jobs:
                j.join()
                if j.exitcode > 0:
                    error = j.exitcode
        else:
            result = {}
    else:
        result, serial_error = serial_analysis(params, source, origin.upper(), runid, acquid, jsonconf.repdata, conf, query_stats, syscls.parstruct[origin], syscls.hasorig)
        if serial_error > 0:
            error = serial_error

    return result, error

def data_intersect(xdata, ydata):
     
    if xdata['dates'].shape[0] > 0 and ydata['dates'].shape[0] > 0:
        xdates = xdata["dates"]
        xvalues = xdata["vals"]
        ydates = ydata["dates"]
        yvalues = ydata["vals"]
        #find intersection with y0 dates
        scatter_dates = intersect_lists(xdates,ydates)
        cond1 = np.in1d(xdates, scatter_dates)
        cond2 = np.in1d(ydates, scatter_dates)
        xfinal = xvalues[cond1]
        yfinal = yvalues[cond2]         
    else:
        xfinal = []
        yfinal = []

    return xfinal, yfinal

def intersect_lists(x,y):
    #if x is not None and y is not None:
    if len(x) > 0 and len(y) > 0:    
        intersection = list(set(x).intersection(y))
    else:
        intersection =[]
    return intersection

def parallel_analysis(params, source, origin, runid, acquid, jsonconf, conf, qstats, parstruct, hasorig, return_dict):
    res, error = serial_analysis(params, source, origin, runid, acquid, jsonconf, conf, qstats, parstruct, hasorig)   
    return_dict.update(res)
    if error > 0:
        exit(error)

def get_operation_branches(p, jsonconf, source, origin, hasorig):

    if hasorig:
        br_root = jsonconf[source][origin]
    else:
        br_root = jsonconf[source]
    flat_dict = util.flatten(br_root)

    final_fd = {}
    for k,v in flat_dict.items():
        ksplit = k.split(".")
        new_k = ".".join(ksplit[:-1])
        opkey = ksplit[-1]
        if new_k not in final_fd:
            final_fd.update({new_k:{opkey : v}})
        else:
            old_v = final_fd[new_k]
            old_v.update({opkey : v})
            final_fd[new_k] = old_v

    return final_fd[p]

def serial_analysis(params, source, origin, runid, acquid, jsonconf, conf, qstats, parstruct, hasorig):
 
    res = {}
    error = 0
    stats_config = {}
    #list of statistical functions slugs
    slugs = np.array([item['stat_slug'] for item in qstats])

    for i in range(len(params)):
        stats_config = {}
        p = params[i]
        k = get_operation_branches(p, jsonconf, source, origin, hasorig, parstruct)
        for op in k.keys():
            curr_k = op.split("_")[0]
            if curr_k == "Operation":
                #get function type
                t = k[op]["Type"]
                try:
                    curr_pos = np.where(slugs==t)[0][0]
                    curr_func = qstats[curr_pos]['stat_function']
                    curr_name = qstats[curr_pos]['stat_name']
                    try:
                        par = k[op]["Parameters"]
                    except:
                        par = ""
                        
                    same_ops = 0                       

                    for n in stats_config.keys():
                        if curr_name == n.split("-")[0]:
                            same_ops+=1                     
                    curr_name += "-"+str(same_ops)
                    
                    if par == "":
                        stats_config.update({curr_name : curr_func})
                    else :
                        stats_config.update({curr_name : {"func" : curr_func, "params" : par, "npar" : len(par)}})
                except:
                    pass
            # calculate statistics
            if len(stats_config)!=0:
                #get stored data values from AIDA DB
                try:
                    connection = util.connect_db(conf.data['local_db'])
                except:               
                    return res, 1

                #get maximum number of runstep for the experiment
                runstep = util.db_query(connection, source.lower()+"_reports_data", "MAX(runstep)", statement = "WHERE param = '"+p+"' AND runID = "+str(runid)+" AND acqID = "+str(acquid)+" AND subsystem = '"+origin+"'", res_type = "one")        
                if runstep['MAX(runstep)'] is not None:
                    max_runstep = int(runstep['MAX(runstep)'])                    
                    if max_runstep > 1:
                        data_str = ""
                        for r in range(1,max_runstep+1):
                            curr_data = util.db_query(connection, source.lower()+"_reports_data", "vals", statement = "WHERE param = '"+p+"' AND runID = "+str(runid)+" AND acqID = "+str(acquid)+" AND subsystem = '"+origin+"' AND runstep = "+str(r), res_type = "one")
                            if curr_data is not None:
                                if r == 1:
                                    data_str = curr_data["vals"]
                                else:
                                    data_str += ","+curr_data["vals"]
                        if data_str[0] == ",":
                            data_str = data_str[1:]
                        data = np.fromstring(data_str,sep=",")
                        connection.close()
                    else:
                        data = util.db_query(connection, source.lower()+"_reports_data", "vals", statement = "WHERE param = '"+p+"' AND runID = "+str(runid)+" AND acqID = "+str(acquid)+" AND subsystem = '"+origin+"'", res_type = "one")
                        if data is not None:
                            data = data['vals']                            
                            data = np.fromstring(data,sep=",")
                        connection.close()

                    if data is not None:
                     #run analysis
                        stats = calc_stat(data, stats_config)
                    else:
                        stats = "No Data"
                    res.update({p : stats})
                    del data
                else:
                    return res, 2
    return res, error

def create_datadict(procnum, params, data, parlist, return_dict):
    for i in range(len(params)):
        ypos = np.where(parlist == params[i])[0][0]
        y = [v[1][ypos] for v in data]
        return_dict.update({params[i] : y})
    return return_dict

def get_keys(data, allowed=[], exclude=[]):
    final_keys = []
    error = 0
    keys = list(data.keys())
    for k in keys:
        if not k in exclude:
            if len(allowed)>0:
                if not k in allowed:
                    error = 1
            final_keys.append(k)

    return final_keys, error

def get_subs(repdata, system, origin = ""):
    try:
        if origin != "":
            keys = get_keys(repdata[system][origin])[0]
        else:
            keys = get_keys(repdata[system])[0]
    except:
        keys = []
    return keys

def get_add(obj,keys):
    """Pull all values of specified key from nested JSON."""
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

def get_pars(dictionary):
    full_list = util.concat_keys(dictionary)
    unique_list = []
    for item in full_list:
        par = item.split(".Operation")[0]
        if par not in unique_list:
            unique_list.append(par)
    return unique_list

def get_y_data2(p, y, jsonop, data, addpos):
    #get first ydata
    ydata = {p : y}
    #get additional parameters (if present)
    try:
        additional = jsonop["Additional Parameters"]
        for item in additional:
            ypos = addpos[item]
            yval  = [v[1][ypos] for v in data]
            ydata.update({item : yval})
    except:
        pass

    return ydata

def get_y_data(p, y, jsonop, data, parlist):
    #get first ydata
    ydata = {p : y}
    #get additional parameters (if present)
    try:
        additional = jsonop["Additional Parameters"]
        for item in additional:
            ypos = np.where(parlist == item)[0][0]
            yval  = [v[1][ypos] for v in data]
            ydata.update({item : yval})
    except:
        pass

    return ydata

def make_histogram(ydata, binsize, fname):
    filename = generate_plot([], ydata, fname, ptype="histogram", binsize = binsize)

    return filename

def make_trend(xdatastr, ydata, fname, fit = False):
    xdata = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in xdatastr]
    filename = generate_plot(xdata, ydata, fname, ptype="trend")

    return filename

def make_scatter(xdata, ydata, fname, xpar = "", fit = False):
    filename = generate_plot(xdata, ydata, fname, ptype="scatter", xlabel = xpar)

    return filename

def generate_plot(xdata, ydata, fname, ptype, xlabel = "", binsize = []):
    filename = []

    if len(ydata) > 1:
        if ptype == "trend":
            #single plot with all data
            singlef = single_plot(xdata, ydata, fname, ptype, binsize)
            filename.append(singlef)
        #multiple plots, one for each parameter
        f = multi_plot(xdata, ydata, fname, ptype, xlabel, binsize)
        for n in f:
            if n != "":
                filename.append(n)
    else:
        #single plot
        singlef = single_plot(xdata, ydata, fname, ptype, binsize)
        if singlef != "":
            filename.append(singlef)

    if len(filename)==0:
        filename = ""

    return filename

def single_plot(xdata, ydata, fname, ptype, binsize = []):
    if ptype=="histogram":
        iswidth = binsize[0]
        binval = binsize[1]
    fig = plt.figure(figsize=(9,6.4), dpi=150)
    ax = fig.add_subplot(1,1,1)
    axlabels=[]
    hasdata = False
    for i in range(len(ydata)):
        ylabel = list(ydata.keys())[i]
        curr_y = ydata[ylabel]
        final_x, final_y = util.remove_nan_data(xdata, curr_y)
        if len(final_y)>0:
            hasdata = True
        if ptype=="trend":
            if len(final_y)>0:
                trend = plt.plot(final_x, final_y, label = ylabel, linewidth=0.5)
                plt.setp(trend, marker = "o", ms = 2)
        elif ptype=="scatter":
            if len(final_y)>0:
                scatter = plt.plot(final_x, final_y, label = ylabel, linewidth=0)
                plt.setp(scatter, marker = "o", ms = 2)
        elif ptype == "histogram":
            if len(final_y)>1:
                if iswidth:
                    b = np.arange(min(final_y), max(final_y) + binval, binval)
                else:
                    b = binval
                a = np.array(final_y)
                h = plt.hist(a, bins=b, edgecolor='#333333', linewidth=0.5)

                del a

                for x in h[1]:
                    axlabels.append(x)
                if iswidth:
                    axl = np.arange(min(axlabels), max(axlabels), binval)
                    ax.set_xticks(axl)
                else:
                    ax.set_xticks(axlabels)
            else:
                plt.figtext(0.4, 0.5, 'No Data Available', fontsize='large')

        del curr_y
        del final_x
        del final_y

    if hasdata:
        set_axes(plt,ax,ptype)
        plt.tight_layout()
        filename = fname
    else:
        filename = ""

    if len(ydata)>1:
        lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='best', borderaxespad=0., prop={'size': 8})
        if filename != "":
            plt.savefig(filename, bbox_extra_artists=(lgd,), bbox_inches='tight', pad_inches=0)
            plt.close()
    else:
        if filename != "":
            plt.savefig(filename)
            plt.close()

    return filename

def set_axes(plt, ax, ptype):
    ax.set_facecolor('#e5ecf6')
    if ptype != "histogram":
        plt.grid(color='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#333333')
    ax.spines['left'].set_color('#333333')
    ax.tick_params(colors='#333333')

    if ptype=="trend":
        locator = mdates.AutoDateLocator(minticks=3, maxticks=10)
        formatter = mdates.ConciseDateFormatter(locator, formats = ['%Y', '%b', '%d', '%H:%M', '%H:%M:%S', '%S'], zero_formats=['', '%Y-%b-%d', '%b', '%Y-%b-%d', '%Y-%b-%d\n%H:%M', '%H:%M'], show_offset = False)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

    plt.xticks(fontsize = 10, rotation=45, ha="right")
    plt.yticks(fontsize = 10)

def multi_plot(xdata, ydata, fname, ptype, xlabel = "", binsize = []):

    if ptype=="histogram":
        iswidth = binsize[0]
        binval = binsize[1]
    img_x_plot = 4
    img_x_row = img_x_plot/2

    ny = len(ydata)
    nfiles = ceil(float(ny)/img_x_plot)

    filename = []
    ykeys = list(ydata.keys())

    yksplitted = np.array_split(ykeys, nfiles)
    hasdata = []
    for i in range(nfiles):
        fig = plt.figure(figsize=(9,6.4), dpi=150)
        curr_labels_arr = yksplitted[i]
        for id,v in enumerate(curr_labels_arr):
            ax = plt.subplot(2,img_x_row, id+1)
            curr_y = ydata[v]
            final_x, final_y = util.remove_nan_data(xdata, curr_y)
            if len(final_y)>0:
                hasdata.append("ok")

            if ptype=="trend":
                ax.set_title(v, fontdict={'fontsize': 10})
                if len(final_y)>0:
                    trend = plt.plot(final_x, final_y, label = v, linewidth=0.5)
                    plt.setp(trend, marker = "o", ms = 1)
                else:
                    ax.text(0.33, 0.5, 'No Data Available', fontsize='large')
            elif ptype=="scatter":
                if xlabel != "":
                    ax.set_xlabel(xlabel, fontsize=10)
                ax.set_ylabel(v, fontsize=10)
                if len(final_y)>0:
                    scatter = plt.plot(final_x, final_y, label = v, linewidth=0)
                    plt.setp(scatter, marker = "o", ms = 1)
                else:
                    ax.text(0.33, 0.5, 'No Data Available', fontsize='large')
            elif ptype == "histogram":
                axlabels=[]
                ax.set_title(v, fontdict={'fontsize': 10})
                if len(final_y)>1:
                    if iswidth:
                        b = np.arange(min(final_y), max(final_y) + binval, binval)
                    else:
                        b = binval
                    a = np.array(final_y)
                    h = plt.hist(a, bins=b, edgecolor='#333333', linewidth=0.5)
                    for x in h[1]:
                        axlabels.append(x)
                    del a
                else:
                    ax.text(0.33, 0.5, 'No Data Available', fontsize='large')

                if iswidth:
                    axl = np.arange(min(axlabels), max(axlabels), binval)
                    ax.set_xticks(axl)
                else:
                    ax.set_xticks(axlabels)

            if len(final_y)>0:
                set_axes(plt,ax,ptype)
            else:
                ax.axes.xaxis.set_ticks([])
                ax.axes.yaxis.set_ticks([])
            plt.tight_layout()
            del curr_y
            del final_x
            del final_y

        f = fname.replace(".png", "_"+str(i)+".png")
        plt.savefig(f)
        plt.close()
        filename.append(f)

    if len(hasdata) == 0:
        filename = ""

    return filename

def get_bins(jsonop):
    #get binsize
    try:
        b = float(jsonop["Bin Size"])
        iswidth = True
    except:
        b = int(jsonop["Number of Bins"])
        iswidth = False
    return iswidth, b

def send_report_mail(mailuser, mailadmin, okreport, maildata, errortype = ""):

    error_descr = {"noxml" : "No XML report generated",
                "conferr" : "Error reading report configuration file",
                "locerr" : "Impossible to connect to local DB"}  
    mailconfig={}
    error = 0
    try:
        if maildata[3] == "ondemand":
            period = "on-demand"
        else:
            period = maildata[3]
        host_name = socket.gethostname()
        ipaddr = socket.gethostbyname(host_name)
        webappdir = util.repConfig().data['webapp_dir']
        mailconfig = Email("../smtp.json")

        if okreport:
            pdf_ok = maildata[8]          
            subject = "New "+period+ " report generated"
            cc = mailadmin
            reportpath = "http://"+maildata[7]+"/"+webappdir+"/users/report/"
            fullfile = reportpath+maildata[0]
            text = mailconfig.ok_report_text(maildata, period, fullfile, pdf_ok)
        else:
            subject = "ATTENTION: Failed "+period+ " report generation"
            cc = mailadmin
            error = error_descr[errortype]
            text = mailconfig.error_report_text(maildata,period,error)

        fromuser = "AIDA"
        to = mailuser
        msg = mailconfig.set_message(subject,fromuser,to,text,cc)
        mailconfig.send_mail(msg)
    except:
        error = 1

    return error

def update_progress(connection, runid, percent="final"):
    sql_get = "SELECT exp_status FROM running_reports WHERE id = "+str(runid)
    with connection.cursor() as cursor:
        cursor.execute(sql_get)
        perc0 = cursor.fetchone()

    p = float(perc0['exp_status'])
    if p == -99.0:
        p=0.0
    if percent == "final":
        percent = 100.0 - p

    out = p + round(percent,1)

    sql_update = "UPDATE running_reports SET exp_status = "+str(out)+" WHERE id = "+str(runid)
    with connection.cursor() as cursor:
        cursor.execute(sql_update)
    connection.commit()