#!/usr/bin/python

import numpy as np
from    os          import path, environ, listdir, remove
import ast
import functions as util
import reportutils as ru
import time
import pymysql.cursors
import classes
import multiprocessing
from    time            import time, localtime, asctime, sleep
from datetime import datetime
import  threading
import h5py
#XML handling
import xml.etree.cElementTree as ET
from xml.dom import minidom

from datetime import datetime
from calculate_statistics import calc_stat
#for PDF report
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.rl_config import defaultPageSize
from pdfcreator import reportTemplate, xmlData, pdfBuilder, MyDocTemplate
import traceback

class xmlThread(threading.Thread):
    def __init__(self, ThreadID, name, s, conf, connconfig, runid, nprocs, parpos):
        threading.Thread.__init__(self)
        self.name=name
        self.id=ThreadID
        self.source = s
        self.conf = conf
        self.connconfig = connconfig
        self.runid = runid
        self.nprocs = nprocs
        self.error_list = []
        self.origins = conf.pars[s]
        self.parpos = parpos        

    def run(self):

        ############### FOR BENCHMARK ###############    
        ants, ants_ts = util.get_time()
        with open(self.conf.bm_tfile, "a") as f:                          
            f.write(self.source + " --- XML GENERATION START (collect data, generate plot, perform stats):\t"+str(ants)+"\n")
        #############################################   
        jobs = []
        pooled_pars = []
        for n in range(self.nprocs):
            out_n = {}      
            for o in self.origins:
                params_k = []
                listpar = self.origins[o]["keys"]
                try:              
                    params_chunk = self.parpos[o][n]
                except:
                    params_chunk = []
                for p in params_chunk:
                    if p in listpar:
                        params_k.append(p)                     
                out_n.update({o : params_k})                  

            if len(out_n) > 0: 
                pooled_pars.append(out_n)
                            
        manager = multiprocessing.Manager()
        error_list = manager.list()
        for n, p in enumerate(pooled_pars):
            j = multiprocessing.Process(target=xml_collect_results, args=(n, p, self.source, self.conf, self.connconfig, self.runid, self.parpos, error_list))
            jobs.append(j)
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

        error_dict = []
        missfile = []
        noconn = []
        h5 = []        
        for item in error_list:
            k = item.keys()
            if "filerr" in k:
                missfile.append(item["filerr"])
            elif "locerr" in k:
                noconn.append(item["locerr"])
            elif "h5err" in k:
                h5.append(item["h5err"])
            else:
                error_dict.append(item)              

        #check if connection errors happen
        locerr = 0  
        for check in noconn:
            if check:
                locerr += 1
        if locerr == len(jobs):
            error_dict.append({"type": "Connection error",
                        "msg" : "Impossible to connect to retrieved data. Analysis can not be performed",
                        "sub" : "GENERAL",
                        "level" : "serious",
                        "system" : self.source})
        elif locerr > 0 and locerr < len(jobs):          
            error_dict.append({"type": "Connection error",
                        "msg" : "Impossible to connect to some retrieved data. Analysis could be incomplete.",
                        "sub" : "GENERAL",
                        "level" : "warning",
                        "system" : self.source})     

        #check if h5 files have been read
        h5err = 0  
        for check in h5:
            if check:
                h5err += 1
        if h5err == len(jobs):
            error_dict.append({"type": "Data read error",
                        "msg" : "Impossible to read retrieved data. Analysis can not be performed",
                        "sub" : "GENERAL",
                        "level" : "serious",
                        "system" : self.source})
        elif h5err > 0 and h5err < len(jobs):          
            error_dict.append({"type": "Data read error",
                        "msg" : "Impossible to read some retrieved data. Analysis could be incomplete.",
                        "sub" : "GENERAL",
                        "level" : "warning",
                        "system" : self.source})        

        #check if XML files have been saved
        filerr = 0    
        for check in missfile:
            if check:
                filerr += 1
        if filerr == len(jobs):
            error_dict.append({"type": "XML error",
                        "msg" : "Impossible to store results in XML file. Analysis cannot be performed.",
                        "sub" : "GENERAL",
                        "level" : "serious",
                        "system" : self.source})
        elif filerr > 0 and filerr < len(jobs):          
            error_dict.append({"type": "XML error",
                        "msg" : "Impossible to store some results in XML file. Analysis could be incomplete.",
                        "sub" : "GENERAL",
                        "level" : "warning",
                        "system" : self.source})         
        self.error_list = error_dict
        
        ############### FOR BENCHMARK ###############    
        syste, syste_ts = util.get_time()
        with open(self.conf.bm_tfile, "a") as f:
            f.write(self.source + " --- XML GENERATION END (collect data, generate plot, perform stats):\t"+str(syste)+"\n")
            f.write(self.source + " --- XML GENERATION DURATION (collect data, generate plot, perform stats)    :\t"+str(util.pretty_time(syste_ts - ants_ts))+"\n")
        print(self.source + " --- XML GENERATION DURATION (collect data, generate plot, perform stats)  :\t"+str(util.pretty_time(syste_ts - ants_ts)))
        ############################################################

def check_out_range(data,minrange,maxrange,hminrange=-999,hmaxrange=-999):

    if minrange == -999:
        minrange = -np.inf
    if maxrange == -999:
        maxrange = np.inf
    if hminrange == -999:
        hminrange = -np.inf
    if hmaxrange == -999:
        hmaxrange = np.inf
    outlist = []
    houtlist = []    

    for idx, item in enumerate(data['vals']):
        if not hminrange <= item <= hmaxrange:
            houtlist.append((data['dates'][idx], item))
        elif not minrange <= item <= maxrange:
            outlist.append((data['dates'][idx], item))

    return outlist, houtlist
        
def check_out_range_GOOD(data,minrange,maxrange):

    if minrange == -999:
        minrange = -np.inf
    if maxrange == -999:
        maxrange = np.inf

    outlist = []

    for idx, item in enumerate(data['vals']):
        if not minrange <= item <= maxrange:
            outlist.append((data['dates'][idx], item))

    return outlist
    
def set_report_filename(conf, id, now):

    #get period
    period = conf.period
    #creation string
    creation = now.strftime("%Y%m%dT%H%M%S")     
    #get start, tstop
    ts = conf.tstart
    ts = ts.replace("-","").replace(":","").replace(" ","")
    te = conf.tstop
    te = te.replace("-","").replace(":","").replace(" ","")
    #get sources
    sources = ""
    for s in conf.systems:
        sources += "_"+s
    sources = sources[1:]

    filename = "IREP_"+creation+"_"+str(id)+"-"+period+"-"+ts+"_"+te+"_"+sources

    return filename
  
def xml_collect_results(procid, pardict, s, conf, connconfig, runid, parpos, errors):
    filerr = False  
    npars = 0

    for k,v in pardict.items():
        npars += len(v)
    h5err = False
    locerr = False        
    if npars > 0:
        origins = conf.pars[s]
        tag_dict = {"sub" : "subsystem", "det" : "detector", "par" : "parameter", "val" : "value", "ic" : "instr_conf", "ec" : "exp_conf", "dp" : "data product", "tag" : "params_group"}
        #get number of acquisitions
        if conf.period == "ondemand":
            nacq =conf.repdata['General Info']['Number of acquisitions']
        else:
            nacq = 1
        # get system class
        sysclass = classes.sys_inst(s)
        #system branch
        sysbr = ET.Element("system", name = sysclass.name)
        #init connection
        try:
            connection = util.connect_db(connconfig)
        except:
            locerr = True
        #get repo configuration file dict
        opmode = util.db_query(connection, "config_files", "opmode" , statement = "WHERE filename = '" +conf.configfile+"'", res_type = "one")['opmode'].lower()
        jsonconf = util.get_json_data("../"+sysclass.name+".conf")[opmode]
        if not locerr:           
            #get list of allowed plots
            query_plots = util.db_query(connection, "plots", "plot_name", "")
            list_plots = []
            for item in query_plots:
                list_plots.append(item['plot_name'].lower())
            #get list of allowed statistics and slugs
            query_stats = util.db_query(connection, "statistics", "stat_name, stat_slug, stat_function", "")
            list_stats = []
            list_slugs = []
            list_func = []
            for item in query_stats:
                list_stats.append(item['stat_name'])
                list_slugs.append(item['stat_slug'])
                list_func.append(item['stat_function'])
            stats_config = {}            

            #origin
            for o in list(pardict.keys()):
                #get repo name
                reponame = jsonconf[o]["repository"]
                #get required keys from forms.json
                formsdict = util.get_json_data("../settings/forms.json")
                reqkeysdict = formsdict[sysclass.name][reponame][o]["required"]
                reqkeysdict = util.flatten(reqkeysdict)
                currorig = ET.SubElement(sysbr, o)
                #parameters
                warning = False
        
                h5file = conf.workdir+s.lower()+"_"+o+"_"+str(procid)+".h5"
                try:
                    hf = h5py.File(h5file, "r")
                except:
                    h5err = True

                if not h5err:
                    #results hdf5 file
                    hfoutfile = conf.workdir+s.lower()+"_"+o+"_res_"+str(procid)+".h5"
                    hfout = h5py.File(hfoutfile, "w")

                    for par in list(pardict[o]):
                        #init hfout for par
                        pgroup = hfout.create_group(par)
                        #get list of operations for selected parameter
                        k = ru.get_operation_branches(par, conf.repdata, s, o.upper(), sysclass.hasorig)

                        currpar = ET.SubElement(currorig, "parameter")
                        currpar.set("name", par)
                        #if parameter name is structured with multi info separated by ".", add tags for each sub-element
                        parname = par
                        par_splitted = par.split(".")

                        parid = 0
                        subname = None
                        extra_stat = ""
                        if len(par_splitted) > 1:
                            #store dp, subsystem, extra filters
                            for idk in [0,1]:
                                curr_k = par_splitted[idk]
                                curr_xmltag = ""
                                for tagname, reqval in reqkeysdict.items():
                                    tag_splitted = tagname.split(".")
                                    if curr_k == tag_splitted[1]:
                                        curr_xmltag = tag_splitted[0].replace(" ","_")
                                        ET.SubElement(currpar, curr_xmltag).text = curr_k
                                        parid += 1
                                        break
                                    else:
                                        if isinstance(reqval,list):
                                            if curr_k in reqval or curr_k=="ALL":
                                                curr_xmltag = tag_splitted[0].replace(" ","_")
                                                ET.SubElement(currpar, curr_xmltag).text = curr_k
                                                parid += 1
                                                break
                                        else:
                                            ET.SubElement(currpar, "params_group").text = curr_k
                                            extra_stat = " AND extra= '"+curr_k+"'"
                                            parid += 1
                                            break

                                if curr_xmltag=="data_product" or curr_xmltag=="subsystem":
                                    subname = curr_k
                            try:
                                curr_k = par_splitted[parid]
                                try:
                                    taglist = sysclass.tagroups
                                    if curr_k in taglist:
                                        parid += 1
                                        ET.SubElement(currpar, "tag_group").text = curr_k
                                        extra_stat = " AND extra= '"+curr_k+"'"
                                except:
                                    pass
                                #store detector info
                                if curr_k.startswith("DET_") or curr_k.startswith("CCD_"):
                                    parid += 1
                                    curr_k_txt = curr_k.split("_")[1].replace("-","").replace("['","-").replace("']","")
                                    ET.SubElement(currpar, "detectorID").text = curr_k_txt   
                            except:
                                pass
                            parname = par_splitted[parid]
                        pxml = ET.Element("name")    

                        #add extra info following parameter name
                        if par_splitted[-1] != parname:
                            extrainfo = par_splitted[parid+1:]
                            try:
                                pxml.text = parname
                                currpar.insert(0, pxml)
                                tagconf = sysclass.tagconf[curr_k]
                                for ief,ef in enumerate(tagconf):
                                    for jef in extrainfo:
                                        if jef.startswith(ef):
                                            ef_val = jef.replace(ef,"")
                                            ET.SubElement(currpar, ef).text = ef_val
                            except:
                                #case for decimal numbers in parameter name or .<value> for, for example, QLA
                                el = extrainfo[0]
                                try:
                                    int(el)
                                    parname += "."+el
                                    extraval = ""
                                except:
                                    extraval = el
                                pxml.text = parname
                                currpar.insert(0, pxml)
                                if extraval != "":
                                    ET.SubElement(currpar, "value").text = extraval
                        else:  
                            pxml.text = parname
                            currpar.insert(0, pxml)

                        #add parameter info from DB
                        if subname is None:
                            statement = "WHERE param = '"+parname+"'"
                        else:
                            statement = "WHERE param = '"+parname+"' AND subsystem = '"+subname+"'"+extra_stat
                        tbl = o+"_"+sysclass.name+"_params"
                        
                        infopar = util.db_query(connection, tbl, "*", statement, "one")
                        #add description
                        try:
                            description = infopar['description']
                        except:
                            description = "Error retrieving info from DB"
                        if description != "" and description is not None:
                            ET.SubElement(currpar, "description").text = description                        

                        #add range
                        hmaxel = ET.SubElement(currpar, "range")
                        hmaxel.set("limit", "hard_max")                        
                        try:
                            hmaxrange = infopar['hardmax']
                            if hmaxrange != -999:
                                hmaxel.text = str(hmaxrange)
                            else:
                                hmaxel.text = "N/A"
                        except:
                            hmaxrange = -999
                            hmaxel.text = "N/A" 
                        hminel = ET.SubElement(currpar, "range")    
                        hminel.set("limit", "hard_min")                        
                        try:
                            hminrange = infopar['hardmin']
                            if hminrange != -999:
                                hminel.text = str(hminrange)
                            else:
                                hminel.text = "N/A"
                        except:
                            hminrange = -999
                            hminel.text = "N/A"
                            
                        maxel = ET.SubElement(currpar, "range")   
                        maxel.set("limit", "soft_max")                        
                        try:
                            maxrange = infopar['maxval']
                            if maxrange != -999:
                                maxel.text = str(maxrange)
                            else:
                                maxel.text = "N/A"
                        except:
                            maxrange = -999
                            maxel.text = "N/A"
                        minel = ET.SubElement(currpar, "range")
                        minel.set("limit", "soft_min")                        
                        try:
                            minrange = infopar['minval']
                            if minrange != -999:
                                minel.text = str(minrange)
                            else:
                                minel.text = "N/A"
                        except:
                            minrange = -999
                            minel.text = "N/A"                            
                        #add acquisition
                        for i in range(nacq):
                            #init hdf5 group for acquisition i
                            acqgroup = pgroup.create_group("acquisition_"+str(i))            
              
                            #init dictionary containing the number of how many times the same statistical function is computed
                            nstat_dict = {}              
                            curracq = ET.SubElement(currpar, "acquisition")
                            curracq.set("n",str(i+1))
                    
                            #get data from hdf5 
                            y0 = hf[par]['acquisition_'+str(i)]
                            withdata = y0['dates'].shape[0] > 0                   
                            #check if parameter has data                     
                            if not withdata:
                                warning = True                      
                                w = ET.SubElement(curracq, "warning")
                                w.set("category","no_data")
                                w.text = "No Data available"
                                errors.append({"type": "Data error",
                                            "msg" : "No data available for parameter "+par+" during acquisition #"+str(i+1),
                                            "sub" : o,
                                            "level" : "warning",
                                            "system" : sysclass.source})                       
                     
                            #check out of range values
                            if withdata and not (minrange == -999 and maxrange == -999 and hminrange == -999 and hmaxrange == -999):                     
                                outlist,houtlist = check_out_range(y0,minrange,maxrange,hminrange,hmaxrange)
                            else:
                                outlist = []
                                houtlist = []                                

                            if len(houtlist) > 0:
                                warning = True                       
                                w = ET.SubElement(curracq, "error")
                                w.set("category","out_of_range")
                                w.text = hfoutfile
  
                                #store outlist to hdf5 outfile
                                oolgroup = acqgroup.create_group("out_of_range")
                                oolgroup.create_dataset("hard", data=houtlist)                              

                                errors.append({"type": "Out of range error",
                                            "msg" : str(len(houtlist))+ " values out of HARD limits for parameter "+par+" during acquisition #"+str(i+1),
                                            "sub" : o,
                                            "level" : "error",
                                            "system" : sysclass.source}) 
                     
                            if len(outlist) > 0:
                                warning = True                       
                                w = ET.SubElement(curracq, "warning")
                                w.set("category","out_of_range")
                                w.text = hfoutfile
  
                                #store outlist to hdf5 outfile)
                                if "out_of_range" not in acqgroup.keys():
                                    oolgroup = acqgroup.create_group("out_of_range")
                                else:
                                    oolgroup = acqgroup["out_of_range"]
                                oolgroup.create_dataset("soft", data=outlist)

                                errors.append({"type": "Out of range error",
                                            "msg" : str(len(outlist))+ " values out of SOFT limits for parameter "+par+" during acquisition #"+str(i+1),
                                            "sub" : o,
                                            "level" : "warning",
                                            "system" : sysclass.source})                      
                            #add operations
                            for op in k.keys():
                                addlist = []
                                nodata_addlist = False
                                k_arr = op.split("_")
                                curr_k = k_arr[0]
                                if curr_k == "Operation":
                                    #get function type
                                    t = k[op]["Type"]
                                    currop = ET.SubElement(curracq, "operation")
                                    currop.set("id",k_arr[1])
                                    currtype = ET.SubElement(currop, "function")
                                    currtype.text = t
                                    if t in list_plots:
                                        currop.set("type","plot")
                                        pclass = classes.plot_inst(t)                                
                                        #get additional parameters
                                        h5add = conf.workdir+s.lower()+"_"+o+"_"+str(procid)+"_add.h5"
                                        addlist = []
                                        if "Additional Parameters" in k[op].keys():
                                            addlist = k[op]["Additional Parameters"]
      
                                        #get X for scatter plot      
                                        extrapars = {"opbranch" : k[op]}
                                        if "X" in k[op].keys():
                                            extrapars.update({"x" : k[op]["X"]})
                                            #create x label
                                            extrapars.update({"xlabel" : k[op]["X"]})                    
                                        #init hdf5 group for current operation
                                        h5op = acqgroup.create_group(op)                                                                
                                        plotdict, nodata, nodatax = pclass.create_plot_output(ET, y0, par, currop, addlist, str(i), conf.plotfromfile, extrapars, h5add, hfoutfile, h5op)
                                        if nodatax:
                                            errors.append({"type": "No data",
                                                        "msg" : "Parameter : " + par + ". 'X' parameter has no data available for Acquisition #"+str(i+1)+", Operation #"+k_arr[1],
                                                        "sub" : o,
                                                        "level" : "warning",
                                                        "system" : sysclass.source})
                                            w = ET.SubElement(curracq, "warning")
                                            w.set("category","no_data")
                                            w.text = "No data available for X parameter "+ k[op]["X"] +" during Operation #"+k_arr[1]
                                        if nodata and withdata and not nodatax:
                                            errors.append({"type": "No data",
                                                        "msg" : "Parameter : " + par + ". One or more additional parameters have no data available for Acquisition #"+str(i+1)+", Operation #"+k_arr[1],
                                                        "sub" : o,
                                                        "level" : "warning",
                                                        "system" : sysclass.source})
                                            w = ET.SubElement(curracq, "warning")
                                            w.set("category","no_data")
                                            w.text = "No data available for one or more additional parameters during Operation #"+k_arr[1]
                             
                                        if conf.plotfromfile:
                                            filename = conf.workdir+t+"__"+sysclass.name+"__"+o+"__"+par+"__"+str(i+1)+"__"+op                                   
                                            plotdata, labels, nodatapar = pclass.arrange_data_plot(plotdict, par)
                                            if len(plotdata) > 0:
                                                # add units to labels where applicable
                                                for li, l in enumerate(labels):
                                                    labels[li] = l                                              
                                                ploterror = make_plot_file(plotdata, labels, nodatapar, pclass, filename)
                                                if ploterror:
                                                    errors.append({"type": "Plot error",
                                                                "msg" : "Impossible to generate all the foreseen "+pclass.ptype+" plots for Parameter '"+par+"', Acquisition #"+str(i+1)+", Operation #"+k_arr[1],
                                                                "sub" : o,
                                                                "level" : "warning",
                                                                "system" : sysclass.source})
                                               
                                    else:
                                        currop.set("type","statistics")
                                        #statistical results
                                        add_text_name = ""
                                        try:
                                            #add analysis parameters if present
                                            funcpar = k[op]["Parameters"]
                                            for fp in funcpar.keys():
                                                curr_fpar = ET.SubElement(currop, "setting")
                                                curr_fpar.set("parameter", fp)
                                                curr_fpar.text = str(funcpar[fp])
                                                add_text_name += " "+fp+"="+str(funcpar[fp])
                                        except:
                                            funcpar = ""
                                        #add statistical value
                                        #search for function slug
                                        fpos = list_slugs.index(t)
                                        #get function name from list_stats
                                        funcname = list_stats[fpos]
                                        dqcfunc = list_func[fpos]
                                        if funcpar == "":
                                            stats_config = {funcname : dqcfunc}
                                            fkey = funcname
                                        else:
                                            stats_config = {funcname : {"func" : dqcfunc, "params" : funcpar, "npar" : len(funcpar)}}
                                            fkey = funcname + add_text_name
                                        if withdata:
                                            try:
                                                stats = calc_stat(y0['vals'], stats_config)
                                                funcvalue = stats[fkey]
                                                if isinstance(funcvalue, str):
                                                    fv_splitted = funcvalue.split("<br/>")
                                                    if len(fv_splitted) == 1:
                                                        #if only one value, add it
                                                        ET.SubElement(currop, "value").text = funcvalue
                                                    else:
                                                        tostore_hdf5 = ["sigma clip"]
                                                        if t in tostore_hdf5:
                                                            h5op = acqgroup.create_group(op)
                                                            res_xml = ET.SubElement(currop, "data")
                                                            res_xml.text = hfoutfile
                                                            #store results in hdf5
                                                            reshdf5 = h5op.create_group("value")
                                                        #split multiple values in more items                                                            
                                                        for res in fv_splitted:
                                                            curr_v_arr = res.split(" : ")
                                                            if t in tostore_hdf5:
                                                                data2store = ast.literal_eval(curr_v_arr[1])
                                                                reshdf5.create_dataset(curr_v_arr[0].lower(), data=data2store)
                                                            else:
                                                                res_xml = ET.SubElement(currop, "value")
                                                                res_xml.set("result",curr_v_arr[0].lower())
                                                                res_xml.text = str(curr_v_arr[1])
                                                else:
                                                    ET.SubElement(currop, "value").text = str(funcvalue)
                                            except Exception as e:
                                                w = ET.SubElement(curracq, "warning")
                                                w.set("category","stats error")
                                                w.text = "Impossible to perform operation '"+funcname+"'"
                                                errors.append({"type": "Stats error",
                                                            "msg" : "Impossible to perform Operation #"+str(k_arr[1])+" for parameter "+par+" during acquisition #"+str(i+1),
                                                            "sub" : o,
                                                            "level" : "warning",
                                                            "system" : sysclass.source}) 
                                                ET.SubElement(currop, "value").text = "N/A"
                                        else:
                                            stats = "No Data"
                                            ET.SubElement(currop, "value").text = "No Data Available" 
                    hf.close()
                    hfout.close()
            connection.close()
        #Finalize XML
        xmlstr = ET.tostring(sysbr, encoding='unicode') 
        #save XML file
        with open(conf.workdir+s+"_"+str(procid)+".xml", "w") as f:
            f.write(xmlstr)
        if not path.isfile(conf.workdir+s+"_"+str(procid)+".xml"):
            filerr = True

    errors.append({"filerr" : filerr})  
    errors.append({"locerr" : locerr})
    errors.append({"h5err" : h5err})    
    return errors  

def xml_combine_output(conf, filename):
    base = ET.parse(conf.workdir+"general.xml").getroot()
    for f in conf.systems:
        listfiles = []
        for fname in listdir(conf.workdir):
            if fname.startswith(f):
                listfiles.append(conf.workdir+fname)
  
        if len(listfiles) > 0 :
            first = listfiles[0]
            data = ET.parse(first).getroot()
            origins = data.findall("*")
            orig_tag = [otag.tag for otag in origins]                  
            for xf in listfiles[1:]:
                dataf = ET.parse(xf).getroot()
                curr_or = dataf.findall("*")
                for elem in curr_or:
                    if elem.tag in orig_tag:
                        idx = orig_tag.index(elem.tag)
                        origins[idx].extend(elem)                        
                    else:
                        origins.append(elem)
                        orig_tag.append(elem.tag)
                del dataf        
        else:
            origins = []
                    
        sysbr = ET.SubElement(base, "system")
        sysbr.set("name", f.lower())                    
        for el in origins:
            sysbr.append(el)            
          
    out = ET.tostring(base)
    xmlstr = minidom.parseString(out).toprettyxml(indent="")
    #save temporary final XML file
    temp_file = conf.workdir+"temp_final.xml"    
    with open(temp_file, "w") as f:    
        f.write(xmlstr)

    #read temp xml and insert lists stored in hdf5 results files
    change_xml(temp_file, "../users/report/"+filename+".xml")    

    #check if file has been created
    if path.isfile("../users/report/"+filename+".xml"):
        return True
    else:
        return False  
  
def change_xml(tmpfile, filename):
    final = open(filename,"w")  
    with open(tmpfile) as xml_file:
        s = None
        origin = None
        par = None
        acq = None
        op = None
        procid = None
        additional = None
        X = None
        while True:
            row = xml_file.readline().lstrip()
            if not row:
                break
            if row.startswith("<system"):
                s = row.split('name="')[1][:-3]
            if row.startswith("<hktm") or row.startswith("<science"):
                origin = row[1:-2]
            if row.startswith("<parameter "):
                par = row.split('name="')[1][:-3]
            if row.startswith("<acquisition "):
                acq = int(row.split('n="')[1][:-3])-1
            if row.startswith("<operation "):
                idstr = row.split(' ')[1]           
                op = idstr.split("=")[1][1:-1]
                additional = None
                X = None
            if row.startswith("<additional "):
                additional = row.split("param=")[1][1:-3]
            if row.startswith('<warning category="out_of_range"') or row.startswith('<error category="out_of_range"'):
                h5file = row.split(">")[1].split("<")[0]
                hf = h5py.File(h5file,"r")
                if row.startswith('<warning'):
                    l = "soft"
                else:
                    l= "hard"
                data = hf[par]['acquisition_'+str(acq)]['out_of_range'][l]
                dates = [datetime.utcfromtimestamp(dx).strftime('%Y-%m-%d %H:%M:%S') for dx in data[:,0]]
                values = list(data[:,1])
                tag_s = row.split(">")[0]+">"
                tag_e = "<"+row.split("<")[2]
                final.write(tag_s+"<dates>"+str(dates)+"</dates>\n")
                final.write("<values>"+str(values)+"</values>"+tag_e+"\n")
                hf.close()            
            elif row.startswith("<data>"):
                h5file = row.split(">")[1].split("<")[0]
                hf = h5py.File(h5file,"r")
                if additional is None:
                    data = hf[par]['acquisition_'+str(acq)]['Operation_'+op]
                    for k in data.keys():
                        if k != "additional" and k!="value" and k!="X":
                            if k == "dates":
                                tostore = [datetime.utcfromtimestamp(dx).strftime('%Y-%m-%d %H:%M:%S') for dx in data[k]]
                            else:
                                tostore = list(data[k][:])
                            final.write("<"+k+">"+str(tostore)+"</"+k+">\n")
                        if k == "value":
                            if len(data["value"].keys())>1:
                                for el in data["value"].keys():
                                    final.write(('<value result="'+el+'">'+str(list(data["value"][el][:]))+'</value>\n'))
                            else:
                                final.write(('<value>'+str(list(data["value"][el][:]))+'</value>\n'))
                else:
                    data = hf[par]['acquisition_'+str(acq)]['Operation_'+op]["additional"][additional]
                    for k in data.keys():
                        if k != "additional" and k!="value":
                            if k == "dates":
                                tostore = [datetime.utcfromtimestamp(dx).strftime('%Y-%m-%d %H:%M:%S') for dx in data[k]]
                            else:
                                tostore = list(data[k][:])
                            final.write("<"+k+">"+str(tostore)+"</"+k+">\n")                
                hf.close()

            elif row.startswith("<X "):
                X = row.split('param="')[1].split('">')[0]
                h5file = row.split(">")[1].split("<")[0]
                if h5file != "No Data available": 
                    hf = h5py.File(h5file,"r")
                    data = str(list(hf[par]['acquisition_'+str(acq)]['Operation_'+op]["X"][:]))
                    final.write('<X param="'+X+'">'+data+'</X>\n')
                    hf.close()
                else:
                    final.write(row)
            else:
                final.write(row)
    final.close()  

def xml_sys_errors(ET, root, conf, errors, inner_err):
    #update errors dict with inner_err
    for el in inner_err:
        curr_sys = el["system"]
        if curr_sys in errors.keys():
            err_list = errors[curr_sys]
            err_list.append(el)
        else:
            errors.update({curr_sys : [el]})
    for k,v in errors.items():
        err_sec = ET.SubElement(root, "system")
        err_sec.set("name",k.lower())
        if len(v)==0:
            ET.SubElement(err_sec, "error_status").text = "No errors detected"
        else:
            ET.SubElement(err_sec, "error_status").text = "Detected "+str(len(v))+" error(s)"
            for el in v:
                err_tag = ET.SubElement(err_sec, "error")
                if el["sub"] != "":
                    err_tag.set("origin",el["sub"])
                err_tag.set("type",el["type"])
                err_tag.set("level",el["level"])
                err_tag.text = el["msg"]

def xml_exp_info(ET, root, conf):
    expinfo = ET.SubElement(root, "exp_info")
    ET.SubElement(expinfo, "tstart").text = str(conf.tstart)
    ET.SubElement(expinfo, "time_window").text = str(conf.t_window)
    ET.SubElement(expinfo, "sampling").text = conf.sampling
    if conf.ts > 0:
        ET.SubElement(expinfo, "time_sampling").text = str(conf.ts)
    if conf.sfunc is not None:
        ET.SubElement(expinfo, "function_sampling").text = str(conf.sfunc)
    if conf.period == "ondemand":
        ET.SubElement(expinfo, "acquisitions_number").text = str(conf.nacq)
        if conf.nacq > 1:
            ET.SubElement(expinfo, "acquisition_time_step").text = str(conf.tacq)
    ET.SubElement(expinfo, "tstop").text = str(conf.tstop)
    
    if conf.nacq > 1:
        acq_det = ET.SubElement(expinfo, "acquisitions_details")
        for i in range(conf.nacq):
            curr_acq = ET.SubElement(acq_det, "acquisition")
            curr_acq.set("n", str(i+1))
            ET.SubElement(curr_acq, "tstart").text = conf.tsarr[i]
            ET.SubElement(curr_acq, "tstop").text = conf.tearr[i]            


def xml_general_info(ET, root, connconfig, conf, creation):
    general = ET.SubElement(root, "general")
    ET.SubElement(general, "generation_date").text = creation
    ET.SubElement(general, "user").text = conf.user
    ET.SubElement(general, "config_file").text = conf.configfile
    #get configfile owner
    con = util.connect_db(connconfig)
    owner = util.db_query(con, "config_files", "username,opmode" , statement = "WHERE filename = '" +conf.configfile+"'", res_type = "one")
    con.close()
    ET.SubElement(general, "config_owner").text = owner['username']
    ET.SubElement(general, "operating_mode").text = owner['opmode']

def xml_values_from_db(par,runid,acqid,subsystem,tbl_name,connection, nitems="one", max_runstep=1):
    if isinstance(par, list):
        statement = "WHERE runID = '"+str(runid)+"' AND (param='"
        add_statement = "' OR param='".join(par)
        statement += add_statement + "') AND acqID = "+acqid+" AND subsystem = '"+subsystem+"' group by param"
    else:
        statement = "WHERE runID = '"+str(runid)+"' AND param = '"+par+"' AND acqID = "+acqid+" AND subsystem = '"+subsystem+"' group by param"

    if max_runstep > 1:
        cols = 'param,GROUP_CONCAT(vals) as "vals", GROUP_CONCAT(dates) as "dates"'
    else:
        cols = 'param,dates,vals'
    res = util.db_query(connection, tbl_name+"_reports_data", cols, statement, nitems)

    return res

def create_xml_report(conf, runid, connconfig, nprocs, errors, parpos):
    """Generate the xml report containing all the results of analysis for all systems

    Parameters
    --------
        conf :
        runid : str
            experiment id assigned by AIDA
        connconfig : dict
            dictionary containing connection info to local AIDA DB

    Returns
    --------
        bool,
        True if the xml output has been created, False otherwise

        creation : string,
            creation date

        filename : string or None,
            if not None, the file name of created xml


    """

    ############### FOR BENCHMARK ###############    
    pipets, pipets_ts = util.get_time()
    ############################################# 
    now = util.utc_now()
    creation = now.strftime("%Y-%m-%d %H:%M:%S")    
    #set filename
    filename = set_report_filename(conf, runid, now)
    threads = []
    error_list = []    
    for i, source in enumerate(conf.systems):
        session = xmlThread(i, "XML_Thread_"+source, source, conf, connconfig, runid, nprocs, parpos[source])        
        threads = threads+[session]
        threads[i].start()    
    for th in threads:
        th.join()
        #get errors
        source_err = th.error_list
        error_list += source_err
       
    ############### FOR BENCHMARK ###############    
    gents, gents_ts = util.get_time()
    with open(conf.bm_tfile, "a") as f:                          
        f.write("GLOBAL SYSTEMS XML CREATION DURATION :\t"+str(util.pretty_time(gents_ts - pipets_ts))+"\n")
    ############################################################       
    
    #XML root with runid
    root = ET.Element("report", id=runid)
    #period
    ET.SubElement(root, "period").text = conf.period
    #filename
    ET.SubElement(root, "filename").text = filename
    #general info
    xml_general_info(ET, root, connconfig, conf, creation)
    #experiment info
    xml_exp_info(ET, root, conf)
    #section Notes
    notes = ET.SubElement(root, "notes")
    #errors summary
    #single system errors
    xml_sys_errors(ET, notes, conf, errors, error_list)
    #store general xml file
    xmlstr = ET.tostring(root, encoding='unicode')
    #save XML file
    with open(conf.workdir+"general.xml", "w") as f:
        f.write(xmlstr)

    ############### FOR BENCHMARK ###############    
    gente, gente_ts = util.get_time()
    with open(conf.bm_tfile, "a") as f:                          
        f.write("GENERAL INFO XML CREATION DURATION :\t"+str(util.pretty_time(gente_ts - gents_ts))+"\n")
    ############################################################            

    if path.isfile(conf.workdir+"general.xml"):
        #create XML output by merging general info & system XML files
        try:
            xml_created = xml_combine_output(conf,filename)
        
            ############### FOR BENCHMARK ###############    
            combote, combote_ts = util.get_time()
            with open(conf.bm_tfile, "a") as f:                          
                f.write("COMBINE XML DURATION :\t"+str(util.pretty_time(combote_ts - gente_ts))+"\n")
            ############################################################          
        
            if xml_created:
                return True, creation, filename
            else:
                return False, creation, None
        except Exception as e:
            return False, creation, None
    else:
        return False, creation, None

def create_pdf_report(filename, plotfromfile = False):
    """Generate the pdf report containing all the results of analysis for all systems

    Parameters
    --------
        filename : string,
            the file name of realated xml

    Returns
    --------
        bool,
        True if the pdf output has been created, False otherwise

    """

    now = util.utc_now()
    creation = now.strftime("%Y-%m-%d %H:%M:%S")
    #set filename
    pdffile = "../users/report/"+filename+".pdf"
    #get xml filename
    xmlfile = "../users/report/"+filename+".xml"
    #instatiate class to get data from XML
    xmldata = xmlData(xmlfile)
    #instantiate class to create pdf
    c = pdfBuilder(xmldata, plotfromfile, xmldata.rep_id)
    doc = MyDocTemplate(pdffile, pagesize=A4, showBoundary=0,leftMargin=5, rightMargin=5, topMargin=5, bottomMargin=5, author=c.author, title=c.title)
    #add report id
    c.add_centred_title("Euclid IOT On-Demand Report id: "+xmldata.rep_id, size=16,textcolor=[1,0,0])
    #add filename
    c.add_centred_title(filename, size=10,textcolor=[0,0,0], mtop=20)

    period = xmldata.get_period()
    #get general info from xml
    general = xmldata.get_general_info()
    c.add_general_info(general, period)

    #get experiment info from xml
    exp_info = xmldata.get_configuration()
   
    c.add_exp_info(exp_info)

    #get acquisitions details from xml
    acq_det = xmldata.get_acquisition_list()
    c.add_acq_details(acq_det)
    #get notes from xml
    notes = xmldata.get_notes()
    c.add_notes(notes)
    #Page break
    c.add_break()
    parsum = xmldata.get_par_summary()

    if len(parsum) > 0:
        c.add_par_summary(parsum)
        #Page break
        c.add_break()
        for so, data in parsum.items():
            s = so.split(" ")[0]
            stext = "System : "+s
            o = so.split(" ")[1]
            c.add_exp_section(stext,o)
            c.add_break()
            for p in data:
                #add parameter info
                c.add_infopar(p)
                #add error/warning list and messages
                errsum = xmldata.get_error_summary(s.lower(),o.lower(),p)
                c.add_error_list(errsum)
                #add summary of performed analysis
                opsum = xmldata.get_ops_summary(s.lower(),o.lower(),p)
                #add results
                expdata = xmldata.get_results(s.lower(),o.lower(),p, opsum)
                #check which analysis are displayed in report
                if len(acq_det)==0:
                    nacq = 1
                else:
                    nacq = len(acq_det)

                displayed = {}
                for nops in range(1,len(opsum)+1):
                    ops_array = []                
                    for na in range(1,nacq+1):
                        if len(expdata) > 0:
                            curr_expdata = expdata[str(na)][str(nops)]['res']
                            curr_optype = expdata[str(na)][str(nops)]['optype']
                        else:
                            curr_expdata = "No Data Available"
                            curr_optype = "None"
                           
                        if len(curr_expdata) == 0 or curr_expdata == "No Data Available":
                            ops_array.append(False)
                        elif isinstance(curr_expdata,dict):
                            hasdata = False
                            if curr_optype == "plot":
                                for resdict in curr_expdata.values():
                                        curr_vals = list(resdict.keys())[1]
                                        if resdict[curr_vals] != "No Data available":
                                            hasdata = True
                            elif curr_optype == "statistics":
                                first_item = list(curr_expdata.values())[0]
                                if first_item != "No Data available":
                                    hasdata = True
                            ops_array.append(hasdata)
                        else:
                            ops_array.append(True)
                    displayed.update({str(nops) : ops_array})
                
                c.add_exp_list(opsum, displayed)

                if len(expdata) > 0:
                    c.add_results(expdata, acq_det, p["par"], opsum, o, s)
                else:
                    c.add_exp_section("NO DATA AVAILABLE", textcolor=[255,0,0], size=26)
                c.content.append(NextPageTemplate('portrait_page'))
                c.add_break()

    c.add_exp_section("************* END OF FILE *************", size=26,textcolor=[0,0,0])
    content = c.content

    doc.multiBuild(content, canvasmaker=reportTemplate)    
   
    #check if created file exists
    if path.isfile(pdffile):
        return True
    else:
        return False
      
def make_plot_file(data, labels, nodata, pclass, filename):
    error = False
    created = []
    if pclass.splitplot == 0:
        #only single plot
        created = pclass.single_plot(data, labels, nodata, filename)
    elif pclass.splitplot == 1:
        #only multiplot if number of pars is > 1
        if len(labels) > 1:
            created = pclass.multi_plot(data, labels, nodata, filename)
        else:
            created = pclass.single_plot(data, labels, nodata, filename)
    elif pclass.splitplot == 2:
        #both single and multi plot, the latter only if number of pars is > 1
        created1 = pclass.single_plot(data, labels, nodata, filename)
        if len(labels) > 1:
            created2 = pclass.multi_plot(data, labels, nodata, filename)
        else:
            created2 = []
        created = created1 + created2
       
    if not all(created):
        error = True
    return error        
                   
def xml_error_pdf(conf, filename):
    base = ET.parse(conf.workdir+"general.xml").getroot()

    notes = base.find("notes")
    pdferror = ET.SubElement(notes,"error")
    pdferror.text = "Impossible to store report PDF file"
    pdferror.set("type", "pdf")

    out = ET.tostring(base, encoding='unicode')
    #save general XML file
    with open(conf.workdir+"general.xml", "w") as f:
        f.write(out)
    xml_combine_output(conf,filename)        
        