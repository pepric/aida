#!/usr/bin/python

import argparse
import sys
import psutil


def main(pid, runid):
	"""Kill report generation process by pid.
	Parameters
	----------
	pid : int,
		Program identifier assigned by OS to the report generation program
	runid: str,
		Run identifier, assigned by the program to the report generation
	"""    
	workdir = "../users/report/temp_id"+runid+"/" 
	try:
		#get parent process      
		parent = psutil.Process(pid)
		#get all children processes        
		procs = parent.children(recursive=True)
		for p in procs:
			#terminate children          
			p.terminate()
		#wait some time to let the process close            
		gone, alive = psutil.wait_procs(procs, timeout=3)
	
		for p in alive:
			#kill still alive processes        
			p.kill()
		#kill parent process            
		parent.kill()
		if len(alive) > 0:
			#if some processes survived, report it to the gui          
			out = alive
		else:
			out = True          	
	except:
		out = False
	#save output in temporary file
	with open(workdir+"procstatus.txt","w") as f:
		f.write(str(out))      

if __name__ == "__main__":

	parser = argparse.ArgumentParser(prog = sys.executable +' kill_cmd.py')

	parser.add_argument('-p', '--pid', metavar="PID", help='PID')
	parser.add_argument('-r', '--runid', metavar="RunID", help='RunID')

	args = parser.parse_args()

	pid = int(vars(args)['pid'])
	runid = vars(args)['runid']
	main(pid, runid)