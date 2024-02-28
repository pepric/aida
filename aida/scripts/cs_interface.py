#!/usr/bin/python

import json
import cgi, cgitb
import classes
import functions as util
cgitb.enable(display=0, logdir="cgi-logs")  # for troubleshooting
from db_io import dbIO
import os
import sys
import psutil
from shutil import copyfile, move
from datetime import datetime
from send_mail import Email
import repos
import ast
import traceback

class Interfaces(object):
    def __init__(self):
        pass

    def check_connection(*args):
        error = 0
        try:
            connconfig = util.repConfig().data['local_db']
            connection = util.connect_db(connconfig)
            connection.close()
        except:
            error = 1
        return {'error' : error}
      
    def check_deltat(*args):
        #get data from client
        source = args[0]["source"].value
        tstart = util.format_date(args[0]["tstart"].value)
        tend = util.format_date(args[0]["tend"].value)
        usecase = args[0]["usecase"].value
        #calculate delta between dates        
        delta_t = (tend - tstart)/3600        
        #query the DB to get delta limits 
        query_res=""
        conf = util.repConfig()       
        connection = util.connect_db(conf.data['local_db'])
        query_res = util.db_query(connection, "systems", "plot_delta", "WHERE name='"+source+"' AND origin='"+usecase+"'", res_type = "one")

        delta_ref = query_res['plot_delta']
        if delta_t > delta_ref and delta_ref > 0:
            delta = 1
        else:
            delta = 0
        out = {"delta" : delta}
        return out

    def direct_download(*args):
        #get data from args
        filename = args[0]["filename"].value      
        source = args[0]["source"].value.lower()
        origin = args[0]["origin"].value
        #get configuration
        conf = util.repConfig(source, origin)
        #retrieve enabled repository
        repo = conf.repclass[origin]
        error = 0
        if repo.method == "ftp":
            ftp = util.open_ftp_connection(source, conf)
        else:
            ftp = ""
        if ftp == "unable":
            return {"result" : 1 }
        else:
            if repo.slug != "eas":
                return {"result" : 2 }
            else:
                settings = repo._setrepoconf(source, conf.opmode, conf.usecase)
                return {"result" : repo.BASE_DSS_URL}
    
    def file_to_image(*args):
        #get data from args
        username = args[0]["username"].value
        filename = args[0]["filename"].value      
        source = args[0]["s"].value.lower()
        origin = args[0]["o"].value 
        # define tmp directory        
        tmpdir = "../users/"+username+"/tmp/"
        
        if os.path.isfile(tmpdir+"/"+source+"/"+filename):
            #return existing filename
            out = {"result" : filename}
        else:
            try:
                #get configuration
                conf = util.repConfig(source, origin)
                #retrieve enabled repository
                repo = conf.repclass[origin]
                if repo.method == "ftp":
                    ftp = util.open_ftp_connection(source, conf)
                else:
                    ftp = ""
                
                if ftp == "unable":
                    result = "error"
                else:
                    #download file
                    filepath = tmpdir+source
                    if not os.path.isdir(filepath):
                        os.mkdir(filepath)              
                    downloaded = repo.download_file(filename, conf, ftp, tmpdir, source)            #DA SPOSTARE IWS E TESTARE
                    if downloaded:
                        result = filename
                        try:
                            #store file info into local_files table
                            dbIO(conf.data['local_db']).insert_local_file(filename, source.upper(), username, ftype="image")
                        except Exception as e:
                            pass
                    else:
                        result = "error"
                        
                    if repo.method == "ftp":
                        ftp.close()
            except Exception as er:
                result = "error"

            out = {"result" : result}

        return out          
 
    def get_repo_list(*args):
        with open("repos.py","r") as repo:
            source=repo.read()
        p = ast.parse(source)
        repoclasses = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        methods = []
        for c in repoclasses:
            cinst = classes.repos_inst(c)
            methods.append(cinst.method)        
  
        out = {"result" : {"classes" : repoclasses, "methods" : methods}}

        return out
        
    def running_reports(*args):
        maindir = "users/config"        
        username = args[0]["username"].value
        role = args[0]["role"].value
        data = []        
        try:        
            connconfig = util.repConfig().data['local_db']
            #get running reports list
            dbio = dbIO(connconfig)
            running_reports = dbio.get_running_reports(role = role, username = username)
            for rr in running_reports:
                curr_id = str(rr['id'])
                if rr['start_date'] is not None:
                    sdate = rr['start_date'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    sdate = "-"
                pid = rr["pid"]           
                #Config File
                cf = rr["config_file"];
                ncf = "<a href='#' onclick='window.open(\""+maindir+"/"+cf+"\", \"\", \"height=800,width=600\")'>"+cf+"</a>";
                #Progress
                status = str(rr['exp_status'])
                if status != "-100.0" and pid > 0:
                    try:
                        process = psutil.Process(pid)
                        process_name = process.name()
                        if not process_name.startswith("python"):
                            dbio.update_running_reports(pid, curr_id, status = -101)
                    except:
                        #set running_reports status to failed
                        dbio.update_running_reports(pid, curr_id, status = -101)            
            
                if status == "-99.0":
                    status_label = "waiting..."
                    add_class = "progress-label progress-label-black"
                elif status == "-100.0":
                    status_label = "paused"
                    add_class = "progress-label progress-label-yellow"
                elif status == "-101.0":
                    status_label = "failed"
                    add_class = "progress-label progress-label-red" 
                elif status == "-102.0":
                    status_label = "scheduled"
                    add_class = "progress-label progress-label-orange"                     
                else:
                    status_label = status
                    add_class = ""
                progress = "<div class='progress'><div class='progress-bar progress-bar-striped progress-bar-animated "+add_class+"' role='progressbar' style='width : "+status+"%;' aria-valuenow='"+status+"' aria-valuemin='0' aria-valuemax='100'>"+status_label+"</div></div>"
            
                #PID
                pid = str(pid)
                npid = "<div class='action-btn' style='min-width:90px'>"     
                if role == "admin" and rr["period"] != "ondemand" and pid[0] != "-":    #and status != "-99.0"
                    if status=="-100.0" or status=="-101.0":
                        npid += "<a href='#' onclick = 'resume_report("+curr_id+", \""+sdate+"\", \""+cf+"\", \""+username+"\", \""+rr["period"]+"\")'><img title='Resume/Restart generation' class='download-icon' src='assets/images/play-button.png'/></a>"
                    else:
                        npid += "<a href='#' onclick = 'stop_report("+curr_id+", "+pid+", \""+cf+"\", \"pause\")'><img title='Pause generation' class='download-icon' src='assets/images/pause_doc_min.png'/></a>"

                if status=="-100.0" or status=="-101.0":
                    title_icon = 'Remove'
                    img_icon = 'trash_48.png'
                    action = 'remove'
                else:
                    title_icon = 'Stop generation'
                    img_icon = 'del_doc_min.png'
                    action = 'kill'
                if pid[0] != "-":
                    npid += "<a href='#' onclick = 'stop_report("+curr_id+", "+pid+", \""+cf+"\", \""+action+"\")'><img title='"+title_icon+"' class='download-icon' src='assets/images/"+img_icon+"'/></a>" 
                npid += "</div>"
                if role == "admin":
                    curr_data = {"ID":curr_id,"User":rr["username"],"Period":rr["period"],"Config File":ncf,"Current Report Start Date":sdate,"Progress":progress,"Pid":npid}           
                else:
                    curr_data = {"ID":curr_id,"Period":rr["period"],"Config File":ncf,"Current Report Start Date":sdate,"Progress":progress,"Pid":npid}             
                data.append(curr_data)

            out = {"sEcho":100,"iTotalRecords":len(data),"iTotalDisplayRecords":len(data),"aaData":data}
        except:
            out = {"sEcho":100,"iTotalRecords":1,"iTotalDisplayRecords":1,"aaData":[{"ID":"ERROR","User":"Unable to retrieve Running Reports data. Please retry or contact AIDA admin","Period":"","Config File":"","Current Report Start Date":"","Progress":"","Pid":""}]}

        return out            
      
    def users_tables(*args):
        status = int(args[0]["status"].value)
        data = []        
        try:        
            connconfig = util.repConfig().data['local_db']
            #get running reports list
            dbio = dbIO(connconfig)
            users = dbio.get_users(status)
            for u in users:
                action = ""
                results = {"Username":u['username'],"E-Mail":u['email'],"Role":u['role']}
                try:
                    action_date = u['action_date'].strftime("%Y-%m-%d %H:%M:%S")
                except:
                    action_date = "-"
                if status == 0:
                    results.update({'Request Date' : action_date})
                elif status == 1:
                    try:
                        last_login = u['last_login'].strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        last_login = "-"
                    try:
                        last_logout = u['last_logout'].strftime("%Y-%m-%d %H:%M:%S")                
                    except:
                        last_logout = "-"
                    results.update({'Activation Date' : action_date, 'Last Login' : last_login, 'Last Logout' : last_logout})
                elif status == 2:
                    results.update({'Deactivation Date' : action_date})
                
                if u['active'] != 1 :
                    action = "<a href='#' onclick='manage_user("+str(u['id'])+", \"active\", \""+u['username']+"\", \""+u['email']+"\")'><img title='Activate' class='download-icon' src='assets/images/activate_48.png'/></a>"
                else:
                    if u['role'] != "admin":
                        action = "<a href='#' onclick='manage_user("+str(u['id'])+", \"deactive\", \""+u['username']+"\", \""+u['email']+"\")'><img title='Deactivate' class='download-icon' src='assets/images/deactivate_48.png'/></a>"
                        
                if (u['role'] != "admin" or (u['role'] == "admin" and u['active']=="0")):
                    action += "<a href='#' onclick='manage_user("+str(u['id'])+", \"remove\", \""+u['username']+"\", \""+u['email']+"\")'><img title='Remove' class='download-icon' src='assets/images/trash_48.png'/></a>"
                    
                results.update({'Actions' : action})
                data.append(results)
            out = {"sEcho":status,"iTotalRecords":len(data),"iTotalDisplayRecords":len(data),"aaData":data}
        except Exception as e:
            out = {"sEcho":status,"iTotalRecords":1,"iTotalDisplayRecords":1,"aaData":[{"Username":"ERROR - Impossible to retrieve data","E-Mail":"","Role":"","Request Date":"","Actions":""}]}

        return out      

    def flagged_reports(*args):
        data = []
        maindir = "users/report"
        extension = ".pdf"
        try:
            #get flagged reports list        
            connconfig = util.repConfig().data['local_db']
            dbio = dbIO(connconfig)
            flagged = dbio.get_flagged(archive="report")
            #render records
            for el in flagged :
                fname = el['filename']
                user = el['username']
                flagdate = el['date_exp'].strftime("%Y-%m-%d %H:%M:%S")
                expstatus = el['status_exp']
                #mod expstatus text
                if expstatus == "nd":
                    flagtxt = "NOT DEFINED"
                else:
                    flagtxt = expstatus.upper()                
                esimg = set_status_img(expstatus)
                comments = json.loads(el['comment_exp'])
                comments = comments["comment"]
                tstart = el['start_date'].strftime("%Y-%m-%d %H:%M:%S")
                tstop = el['end_date'].strftime("%Y-%m-%d %H:%M:%S")
                expstatustxt = '<img src="'+esimg[0]+'"/><span style="display:none">'+esimg[1]+'</span>'
                onclick = "onclick='window.open(\""+maindir+"/"+fname+extension+"\", \"\", \"height=800,width=600\")'";
                exptxt = '<a href="#" '+onclick+'>'+fname+'</a>'
                period = el['period']
                #render report summary panel
                morecontent = "<table><tr><td colspan='2' style='padding-bottom: 10px; text-decoration: underline;'>REPORT INFO</td></tr>"
                morecontent += "<tr><td>Period: </td><td style='padding-left: 20px;'>"+period.upper()+"</td></tr>"
                morecontent += "<tr><td>Creation Date: </td><td style='padding-left: 20px;'>"+el['upload_date'].strftime("%Y-%m-%d %H:%M:%S")+"</td></tr>"
                morecontent += "<tr><td>Owner: </td><td style='padding-left: 20px;'>"+user+"</td></tr>"
                morecontent += "<tr><td>Start Date (UTC): </td><td style='padding-left: 20px;'>"+tstart+"</td></tr>"
                morecontent += "<tr><td>End Date (UTC): </td><td style='padding-left: 20px;'>"+tstop+"</td></tr>"
                morecontent += "<tr><td>Configuration File: </td><td style='padding-left: 20px;'>"+el['config_file']+"</td></tr></table>"
                morecontent += "<table><tr><td colspan='2' style='padding-bottom: 10px; text-decoration: underline; padding-top:20px'>FLAG INFO</td></tr>"
                morecontent += "<tr><td>Status: </td><td style='padding-left: 20px;'>"+flagtxt+"</td></tr>"
                morecontent += "<tr><td>Flag Date: </td><td style='padding-left: 20px;'>"+flagdate+"</td></tr>"
                morecontent += "<tr><td>Flag Creator: </td><td style='padding-left: 20px;'>"+el['flaguser']+"</td></tr>"
                morecontent += "<tr><td>Comments: </td><td style='padding-left: 20px;'>"+comments+"</td></tr>"
                morecontent += "</table>"
                action_onclick = "show_rep_info('"+fname+"','"+expstatus+"')"
                actions = '<div class="rep_info" onclick="'+action_onclick+'"><img src="assets/images/info_32.png"/><span style="display:none" id="'+fname+'">'+morecontent+'</span></div>'
                results = {'Flag' : expstatustxt, 'Report' : exptxt, 'Period' :period,'Start Date (UTC)':tstart,
                            'End Date (UTC)' : tstop,'Actions' : actions}
                data.append(results)
        except Exception as e:
            pass
        out = {"sEcho":1,"iTotalRecords":len(data),"iTotalDisplayRecords":len(data),"aaData":data}   
        return out 
      
    def flagged_tables(*args):
        username = args[0]["user"].value
        tbl = args[0].getlist('tbl[]')
        tbl_map = {'datatable-anomalies' : {"mode" : "par", "archive" : "public"}, 
                   'datatable-anomalies1' : {"mode" : "par", "archive" : "user"},
                  'datatable-anomalies2' : {"mode" : "exp", "archive" : "public"},
                   'datatable-anomalies3' : {"mode" : "exp", "archive" : "user"}
                  }        
        out = {}
        for t in tbl:
            mode = tbl_map[t]["mode"]
            if tbl_map[t]["archive"] == "public":
                archive = "public"
            else : 
                archive = username
            
            data = []
            maindir = "users/"
            isuser = False
            ext = ""
            try:
                connconfig = util.repConfig().data['local_db']
                #get running reports list
                dbio = dbIO(connconfig)
                flagged = dbio.get_flagged(mode,archive)
                #render records
                for el in flagged :
                    extension = ""
                    if el['filepath'] != 'stored':
                        isuser = True
                        dir = maindir+el['filepath']+"/stored"
                    else:
                        if el['filetype'] == "report":
                            dir = maindir+"report"
                            extension = ".pdf"
                        else:
                            dir = maindir+"stored"
                    fname = el['filename']
                    user = el['username']
                    expdate = el['date_exp'].strftime("%Y-%m-%d %H:%M:%S")
                    expstatus = el['status_exp']
                    esimg = set_status_img(expstatus)
                    comments = json.loads(el['comment_exp'])
                    
                    if el['exp_tstart'] is not None:
                        tstart = el['exp_tstart'].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        tstart = "-"
                    if el['exp_tstop'] is not None:
                        tstop = el['exp_tstop'].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        tstop = "-"

                    exptype = el['filetype']
                    plotid = el['plot_id']
                    expstatustxt = '<img src="'+esimg[0]+'"/><span style="display:none">'+esimg[1]+'</span>'
                    onclick = "onclick='window.open(\""+dir+"/"+fname+extension+"\", \"\", \"height=800,width=600\")'";
                    exptxt = '<a href="#" '+onclick+'>'+fname+'</a>'
                    try:
                        params = json.loads(el['parinfo'])
                    except:
                        params = {}
                    if mode == "par":
                        if len(params) > 0:
                            for k,v in params.items():
                                psource = v['system']
                                pstatus = set_status_img(v['status'])
                                pstatustxt = '<img src="'+pstatus[0]+'"/><span style="display:none">'+pstatus[1]+'</span>'
                                try:
                                    curr_comm = comments[k]
                                except:
                                    curr_comm = "None"
                                if curr_comm == "None":
                                    curr_comm = ""
                                results = {'Flag' : pstatustxt, 'Parameter' : k, 'System' : psource, 'Experiment' : exptxt, 
                                           'Exp Flag' :expstatustxt,'Experiment Start Date (UTC)':tstart,'Experiment Stop Date (UTC)' : tstop,'Generation Date (UTC)' : expdate}
                                if not isuser:
                                    results.update({'User' : user})
                                results.update({'Comments' : curr_comm})
                                data.append(results)
                    elif mode == "exp":
                        results = {'Flag' : expstatustxt, 'Experiment' : exptxt,
                                    'Exp Type' :exptype,'Experiment Start Date (UTC)':tstart,
                                    'Experiment Stop Date (UTC)' : tstop,'Generation Date (UTC)' : expdate}
                        if not isuser:
                            results.update({'User' : user})
                        hasimg = 1
                        commtxt = ""
                        if len(comments) > 0:
                            for k,v in comments.items():
                                if k != "img":
                                    if exptype == "image":
                                        imgname = k
                                        commtxt += v+"<br/>"
                                    elif  exptype == "report":
                                        commtxt += v+"<br/>"
                                    else:
                                        if v == "None" : v = "-"
                                        commtxt += "<span><b>"+k+": </b></span>"+v+"<br/>"
                                    results.update({"Comments" : commtxt})
                                else:   
                                    hasimg = int(v)
                        else:
                            results.update({"Comments" : "-"})
                        view_link = ""
                        if plotid != 0:
                            onclick_view = "onclick='window.open(\"view_plot.php?id="+str(plotid)+"&s="+el['sourcename']+"\", \"\",\"height=1024,width=1600\")'"
                            view_link = '<a href="#" '+onclick_view+'><img src="assets/images/view_plot_48.png" width="30" title="View plot"/></a>'
                        if exptype == "image":
                            if hasimg == 1:
                                onclick_view = "onclick='window.open(\"image-explorer.php?file="+dir+"/"+imgname+"&isflagged=1\", \"Image-Explorer_"+imgname+"\", \"width=2048,height=1024\")'"
                                view_link='<a href="#" '+onclick_view+'><img src="assets/images/view_img_48.png" width="30" title="View image"/></a>';
                            else:
                                view_link="<img title='Image not available on server(s). Analysis done on local image.' class='download-icon' style='opacity : 0.5' src='assets/images/view_img_48.png'/>"
                        results.update({"Actions" : view_link})     
                        data.append(results)            
                out.update({t : data})
            except Exception as e:
                results = {'Flag' : '', 'Parameter' : 'ERROR - Impossible to get data from local DB', 'System' : '', 'Experiment' : '', 'Exp Flag' :'','Experiment Start Date (UTC)':'','Experiment Stop Date (UTC)' : '','Generation Date (UTC)' : ''}
                if archive == "public":
                    results.update({'User' : ''})
                results.update({'Comments' : ''})
                out.update({t:[results]})

        return out        
            
    def resume_report(*args):
        #get settings       
        username = args[0]["username"].value
        runid = args[0]["runid"].value
        #by default, assign the pid of this script to the experiment, it will be changed later
        resumereport_pid = os.getpid()
        connconfig = util.repConfig().data['local_db']
        dbio = dbIO(connconfig)
        exp_status = dbio.get_report_status(runid)        
        dbio.update_running_reports(-resumereport_pid, runid, status=-99.0)        
                
        configfile = args[0]["configfile"].value
        period = args[0]["period"].value
        t0 = args[0]["start_time"].value
        #convert datetime to timestamp
        try:
            t0_stamp = util.format_date(t0)
        except:
            t0_stamp = None
        url = args[0]["iodaurl"].value
     
        #get email from DB
        connection = util.connect_db(connconfig)
        email = util.get_email(connection, username)
        #update history
        if exp_status == -100:
            msg = "Resumed report generation"
        else:
            msg = "Restarted report generation"
             
        util.update_history(connection, username, msg, input="NA", output='{"Run ID" : "'+str(runid)+'", "Configuration file": "'+configfile+'", "Action by": "'+username+'"}', config="NA")
        connection.close()
        cmd=sys.executable + " generate_report.py -c "+configfile+" -u "+username+" -p "+period+" -w "+url+" -r "+str(runid)+" -e "+email
        if t0_stamp is not None:
            cmd += " -t "+str(t0_stamp)
        os.system(cmd)

    def set_labels(*args):
        adu = args[0]["adu"].value
        par = args[0]["par"].value
        s = args[0]["s"].value
        o = args[0]["o"].value
        connconfig = util.repConfig().data['local_db']
        if adu == "True":           #calibrated
            conn = util.connect_db(connconfig)        
            qres = util.db_query(conn, o+"_"+s.lower()+"_params", "units", "WHERE param = '"+par+"'", res_type="one")
            if qres["units"] is not None:
                result = {"units" : "("+qres["units"]+")"}
            else:
                result = {"units" : "(no units)"}
        else:
            result = {"units" : "(ADU)"}
        return result        
        
    def view_plot_from_db(data):
        #get plot id        
        plotid = data["plotid"].value
        connconfig = util.repConfig().data['local_db']
        conn = util.connect_db(connconfig)        
        result = util.db_query(conn, "stored_plots", "*", "WHERE id = "+plotid, res_type="one")               

        return result
        
    def flagged_images(data):
        user = data['user'].value
        fullname = data['filename'].value
        filename = fullname.split("/")[-1]
        connconfig = util.repConfig().data['local_db']
        conn = util.connect_db(connconfig)
        data = []
        if user == "all":
            #public table
            result = util.db_query(conn, "stored_files", "username, status_exp, comment_exp", "WHERE parinfo = '"+filename+"'")
            for el in result:
                comment_col = json.loads(el["comment_exp"])
                comment = comment_col[filename]
                flag_arr = set_status_img(el["status_exp"])
                flag = "<img src='"+flag_arr[0]+"' width='18px'/><span style='display:none'>"+flag_arr[1]+"</span>"
                data.append({"Flag" : flag, "User" : el["username"], "Notes" : comment})
        else:
            #private table
            result = util.db_query(conn, "user_files", "status_exp, comment_exp", "WHERE parinfo = '"+filename+"' AND username = '"+user+"'")
            for el in result:
                comment_col = json.loads(el["comment_exp"])
                comment = comment_col[filename]
                flag_arr = set_status_img(el["status_exp"])
                flag = "<img src='"+flag_arr[0]+"' width='18px'/><span style='display:none'>"+flag_arr[1]+"</span>"
                data.append({"Flag" : flag, "Notes" : comment})
        out = {"sEcho":1,"iTotalRecords":len(data),"iTotalDisplayRecords":len(data),"aaData":data}

        return out

    def update_systems(data):
        out = {"data" : data}
        return data

def set_status_img(status):
    imgdir = "assets/images/"
    if status == "Not Defined":
        status = "nd"
    smap =  {"nd" : "0", "ok" : "1", "warning" : "2", "serious" : "3"}
    img = imgdir+status+".png"
    imid = smap[status]
    return img, imid
        
def main(data):
    try:
        action = data['action'].value
        method = getattr(Interfaces, action)
        out = method(data)        
    except Exception as e:
        out={"error":str(data)}
    
    print(json.JSONEncoder().encode(out))

if __name__ == "__main__":
    print("Content-Type: application/json")
    print()
    
    #the cgi library gets vars from html
    data = cgi.FieldStorage()
    
    main(data)