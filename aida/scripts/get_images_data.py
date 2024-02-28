#!/usr/bin/python

import json
import numpy as np
import cgi, cgitb 
cgitb.enable(display=0, logdir="cgi-logs")   # for troubleshooting
import functions as util

def get_file_list(data,e):
    source = data['source'].value
    ny = int(data['ny'].value)
    usecase = 'image'
    conf = util.repConfig(source,usecase)
    connmsg={}
    result = {}
    if conf.error == 0:
        lmain = len(conf.main)
        curr_main = util.set_path(conf.root[-lmain:-1])
        if curr_main != conf.main:
            e.mainstatus = 1        
        nthreads = int(conf.sourcedata.get('nprocs',1))
        result, e = conf.repclass[usecase].retrieve_image_list(conf, e, data)
    else:
        e.confstatus = 1    
    
    return result

def main(data):

    e = util.statusMsg()
    action = data['action'].value
    if action == "get_file_list":
        result = get_file_list(data,e)
        status = e.get_status()
        result.update({"errors" : {}})
        result["errors"].update({"errstatus" : status[0]})
        result["errors"].update({"warningstatus" : status[1]})
        result["errors"].update({"datastatus" : status[2]})
        result["errors"].update({"infostatus" : status[3]})
        result["errors"].update({"msg" : e.error})
        result["errors"].update({"infomsg" : e.info})  
        print(json.JSONEncoder().encode(result))

if __name__ == "__main__":
    print("Content-Type: application/json")
    print()
    #the cgi library gets vars from html
    data = cgi.FieldStorage()
    
    main(data)