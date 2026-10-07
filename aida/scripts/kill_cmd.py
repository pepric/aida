#!/usr/bin/python

"""
Process Termination CLI Utility.

This module provides command-line functions to terminate a running report 
process tree and its child processes using psutil.

@package AIDA
@module kill_cmd
"""

import argparse
import sys
import psutil


def main(pid, runid):
    """Terminate parent process and all recursive child processes for a report job.

    Parameters
    ----------
    pid : int
        Process ID of the parent report generation job.
    runid : str
        Unique run identifier string for the experiment.
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