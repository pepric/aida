#!/usr/bin/python

import cgi, cgitb 
import json
import sys
import os
from shutil import rmtree
import functions as util
import db_io
from send_mail import Email


def stop_report_email(user, mailadmin, out, runid):
	mailconfig = Email("../smtp.json")
	subject = "Report generation stopped"
	fromuser = "AIDA"
	to = mailadmin    
	text = mailconfig.stop_report_text(user, out, runid)
	msg = mailconfig.set_message(subject,fromuser,to,text)
	mailconfig.send_mail(msg)    
			   

def main(data):
	"""Kill report generation.
	Parameters
	----------
	data : cgi.FieldStorage,
		Contains all data coming from client side script: pid, runid, config file name, username
	"""        
	error = 0
	pid= data['pid'].value
	runid = data['runid'].value
	configfile = data['configfile'].value
	action = data['action'].value
	user = data['user'].value

	workdir = "../users/report/temp_id"+str(runid)   
   
	#get connection parameters
	conf = util.repConfig()
	out = {}
	error = 0
	msg = ""    
	if conf.error == 0:
		connconfig = conf.data['local_db']
		dbio = db_io.dbIO(connconfig)
		#connect to AIDA DB
		locerr, connection = dbio.connect()
		if locerr == 1:
			out = {"error" : 1, "msg" : "Impossible to connect to local DB."}    
			print(json.JSONEncoder().encode(out))
			exit()  

		#kill pid
		cmd=sys.executable + " kill_cmd.py -p "+str(pid)+" -r "+str(runid)
		os.system(cmd)
		if action != "remove":
			try:  
				f = open(workdir+"/procstatus.txt","r")
				canceled = f.read()
				f.close()
				if canceled == "False":
					out.update({"error" : 1, "msg" : "Impossible to stop process with PID = "+str(pid)+"."})
					print(json.JSONEncoder().encode(out))  
					exit()
				elif canceled == "True":
					pass
				else:
					error = 2
					msg = "Subprocesses with pids = "+str(canceled)+" are still running."            
			except:
				pass

		#open config file        
		fileobj = open("../users/config/"+configfile, "r")
		jsonstr = fileobj.read()
		fileobj.close()
		#change slashes
		jsonstr = jsonstr.replace("\\","/")
		#convert input string to json object
		repdata = json.loads(jsonstr)          

		if action != "remove":
			try:              
			#remove report tmp directory
				rmtree(workdir)
			except:
				#if directory still exists
				if os.path.isdir(workdir):
					if error == 2:
						msg += "\n"
					msg += "Impossible to remove report temporary directory"
					error = 2
		try:            
		#set config file isrunning = 0
			if action == "kill" or action == "remove":
				isrunning = 0
				sd = repdata["General Info"]["Start Time"]
				util.update_history(connection, user, "Report generation stopped", input="NA", output='{"Run ID" : "'+str(runid)+'", "Configuration file": "'+configfile+'", "Action by": "'+user+'"}', config="NA")                
			elif action == "pause":
				isrunning = 3
				sd = None
				util.update_history(connection, user, "Report generation paused", input="NA", output='{"Run ID" : "'+str(runid)+'", "Configuration file": "'+configfile+'", "Action by": "'+user+'"}', config="NA")                  
			dbio.update_config_files(configfile, isrunning, start_date=sd, keep_open=True)
		except Exception as e:
			if error == 2:
				msg += "\n"
			msg += "Impossible to update config file status"
			msg += "\n"+e
			error = 2
		try:            
			#remove record from running reports
			if action == "kill" or action == "remove":
				dbio.remove_running_report(runid, keep_open=True)
            #or update to "pause"
			elif action == "pause":
				dbio.update_progress(runid, percent = "final")
				dbio.update_progress(runid, percent = -200)				
			
		except:
			if error == 2:
				msg += "\n"
			msg += "Impossible to update running reports status"
			error = 2
            
		out.update({"error" : error, "msg" : msg})          

		allok = True
		try:
			dbio.close()
		except:
			pass
	else:     
		out.update({"error" : 1, "msg" : "Impossible to read local DB settings."})
		allok = False
        
	if allok and (action == "kill" or action == "remove"):
        #send email to admin
		try:        
			mailadmin = conf.data["admin_email"]
			stop_report_email(user, mailadmin, out, runid)
		except:
			pass

	print(json.JSONEncoder().encode(out))	

if __name__ == "__main__":
	print("Content-Type: application/json")
	print()

	#the cgi library gets vars from html
	data = cgi.FieldStorage()

	main(data)