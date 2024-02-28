#!/usr/bin/python

import json
import cgi, cgitb 
cgitb.enable()  # for troubleshooting
import glob
import os
from functions import db_query, read_db_config, connect_db, repConfig

class Tree():
	def __init__(self, data):
		self.dir = data['maindir'].value
		self.ext = data.getlist('ext[]')
		self.link = int(data['link'].value)
		self.report_rootdir = [{"id" : "daily", "parent" : "#", "text" : "daily"},{"id" : "monthly", "parent" : "#", "text" : "monthly"},{"id" : "weekly", "parent" : "#", "text" : "weekly"}, {"id" : "ondemand", "parent" : "#", "text" : "ondemand"}, {"id" : "custom", "parent" : "#", "text" : "custom"}]		
		self.img_rootdir = [{"id" : "public", "parent" : "#", "text" : "Public Flagged"},{"id" : "private", "parent" : "#", "text" : "Private Flagged"},{"id" : "temp", "parent" : "#", "text" : "Temporary"}]		        
		try:
			self.user = data['user'].value
		except:
			self.user = None

	def build_query(self):
		sections = ["stored", "report", "config"]
		statement = ""
		if self.dir not in sections:
			#table = "tmp_files"
			table = "user_files"
			storedby = "'"+ self.dir+"'"
			statement = "WHERE username = "+storedby
			if len(self.ext)>0:
				statement += " AND "
		else :
			table = self.dir+"_files"
			if len(self.ext)>0:
				statement = "WHERE "
				
		if len(self.ext)>0:
			statement += "(ext = '"+self.ext[0]+"'"
			for i in range(1, len(self.ext)):
				statement += " OR ext = '"+self.ext[i]+"'"
			statement += ")"
		statement += " ORDER BY id DESC"

		return table, statement

	def create_stored_html(self, db):
		
		try:
			currlist = db[0].get('filepath')
		except:
			currlist=""
		
		dicttmp = {}
		dictimg = {}
		dictdoc = {}		

		for n in db:
			if n.get('status_exp') is not None:
				status_val = n.get('status_exp')
				status = 1
			else:
				status_val = ""
				status = 0
		
			curr_item = {'name' : n.get('filename'), 'type' : n.get('filetype'), 'path' : n.get('filepath'), 'ext' : n.get('ext'), 'status' : status_val}
			
			if n.get('filetype') == 'document':
				l = len(dictdoc)
				dictdoc.update({'item'+str(l+1) : curr_item})
			elif n.get('filetype') == 'image':
				l = len(dictimg)
				dictimg.update({'item'+str(l+1) : curr_item})
			elif n.get('filetype') == 'tmp':
				l = len(dicttmp)
				dicttmp.update({'item'+str(l+1) : curr_item})
		
		listdoc = self.create_file_list(dictdoc, 'docs')
		listimg = self.create_file_list(dictimg, 'images')
		if currlist != "stored":
			listtmp = self.create_file_list(dicttmp, 'temp')
		else:
			listtmp = ""

		listhtml = listdoc+listimg+listtmp
		
		return listhtml
		
	def create_file_list(self, mydict, folder):
		if folder == "config":
			opened = "true"
		else:
			opened = "false"
		
		listhtml = "<ul><li data-jstree='{ \"opened\" : "+opened+" }' class='folder'>"+folder+"<ul>"
		for i in range(len(mydict)):
			curr_item = mydict['item'+str(i+1)]
			#define icon
			status = curr_item['status']
			if status != "":
				jstreetag='"icon": "assets/images/'+status+'.png"'
			elif status == "nd":
				jstreetag='"icon": "assets/images/nd.png"'
			else:
				jstreetag='"icon": "assets/images/'+curr_item['type']+'.png"'

			#get name
			fname = curr_item['name']
			if len(fname)>33:
				filename = fname[:33]+"..."
			else:
				filename = fname
			
			#get file path
			filepath = curr_item['path']
			#add extension to fname if report
			if filepath == "report":
				fname+="."+curr_item['ext']
	
			#get file type
			ftype = curr_item['type']
			if self.link == 1 :
				if ftype == "image":
					onclick = ""
				else:
					onclick = 'window.open("users/'+filepath+'/'+fname+'", "", "height=800,width=600")'
			listhtml += "<li data-jstree='{"+jstreetag+"}'><a onclick='"+onclick+"'>"+filename+"</a></li>"
		listhtml += "</ul></li></ul>"
		
		return listhtml
		
	def create_config_html(self, db):	
		
		dictondemand = {}
		dictweek = {}
		dictmonth = {}
		dictcustom = {}		
		#dictconf = {}
		for n in db:
			if n.get('status_exp') is not None:
				status_val = n.get('status_exp')
				status = 1
			else:
				status_val = ""
				status = 0
		
			curr_item = {'name' : n.get('filename'), 'type' : n.get('filetype'), 'path' : n.get('filepath'), 'ext' : n.get('ext'), 'status' : status_val, 'period' : n.get('period')}
			if n.get('period') == 'monthly':
				l = len(dictmonth)
				dictmonth.update({'item'+str(l+1) : curr_item})
			elif n.get('period') == 'weekly':
				l = len(dictweek)
				dictweek.update({'item'+str(l+1) : curr_item})
			elif n.get('period') == 'ondemand':
				l = len(dictondemand)
				dictondemand.update({'item'+str(l+1) : curr_item})
			elif n.get('period') == 'custom':
				l = len(dictcustom)
				dictcustom.update({'item'+str(l+1) : curr_item})                
		
		listm = self.create_file_list(dictmonth, 'monthly')
		listw = self.create_file_list(dictweek, 'weekly')
		listd = self.create_file_list(dictondemand, 'on demand')
		listc = self.create_file_list(dictcustom, 'custom')        
		listhtml = listm+listw+listd+listc
		
		return listhtml		

	def create_report_html(self, db):
		
		dictondemand = {}
		dictweek = {}
		dictmonth = {}
		dictcustom = {}

		for n in db:
			curr_item = {'name' : n.get('filename'), 'type' : n.get('filetype'), 'path' : n.get('filepath'), 'ext' : n.get('ext'), 'status' : "", 'period' : n.get('period')}
			if n.get('period') == 'monthly':
				l = len(dictmonth)
				dictmonth.update({'item'+str(l+1) : curr_item})
			elif n.get('period') == 'weekly':
				l = len(dictweek)
				dictweek.update({'item'+str(l+1) : curr_item})
			elif n.get('period') == 'ondemand':
				l = len(dictondemand)
				dictondemand.update({'item'+str(l+1) : curr_item})
			elif n.get('period') == 'custom':
				l = len(dictcustom)
				dictcustom.update({'item'+str(l+1) : curr_item})
		
		listm = self.create_file_list(dictmonth, 'monthly')
		listw = self.create_file_list(dictweek, 'weekly')
		listd = self.create_file_list(dictondemand, 'on demand')
		listc = self.create_file_list(dictcustom, 'custom')
		listhtml = listm+listw+listd+listc
		
		return listhtml		

	def create_html(self, db):
		
		listhtml = "<ul><li data-jstree='{ \"opened\" : true }' class='folder'>"+self.dir+"<ul>"
		listfile = []
		listpath = []
		listtype = []
		listext = []
		liststatus = []

		for n in db:
			listfile.append(n.get('filename'))
			listtype.append(n.get('filetype'))
			listpath.append(n.get('filepath'))
			listext.append(n.get('ext'))
			if n.get('status') is not None:
				liststatus.append(n.get('status'))
				status = 1
			else:
				status = 0
	
		onclick = ""
		jstreetag='"icon": "assets/images/png_icon.png"'
		
		for i in range(len(listfile)):
			fname = listfile[i]
			if len(fname)>33:
				filename = fname[:33]+"..."
			else:
				filename = fname
			
			if status == 0:
				ftype = listtype[i]
				jstreetag='"icon": "assets/images/file.png"'
				if ftype != "":
					jstreetag='"icon": "assets/images/'+listtype[i]+'.png"'
				else:
					jstreetag='"icon": "assets/images/file.png"'
			else:
				jstreetag='"icon": "assets/images/'+liststatus[i]+'.png"'
			
			f = "users/"+self.dir+"/"+fname
			
			if self.link == 1 :
				if ftype == "image":
					onclick = ""
				else:
					onclick = 'window.open("users/'+listpath[i]+'/'+fname+'", "", "height=800,width=600")'
			listhtml += "<li data-jstree='{"+jstreetag+"}'><a onclick='"+onclick+"'>"+filename+"</a></li>"
		listhtml += "</ul></li></ul>"
		
		return filename, listhtml

	def create_stored_json(self, db):
		jsonout = [{"id" : "image", "parent" : "#", "text" : "images"}, {"id" : "report", "parent" : "#", "text" : "reports"}, {"id" : "plot", "parent" : "#", "text" : "plots"}, {"id" : "statistics", "parent" : "#", "text" : "statistics"}, {"id" : "model", "parent" : "#", "text" : "ML models"}, {"id" : "data", "parent" : "#", "text" : "ML outputs"}]		
		for n in db:
			status_val = n.get('status_exp')
			fileicon = "assets/images/"+status_val+".png"
			id = n.get('id')
			fname = n.get('filename')
			filepath = n.get('filepath')
			ftype = n.get('filetype')
			if filepath != "stored":
				filepath = n.get('username')+"/stored"
				
			if ftype == "data" or ftype == "model":
				onclick = 'window.open("users/'+filepath+'/'+fname+'")'
			else: 
				onclick = 'window.open("users/'+filepath+'/'+fname+'", "", "height=800,width=600")'			
			jsonout.append({"id" : id, "parent" : ftype, "text" : fname, "icon" : fileicon, "a_attr":{"onclick" : onclick}})			

		return jsonout

	def create_report_json(self, db):	
		jsonout = self.report_rootdir
		for n in db:
			ext = n.get('ext')
			fileicon = "assets/images/"+ext+".png"
			id = n.get('id')
			fname = n.get('filename')
			period = n.get('period')
			jsonout.append({"id" : id, "parent" : period, "text" : fname, "icon" : fileicon, "a_attr":{"onclick" : 'window.open("users/report/'+fname+'.'+ext+'", "", "height=800,width=600")'}})

		return jsonout

	def create_config_json(self, db):	
		jsonout = self.report_rootdir
		for n in db:
			iscomplete = n.get('iscomplete')
			if iscomplete == 1:
				ext = n.get('ext')
				fileicon = "assets/images/"+ext+".png"
				id = n.get('id')
				fname = n.get('filename')
				period = n.get('period')
				jsonout.append({"id" : id, "parent" : period, "text" : fname, "icon" : fileicon, "a_attr":{"onclick" : 'window.open("users/config/'+fname+'", "", "height=800,width=600")'}})

		return jsonout

	def create_img_json(self,db, tbl, startimg = "None"):
		jsonout = []
		isflagged = 0
		if tbl == "stored_files":
			parent = "public"
			isflagged = 1
		elif tbl == "user_files":
			parent = "private"
			isflagged = 1            
		elif tbl == "local_files":
			parent = "temp"
		for n in db:
			try:
				hasimg = int(json.loads(n.get('comment_exp'))['img'])
			except:
				#raised when queried temp image file
				hasimg = 1
			if hasimg:
				status_val = n.get('status_exp')
				if status_val is not None:
					fileicon = "assets/images/"+status_val+"_18.png"
				else:
					fileicon = "fa fa-file"
				id = n.get('id')
				fname = n.get('filename')
				filepath = n.get('filepath')
				ftype = n.get('filetype')
				if filepath is None:
					filepath = n.get('username')+"/tmp/"+n.get("data_source").lower()
					imgfile = fname
					id = "t"+str(id)
				elif filepath != "stored":
					filepath = n.get('username')+"/stored"
					imgfile = n.get('parinfo')
					id = "u"+str(id)
				else:
					imgfile = n.get('parinfo')
					id = "s"+str(id)
					
				#JS9 OPEN
				onclick = 'window.location.href = "image-explorer.php?file=users/'+filepath+'/'+imgfile+'"'            
				jsonout.append({"id" : id, "parent" : parent, "text" : fname, "icon" : fileicon, "a_attr":{"onclick" : onclick}})			
		
		return jsonout
        
	def build_img_sql(self, t):
		sections = ["stored", "report", "config"]
		sql_dict = {}
		for tbl in t:
			statement = "WHERE filetype = 'image'"
			table = tbl+"_files"
			if tbl not in sections:
				statement += " AND username = '"+self.user+"'"              
			statement += " ORDER BY id DESC"
			sql_dict.update({table : statement})

		return sql_dict              
              
def main(data):
	#Instantiate tree object
	t = Tree(data)
	dir = t.dir

	link = t.link
	config = repConfig()    
	try:
		startimg = data['startimg'].value
	except:
		startimg = "None"
   
	if dir == "image":
		try:
			connection = connect_db(config.data['local_db'])
			out = t.img_rootdir
			tbls = ["stored", "user", "local"]
			sqls = t.build_img_sql(tbls)
			for tbl, sql in sqls.items():
				x = db_query(connection, tbl, "*", sql, "all")
				listhtml = t.create_img_json(x, tbl, startimg)
				for el in listhtml:
					out.append(el)

			print(json.JSONEncoder().encode(out))            
			connection.close()
		except Exception as e:
			print(json.JSONEncoder().encode({"error" : str(e)}))          
	else:
		#Connect to AIDA DB and download file list and infos
		try:    
          	#build the query to download file list
			table, statement = t.build_query()
			connection = connect_db(config.data['local_db'])
			x = db_query(connection, table, "*", statement, "all")
			connection.close()	
	
			dicttmp = {}
			dictimg = {}
			dictdoc = {}	
	
			if dir == "report":
				listhtml = t.create_report_json(x)
			elif dir == "config":
				listhtml = t.create_config_json(x)
			else:
				listhtml = t.create_stored_json(x)

			print(json.JSONEncoder().encode(listhtml))
		except:
			print(json.JSONEncoder().encode({"error" : 1}))

if __name__ == "__main__":
	#print("Content-Type: text/plain;charset=utf-8")
	print("Content-Type: application/json")
	print()
	
	#the cgi library gets vars from html
	data = cgi.FieldStorage()
	
	main(data)