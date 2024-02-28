#!/usr/bin/python

import cgi, cgitb 
cgitb.enable()  # for troubleshooting
from functions import db_query, connect_db, repConfig
import json

def main(data):
    """Create HTML output to list history entries.
    Parameters
    ----------
    data : cgi.FieldStorage,
        Contains all data coming from client side script: user 
    """     
    user = data['user'].value

    #if user is "global", get all entries from DB    
    if user == "global":
        statement = "ORDER BY UNIX_TIMESTAMP(date_time) DESC"
    else:
        statement = "WHERE username = '"+user+"' ORDER BY UNIX_TIMESTAMP(date_time) DESC LIMIT 100"
        
    #get local DB config    
    config = repConfig()
    #connect to local DB
    try:    
        connection = connect_db(config.data['local_db'])
        x = db_query(connection, "history", "*", statement, "all")
        connection.close()
        error = 0
    except:
        error = 1

    if error == 0:        
        dateformat = '%Y-%m-%dT%H:%M:%S'
        listhtml = "<ul>"
        onclick = ""
        n_user = ""
        #for each entry, build history line
        for n in x:
            n_date = n.get('date_time').strftime(dateformat)
            n_id = str(n.get('id'))
            onclick = "show_hist_info("+n_id+",\""+user+"\")"
            
            #Populate info box with DB data
            morecontent = "<table class='tbl_hist_info'><tr><td>Date: </td><td style='padding-left: 20px;'>"+ n_date.replace("T"," ") + "</td></tr>"
           
            if user == "global":
                n_user = n.get('username')

                morecontent += "<tr><td>User: </td><td style='padding-left: 20px;'>"+ n_user +"</td></tr>"
        
            morecontent += "<tr><td>Operation: </td><td style='padding-left: 20px;'>"+ n.get('operation') +"</td></tr>"
            #additional infos
            outdata = n.get('output')
            if outdata is not None:  
                if outdata != "NA":
                    info = json.loads(outdata)
                    for k,v in info.items():
                        morecontent += "<tr><td>"+k.capitalize()+":</td><td style='padding-left: 20px;'>"+str(v).replace(",",", ")+"</td></tr>"

            settings = n.get('configuration')
            if settings is not None:
                if settings != "NA":
                    try:
                        info = json.loads(settings)
                        for k,v in info.items():
                            morecontent += "<tr><td>"+k.capitalize()+":</td><td style='padding-left: 20px;'>"+str(v).replace(",",", ")+"</td></tr>"
                    except:
                        pass
                        
            morecontent += "</table>"
            # build id and string for global or user            
            if user == "global":
                pref = "hg"
                aid = pref+n_id
                str_user = "  -  " + n_user
            else:
                pref = "hu"
                aid = pref+n_id
                str_user = n_user
            
            line = n_date + str_user + "  :   " + n.get('operation')
            #final HTML        
            listhtml += "<li class=\"dashrecord\"><span style='display : none' id='more-"+pref+"-"+n_id+"'>"+morecontent+"</span><a id='"+aid+"'onclick='"+onclick+"'>"+line+"</a></li>"
    
        listhtml += '</ul>'
    else:
        listhtml = '<p>Unable to retrieve History data. Please retry or contact AIDA admin.</p>'      
    print(listhtml)


if __name__ == "__main__":
    print("Content-Type: application/json")
    print()
    
    #the cgi library gets vars from html
    data = cgi.FieldStorage()

    main(data)