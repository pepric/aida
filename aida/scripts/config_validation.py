#!/usr/bin/python

import cgi, cgitb 
cgitb.enable(display=0, logdir="cgi-logs")  # for troubleshooting
import numpy as np
import json
import datetime
import functions as util
import classes
debug = 1

class configCheck():
    def __init__(self, text, period):
        period_map = {"custom" : 0, "ondemand" : 0, "daily" : 24, "weekly" : 168, "monthly" : 720}
        self.msg = ""
        self.text = text
        self.period = period
        self.default_tw = period_map[period]
        self.connpars = util.get_localdb_info()
        self.allowed_plots = None
        self.allowed_stats = None
        self.listplots = None
        self.liststats = None
        self.allowed_subs=None
        self.subs_detector = None
        self.connection = util.connect_db(self.connpars)
        
    def __get_branch(self, leaves):
        root = self.text
        tree = ""  
        for item in leaves:       
            if item != "":
                root = root[item]
                tree += item+"/"
        return root, tree
        
    def check_allowed(self, keys, allowed):
        check = True
        msgarr = []
        for k in keys:
            if k not in allowed:
                msgarr.append('Key Error! "'+k+'" is not an allowed key\n')
                
            #temporary addition to avoid EFD in configuration files
            # if k == "EFD":
                # msgarr.append('Key Error! "'+k+'" system is not currently enabled for reports\n')            
        
        if len(msgarr)>0:
            check = False
       
        return check, msgarr

    def check_bins(self, root, tree):
        isvalid = True
        msg=""
        if "Bin Size" in list(root.keys()):
            #check if it is a float >0
            try:
                val = float(root["Bin Size"])
                if val <= 0:
                    isvalid = False
                    msg = "Value Error! \"Bin Size\" is a number not greater than 0 in "+tree+"\n"
            except:
                isvalid = False
                msg = "Value Error! \"Bin Size\" is a not number in "+tree+"\n"
        else:
            #check if it is an integer
            try:
                val = int(root["Number of Bins"])
                #check if it is a float
                if str(val)!=str(root["Number of Bins"]):
                    isvalid = False
                    msg = "Value Error! \"Number of Bins\" is not an integer in "+tree+"\n"
                #check if it is >1
                else:
                    if val <= 1:
                        isvalid = False
                        msg = "Value Error! \"Number of Bins\" is not greater than 1 in "+tree+"\n"
            except:
                isvalid = False
                msg = "Value Error! \"Number of Bins\" is not an integer in "+tree+"\n"
                
        return isvalid, msg      

    def check_composed_par(self, item, tpl_arr, extra_tpl, tree, extra_name):

        check = True
        msg = ""
        tree_arr = tree.split("/")
        source = tree_arr[0]
        origin = tree_arr[1]
        curr_add = item.split(".")
        #check that parameter has the same length of template
        if len(curr_add) != len(tpl_arr):
            msg = 'Value Error! "'+extra_name+'" elements must be in the form: '+extra_tpl+ ' in '+tree+"\n"
            return False, msg   
        if tpl_arr[0] == "sub":
            next_for_id = 1
            #first element of additional parameter tree must be the subsystem
            curr_sub = curr_add[0]
            checksub, msgsub = self.check_allowed([curr_sub], self.allowed_subs)
            if checksub:
                k_idx = np.where(np.array(self.allowed_subs)==curr_sub)[0][0]
            else:
                msg = 'Value Error! Invalid Sub-system key '+curr_sub+' for "'+extra_name+'" in '+tree+"\n"
                return False, msg
        else:
            curr_sub = tree_arr[1]
            next_for_id = 0
            k_idx = np.where(np.array(self.allowed_subs)==curr_sub)[0][0]
        
      
        
                      
        check_par = False
        for i in range(next_for_id,len(tpl_arr)):          
            curr2check = curr_add[i]
            if tpl_arr[i] == "det":
                checkdet= self.check_detectors(curr_sub, [curr2check], curr_det_prefix)
                if not checkdet['isvalid']:
                    msg = 'Value Error! Invalid detector '+curr2check+' for "'+extra_name+'" in '+tree+"\n"
                    return False, msg
            elif tpl_arr[i] == "par":
                #get list par for additional parameter keys
                curr_inst = classes.sys_inst(source)
                stat=""
                if tpl_arr[0] == "sub":
                    stat = "WHERE subsystem='"+curr_sub+"'"
                    if i!=0:
                        if tpl_arr[i-1] == "field":
                            stat += " AND extra='"+curr_add[i-1]+"'"
                    
                listpar, listval = curr_inst.get_params_list(origin, self.connection,stat)
                check_par = curr2check in listpar
                if not check_par:
                    msg = 'Value Error! Parameter '+curr2check+' is not allowed for "'+extra_name+'" in '+tree+"\n"
                    return False, msg
                else:
                    par = curr2check
            elif tpl_arr[i] == "val":
                #check if parameter has been previously defined
                if not check_par:
                    msg = 'Value Error! Parameter name must be defined before Value = '+curr2check+' for "'+extra_name+'" in '+tree+"\n"
                    return False, msg
                else:
                    id = listpar.index(par)
                    if listval[id] == []:
                        msg = 'Value Error! No available Values for Parameter = '+par+' in "'+extra_name+'" defined in '+tree+"\n"
                        return False, msg
                    else:
                        check_val = curr2check in listval[id]
                        if not check_val:
                            msg = 'Value Error! Value not allowed for "'+extra_name+'" in '+tree+"\n"
                            return False, msg
            elif tpl_arr[i] == "field":
                curr_inst = classes.sys_inst(source)
                sys = curr_inst.name
                ss = origin.lower()
                table = ss+"_"+sys+"_params"
                query_allowed_extra = util.db_query(self.connection, table, 'extra', "GROUP BY extra", "all")
                allowed_extra = []
                for el in query_allowed_extra:
                    allowed_extra.append(el["extra"])
                if curr2check not in allowed_extra:
                    return False, "Value Error! "+curr2check.upper()+" value not allowed for "+extra_name+" in "+tree+"\n"

            else:
                req_filters = self.get_filters(source, curr_sub, True)
                allowed_f = req_filters[tpl_arr[i]]['values']
                allowed_f.append("ALL")
                if curr2check not in allowed_f:
                    return False, "Value Error! "+tpl_arr[i].upper()+" value not allowed for "+extra_name+" in "+tree+"\n"

        return check, msg      
      
    def check_datetime(self, date_str):
        #check is a date as string has the correct AIDA format
        msg = ""
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError as e:
            msg = "Date Format Error! Incorrect date format, should be yyyy-mm-ddThh:mm:ss\n"
            return False, msg
        
        return True, msg

    def check_detectors(self, subs, dets, detname):
        check = True
        msg = ""       
        listpar = []
        if detname == "DET":
            minid = 1
            maxid = 4
            maxlen = 2
        elif detname == "CCD": 
            minid = 1
            maxid = 6
            minlen = 3

        for d in dets:
            deterr = 0
            error_msg = "Key Error! Invalid syntax "+d+" as Detector key in: "
            det =d.split("_")

            if len(det)!=2:
                check = False
                msg = error_msg
                break                
            
            name = det[0]       
            #check name
            if name != detname:
                check = False
                msg = error_msg
                break          
            if name == "DET":
                if len(det[1]) != maxlen:
                    check = False
                    msg = error_msg
                    break            
            else:
                idstr = det[1][:minlen]
                if len(idstr)!=minlen or idstr[1]!="-":
                    check = False
                    msg = error_msg
                    break            
    
            row = det[1][0]
            if name == "DET":
                col = det[1][1]
            else:
                col = det[1][2]
           
            #check if detector ids are integers
            try:
                r=int(row)
                c =int(col)
                if r<minid or r>maxid or c<minid or c>maxid:
                    check = False
                    msg = error_msg
                    break                  
            except:
                check = False
                msg = error_msg
                break    

            #check quadrant for CCD case
            if detname == "CCD":
                if len(det[1])>minlen:
                    q = det[1][3:]
                    #check if it starts with [ and ends with ]
                    leftok = q.startswith("['")
                    rightok = q.endswith("']")
                    if not leftok or not rightok:
                        check = False
                        msg = error_msg
                        break
                    l = q[2]
                    quadlen = 5
                    #check quadrant definition length
                    if len(q)!= quadlen:
                        check = False
                        msg = error_msg
                        break
                    if l not in ["E","F","G","H"]:
                        check = False
                        msg = error_msg
                        break  
                else:
                    if subs in ["HKTM","SCIENCE","CALIBRATION"]:
                        check = False
                        msg = "Key Error! Quadrant not defined for Detector key "+d+" in: "     
                        break
        return {"isvalid" : check, "msg" : msg}       

    def check_exp(self, *args, listpar, listval=[], extra_tpl="par"):
        isvalid = True
        msg = ""
        exp_data, treetext = self.__get_branch(args)        
        
        #get keys of experiment parameters
        try:
            keys = self.get_keys(exp_data, exclude = ["Type"])
        except:
            msg = 'ERROR! Invalid branch structure in '+treetext+"\n"
            return {"isvalid" : False, "msg" : msg}
  
        #check experiment "Type"
        isvalid, msg, pstr = self.check_exp_type(exp_data, keys, treetext)
        if not isvalid:
            return {"isvalid" : False, "msg" : msg}
            
        #check values
        curr_type = exp_data['Type']
        if curr_type in self.listplots:
            for p in keys:
                #check parameters in "Additional Parameters", "X"
                isvalid, msg = self.check_plot_config(p, exp_data, listpar, pstr, treetext, extra_tpl)
                if not isvalid:
                    return {"isvalid" : False, "msg" : msg}
            #check required parameters
            if not pstr is None:
                isvalid, msg = self.check_required(curr_type, keys, pstr, treetext)
                if not isvalid:
                    return {"isvalid" : False, "msg" : msg}
        elif curr_type in self.liststats:
            if not pstr is None:
                #list of available parameters for the current functions
                func_par = list(pstr.keys())
                list_required = []
                #create list of required parameters
                for item in func_par:
                    isreq = pstr[item]['required']
                    if isreq == "True":
                        list_required.append(item)
                #check if "Parameters" section is defined
                try:
                    #list of parameters set in configuration
                    pars_set = list(exp_data['Parameters'].keys())
                except:
                    if len(list_required)>0:
                        msg = 'Missing required "Parameters" section in ' +treetext+"\n"
                        return {"isvalid" : False, "msg" : msg}
                    else:
                        pars_set=[]
                #check if parameters in config are allowed
                isvalid, msg = self.check_allowed(pars_set, func_par)
                if not isvalid:
                    msg = msg[0] + " in " + treetext
                    return {"isvalid" : False, "msg" : msg}
                #check if the parameter value is in the right format
                for p in pars_set:                  
                    par_conf = pstr[p]
                    val = exp_data['Parameters'][p]
                    isvalid, msg = self.check_par_format(p, val, par_conf, treetext)
                    if not isvalid:
                        return {"isvalid" : isvalid, "msg" : msg}
                #check required parameters
                isvalid, msg = self.check_required(curr_type, pars_set, pstr, treetext)
                if not isvalid:
                    return {"isvalid" : False, "msg" : msg}
                    
        return {"isvalid" : isvalid, "msg" : msg}      
      
    def check_exp_type(self, exp_data, keys, tree=""):
        msg = ""
        pstr = ""
        plots_par = [x['parameters'] for x in self.allowed_plots]
        stats_par = [x['parameters'] for x in self.allowed_stats]

        #check if "Type" key is defined
        try:
            curr_type = exp_data['Type']
        except:
            msg = 'Key Error! "Type" key not found in ' + tree+"\n"
            return False, msg, pstr
        #check if "Type" value is allowed. If "Type" value is allowed, check configuration keys for the current test.
        if curr_type in self.listplots:
            idx = self.listplots.index(curr_type)
            pstr = plots_par[idx]
            if not pstr is None:
                pstr = json.loads(pstr)
                params = list(pstr.keys())
            else:
                params = []
            params.append("Additional Parameters")
            params.append("Optional Filters")
            check, msgarr = self.check_allowed(keys, params)

        elif curr_type in self.liststats:
            idx = self.liststats.index(curr_type)
            pstr = stats_par[idx]
            if not pstr is None:
                pstr = json.loads(pstr)
            check, msgarr = self.check_allowed(keys, ["Parameters"])
        else: 
            msg = 'Value Error! "Type" value not allowed in ' + tree+"\n"
            return False, msg, pstr     

        for i in range(len(msgarr)):
            msgarr[i] += " in "+tree
        
        if len(msgarr)>0:
            msg = "\n".join(msgarr)
            return False, msg, pstr
        
        return True, msg, pstr      

    def check_hist_required(self, k, p):
        error = 0
        if (not "Bin Size" in k) and (not "Number of Bins" in k):
            error = 1
        elif ("Bin Size" in k) and ("Number of Bins" in k):
            error = 2
        
        return error

    def check_general_info(self):
        msg = ""
        isvalid = True
        msgarr = []
        try:
            #Get start time
            tstart = self.text["General Info"]["Start Time"]
            #check tstart format
            checkt, tmsg = self.check_datetime(tstart)
            if not checkt:
                tmsg = '"Start Time" ' + tmsg
                msgarr.append(tmsg)
            #Get window
            t_window = self.text["General Info"]["Time Window"]
            #check t_window format
            checktw, twmsg = self.check_twindow(t_window)
            if not checktw:
                twmsg = '"Time Window" ' + twmsg
                msgarr.append(twmsg)            
                
            #Check Sampling
            checksamp, sampmsg = self.check_sampling()
            if not checksamp:
                msgarr.append(sampmsg)
            #Get number of acquisitions and acquisition time step
            if self.period == "ondemand":
                #Get number of acquisitions
                nacq = self.text["General Info"]["Number of acquisitions"]
                checknacq, nacqmsg = self.check_isnumbergt(nacq, 0, False, True)
                if checknacq:
                    nacq = int(nacq)
                else:
                    nacqmsg = '"Number of acquisitions" ' + nacqmsg
                    msgarr.append(nacqmsg)
                
                #Get acquisition time step
                if nacq > 1:
                    tacq = self.text["General Info"]["Acquisition time step"]
                    checktacq, tacqmsg = self.check_isnumbergt(tacq, 0, False, False)
                    if not checktacq:
                        tacqmsg = '"Acquisition time step" ' + tacqmsg
                        msgarr.append(tacqmsg)
                
            if len(msgarr)>0:
                msg = "\n".join(msgarr)
                isvalid = False
        except:
            msg = 'Value Error! Error reading "General Info" data. Please check the syntax and required keys.\n'
            isvalid = False

        return {"isvalid" : isvalid, "msg" : msg}      
      
    def check_isjson(self):
        msg = ""
        isvalid = True
        try:
            json_object = json.loads(self.text)
            self.text = json_object
        except:
            msg = "JSON Error! The configuration is not a valid JSON text\n"
            isvalid =  False
            
        return {"isvalid" : isvalid, "msg" : msg}      
      
    def check_isnumbergt(self, val, checkval = 0, isincluded = False, isint = False):
        #check if an input value is a number (or int) greater (or equal) than checkval
        msg = ""
        try:
            #check if val is floatable
            n = float(val)
            #check if is integer
            if isint:
                isok = n.is_integer()
                if not isok:
                    msg = "Type Error! Input value is not integer\n"
                    return False, msg
            if isincluded:
                res = n >= checkval
                addmsg = "or equal "
            else:
                res = n > checkval
                addmsg = ""
            if not res:
                msg = "Value Error! Input value is not greater "+addmsg+"than "+str(checkval)+"\n"
                return False, msg
        except ValueError as e:
            msg = "Type Error! Input value is not a number\n"
            return False, msg
        
        return True, msg      

    def check_ondemand_dates(self):
        msg = ""
        isvalid = True
        tstart = self.text["General Info"]["Start Time"]
        tstart = tstart.replace("T", " ")
        ts_stamp = util.format_date(tstart)
        t_window = float(self.text["General Info"]["Time Window"])
        deltat = t_window*3600.0
        
        #Get number of acquisitions
        nacq = int(self.text["General Info"]["Number of acquisitions"])
        tacq = 0
        if nacq > 1:
            tacq = float(self.text["General Info"]["Acquisition time step"])
        te_stamp = ts_stamp + (nacq-1)*tacq*3600+t_window*3600

        #Check for not allowed dates in the future
        if debug == 0:
            now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            now_stamp = util.format_date(now)
            if (ts_stamp>now_stamp) or (te_stamp > now_stamp):
                msg = 'Value Error! Start date and/or calculated stop date must be before today. Please check.'
                isvalid = False

        return {"isvalid" : isvalid, "msg" : msg}      
      
    def check_op(self, *args):
        #check if "Operation_<i>" keys are well defined
        msg=""
        isvalid = True
        root, tree = self.__get_branch(args)
        try:
            opkeys = self.get_keys(root)                
        except:
            msg = 'ERROR! Invalid branch structure in '+tree+"\n"
            return 0, {"isvalid" : False, "msg" : msg}
            
        if len(opkeys)>0:
            #check if all keys are in the form "Operation_<i>"
            optext = np.unique([elem[:10] for elem in opkeys])
            opids = np.unique([elem[10:] for elem in opkeys])
            if len(optext)>1 or optext[0] != "Operation_":
                    isvalid = False
            else:
                #check if <i> is a complete sequence of integers
                try:
                    #check list contains integers
                    opids = list(map(int, opids))
                    #check if values are consecutive
                    sorted_opids = sorted(opids)
                    isvalid = sorted_opids == list(range(1, max(sorted_opids)+1))
                except:
                    isvalid = False
        else:
            isvalid = False
            msg = "Key Error! No Operation defined in "+tree+". Please, check your configuration file.\n"
            return "", {"isvalid" : False, "msg" : msg}            
            
        if not isvalid:
            msg = 'Key Error! Invalid syntax for one or more "Operation" keys in '+tree+"\n"
        
        return len(opkeys), {"isvalid" : isvalid, "msg" : msg}       

    def check_origin(self, mainsys, treeroot, allowed):
        #check if defined systems are allowed
        msg=""
        keys = self.get_keys(root=treeroot)
        check, msgarr = self.check_allowed(keys, allowed)
        if len(msgarr)>0:
            for m in msgarr:
                msg_m = m+' for system ' +mainsys+'\n'
                msg += msg_m
        tree_arr = []
        for i in range(len(keys)):
            newtree = treeroot[keys[i]]
            tree_arr.append(newtree)
        
        return keys,{"isvalid" : check, "msg" : msg}, tree_arr      

    def check_optional_filters(self, root, listpar, tree):
        msg = ""
        check = True
        listopf = root["Optional Filters"]
        extra_name = "Optional Filters"
        source = tree.split("/")[0].lower()
        allowed_origin = ["HKTM", "SCIENCE"]
        known_types = {'int': int,'float': float,'str': str,'list':list}
        if tree.split("/")[1] not in allowed_origin:
            sub = "hktm"
        else:
            sub = tree.split("/")[1].lower()
        
        if not isinstance(listopf, dict):
            msg = 'Value Error! "Optional Filters" value must be a dictionary in '+tree+"\n"
            return False, msg
          
        #get list of allowed filters from DB
        add_filters = self.get_filters(source,sub,False)
        if len(add_filters) == 0:
            msg = "Value Error! 'Optional filters' key not allowed for current Operating Mode\n"
            return False, msg          

        for k,v in listopf.items():
            if k not in add_filters.keys():
                msg = "Value Error! Not valid key '"+k+"' for "+extra_name+" in "+tree+"\n"
                return False, msg
            else:
                add_type = known_types[add_filters[k]['type']]
                if not isinstance(v, add_type):
                    msg = "Type Error! '"+k+"' type must be "+str(add_type)+" for "+extra_name+" in "+tree+". Detected "+str(type(v))+".\n"
                    return False, msg
                  
                val_format = known_types[add_filters[k]['format']]
                if isinstance(v, list):
                    for vals in v:
                        if not isinstance(vals,val_format):
                            msg = "Type Error! All elements of '"+k+"' type must be "+str(val_format)+" for "+extra_name+" in "+tree+".\n"
                            return False, msg            
                
        return check, msg        
      
    def check_par_format(self, p, val, conf, tree):
        isvalid = True
        msg = ""
        t = conf["type"]
        if t == "number":
            try:
                val = float(val)
            except:
                msg = 'Value Error! "'+p+'" value in '+tree+' is not a number\n'
                return False, msg
        elif t == "integer":
            try:
                isint = float(val).is_integer()
                if not isint:
                    msg = 'Value Error! "'+p+'" value in '+tree+' is not an integer\n'
                    return isvalid, msg
            except:
                msg = 'Value Error! "'+p+'" value in '+tree+' is not an integer\n'
                return False, msg
        elif t == "select":
            opt = conf['option']
            if val not in opt:
                msg = 'Value Error! "'+p+'" value in '+tree+' is not allowed\n'
                return False, msg
        
        #check the parameter limits
        try:
            vmintxt = conf["min"]
            vmin = float(vmintxt)
            include = conf["include_min"]
            
            if include == 0:
                isvalid = float(val) > vmin
                txt = "than "+str(vmin)
            elif include == 1:
                isvalid = float(val) >= vmin
                txt = "or equal to "+str(vmintxt)
            if not isvalid:
                msg = 'Value Error! "'+p+'" value in '+tree+' is not greater '+txt+"\n"
                return isvalid, msg
        except:
            pass

        return isvalid, msg
      
    def check_params(self, *args, listpar, listval=[]):
        #check parameters for selected system/subsystem
        msg=""
        root, root_text = self.__get_branch(args)
        if root=={}:
            msg = "Key Error! No Parameter key(s) defined in "+root_text+". Please, check your configuration file.\n"
            return "", {"isvalid" : False, "msg" : msg}
        if not isinstance(root,dict):
            return "", {'isvalid':False, 'msg':'ERROR! Invalid branch structure in '+root_text+"\n"}            
        keys = self.get_keys(root)  
        if len(listval)>0:
            try:
                par2check = [x.split(".")[0] for x in keys]
                val2check = [x.split(".")[1] for x in keys]
            except:
                msg = "Key Error! Unrecognized key(s) in "+root_text+". Please, check your configuration file.\n"
                return "", {"isvalid" : False, "msg" : msg}
        else:
            par2check = keys
        try:
            check, msgarr = self.check_allowed(par2check, listpar)
            if len(msgarr)>0:
                for m in msgarr:
                    msg_m = m+' for ' +root_text+'\n'
                    msg += msg_m
                return "", {"isvalid" : False, "msg" : msg} 
                    
            if len(listval)>0:  
                for i in range(len(par2check)):
                    curr_par = par2check[i]
                    curr_val_id = listpar.index(curr_par)
                    curr_listval = listval[curr_val_id]
                    checkval, msgarrval = self.check_allowed(val2check, curr_listval)
                    if len(msgarrval)>0:
                        for m in msgarrval:
                            msg_m = m+' for ' +root_text+'\n'
                            msg += msg_m
                        return "", {"isvalid" : False, "msg" : msg}                 
        except:
            check = True

        return keys,{"isvalid" : check, "msg" : msg}        
      
    def check_plot_config(self, p, root, listpar, pstr, tree="", extra_tpl = "par"):
        

        
        isvalid = True
        msg = ""
        if p == "Additional Parameters":
            #check if "Additional Parameters" values are allowed
            extra_dict = {"Additional Parameters" : root["Additional Parameters"]}
            if isinstance(root["Additional Parameters"],list):
                isvalid, msg = self.check_extra_params(extra_dict, listpar, tree, extra_tpl)
            else:
                isvalid = False
                msg = "Value Error! Invalid type for "+p+". It must be a list.\n"
        elif p=="X":
            # Parameter for scatter
            extra_dict = {"X" : [root["X"]]}
            if isinstance(root["X"], str):
                if root["X"] != "":
                    isvalid, msg = self.check_extra_params(extra_dict, listpar, tree, extra_tpl)
                else:
                    isvalid = False
                    msg = "Value Error! 'X' cannot be an empty string.\n"                     
            else:
                isvalid = False
                msg = "Value Error! Invalid type for "+p+". It must be a string.\n"                
        elif p=="Bin Size" or p=="Number of Bins":
            isvalid, msg=self.check_bins(root, tree)
        elif p == "Optional Filters":
            #check if "Optional Filters" values are allowed
            isvalid, msg = self.check_optional_filters(root, listpar, tree)

        return isvalid, msg      

    def check_required(self, t, k, p, tree=""):
        isvalid = True
        msg = ""
        #check for scatter required
        if t == "scatter":
            error = self.check_scatter_required(k,p)
            if error == 1:
                msg = "Missing required parameters in "+tree+"\n"
                return False, msg
        #check for histogram required
        elif t == "histogram":
            error = self.check_hist_required(k,p)
            if error == 1:
                msg = "Missing required parameters in "+tree+"\n"
                return False, msg
            elif error == 2:
                msg = "Conflicting parameters in "+tree+"\n"
                return False, msg
        else:       
        #check for statistical functions required parameters
            func_k = list(p.keys())
            #get only required parameters
            for par in func_k:
                error = self.check_stats_required(k,par,p)
                if error == 1:
                    msg = 'Missing required parameter "'+par+'" in '+tree+"\n"
                    return False, msg
    
        return isvalid, msg

    def check_sampling(self):
        isvalid = True
        msg = ""
        allowed_samp = ["full", "by time", "by function"]
        allowed_func = ["mean", "median"]
        #Get sampling type
        try:
            self.sampling = self.text["General Info"]["Sampling"]
            if self.sampling not in allowed_samp:
                return False, "Value Error! Not allowed value for 'Sampling'.\n"
        except:
            return False, "Value Error! Error reading 'Sampling' value\n"
        
        try:
            #Get sampling period
            if self.sampling != "full":
                self.ts = self.text["General Info"]["Sampling period"]
                #check if it is number > 0
                checkts, stmsg = self.check_isnumbergt(self.ts, 0, False, False)
                if not checkts:
                    stmsg = '"Sampling period" ' + stmsg+"\n"
                    return False, stmsg
            else:
                self.ts = 0
            #get function in "by function" usecase
            if self.sampling == "by function":
                self.sampfunc = self.text["General Info"]["Sampling function"]
                if self.sampfunc not in allowed_func:
                    return False, 'Value Error! "Sampling" function not allowed\n'
            else:
                self.sampfunc = None
        except:
            return False, 'Value Error! Error reading "Sampling" configuration parameters\n'
          
        return isvalid, msg
    
    def check_scatter_required(self, k, p):
        error = 0
        if not "X" in k:
            error = 1
        
        return error    
    
    def check_stats_required(self, k, par, p):
        error = 0
        isreq = p[par]['required']
        if isreq == "True":
            #check if required parameter is set 
            if not par in k:
                error = 1
        
        return error

    def check_subsystems(self, mainsys, allowed):
        #check if defined systems are allowed
        msg=""
        try:
            keys = self.get_keys(root=self.text[mainsys])
        except:
            msg = 'ERROR! Invalid branch structure for system '+mainsys+"\n"
            return "",{"isvalid" : False, "msg" : msg} 

        check, msgarr = self.check_allowed(keys, allowed)
        if len(msgarr)>0:
            for m in msgarr:
                msg_m = m+' for system ' +mainsys+'\n'
                msg += msg_m

        return keys,{"isvalid" : check, "msg" : msg}      
      
    def check_systems(self, allowed):
        msg=""
        #check if defined systems are allowed
        self.syskeys = self.get_keys(exclude = ["General Info"])
        check, msgarr = self.check_allowed(self.syskeys, allowed)
        if len(msgarr)>0:
            msg = "\n".join(msgarr)        
        #check if repository settings are available
        if check:
            opmode = util.db_query(self.connection, "operation_modes", 'mode', "WHERE enable=1", "one")['mode']
            for s in self.syskeys:
                repo_json = util.get_json_data("../"+s.lower()+".conf")
                try:
                    repo = repo_json[opmode]
                except:
                    check = False
                    msg += "\nERROR! Operating Mode : "+opmode.upper()+" not set for system '"+s+"' in configuration file.\n"
        return {"isvalid" : check, "msg" : msg}       

    def check_twindow(self, t_window):
        checktw, twmsg = self.check_isnumbergt(t_window, 0, False, False)

        #check if t_window is compliant to period
        if checktw:
            if self.period in ["daily","weekly","monthly"]:
                if t_window != self.default_tw:
                    checktw = False
                    twmsg = "Value Error! The entered Time Window value is not compliant with period "+self.period.upper()+" ("+str(self.default_tw)+")\n"
                    
        return checktw, twmsg

    def check_extra_params(self, extra_dict, listpar, tree, extra_tpl):
        check=True
        msg=""
        extra_name = list(extra_dict.keys())[0]
        listadd = extra_dict[extra_name]
        if extra_tpl != "tbd":
            if extra_tpl == "system":
                #extra parameters structure checked by systems methods
                source = tree.split("/")[0]
                usecase = tree.split("/")[1]
                sub = tree.split("/")[2]
                syscls = classes.sys_inst(source.lower())
                check, msg, listpar = syscls.check_report_extraparams(listadd,self.connection,usecase,sub,tree)
                if not check:
                    if msg == "":
                        msg = "Value Error! Invalid '"+extra_name+"' value in "+tree+". Please, check your configuration file.\n"
            else:
                tpl_arr=extra_tpl.split(".")
                #if tpl length = 1, then it must be the parameter name
                if len(tpl_arr) == 1:
                    check, msgarr = self.check_allowed(listadd, listpar)
                    if not check:
                        msg = 'Value Error! "'+extra_name+'" not allowed in '+tree+"\n"
                        return False, msg
                else:
                    for item in listadd:
                        check, msg = self.check_composed_par(item, tpl_arr, extra_tpl, tree, extra_name)
                        if not check:
                            return False, msg
        else:
            #extra parameters structure defined by form.json dictionaries
            #get experiment source and usecase
            source = tree.split("/")[0]
            usecase = tree.split("/")[1]
            #get source branch from forms.json
            subsystems_dict = util.get_subsystems_from_file(usecase.lower(), source.lower(), self.connection)
            #define allowed lengths
            l_full = util.finddepth(subsystems_dict)
            l_det = l_full+1
            
            for item in listadd:
                add_spl = item.split(".")
                l_add = len(add_spl)
                #get list par for additional parameter keys
                if l_add > 1:
                    stat = "WHERE subsystem='"+add_spl[0]+"' AND extra='"+add_spl[1]+"'"
                else:
                    stat = ""                
                curr_inst = classes.sys_inst(source)
                listpar, listval = curr_inst.get_params_list(usecase, self.connection, stat)    
              
                if l_add == l_full or l_add == l_det:
                    #check structure
                    if l_add == 1:
                        #only parameter
                        check, msgarr = self.check_allowed(item, listpar)
                        if not check:
                            msg = 'Value Error! "'+extra_name+'" not allowed in '+tree+"\n"
                            return False, msg
                    else:
                        #composed parameter
                        for k,v in subsystems_dict.items():
                            conf_dict = v
                            for el in add_spl[:-1]:       #to change if parameter accepts values field too
                                try:
                                    if isinstance(conf_dict, dict):
                                        conf_dict = conf_dict[el]
                                except:
                                    return False, 'Value Error! "'+el+'" not allowed for "'+extra_name+'" in '+tree+"\n"
                                
                            if conf_dict=="det":
                                #check detector
                                det2check = add_spl[-2]     #to change if parameter accepts values field too
                                if l_add != l_det:
                                    return False, 'Value Error! Not valid format for "'+extra_name+'" element(s) in '+tree+"\n"
                                k_idx = np.where(np.array(self.allowed_subs)==usecase)[0][0]
                                curr_det_prefix = self.subs_detector[k_idx]                                    
                                checkdet= self.check_detectors(usecase, [det2check], curr_det_prefix)
                                if not checkdet['isvalid']:
                                    msg = 'Value Error! Invalid detector '+det2check+' for "'+extra_name+'" in '+tree+"\n"
                                    return False, msg
                            else:
                                if l_add != l_full:
                                    return False, 'Value Error! Not valid format for "'+extra_name+'" element(s) in '+tree+"\n"
                            
                            #check parameter name
                            par2check = add_spl[-1]     #to change if parameter accepts values field too
                            check_par = par2check in listpar
                            if not check_par:
                                msg = 'Value Error! Parameter '+par2check+' is not allowed for "'+extra_name+'" in '+tree+"\n"
                                return False, msg
                else:
                    msg = 'Value Error! Not valid format for "'+extra_name+'" element(s) in '+tree+"\n"
                    return False, msg                
                    
        return check, msg        
      
    def check_x_scatter(self, root, listpar, tree, extra_tpl):
        check=True
        msg=""
        x = root["X"]
        extra_name = "X"
        #check if x is a string
        if not isinstance(x, str):
            msg = 'Value Error! "X" value in '+tree+' must be a string\n'
            return False, msg
        if extra_tpl != "tbd":
            tpl_arr=extra_tpl.split(".")
            #if tpl length = 1, then it must be the parameter name
            if len(tpl_arr) == 1:
                if x not in listpar:
                    msg = 'Value Error! "X" value in '+tree+' is not allowed\n'
                    return False, msg
            else:
                check, msg = self.check_composed_par(x, tpl_arr, extra_tpl, tree, extra_name)
                if not check:
                    return False, msg
        else:
            #additional parameters structure defined by form.json dictionaries
            #get experiment source and usecase
            source = tree.split("/")[0]
            usecase = tree.split("/")[1]
            #get source branch from forms.json
            subsystems_dict = util.get_subsystems_from_file(usecase.lower(), source.lower(), self.connection)
            #define allowed lengths
            l_full = util.finddepth(subsystems_dict)
            l_det = l_full+1
            #split X parameter
            add_spl = x.split(".")
            l_add = len(add_spl)
            #get list par for x parameter keys
            if l_add > 1:
                stat = "WHERE extra='"+add_spl[1]+"'"
            else:
                stat = ""
            curr_inst = classes.sys_inst(source)
            listpar, listval = curr_inst.get_params_list(usecase, self.connection, stat)  

            if l_add == l_full or l_add == l_det:
                #check structure
                if l_add == 1:
                    #only parameter
                    check, msgarr = self.check_allowed(x, listpar)
                    if not check:
                        msg = 'Value Error! X in '+tree+' is not allowed\n'
                        return False, msg
                else:
                    #composed parameter
                    for k,v in subsystems_dict.items():
                        conf_dict = v
                        for item in add_spl[:-1]:       #to change if parameter accepts values field too (like QLA)
                            try:
                                if isinstance(conf_dict, dict):
                                    conf_dict = conf_dict[item]
                            except:
                                return False, 'Value Error! "'+item+'" not allowed for "'+extra_name+'" in '+tree+"\n"
                            
                        if conf_dict=="det":
                            #check detector
                            det2check = add_spl[-2]     #to change if parameter accepts values field too (like QLA)
                            if l_add != l_det:
                                return False, 'Value Error! Not valid format for "'+extra_name+'" elements in '+tree+"\n"
                            k_idx = np.where(np.array(self.allowed_subs)==usecase)[0][0]
                            curr_det_prefix = self.subs_detector[k_idx]                                    
                            checkdet= self.check_detectors(source, usecase, [det2check], curr_det_prefix)
                            if not checkdet['isvalid']:
                                msg = 'Value Error! Invalid detector '+det2check+' for "'+extra_name+'" in '+tree+"\n"
                                return False, msg
                        else:
                            if l_add != l_full:
                                return False, 'Value Error! Not valid format for "'+extra_name+'" elements in '+tree+"\n"
                        
                        #check parameter name
                        par2check = add_spl[-1]     #to change if parameter accepts values field too (like QLA)
                        check_par = par2check in listpar
                        #return False, str(par2check)+"---"+str(listpar)
                        if not check_par:
                            msg = 'Value Error! Parameter '+par2check+' is not allowed for "'+extra_name+'" in '+tree+"\n"
                            return False, msg
                        else:
                            par = par2check
            else:
                msg = 'Value Error! Not valid format for "'+extra_name+'" elements in '+tree+"\n"
                return False, msg                

        return check, msg

    def get_filters(self, system, origin="hktm", required = True):
        filters=""
        if required:
            node = "required"
        else:
            node = "optional"
        filters = util.get_subsystems_from_file(origin.lower(), system.lower(), self.connection, node)
        
        return filters      
      
    def get_keys(self, root = None, exclude = []):
        keys=[]
        if root is None:
            keys = list(self.text.keys())
        else:
            keys = list(root.keys())
        
        finalk = [x for x in keys if x not in exclude]
        
        return finalk
      
    def isvoid_branch(self, s):
        curr_branch = self.text[s]
        if isinstance(curr_branch,dict):
            if len(curr_branch) == 0:
                return 1, ""
            else:
                return 0, len(curr_branch)
                for k,v in curr_branch.items():
                    if len(v) == 0:
                        return 1, k
                    else:
                        return 0, ""
        else:
            return 2, ""

def main(data, period):

    check = configCheck(data, period)

    #check if file is json
    isjson = check.check_isjson()
    if not isjson['isvalid']:
        print(json.JSONEncoder().encode(isjson))
        exit(1)
    
    #check general info
    checkgen = check.check_general_info()
    if not checkgen['isvalid']:
        print(json.JSONEncoder().encode(checkgen))
        exit(1)
        
    #check if tstart and tstop are allowed if the period is ondemand (only datetime less than now)
    if period == "ondemand":
        checkdate = check.check_ondemand_dates()
        if not checkdate['isvalid']:
            print(json.JSONEncoder().encode(checkdate))
            exit(1) 

    #get allowed plots dictionary
    check.allowed_plots = util.db_query(check.connection, "plots", 'plot_name, parameters', res_type = "all")
    #list of available plots
    check.listplots = [x['plot_name'].lower() for x in check.allowed_plots]
    
    #get allowed stats dictionary
    check.allowed_stats = util.db_query(check.connection, "statistics", 'stat_name, parameters', res_type = "all")
    #list of available stats
    check.liststats = [x['stat_name'].lower().replace("_", " ") for x in check.allowed_stats]  #cambiare in stats_slug
    
    allowed_systems_db = util.db_query(check.connection, "systems", '*', "WHERE enabled = 1", res_type = "all")
    allowed_systems = np.unique([item['name'] for item in allowed_systems_db])
  
    #check systems
    checksys = check.check_systems(allowed_systems)
    if not checksys['isvalid']:
        print(json.JSONEncoder().encode(checksys))
        exit(1)

    #For each system, check json tree keys and values   
    isvalid_arr = []
    msg_arr = []
     
    for s in check.syskeys:
        currsys = classes.sys_inst(s)
        #check if tree is empty
        isempty = check.isvoid_branch(s)
        if isempty[0] == 1:
            isvalid_arr.append(False)
            if isempty[1] == "":
                msg_arr.append("ERROR! Branch for system "+s+" is empty. Please, remove it from configuration file.\n")
            else:
                msg_arr.append("ERROR! Branch "+isempty[1]+" for system "+s+" is empty. Please, remove it from configuration file.\n")
        elif isempty[0] == 0:
            check_tree = currsys.check_report_tree(check)
            isvalid_arr.append(check_tree['isvalid'])
            msg_arr.append(check_tree['msg'])
        elif isempty[0] == 2:
            isvalid_arr.append(False)
            msg_arr.append("ERROR! Invalid or missing branch for system "+s+".\n")            
        
    check.connection.close()    
    msg = ""
    isvalid = True
    for i in range(len(isvalid_arr)):
        if not isvalid_arr[i]:
            msg+=msg_arr[i]
            isvalid = False

    print(json.JSONEncoder().encode({'isvalid' : isvalid, 'msg' : msg}))
    
if __name__ == "__main__":
    print("Content-Type: application/json")
    print()

    #the cgi library gets vars from html
    data = cgi.FieldStorage()
    source = data['from'].value
    period = data['period'].value
    if source == "editor":
        jsontext = data['jsontext'].value
    elif source == "upload":
        f = data['filename'].value
        with open(f,"r") as F:
            jsontext = F.read()

    main(jsontext, period)