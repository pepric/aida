#!/usr/bin/python

"""
Report Generation Request Handler.

This module serves as the CGI entry point to initiate report generation 
jobs, recording the running job in the database and invoking the background 
report pipeline.

@package AIDA
@module run_report
"""

import cgi, cgitb 
cgitb.enable()  # for troubleshooting
from    os              import system, getpid
import datetime
import sys
import functions as util


def main(data):
    """Start a new background report generation job and log run in database.

    Parameters
    ----------
    data : cgi.FieldStorage
        HTTP POST request payload containing username, periodicity mode, 
        configuration filename, running state flag, and application URL.
    """      
    #get input values   
    user = data['user'].value
    period = data['period'].value
    configfile = data['config'].value
    isrunning = int(data['isrunning'].value)
    if isrunning == 2:
        exp_status = -102
    else:
        exp_status = -99
    url = data['iodaurl'].value
    now = util.utc_now().strftime("%Y-%m-%d %H:%M:%S") #current UTC datetime
    #by default, assign the pid of this script to the experiment, it will be changed later    
    runreport_pid = getpid()
    
    #create record in running_reports table in AIDA DB
    connconfig = util.repConfig().data['local_db']
    connection = util.connect_db(connconfig)
    sql="INSERT INTO running_reports (username, config_file, run_date, period, exp_status, pid) VALUES ('"+user+"', '"+configfile+"', '"+now+"', '"+period+"', "+str(exp_status)+","+"-"+str(runreport_pid)+")"
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()
    runid = cursor.lastrowid
    #get user email          
    email = util.get_email(connection, user)
    connection.close()      
    #run generation
    cmd=sys.executable + " generate_report.py -c "+configfile+" -u "+user+" -p "+period+" -w "+url+" -r "+str(runid)+" -e "+email+" >logs/log_"+str(runid)+".log 2>&1"
    system(cmd)

if __name__ == "__main__":
    print("Content-Type: application/json")
    print()
    
    data = cgi.FieldStorage()
    main(data)