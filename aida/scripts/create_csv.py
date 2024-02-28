#!/usr/bin/python

import json
import cgi, cgitb 
cgitb.enable(display=0, logdir="cgi-logs")  # for troubleshooting
import csv

def main(data):
	"""Create csv file of plotted data.
	Parameters
	----------
	data : cgi.FieldStorage,
		Contains all data coming from client side script: parameters values and labels, output file name, app url
	"""  
	#Get Data Source
	labels = data.getlist('labels[]')
	values = json.loads(data['indata'].value)
	filename = data['filename'].value
	fromurl = data['iodaurl'].value

	localname = "../tmp/"+filename

	#if X label is None, then X is the date    
	if labels[0] == "None":
		labels[0] = "DATETIME"
		l=labels
		hasx = False
	else:
		l = ["DATETIME"]
		for i in labels:
			l.append(i)
		hasx = True

	#store data in csv
	with open(localname, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(l)
		for i in range(len(values['date'])):
			row = [values['date'][i]]
			if hasx:
				if values['x'][i] != "-999.0":
					row.append(values['x'][i])
				else: row.append("")
			for j in range(1,len(labels)):
				if values["y"+str(j-1)][i] != "-999.0" :              
					row.append(values["y"+str(j-1)][i])
				else: row.append("")
                  
			writer.writerow(row)

	#Set name of remote file to download
	fromurl_arr = fromurl.split("/")
	fromurl_arr = fromurl_arr[:-1]
	remotename = "/".join(fromurl_arr)+"/tmp/"+filename
	out = {"url" : remotename}
	print(json.JSONEncoder().encode(out))

	
if __name__ == "__main__":
	print("Content-Type: application/json")
	print()

	#the cgi library gets vars from html
	data = cgi.FieldStorage()

	main(data)