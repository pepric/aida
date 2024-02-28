#!/usr/bin/python

import cgi, cgitb 
cgitb.enable(display=0, logdir="cgi-logs")  # for troubleshooting
import glob
import os
import base64
import json
import classes
import ast
from pathlib import Path
from datetime import datetime
import sys
import functions as util
import socket
from math import ceil
from send_mail import Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import db_io
from shutil import copyfile, move, rmtree
# XML handling
import xml.etree.cElementTree as ET
from xml.dom import minidom
from time import sleep
import traceback
# PDF generation
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle,BaseDocTemplate, PageTemplate, Frame, PageBreak,NextPageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.axes import XValueAxis, YValueAxis, AdjYValueAxis, NormalDateXValueAxis
from svglib.svglib import svg2rlg
from io import BytesIO
os.environ['MPLCONFIGDIR'] = './tmp/'
import matplotlib
matplotlib.use('Agg')
os.environ['HOME'] = '/'
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
styleN = styles["Normal"]
styleH2 = styles["Heading2"]

class reportTemplate(canvas.Canvas):
    """
    Create report template with header and page numbers
    """
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

        
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
        
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
            
        canvas.Canvas.save(self)
        
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        page = "Page %s/%s" % (self._pageNumber, page_count)
        self.setFillColorRGB(0.8,0.8,0.8)
        self.setFont("Helvetica", 8)
        self.drawRightString(self.w-20, 0.2 * inch, page)

    def header(self, doc):
        """
        Add header
        """
        self.setPageSize(portrait(A4))
        self.h = PAGE_HEIGHT
        self.w = PAGE_WIDTH
        iodalogo = "../assets/images/minilogo_aida.png"
        self.drawImage(iodalogo,30,self.h-80,width=85,height=75,mask='auto')
        self.setFont('Helvetica-Bold',28)
        self.drawCentredString(self.w/2.0, self.h-50, "AIDA")
        self.setFont('Times-Bold',22)
        self.drawCentredString(self.w/2., self.h-85, "Advanced Infrastructure for Data Analysis")
        lsst_logo = "../assets/images/lsstback1.png"
        self.drawImage(lsst_logo,480,self.h-68,width=100,height=63,mask='auto')   

    def make_landscape(self,doc):
        """
        Settings for landscape page
        """
        self.setPageSize(landscape(A4))
        self.h = PAGE_WIDTH
        self.w = PAGE_HEIGHT

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        frame_a4 = Frame(self.leftMargin, self.bottomMargin+30, self.width, self.height-120,id='normal')
        frame_land = Frame(self.leftMargin, self.bottomMargin+30,self.height, self.width-30,id='landscape')
        template = PageTemplate(id='portrait_page', frames=frame_a4, onPage=reportTemplate.header)
        template_landscape = PageTemplate(id='landscape_page', frames=frame_land, onPage=reportTemplate.make_landscape)
        self.addPageTemplates([template, template_landscape])

class xmlData():
    def __init__(self, xmlfile):
        data = ET.parse(xmlfile)
        self.root = data.getroot()
        self.rep_id = self.root.get("id")
        self.filename = ""
        self.general_info = {}
        self.configuration = []
        self.notes = []
        self.systems = self.root.findall("system")

    def get_acquisition_list(self):
        output = []
        xmlacq = self.root.find("exp_info/acquisitions_details")
        if xmlacq is not None:
            acq_list = xmlacq.findall("acquisition")
            for item in acq_list:
                acqid = item.get("n")
                tstart = item.find("tstart").text
                tstop = item.find("tstop").text
                output.append([acqid,tstart,tstop])
        
        return output

    def get_configuration(self):
        output = {}
        xmlexp = self.root.find("exp_info")
        
        el = xmlexp.find("tstart")
        output.update({"Date Start :" : el.text})
        el = xmlexp.find("tstop")
        output.update({"Date Stop :" : el.text})  

        el = xmlexp.find("time_window")
        output.update({"Time Window (hours) :" : el.text})      
        
        el = xmlexp.find("sampling")
        output.update({"Sampling :" : el.text})
     
        if el.text != "full":
            #add additional settings for sampling TODO
            el = xmlexp.find("time_sampling")
            output.update({"Sampling time :" : el.text})
        if el.text == "by function":
            el = xmlexp.find("function_sampling")
            output.update({"Sampling function :" : el.text})
        try:
            el = xmlexp.find("acquisitions_number")
            output.update({"Number of acquisitions :" : el.text})
            if int(el.text) > 1:
                el = xmlexp.find("acquisition_time_step") 
                output.update({"Acquisition Time Step :" : el.text})
        except:
            pass
        return output

    def get_error_summary(self, s, origin, par):
        result = []
        for elem in self.root.iterfind('system[@name="'+s+'"]/'+origin+'/parameter[@name="'+par['par']+'"]'):
            xmlacq = elem.findall("acquisition")
            for a in xmlacq:
                acquid = a.get("n")
                errors = a.findall("error")
                warnings = a.findall("warning")
                errorlist = errors+warnings
                for err in errorlist:
                    estatus = err.tag
                    ecat = err.get("category")
                    if ecat == "out_of_range":
                        etxt = err.findall("dates")[0].text
                    else:
                        etxt = err.text
                    result.append({"acqid":acquid,"status":estatus, "cat":ecat, "text":etxt})

        return result
        
    def get_general_info(self):
        output = {}
        xmlgeneral = self.root.find("general")
        el = xmlgeneral.find("generation_date")
        output.update({"Report generation time :" : el.text})
        el = xmlgeneral.find("user")
        output.update({"Generated by :" : el.text})        
        el = xmlgeneral.find("config_file")
        output.update({"Configuration file :" : el.text})
        el = xmlgeneral.find("config_owner")
        output.update({"Owner :" : el.text})
        el = xmlgeneral.find("operating_mode")
        output.update({"Operating Mode :" : el.text})

        return output

    def get_notes(self):
        output = {}
        xmlnotes = self.root.find("notes")
        systems = xmlnotes.findall('system')
        for s in systems:
            curr_sys_err=[]
            sname = s.get("name").upper()
            error_status = s.find("error_status")
            errors = s.findall("error")
            for e in errors:
                level = e.get("level")
                origin = e.get("origin")
                if origin is None:
                    origin = "N/A"
                description = e.text
                curr_sys_err.append({"level" : level, "origin":origin,"descr":description})
            output.update({sname : {"status" : error_status.text, "list_err" : curr_sys_err}})              
        return output

    def get_ops_summary(self, s, o, p):
        result = {}
        plot_tags = ["additional", "setting", "X"]
        stat_tags = ["setting"]
        for elem in self.root.iterfind('system[@name="'+s+'"]/'+o+'/parameter[@name="'+p['par']+'"]/acquisition[@n="1"]'):
            ops = elem.findall("operation")
            for el in ops:
                opid = el.get("id")
                optype = el.get("type")
                func = el.find("function").text
                additional = []
                setting = []
                x = ""
                if optype == "plot":
                    for t in plot_tags:
                        extra = el.findall(t)
                        for e in extra:
                            xmlpar = e.get("param")
                            if e.tag == "additional":
                                additional.append(xmlpar)
                            elif e.tag == "setting":
                                setting.append(xmlpar+" : "+e.text)
                            elif e.tag == "X":
                                x += xmlpar
                elif optype == "statistics":
                    for t in stat_tags:
                        extra = el.findall(t)
                        for e in extra:
                            xmlpar = e.get("parameter")
                            if e.tag == "setting":
                                setting.append(xmlpar+" : "+e.text)
                result.update({opid : {"optype": optype, "type": func, "additional":additional,"setting":setting, "X":x}})

        return result

    def get_par_summary(self):
        output = {}
        if len(self.systems) > 0:
            for s in self.systems:
                origin = s.findall("*")
                for o in origin:
                    #set section name as "<system> <origin>"
                    section = s.get("name").upper()+" "+o.tag.upper()
                    #get parameters
                    pars = o.findall("*")
                    pardata = []
                    for p in pars:
                        #parameter fullname
                        parname = p.get("name")                    
                        elemList = p.findall("*")
                        datapar = {"par" : parname}

                        for elem in elemList:
                            curr_tag = elem.tag
                            if curr_tag != "acquisition" and curr_tag!="range":
                                curr_xml = p.find(curr_tag)
                                if curr_xml is not None:
                                    curr_txt = curr_xml.text
                                else:
                                    curr_txt = None
                                datapar.update({curr_tag : curr_txt})
                            
                        #get parameters summary data
                        haserror = False
                        haswarning = False
                        xmlacq = p.findall("acquisition")
                        if len(xmlacq) == 0:
                            haserror = True
                        else:
                            for a in xmlacq:
                                #errors
                                error = a.find("error")
                                #warnings
                                warning = a.find("warning")
                                if error is not None:
                                    haserror = True
                                if warning is not None:
                                    haswarning = True
                        datapar.update({"error" : haserror, "warning" : haswarning})
                        #range (if present)
                        ranges = p.findall("range")
                        extra = {}
                        if len(ranges) > 0:
                            for l in ranges:
                                limit = l.get("limit")
                                val = l.text
                                extra.update({limit : val})
                        datapar.update(extra)
                        pardata.append(datapar)
                    output.update({section : pardata})
        return output
        
    def get_period(self):
        return self.root.find("period").text.upper()
        
    def get_results(self, s, o, p, opssum):
        results = {}
        #parameter xml branch
        for elem in self.root.iterfind('system[@name="'+s+'"]/'+o+'/parameter[@name="'+p['par']+'"]'):
            #get all acquisitions
            xmlacq = elem.findall("acquisition")
            nacq = len(xmlacq)
            nores_array = []
            for acq in range(nacq):
                curr_xml = xmlacq[acq]
                acqid = acq+1
                #get all operations
                oplist = curr_xml.findall("operation")
                op_output = {}
                no_res = True
                for op in oplist:
                    #operation type (plot/statistics)
                    optype = op.get('type')
                    #operation id
                    opid = op.get('id')
                    #operation function
                    func = op.find('function').text
                    op_res = None
                    op_setting = []
                    if optype == "plot":
                        #get plot data
                        if func == "trend":
                            #get dates and values for main parameter
                            d = op.find('dates').text
                            v = op.find("values").text
                            no_res = False
                            op_res = {p["par"] : {"dates" : d, "vals" : v}}
                            #get dates and values for additional parameters
                            add = op.findall("additional")
                            for a in add:
                                aname = a.get('param')
                                op_res.update({aname : {"dates" : a.find('dates').text, "vals" : a.find("values").text}})
                        elif func == "scatter":
                            #get X and values for main parameter
                            x = op.find("X")
                            v = op.find("values").text
                            if v != "No Data available" and x.text != "No Data Available":
                                no_res = False
                            xname = x.get("param")
                            op_res = {p["par"] : {"X" : {"name":xname, "vals":x.text}, "vals" : v}}
                            #get X and values for additional parameters
                            add = op.findall("additional")
                            for a in add:
                                aname = a.get('param')
                                op_res.update({aname : {"X": {"name":xname, "vals":a.find("X").text}, "vals":a.find("values").text}})
                        elif func == "histogram":
                            #get counts and edges for main parameter
                            c = op.find('counts').text
                            e = op.find("edges").text
                            no_res = False                                
                            op_res = {p["par"] : {"counts" : c, "edges" : e}}
                            #get counts and edges for additional parameters
                            add = op.findall("additional")
                            for a in add:
                                aname = a.get('param')
                                op_res.update({aname : {"counts" : a.find('counts').text, "edges" : a.find("edges").text}})
                    else:
                        #get setting parameters
                        extra = op.findall("setting")
                        for e in extra:
                            op_setting.append(e.get('parameter')+" = "+e.text)
                        #all "value" tags
                        vals = op.findall("value")                   
                        if len(vals) > 1:
                            #result is composed by more values
                            op_res = {}
                            for v in vals:
                                k = v.get("result")
                                op_res.update({k : v.text})
                        else:
                            #single value result
                            op_res = vals[0].text
                        if op_res is not None and op_res != "No Data Available":
                            no_res = False
                    op_output.update({opid : {"optype" : optype, "func" : func, "res" : op_res, "set" : op_setting}})
                    #update output
                nores_array.append(no_res)
                results.update({str(acqid) : op_output})
        
        if any(nores_array):
            results = {}

        return results
        
class pdfBuilder():
    """
    Render XML data in PDF document
    """
    def __init__(self, xmldata="", plotfromfile = False, repid = ""):
        self.content = []
        self.plotfromfile = plotfromfile
        self.workdir = "../users/report/temp_id"+repid
        self.txt_fontsize = 8
        self.tbl_title_fontsize = 12
        self.paragraph_style = ParagraphStyle(
                                    name='Normal',
                                    fontSize=self.txt_fontsize, splitLongWords = 1)
        self.tbl_title_style =  ParagraphStyle('tblTitleStyle',
                                    fontName="Helvetica",
                                    fontSize= self.tbl_title_fontsize,
                                    textColor = colors.Color(0, 0, 0),
                                    alignment=TA_CENTER)
        self.author = "AIDA"
        self.title = "AIDA Report"
        self.toc = TableOfContents()

    def add_acq_details(self, alist):
        if len(alist) > 0:
            self.content.append(Spacer(1,0.2*inch))
            p = Paragraph("<b>Acquisition Details</b>", self.paragraph_style)
            t=Table([[p]],[2.5*inch], [0.2*inch], hAlign='LEFT')
            self.content.append(t)
            tbl_acq=[]
            self.content.append(Spacer(1,0.1*inch))
            h_acq = Paragraph('''<para align="center"><b>Acquisition #</b></para>''', self.paragraph_style)
            h_start = Paragraph('''<para align="center"><b>Start Date</b></para>''', self.paragraph_style)
            h_stop = Paragraph('''<para align="center"><b>End Date</b></para>''', self.paragraph_style)
            header = [h_acq, h_start, h_stop]
            tbl_acq.append(header)
            
            for a in alist:
                acqid = Paragraph('''<para align="center">'''+a[0]+'''</para>''', self.paragraph_style)
                tstart = Paragraph('''<para align="center">'''+a[1]+'''</para>''', self.paragraph_style)
                tstop = Paragraph('''<para align="center">'''+a[2]+'''</para>''', self.paragraph_style)
                tbl_acq.append([acqid, tstart, tstop])
            
            t=Table(tbl_acq, colWidths=[inch, 2*inch, 2*inch], hAlign='LEFT')
            t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

            alt_color_tbl(t, len(tbl_acq), startline = 1)
            self.content.append(t)
            self.content.append(Spacer(1,0.2*inch))         

    def add_break(self):
        self.content.append(PageBreak())
        
    def add_centred_title(self, text, textcolor=[0,0,0], size=28, mtop=0, mbottom=0):
        titleStyle = ParagraphStyle('title',
                           fontName="Helvetica-Bold",
                           fontSize=size,
                           textColor = colors.Color(textcolor[0], textcolor[1], textcolor[2]),
                           alignment=TA_CENTER,
                           spaceBefore=mtop,
                           spaceAfter=mbottom)
        p = Paragraph(text, titleStyle)
        self.content.append(p)

    def add_error_list(self, elist):
        if len(elist)>0:
            self.content.append(Spacer(1,0.2*inch))
            p = Paragraph("<b>Errors/Warnings Details</b>", self.paragraph_style)
            t=Table([[p]],[2.5*inch], [0.2*inch], hAlign='LEFT')
            self.content.append(t)
            
            tbl_error=[]
            self.content.append(Spacer(1,0.1*inch))
            h_level = Paragraph('''<para align="center"><b>Status</b></para>''', self.paragraph_style)
            h_acq = Paragraph('''<para align="center"><b>Acquisition #</b></para>''', self.paragraph_style)
            h_cat = Paragraph('''<para align="center"><b>Category</b></para>''', self.paragraph_style)
            h_descr = Paragraph('''<para align="center"><b>Description</b></para>''', self.paragraph_style)
            
            header = [h_level, h_acq, h_cat, h_descr]
            tbl_error.append(header)
            
            for e in elist:
                level = e["status"]
                if level == "error":
                    I = Image('../assets/images/serious.png', 0.15*inch, 0.15*inch) #DA CAMBIARE IL PATH
                elif level == "warning":
                    I = Image('../assets/images/warning.png', 0.15*inch, 0.15*inch)
                acqid = Paragraph('''<para align="center">'''+e["acqid"]+'''</para>''', self.paragraph_style)
                cat = Paragraph('''<para align="center">'''+e["cat"].replace("_"," ")+'''</para>''', self.paragraph_style)
                d_obj = e["text"]
                try:
                    d_list = ast.literal_eval(d_obj)
                    if isinstance(d_list, list):
                        l = len(d_list)
                        descr = Paragraph(level.capitalize()+" occurred "+str(l)+" time(s). See XML version for detailed info.", self.paragraph_style)
                except:
                    descr = Paragraph(d_obj, self.paragraph_style)

                tbl_error.append([I, acqid, cat, descr])
            
            t=Table(tbl_error, colWidths=[0.6*inch, 1.1*inch, inch, 5.3*inch], hAlign='LEFT')
            t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                    ('ALIGN', (0,0),(1,-1),"CENTER"),
                                    ('VALIGN',(0,0),(-1,-1),"MIDDLE")]))

            alt_color_tbl(t, len(tbl_error), startline = 1)
            self.content.append(t)
            self.content.append(Spacer(1,0.2*inch))         
            
    def add_exp_info(self, data):
        self.add_section("*** Configuration", color=[0,0,190])
        tabledata = []
        for k,v in data.items():
            p0 = Paragraph('''<b>'''+k+"""</b>""", self.paragraph_style)
            p1 = Paragraph(v, self.paragraph_style)
            tabledata.append([p0,p1])
        t=Table(tabledata,2*[2.5*inch], len(data)*[0.2*inch], hAlign='LEFT')
        self.content.append(t)

    def add_exp_list(self, data, displayed):
        self.content.append(Spacer(1,0.2*inch))

        if len(data) > 0:
            p = Paragraph("<b>List of performed analysis</b>", self.paragraph_style)
            t=Table([[p]],[2.5*inch], [0.2*inch], hAlign='LEFT')
            self.content.append(t)
            tbl_ops=[]
            self.content.append(Spacer(1,0.1*inch))
            h_name = Paragraph('''<para align="center"><b>Analysis</b></para>''', self.paragraph_style)
            h_opid = Paragraph('''<para align="center"><b>Op_ID</b></para>''', self.paragraph_style)
            h_notes = Paragraph("", self.paragraph_style)
            header = [h_name, h_opid, h_notes]
            cw = [1.1*inch, 0.8*inch, None]
            lendisp = len(displayed['1'])
            if lendisp == 1:
                header.append(Paragraph('''<para align="center"><b>Acq#1</b></para>''', self.paragraph_style))
                cw.append(0.8*inch)
            else:
                for nd in range(0,lendisp):
                    header.append(Paragraph('''<para align="center"><b>Acq#'''+str(nd+1)+'''</b></para>''', self.paragraph_style))
                    cw.append(None)
                    
            tbl_ops.append(header)

            for k,v in data.items():
                opid = Paragraph('''<para align="center">'''+k+'''</para>''', self.paragraph_style)
                exptype = v["optype"]
                if exptype == "statistics":
                    functxt = "Statistics"
                else:
                    functxt = v["type"].capitalize()
                expfunc = Paragraph('''<para align="center">'''+functxt+'''</para>''', self.paragraph_style)
                
                expadd = v["additional"]
                extrarow = []
                
                expset = v["setting"]
                expx = v["X"]
                if expx != "":
                    extrarow.append(Paragraph('''<para spaceAfter=5><b>X parameter : </b>''' + expx+'''</para>''', self.paragraph_style))
                
                if exptype != "statistics":
                    if len(expset) > 0:
                        for s in expset:
                            sname = s.split(" : ")[0]
                            sval = s.split(" : ")[1]
                            extrarow.append(Paragraph('''<para spaceAfter=5><b>'''+sname+''' : </b>'''+sval+'''</para>''', self.paragraph_style))
                else:
                    funame = v["type"].capitalize()
                    if len(expset) > 0:
                        settxt = str(expset).replace("[","(").replace("]",")").replace(":", "=").replace("'","")
                        extrarow.append(Paragraph('''<para spaceAfter=5>'''+funame+''' '''+settxt+'''</para>''', self.paragraph_style))
                    else:
                        extrarow.append(Paragraph('''<para spaceAfter=5>'''+funame+'''</para>''', self.paragraph_style))
                cols = [expfunc, opid, extrarow]
                if len(expadd) > 0:
                    extrarow.append(Paragraph("<b>Additional parameters : </b>"+", ".join(expadd), self.paragraph_style))           
                curr_disp = displayed[k]

                for icon in curr_disp:
                    if icon:
                        icon_disp = Image('../assets/images/ok.png', width=0.15*inch, height=0.15*inch)
                    else:
                        icon_disp = Image('../assets/images/serious.png', width=0.15*inch, height=0.15*inch)
                    cols.append(icon_disp)

                tbl_ops.append(cols)

            t=Table(tbl_ops, colWidths=cw, hAlign='LEFT')
            t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                    ('ALIGN', (0,0),(1,-1),"CENTER"),
                                    #('SPAN', (3,0),(-1,0)),
                                    ('VALIGN', (3,1),(-1,-1),"MIDDLE"),
                                    ('ALIGN', (3,1),(-1,-1),"CENTER"),
                                    ('VALIGN', (0,1),(1,-1),"MIDDLE")]))
                                    
            alt_color_tbl(t, len(tbl_ops),  startline = 1)
            self.content.append(t)
        else:
            p = Paragraph("<b>List of performed analysis : </b>", self.paragraph_style)
            p1 = Paragraph("<para color=red><b>NONE</b></para>", self.paragraph_style)
            t=Table([[p,p1]],2*[2*inch], [0.2*inch], hAlign='LEFT')
            self.content.append(t)

    def add_exp_section(self, maintext, subtext = "", textcolor=[0,0,190], size=28, subsize = 28):
        self.content.append(Spacer(1,150))
        tabledata = []
        titleStyle = ParagraphStyle('title',
                    fontName="Helvetica-Bold",
                    fontSize=size,
                    textColor = colors.Color(textcolor[0], textcolor[1], textcolor[2]),
                    alignment=TA_CENTER)
        
        p = Paragraph("<b>"+maintext+"</b>", titleStyle)
        tabledata.append([p])

        subtitleStyle = ParagraphStyle('subtitle',
                           fontName="Helvetica-Bold",
                           fontSize=subsize,
                           alignment=TA_CENTER)
        p = Paragraph("<b>"+subtext+"</b>", subtitleStyle)
        tabledata.append([p])
        
        t=Table(tabledata,PAGE_WIDTH,100)
        t.setStyle(TableStyle([ ('VALIGN',(0,0),(0,0),1),
                                ('VALIGN',(-1,-1),(-1,-1),'TOP')]))     
        self.content.append(t)
        
    def add_general_info(self, data, period):
        self.content.append(Spacer(1,0.4*inch))
        tabledata = []
        p = Paragraph('''<b>Report Periodicity</b>''', self.paragraph_style)
        period_p = Paragraph(period, self.paragraph_style)
        tabledata.append([p,period_p])
        ndata = len(data.items())+1
        for k,v in data.items():
            p0 = Paragraph('''<b>'''+k+"""</b>""", self.paragraph_style)
            p1 = Paragraph(v, self.paragraph_style)
            tabledata.append([p0,p1])
        t=Table(tabledata,2*[2.5*inch], ndata*[0.2*inch], hAlign='LEFT')
        self.content.append(t)

    def add_infopar(self, data):
        excluded_keys = ['par', 'error', 'warning', 'hard_max', 'hard_min', 'soft_max', 'soft_min']
        #get parameter name
        fullname = Paragraph('''<b>'''+data['par']+'''</b>''', self.paragraph_style)
        pname = Paragraph("<b>Parameter :</b>", self.paragraph_style)
        #init infotable
        infotable = [[pname, fullname]]
        #get info from specific fields
        for k,v in data.items():
            if k not in excluded_keys:
                curr_k = k.replace("_"," ")
                curr_k = curr_k[0].upper()+curr_k[1:]
                curr_k = Paragraph("<b>"+curr_k+" :</b>", self.paragraph_style)
                infotable.append([curr_k,Paragraph(v, self.paragraph_style)])
           
        #get range
        #soft
        try:
            minval = data['soft_min']
        except:
            minval = None
        try:
            maxval = data['soft_max']
        except:
            maxval = None           
            
        if (minval == "N/A") and (maxval == "N/A"):
            r = "N/A"
        elif (minval == "N/A") and (maxval != "N/A"):
            r="(-inf, "+maxval+"]"
        elif (minval != "N/A") and (maxval == "N/A"):
            r="["+minval+", +inf)"
        else:
            r="["+minval+", "+maxval+"]"
        r = Paragraph(r, self.paragraph_style)
        #hard        
        try:
            hminval = data['hard_min']
        except:
            hminval = None
        try:
            hmaxval = data['hard_max']
        except:
            hmaxval = None          

        if (hminval == "N/A") and (hmaxval == "N/A"):
            hr = "N/A"
        elif (hminval == "N/A") and (hmaxval != "N/A"):
            hr="(-inf, "+hmaxval+"]"
        elif (hminval != "N/A") and (hmaxval == "N/A"):
            hr="["+hminval+", +inf)"
        else:
            hr="["+hminval+", "+hmaxval+"]"
        hr = Paragraph(hr, self.paragraph_style)
        prange = Paragraph("<b>Soft Limits:</b>", self.paragraph_style)
        hprange = Paragraph("<b>Hard Limits:</b>", self.paragraph_style)        
        infotable.append([prange,r])
        infotable.append([hprange,hr])
  
        #get error status
        e = data['error']
        #get warning status
        w = data['warning']
        if e:
            I = Image('../assets/images/serious.png', width=0.15*inch, height=0.15*inch) #DA CAMBIARE IL PATH
        elif w:
            I = Image('../assets/images/warning.png', width=0.15*inch, height=0.15*inch) #DA CAMBIARE IL PATH
        else:
            I = Image('../assets/images/ok.png', width=0.15*inch, height=0.15*inch) #DA CAMBIARE IL PATH
            
        perror = Paragraph("<b>Error status :</b>", self.paragraph_style)
        infotable.append([perror,I])      
       
        t=Table(infotable, colWidths=[2*inch, 3.5*inch], rowHeights = self.txt_fontsize+2, hAlign='LEFT')
        self.content.append(t)

    def add_notes(self, data):
        self.add_section("*** Notes", color=[0,0,190])
        for s,v in data.items():
            #status summary
            statustable=[]
            p0 = Paragraph('''<b>'''+s+""" Status :</b>""", self.paragraph_style)
            p1 = Paragraph(v["status"], self.paragraph_style)       
            statustable.append([p0,p1])
            t=Table(statustable,2*[2.5*inch], [0.2*inch], hAlign='LEFT')
            self.content.append(t)
        #error list    
        for s,v in data.items():
            if len(v["list_err"])>0:
                self.content.append(Spacer(1,0.2*inch))
                p = Paragraph('''<b>'''+s+""" Error List</b>""", self.paragraph_style)
                t=Table([[p]],[2.5*inch], [0.2*inch], hAlign='LEFT')
                self.content.append(t)
                
                tbl_error=[]
                self.content.append(Spacer(1,0.1*inch))
                h_origin = Paragraph('''<para align="center"><b>Origin</b></para>''', self.paragraph_style)
                h_descr = Paragraph('''<para align="center"><b>Description</b></para>''', self.paragraph_style)
                h_level = Paragraph('''<para align="center"><b>Level</b></para>''', self.paragraph_style)
                header = [h_level, h_origin, h_descr]
                tbl_error.append(header)
                for d in v["list_err"]:
                    curr_level = d["level"]
                    if curr_level == "error":
                        curr_level = "serious"
                    I = Image('../assets/images/'+curr_level+'.png') #DA CAMBIARE IL PATH
                    I.drawHeight = 0.15*inch
                    I.drawWidth = 0.15*inch
                   
                    curr_origin = Paragraph('''<para align="center">'''+d["origin"].upper()+'''</para>''', self.paragraph_style)
                    curr_descr = Paragraph(d["descr"], self.paragraph_style)

                    tbl_error.append([I, curr_origin, curr_descr])

                t=Table(tbl_error,colWidths=[0.6*inch, inch, None],hAlign='LEFT')
                t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('ALIGN', (0,0),(-1,-1),"CENTER")]))

                alt_color_tbl(t, len(tbl_error),  startline = 1)
                self.content.append(t)
                self.content.append(Spacer(1,0.2*inch))

    def add_par_summary(self, data):
        self.add_section("*** Summary of analyzed parameters", color=[0,0,190])
        for section, d in data.items():
            tabledata = []
            s = Paragraph('''<para align="center"><b>'''+section+'''</b></para>''', self.tbl_title_style)
            tabledata.append([s,"","",""])
            h_par = Paragraph('''<para align="center"><b>Parameter</b></para>''', self.paragraph_style)
            h_sub = Paragraph('''<para align="center"><b>Subsystem / Data Product</b></para>''', self.paragraph_style)
            h_descr = Paragraph('''<para align="center"><b>Description</b></para>''', self.paragraph_style)
            h_level = Paragraph('''<para align="center"><b>Status</b></para>''', self.paragraph_style)
            tabledata.append([h_par,h_sub,h_descr,h_level])
            for items in d:    
                #column Parameter
                par = Paragraph(items["par"], self.paragraph_style)
                #column Subsystem
                sub = items.get("subsystem","-")
                dp = items.get("data_product","-")
                subpar = Paragraph('''<para align="center">'''+sub+" / "+dp+'''</para>''', self.paragraph_style)
                #column Description
                descr = items.get("description","")
                descr = Paragraph(descr, self.paragraph_style)
                #column Status
                e = items["error"]
                w = items["warning"]
                if e:
                    I = Image('../assets/images/serious.png') #DA CAMBIARE IL PATH
                elif w:
                    I = Image('../assets/images/warning.png') #DA CAMBIARE IL PATH
                else:
                    I = Image('../assets/images/ok.png') #DA CAMBIARE IL PATH
                I.drawHeight = 0.15*inch
                I.drawWidth = 0.15*inch
                tabledata.append([par,subpar,descr,I])
            #draw table
            rowH = (len(d)+2)*[None]
            rowH[0] = 30            
            t=Table(tabledata, colWidths=[None, None, None, 0.6*inch], rowHeights=rowH)
            t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                    ('ALIGN', (-2,2),(-1,-1),"CENTER"),
                                    ('ALIGN', (0,0),(-1,0),"CENTER"),
                                    ('SPAN', (0,0),(-1,0)),
                                    ('VALIGN',(0,0),(-1,-1),"MIDDLE")]))
            
            alt_color_tbl(t, len(tabledata),  startline = 2)
            self.content.append(t)
            self.content.append(Spacer(1,0.2*inch))

    def add_results(self, data, acq_det, par, opdata, origin, s):
        for i, acq_data in data.items():
            #if l(data) > 1, create page with acquisition title          
            if len(data) > 1:
                ts = acq_det[int(i)-1][1]
                te = acq_det[int(i)-1][2]
                sub = "["+ts + ", " + te +"]"
                self.content.append(NextPageTemplate('portrait_page'))
                self.add_break()
                self.add_exp_section("Acquisition #"+i, subtext = sub, textcolor=[0,0,0], size=26, subsize=22)
            statres = []
            for op, res in acq_data.items():
                optype = res['optype']
                if optype == "plot":
                    func = res["func"]
                    pclass = classes.plot_inst(func)
                    curr_op = opdata[str(op)]
                    if self.plotfromfile:
                        #current filename withour final image id
                        curr_img = []                        
                        curr_fname = func+"__"+s.lower()+"__"+origin.lower()+"__"+par+"__"+i+"__Operation_"+str(op)
                        for f in os.listdir(self.workdir):
                            if f.startswith(curr_fname):
                                curr_img.append(f)
                        curr_img.sort()
                        if len(curr_img) > 0:
                            self.plot_header(op,curr_op, par, pclass.name)
                            for img in curr_img:
                                I = Image(self.workdir+"/"+img)
                                I.drawHeight = PAGE_WIDTH-200
                                I.drawWidth = PAGE_HEIGHT-75
                                self.content.append(I)
                    else:
                        plotdata, labels, nodatapar, hasdata = pclass.arrange_data_plot(res['res'], par)
                        if hasdata:
                            self.plot_header(op,curr_op, par, pclass.name)
                            self.make_plot(plotdata, labels, nodatapar, pclass)
                elif optype == "statistics":
                    func = res["func"].capitalize()
                    setting = res["set"]
                    if len(setting) > 0:
                        func += " (" + ", ".join(setting) + ")"
                    val =  res["res"]
                    statres.append((func,val))
            if len(statres) > 0:
                self.render_statistics(statres, par)

    def add_section(self, text, fsize=12, color = [0,0,0], align = "LEFT"):     
        r = color[0]
        g = color[1]
        b = color[2]

        if align == "LEFT":
            sec_al = TA_LEFT
        elif align == "CENTER":
            sec_al = TA_CENTER            
        elif align == "RIGHT":
            sec_al = TA_RIGHT
            
        sectiontStyle = ParagraphStyle('sectiontStyle',
                   fontName="Helvetica",
                   fontSize=fsize,
                   textColor = colors.Color(r, g, b),
                   alignment=sec_al,
                   spaceBefore=20,
                   spaceAfter=10)
                   
        p = Paragraph(text, sectiontStyle)
        self.content.append(p)

    def add_toc(self, entry = None):
        if entry is None:
            self.add_section("*** Table of Contents", color=[0,0,190])      
            self.content.append(self.toc)
        else : 
            level = entry[0]
            title = entry[1]
            page = entry[2]
            self.toc.addEntry(level, title,page)

    def make_plot(self, data, labels, nodata, pclass):
        if pclass.splitplot == 0:
            #only single plot
            drawing = pclass.single_plot(data, labels, nodata)
            self.content.append(drawing)
        elif pclass.splitplot == 1:
            #only multiplot if number of pars is > 1
            if len(labels) > 1:
                drawing = pclass.multi_plot(data, labels, nodata)
                for item in drawing:
                    self.content.append(item)
            else:
                drawing = pclass.single_plot(data, labels, nodata)
                self.content.append(drawing)
        elif pclass.splitplot == 2:
            #both single and multi plot, the latter only if number of pars is > 1
            drawing = pclass.single_plot(data, labels, nodata)
            self.content.append(drawing)
            if len(labels) > 1:
                drawing = pclass.multi_plot(data, labels, nodata)
                for item in drawing:
                    self.content.append(item)

    def plot_header(self, op, curr_op, par, func):
        #horizontal template for plots
        self.content.append(NextPageTemplate('landscape_page'))
        self.add_break()
    
        title = Paragraph('''<para align="center"><b>'''+func.upper()+" - "+par+'''</b></para>''', self.tbl_title_style)
        opid = Paragraph('''<para align="center"><b>Operation '''+str(op)+'''</b></para>''', self.tbl_title_style)
        header = []
        tospan = 0
        header.append([opid,title])
        #get settings
        settings = curr_op['setting']
        for s in settings:
            curr_s = Paragraph('''<para align="left"><b>'''+s+'''</b></para>''', self.tbl_title_style)
            header.append([curr_s,""])
            tospan += 1
        #get X
        xpar = curr_op['X']
        if xpar != "":
            curr_x = Paragraph('''<para align="left"><b>X parameter : '''+xpar+'''</b></para>''', self.tbl_title_style)
            header.append([curr_x,""])
            tospan += 1
        #get additional parameters
        additional = curr_op['additional']
        if len(additional) > 0:
            if len(additional) > 3:
                addtext = "Too many additional parameters. See related table for details"
            else:
                addtext = ", ".join(additional)
            curr_a = Paragraph('''<para align="left"><b>Additional Parameters : '''+addtext+'''</b></para>''', self.tbl_title_style)
            header.append([curr_a,""])
            tospan += 1

        rowH = [24]
        for i in range(tospan):
            rowH +=[None]
        t=Table(header, colWidths=[2*inch, None], rowHeights=rowH, hAlign="CENTER")
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('VALIGN', (0,0), (-1,0), "MIDDLE"),
                                ('BACKGROUND', (1, 0), (1, 0), colors.lightgrey),
                                ('BACKGROUND', (0, 0), (0, 0), colors.yellow)]))
                                                    
        #span extra info columns
        for i in range(tospan):
            t.setStyle(TableStyle([('SPAN', (0, i+1), (-1, i+1))])) 
                                                    
        self.content.append(t)
        self.content.append(Spacer(1,0.2*inch))
        
    def render_statistics(self, data, par):
        hasdata = False
        tabledata = []
        #create header
        s = Paragraph('''<para align="center"><b>Statistical Analysis - '''+par+'''</b></para>''', self.tbl_title_style)
        tabledata.append([s,""])

        for r in data:
            f = Paragraph('''<b>'''+r[0]+'''</b>''', self.paragraph_style)
            if not isinstance(r[1], dict):
                if r[1] != 'No Data Available':
                    hasdata = True
                v = Paragraph(r[1], self.paragraph_style)
            else:
                v = []
                for k,item in r[1].items():
                    try:                  
                        d = ast.literal_eval(item)
                        if isinstance(d, list):
                            d_final = str(len(d)) + " values: see XML for more info"
                        else:
                            d_final = item
                    except:
                        d_final = item
                    if d_final != 'No Data Available':
                        hasdata = True
                    cell = Paragraph('''<b>'''+k+''' : </b>'''+d_final, self.paragraph_style)
                    v.append(cell)
            tabledata.append([f,v])

        rowH = (len(data)+1)*[None]
        rowH[0] = 30
        t=Table(tabledata, rowHeights=rowH, hAlign="CENTER")
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('SPAN', (0,0),(-1,0)),
                                ('VALIGN',(0,0),(-1,-1),"MIDDLE")]))
        alt_color_tbl(t, len(tabledata),  startline = 1)
        if hasdata:
            self.content.append(NextPageTemplate('portrait_page'))
            self.add_break()        
            self.content.append(t)

class pdfExpBuilder():
    """
    Render data from online experiments in PDF document
    """
    def __init__(self):
        self.content = []
        self.txt_fontsize = 12
        self.tbl_title_fontsize = 12
        self.paragraph_style = ParagraphStyle(
                                    name='Normal',
                                    fontSize=self.txt_fontsize)
        self.tbl_title_style =  ParagraphStyle('tblTitleStyle',
                                    fontName="Helvetica",
                                    fontSize= self.tbl_title_fontsize,
                                    textColor = colors.Color(0, 0, 0),
                                    alignment=TA_CENTER)
        self.author = "AIDA"
        self.title = "AIDA Experiment"

    def add_centred_title(self, text, textcolor=[0,0,0], size=28, mtop=0, mbottom=0):
        titleStyle = ParagraphStyle('title',
                           fontName="Helvetica-Bold",
                           fontSize=size,
                           textColor = colors.Color(textcolor[0], textcolor[1], textcolor[2]),
                           alignment=TA_CENTER,
                           spaceBefore=mtop,
                           spaceAfter=mbottom)
        p = Paragraph(text, titleStyle)
        self.content.append(p)

    def add_comments(self, notes, labels, flags, mtop=30):
        self.content.append(Spacer(1,mtop))
        title = Paragraph('''<b>Summary:</b>''', self.paragraph_style)
        title_tbl = Table([[title]])
        self.content.append(title_tbl)
        self.content.append(Spacer(1,10))
        
        notes_tbl = []
        h_status = Paragraph(''' ''', self.tbl_title_style)
        h_par = Paragraph('''<para align="center"><b>Parameter</b></para>''', self.tbl_title_style)
        h_note = Paragraph('''<para align="center"><b>Comments</b></para>''', self.tbl_title_style)
        notes_tbl.append([h_status,h_par,h_note])        
        for i, n in enumerate(labels):
            if n != "None":
                curr_flag = flags[i]
                if curr_flag == "Not Defined":
                    flagfile = "nd.png"
                else:
                    flagfile = curr_flag.lower()+".png"
                I = Image('../assets/images/'+flagfile, 0.15*inch, 0.15*inch)
                p1 = Paragraph('''<b>'''+n+'''</b>''', self.paragraph_style)
                curr_note = notes[i]
                if curr_note == "None":
                    curr_note = ""
                p2 = Paragraph(curr_note, self.paragraph_style)
                notes_tbl.append([I,p1,p2])
        t = Table(notes_tbl, colWidths=[0.3*inch, None, None])
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('VALIGN',(0,0),(-1,-1),"MIDDLE")]))
        alt_color_tbl(t, len(notes_tbl), startline = 1)        
        self.content.append(t)

    def add_filelist(self, flist, mtop=30):
        self.content.append(NextPageTemplate('landscape_page'))      
        self.content.append(PageBreak())        
        #Title
        h = Paragraph("<para align='center' spacea=10><b>List of involved files</b></para>", self.paragraph_style)
        t = Table([[h]], rowHeights=0.5*inch, hAlign="CENTER")
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey), 
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))            
        self.content.append(t)
        #Table Header
        tabledata = []
        r0 = flist[0]
        header = []
        for k in r0.keys():
            header.append(Paragraph('''<para align="center"><b>'''+k+'''</b></para>''', self.tbl_title_style))
        tabledata.append(header)
        #Table data
        for r in flist:
            content = []
            for k,v in r.items():
                if "file" in k or "File" in k: 
                    if k=="Filename":
                        fname = v
                    else:
                        fname=v.split(">")[1].replace("</a","")
                    content.append(Paragraph('''<para align="center">'''+fname+'''</para>''', self.paragraph_style))
            tabledata.append(content)
        
        t = Table(tabledata)
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('VALIGN',(0,0),(-1,-1),"MIDDLE")]))
        alt_color_tbl(t, len(tabledata), startline = 1)        
        self.content.append(t)      
        
    def add_image(self, fname, w=None, h=None):
        self.content.append(NextPageTemplate('landscape_page'))
        self.content.append(PageBreak())
        I = Image(fname)
        if w is None:
            I.drawHeight = PAGE_WIDTH-60
        else:
            I.drawHeight = w
        if h is None:
            I.drawWidth = PAGE_HEIGHT
        else:
            I.drawWidth = h 
        self.content.append(I)    

    def add_overplots_info(self, marr, sarr, mtop = 10):

        self.content.append(Spacer(1,mtop))      
        tabledata = []

        h_stats = Paragraph('''<b>-  Overplots</b>''', self.paragraph_style)
        tabledata.append([h_stats, ""])
        for i,mt in enumerate(marr):
            parr = []
            parrname = []
            m = mt[1]
            mname = mt[0]            
            s = sarr[i][1]
            sname = sarr[i][0]
            if m is not None and m!=-999:
                mstr = mname + " : "+m
                parr.append(mstr)
            if s is not None and s!=-999:
                sstr = sname + " : "+s
                parr.append(sstr)                
            l = ", ".join(parr).replace("_"," ")
            p = Paragraph(l, self.paragraph_style)        
            tabledata.append(["", p])
        t=Table(tabledata, colWidths=[0.3*inch, None])
        t.setStyle(TableStyle([('SPAN', (0,0),(-1,0))]))
        self.content.append(t)
        
    def add_par_summary(self, data, source, mtop=30):
        self.content.append(Spacer(1,mtop))
        title = Paragraph('''<b>Analyzed Parameters:</b>''', self.paragraph_style)
        title_tbl = Table([[title]])
        self.content.append(title_tbl)
        self.content.append(Spacer(1,10))
        
        tabledata = []
        h_source = Paragraph('''<para align="center"><b>'''+source+'''</b></para>''', self.tbl_title_style)
        tabledata.append([h_source, "",""])
        h_par = Paragraph('''<para align="center"><b>Parameter</b></para>''', self.tbl_title_style)
        h_sub = Paragraph('''<para align="center"><b>Subsystem</b></para>''', self.tbl_title_style)
        h_descr = Paragraph('''<para align="center"><b>Description</b></para>''', self.tbl_title_style)
        header = [h_par,h_sub,h_descr]
        if len(data[0][3]) > 0:
            for k in data[0][3].keys():
                header.append(Paragraph('''<para align="center"><b>'''+k+'''</b></para>''', self.tbl_title_style))
        tabledata.append(header)
       
        for item in data:
            par = Paragraph(item[0], self.paragraph_style)          
            sub = item[1]
            if sub is None:
                sub = ""
            sub = Paragraph(sub, self.paragraph_style)
            descr = item[2]
            if descr is None:
                descr = ""
            
            descr = Paragraph(descr, self.paragraph_style)
            content = [par,sub,descr]
            if len(item[3]) > 0:
                for k,v in item[3].items():
                    content.append(Paragraph(v, self.paragraph_style))
            tabledata.append(content)        
        
        t=Table(tabledata, colWidths=[None, None, None])
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                ('SPAN', (0,0),(-1,0)),
                                ('VALIGN',(0,0),(-1,-1),"MIDDLE")]))
        alt_color_tbl(t, len(tabledata),  startline = 2)
        self.content.append(t)

    def add_plot_info(self, pclass, labels, mtop=10, title=None):    
        self.content.append(Spacer(1,mtop))      
        tabledata = []
        if title is not None:
            h = title
        else:
            h = pclass.name
        if isinstance(pclass.vs, int):
            vs = labels[pclass.vs]
        else:
            vs = pclass.vs

        h_plot = Paragraph('''<b>-  '''+h+'''</b>''', self.paragraph_style)
        tabledata.append([h_plot, ""])            
            
        for i in range(1,len(labels)):
            descr = labels[i]
            if vs!="":
                descr = descr + " vs " + vs
            p = Paragraph(descr, self.paragraph_style)
            tabledata.append(["", p])           
        t=Table(tabledata, colWidths=[0.3*inch, None])
        t.setStyle(TableStyle([('SPAN', (0,0),(-1,0))]))
        self.content.append(t)           
        
    def add_single_row(self, row1, row2, fontsize = None, mtop = 15):
        self.content.append(Spacer(1,mtop))
        if fontsize is None:
            fontsize = self.txt_fontsize          
        c1 = Paragraph("<para fontsize='"+str(fontsize)+"'><b>"+row1+"</b></para>", self.paragraph_style)
        c2 = Paragraph("<para fontsize='"+str(fontsize)+"'>"+row2+"</para>", self.paragraph_style)
        line = [[c1,c2]]
        if row2 == "":
            cols = [6*inch, inch]
        else:
            cols = [2*inch, 6*inch]
        t=Table(line, colWidths=cols, rowHeights = self.txt_fontsize+2, hAlign='LEFT')
        self.content.append(t)        

    def add_statistics(self, stats, labels):
        txt_font = 'Helvetica-Bold'
        txt_fontsize = 10
        space_len = stringWidth(" ", txt_font, txt_fontsize)
      
        self.content.append(NextPageTemplate('portrait_page'))
        stats = ast.literal_eval(stats)

        stats_k = list(stats.keys())
        for i, par in enumerate(labels):
            if par != 'None':
                self.content.append(PageBreak())        
                h = Paragraph("<para align='center' spacea=10><b>"+par+" Statistics</b></para>", self.paragraph_style)
                t = Table([[h]], rowHeights=0.5*inch, hAlign="CENTER")
                t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey), 
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))            
                self.content.append(t)
                curr_k = stats_k[i]
                curr_stats = stats[curr_k]
                max_stats = max(curr_stats.keys(), key = len).replace("_"," ")
                max_stats_width = stringWidth(str(max_stats), txt_font, txt_fontsize)
                sep_width = stringWidth(" : ", txt_font, txt_fontsize)                
                stats_style =   ParagraphStyle('stats',
                                            fontName="Helvetica",
                                            fontSize= txt_fontsize,
                                            textColor = colors.Color(0, 0, 0),
                                            leading = txt_fontsize+4,
                                            alignment=TA_LEFT, spaceBefore = 15,
                                            firstLineIndent = -max_stats_width-10,
                                            leftIndent = max_stats_width+sep_width+30,
                                            splitLongWords = 1)
                
                for k, v in curr_stats.items():
                    v = str(v)
                    v = v.replace("<br>","<br/>")


                    curr_stat = k.replace("_", " ")
                    stat_width = stringWidth(curr_stat, txt_font, txt_fontsize)               
                    space_to_add = ceil((max_stats_width - stat_width)/space_len)
                    p = Paragraph("<b>"+curr_stat+space_to_add*'&nbsp'+" :&nbsp</b>"+v, stats_style)
                    self.content.append(p)
                                      
    def add_op_info(self, op, flist, mtop = 10):
        self.content.append(Spacer(1,mtop))      
        tabledata = []
        if op == "difference":
            title = 'Statistics on "DIFFERENCE" Image (A - B)'
        else:
            title = "NA"
        h_op = Paragraph('''<b>   - Operation: </b>'''+title, self.paragraph_style)
        tabledata.append([h_op, ""])
        if op == "difference":
            h_1 = Paragraph('''<b>   - File A: </b>''', self.paragraph_style)
            f_1 = Paragraph(flist[0], self.paragraph_style)
            tabledata.append([h_1, ""])
            tabledata.append([f_1, ""])
            h_2 = Paragraph('''<b>   - File B: </b>''', self.paragraph_style)
            f_2 = Paragraph(flist[1], self.paragraph_style)
            tabledata.append([h_2, ""]) 
            tabledata.append([f_2, ""]) 
            h_3 = Paragraph('''<b>   - Difference File: </b>''', self.paragraph_style)
            f_3 = Paragraph(flist[2], self.paragraph_style)
            tabledata.append([h_3, ""])    
            tabledata.append([f_3, ""])    

        t=Table(tabledata, colWidths=[None, None])
        t.setStyle(TableStyle([('SPAN', (0,0),(-1,0))]))
        self.content.append(t)        
        
    def add_stats_info(self, stats, mtop = 10):
        self.content.append(Spacer(1,mtop))      
        tabledata = []

        h_stats = Paragraph('''<b>-  Statistics</b>''', self.paragraph_style)
        tabledata.append([h_stats, ""])             
        l = ", ".join(stats).replace("_"," ")
        p = Paragraph(l, self.paragraph_style)        
        tabledata.append(["", p])
        t=Table(tabledata, colWidths=[0.3*inch, None])
        t.setStyle(TableStyle([('SPAN', (0,0),(-1,0))]))
        self.content.append(t)

    def add_status(self, status, mtop = 15):
        self.content.append(Spacer(1,mtop)) 
        if status == "nd":
            status_val = "N/A"
        else:
            status_val = status.upper()
        pstatus = Paragraph(status_val, self.paragraph_style)
   
        I = Image('../assets/images/'+status+'.png')
                    
        I.drawHeight = 0.15*inch
        I.drawWidth = 0.15*inch 

        tabledata = []
        h_status = Paragraph("<b>Experiment Status:</b>", self.paragraph_style)
        tabledata.append([h_status, pstatus, I])
        t=Table(tabledata, colWidths=[2*inch, inch, inch], hAlign='LEFT')
        self.content.append(t)      

class pdfImgBuilder(pdfExpBuilder):
    """
    Render data from online experiments in PDF document
    """
    def __init__(self):
        self.content = []
        self.txt_fontsize = 12
        self.tbl_title_fontsize = 12
        self.paragraph_style = ParagraphStyle(
                                    name='Normal',
                                    fontSize=self.txt_fontsize)
        self.tbl_title_style =  ParagraphStyle('tblTitleStyle',
                                    fontName="Helvetica",
                                    fontSize= self.tbl_title_fontsize,
                                    textColor = colors.Color(0, 0, 0),
                                    alignment=TA_CENTER)
        self.author = "AIDA"
        self.title = "AIDA Experiment"
        
    def add_img_comment(self, notes, mtop = 15):
        self.content.append(Spacer(1,mtop)) 
        pstatus = Paragraph(notes, self.paragraph_style)
        tabledata = []
        h_status = Paragraph("<b>Comments:</b>", self.paragraph_style)
        tabledata.append([h_status, pstatus])
        t=Table(tabledata, colWidths=[2*inch, None], hAlign='LEFT')
        self.content.append(t)          
        
def alt_color_tbl(tbl, nrows, startline = 0):
    for each in range(startline,nrows):
        if each % 2 == 0:
            bg_color = colors.lightgrey
        else:
            bg_color = colors.whitesmoke
        tbl.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))         
        
def set_filename(plot, now):
    date = now.strftime("%Y%m%d")
    time = now.strftime("%H%M%S")
    name = "exp_"+plot+"_"+date+"_"+time

    return name

def create_png(img, fname, user):

    error = 0
    complete_name = "../users/" + user + "/" + fname + ".png"
    img64 = img.split(",")[1]
    b64 = bytes(img64+"===",'utf-8')
    try:
        with open(complete_name, "wb") as fh:
            fh.write(base64.decodebytes(b64))
    except:
            error = 1
            
    return error, complete_name
    
def add_stats_table(pdf, stats, labels):

    keys=[]
    stats = json.loads(stats)
    for key in stats:
        keys.append(key)

    effective_page_width = pdf.w - 2*pdf.l_margin

    for i in range(len(labels)):
        par_name = labels[i]
        if par_name != "None":
            pdf.ln(15)
            #create line with parameter name
            pdf.set_font('Arial', 'B', 14)

            values = stats[keys[i]]
            pdf.add_stats_results(values, par_name, t = True)
            
def create_image_pdf(data):
    #Flag image into DB without creating PDF. To create PDF you need to modify pdfcreator
    #get data from args
    error = 0
    username = data["user"].value
    filename = data["filename"].value
    try:
        source = data["source"].value
    except:
        source = "generic"
    status = data["status"].value 
    save = data["save"].value
    try:        
        notes = data["notes"].value
    except:
        notes = "-"
    try:
        emailto = data['email'].value
    except:
        emailto = ""
    try:        
        imgs = data.getlist('images[]')
    except:
        imgs = []
    
    fullname = data["fullname"].value

    if len(fullname.split("/")) > 1:
        local = False
    else:
        local = True

    hasimg = 0    
    if not local:
        #image is not from local pc
        filein = "../"+fullname
        hasimg = 1        
    if save == "private":
        fileout = "../users/"+username+"/stored/"+filename
        fpath = username
        tbl = "user"
        store_dir = username+"/stored"        
    else:
        fileout = "../users/stored/"+filename
        fpath = "stored"
        tbl = "stored"
        store_dir = "stored"        
        
    now = util.utc_now()
    sleep(5)
    try:
        #create PDF      
        pfile = set_filename("image", now)
        title = "Image analysis on "+now.strftime("%Y-%m-%d %H:%M:%S")      
        c = pdfImgBuilder()  
        #experiment title
        c.add_centred_title(title, size=18,textcolor=[0,0,0])
        #add user
        c.add_single_row("User: ", username, mtop = 60) 
        #image filename      
        c.add_single_row("Image File: ", filename, mtop = 30)
        #add image origin
        if local:
            origin = "Local"
        else:
            opmode = util.repConfig().get_opmode()
            origin = "Remote archive - "+opmode[0].upper()
        c.add_single_row("Image repository: ", origin, mtop = 15)
        #source
        if source != "generic":
            c.add_single_row("System: ", source, mtop = 30)
        else:
            c.add_single_row("System: ", "N/A", mtop = 30)
        #add exp status           
        c.add_status(status, mtop=30) 
        #add comment
        c.add_img_comment(notes)
        img_dir =  "../users/"+username+"/tmp/"+filename
        if len(imgs) > 0:
            mainimg = imgs[0]+".jpg"
            #add main image 
            c.add_image(img_dir+"/"+mainimg, w=4.5*inch, h=2.35*4.5*inch)  
            #add analysis images
            aux_arr = []
            regstats = []
            for el in imgs[1:]:
                try:
                    curr_img = img_dir+"/"+el+".jpg"
                    fsize = os.stat(curr_img).st_size
                    if fsize >= 2048:
                        I1 = Image(curr_img)
                    else:
                        raise Exception
                except Exception as e:
                    I1 = Image("../assets/images/"+el+"_error.jpg")
                    
                if el != "js9_RegionStats":
                    I1.drawHeight = 3*inch
                    I1.drawWidth = 3*inch
                    aux_arr.append(I1)
                else:
                    I1.drawHeight = 2.5*inch
                    I1.drawWidth = 4*inch                  
                    regstats.append(I1)
                    
            tabledata = [aux_arr[x:x+2] for x in range(0, len(aux_arr), 2)]
            t=Table(tabledata, hAlign='CENTER')
            if len(regstats) > 0:
                rt = Table([regstats], hAlign='CENTER')
                c.content.append(Spacer(1,15))          
                c.content.append(rt)
            c.content.append(NextPageTemplate('portrait_page'))
            c.content.append(PageBreak())            
            c.content.append(t)                    
  
        downloadfile = "users"+"/"+store_dir+"/"+pfile+".pdf"      
        pdffile = '../'+downloadfile
  
        content = c.content
        doc = BaseDocTemplate(pdffile, pagesize=A4, showBoundary=0,leftMargin=5, rightMargin=5, topMargin=5, bottomMargin=5, author=c.author, title=c.title)
        frame_a4 = Frame(doc.leftMargin, doc.bottomMargin+30, doc.width, doc.height-120,id='normal')
        frame_land = Frame(doc.leftMargin, doc.bottomMargin+30,doc.height, doc.width-30,id='landscape')

        template = PageTemplate(id='portrait_page', frames=frame_a4, onPage=reportTemplate.header)
        template_landscape = PageTemplate(id='landscape_page', frames=frame_land, onPage=reportTemplate.make_landscape)
        doc.addPageTemplates([template, template_landscape])

        doc.build(content, canvasmaker=reportTemplate)        

        #remove img temp directory
        rmtree(img_dir)         
        if hasimg and not os.path.isfile(fileout):        
            #copy file to stored directory      
            copyfile(filein,fileout)
        connconf = util.repConfig().data['local_db']
        connection = util.connect_db(connconf)            
        util.update_stored(connection, pfile, username, util.utc_now(), "fits", "image", status, fpath, tbl = tbl, comment=json.dumps({filename : notes, "img" : hasimg}), pars=filename, source=source, plot_id=0) 
           
        connection.close()
            
        #send email
        if emailto!="":
            try:
                mail = Email("../smtp.json")
                s = "New image flagged and stored"
                f = "AIDA"
            
                text = mail.ok_flagged([username, save, source, status, notes], filename, "image")
                msg = mail.set_message(s,f,emailto,text,"")
                mail.send_mail(msg)
            except:
                error = 2
    except Exception as e:
        downloadfile="none"
        error = 1

    out = {"error" : error, "file" : filename, "pdffile" : util.repConfig().main+"/"+downloadfile}
    return out    
  
def create_plot_pdf(data):
    error = 0
    #get data from frontend
    img = data['img'].value
    source = data['source'].value
    tstart = data['tstart'].value
    tstop = data['tstop'].value
    user = data['user'].value
    plot = data['plot'].value
    try:
        pid = data['pid'].value
    except:
        pid = "undefined"
    usecase = data['usecase'].value
    save = data['save'].value    
    tbl = data['tbl'].value 
    try:
        op = data['plot_subtype'].value
    except:
        op = None
    
    try:
        pdata = data['plotdata'].value
        expres = json.loads(pdata)
    except:
        pdata = None
        expres = None
    labels = data.getlist('labels[]')
    notes = data.getlist('notes[]')
    flags = data.getlist('flags[]')
    status = data['status'].value
    loc = data['location'].value
    if plot != "img_analysis":
        if usecase == "pre-generated":
            stats = None
        else:
            stats = data['stats'].value
    else:
        labels = [l.strip() for l in labels]
        stats = {}
        for i,l in enumerate(labels):
            stats.update({"y"+str(i)+"_stats" : expres[l]})
        stats = str(stats).replace("'","\"")   

    try:
        emailto = data['email'].value
    except:
        emailto = ""

    try:
        flist = json.loads(data["filesdata"].value) 
    except:
        flist = []
        
    #get connection parameters
    conf = util.repConfig()
    connmsg={}  
    if conf.error == 0:
        try:
            connection = util.connect_db(conf.data['local_db'])
            locerr = 0
        except:
            locerr = 1
            e.localstatus = 1
            exit(1)

        now = util.utc_now()

        try:
            if usecase == "pre-generated":
                plotname = "pre-generated_"+op
            else:
                plotname = plot
            filename = set_filename(plotname, now)
            title = "Experiment on "+now.strftime("%Y-%m-%d %H:%M:%S")
            c = pdfExpBuilder()  
            #experiment title
            c.add_centred_title(title, size=18,textcolor=[0,0,0])
            #add user
            c.add_single_row("User: ", user, mtop = 60)            
            #add date start/stop
            if usecase != "image analysis":
                if tstart != "undefined":
                    c.add_single_row("Date Start: ", tstart, mtop = 30) 
                if tstop != "undefined":
                    c.add_single_row("Date End: ", tstop, mtop = 5)
                if pid != "undefined":
                    c.add_single_row("Product ID: ", pid, mtop = 30)
            #add operating mode
            opmode = util.db_query(connection, "operation_modes", "mode", statement = "WHERE enable=1", res_type = "one")
            c.add_single_row("Operating mode: ", opmode['mode'].upper(), mtop = 15) 
            #add parameters info
            if usecase != "image analysis":
                tbl = tbl+"_"+source.lower()+"_params"
                par_items=[]
                for p in labels:
                    if p != "None":
                        pcore = p.split(" (")[0]
                        x = classes.sys_inst(source)
                        curr_paritems = x.set_pdf_params_items(pcore, connection, tbl, usecase)
                        if curr_paritems not in par_items:
                            par_items.append(curr_paritems)   
                c.add_par_summary(par_items, source)
            connection.close()            
            #add exp description
            c.add_single_row("Experiment Description:", "", mtop = 30)
            # plot info
            if plot != "statistics" and plot != "img_analysis":
                if usecase == "pre-generated":
                    pclass = classes.plot_inst(op)
                    tit_plot = "PRE-GENERATED "+pclass.name
                else:
                    pclass = classes.plot_inst(plot)                
                    tit_plot = None
                c.add_plot_info(pclass, labels, title=tit_plot)
            elif plot == "img_analysis":
                #extract file list
                filelist = [x["Filename"] for x in flist]
                #add info about operation
                c.add_op_info(op, filelist)
            #statistics info
            if stats is not None:
                stats_dict = ast.literal_eval(stats)
                c.add_stats_info(stats_dict["y0_stats"].keys())
            else:
                if usecase == "pre-generated":
                    if expres is not None:
                        m = []
                        s = []
                        for d,dres in expres.items():
                            if isinstance(dres,dict):
                                mname = list(dres)[2]
                                sname = list(dres)[3]
                                m.append((mname,dres[mname]))
                                s.append((sname,dres[sname]))
                        c.add_overplots_info(m,s)
            #add exp status           
            c.add_status(status, mtop=30)
            #add comments
            comment_exp={} 
            if len(notes) > 0:
                c.add_comments(notes, labels, flags, mtop=30)
                for i,n in enumerate(notes):
                    if labels[i] != "None":
                        comment_exp.update({labels[i] : n})
            #add image
            if plot != "statistics" and plot != "img_analysis":
                #save temp image
                img_err, fname = create_png(img, filename, user)             
                if img_err == 0:
                    #add plot image 
                    c.add_image(fname)                    
                else:
                    c.content.append(PageBreak())
                    c.add_centred_title("Impossible to store plot image!", size=26,textcolor=[1,0,0], mtop = PAGE_WIDTH/2)                    
            #add statistics
            if stats is not None:
                c.add_statistics(stats, labels)
           
            #store pdf
            if save == "private":
                store_dir = user+"/stored"
                fpath = user
                tbl = "user"            
            else:
                store_dir = "stored"
                fpath = "stored"  
                tbl = "stored"  
            downloadfile = "users"+os.sep+store_dir+os.sep+filename+".pdf"      
            pdffile = '../'+downloadfile
  
            content = c.content
            doc = BaseDocTemplate(pdffile, pagesize=A4, showBoundary=0,leftMargin=5, rightMargin=5, topMargin=5, bottomMargin=5, author=c.author, title=c.title)
            frame_a4 = Frame(doc.leftMargin, doc.bottomMargin+30, doc.width, doc.height-120,id='normal')
            frame_land = Frame(doc.leftMargin, doc.bottomMargin+30,doc.height, doc.width-30,id='landscape')

            template = PageTemplate(id='portrait_page', frames=frame_a4, onPage=reportTemplate.header)
            template_landscape = PageTemplate(id='landscape_page', frames=frame_land, onPage=reportTemplate.make_landscape)
            doc.addPageTemplates([template, template_landscape])

            doc.build(content, canvasmaker=reportTemplate)             
          
            if plot != "statistics" and plot != "img_analysis":
                os.remove(fname)              
     
            if os.path.isfile(pdffile):
                parinfo = {}
                for i, n in enumerate(labels):
                    if n != "None" and len(flags) > 0:
                        curr_flag = flags[i]
                        if curr_flag == "Not Defined":
                            statusflag = "nd"
                        else:
                            statusflag = curr_flag.lower()
                        parinfo.update({n : {"system" : source, "status" : statusflag}})     
                #store plot in db
                if plot != "statistics" and plot != "img_analysis":
                    if plot == "pre-generated":
                        op2db = op
                    else:
                        op2db = plot
                    try:                  
                        dbio = db_io.dbIO(conf.data['local_db'])
                        dbio.connect()
                        plot_id = dbio.insert_temp_plot(pdata, usecase, op2db, user, " "+", ".join(labels)+" ", "None", "None", pclass.name, tstart, tstop, 1)
                    except:
                        plot_id = 0
                else:
                    plot_id = 0
                connection = util.connect_db(conf.data['local_db'])
                
                if plot == "statistics":
                    exptype = "statistics"
                elif plot == "img_analysis":
                    exptype = "image analysis"
                elif plot == "pre-generated":
                    exptype = "pre-generated plot"
                else:
                    exptype = "plot"
                util.update_stored(connection, fname = filename, user = user, date = now, ext="pdf", ftype = exptype, status=status, filepath = fpath, tbl = tbl, comment=json.dumps(comment_exp), pars=json.dumps(parinfo), source=source, tstart=tstart, tstop=tstop, plot_id=plot_id)
                connection.close()
            #download file
            filepath = os.sep+conf.main+downloadfile
            filepath = filepath.replace(os.sep, "/")
            
            #send email
            if emailto!="":
                try:
                    mail = Email("../smtp.json")
                    s = "New experiment flagged and stored"
                    f = "AIDA"
                    maildata = [user, save, source, status, comment_exp]                
                    text = mail.ok_flagged(maildata, etype=exptype)
                    msg = mail.set_message(s,f,emailto,text,"")
                    mail.send_mail(msg)
                except:
                    error = 2
            
            out = {"file" : filepath, "error" : error}

        except Exception as e:
            print(traceback.format_exc())
            out = {"file" : "", "error" : 1}          

    else:
        out = {"file" : "", "error" : 1}              
              
    return out
  
def insert_report_flag(data):
    error = 0
    #get data from frontend
    error = 0
    user = data["creator"].value
    filename = data["filename"].value
    status = data["status"].value 
    try:        
        notes = data["notes"].value
    except:
        notes = "-"
    try:
        emailto = data['email'].value
    except:
        emailto = ""
        
    #get connection parameters
    conf = util.repConfig()
    connmsg={}  

    if conf.error == 0:
        try:
            connection = util.connect_db(conf.data['local_db'])
            locerr = 0
        except:
            locerr = 1
            e.localstatus = 1
            exit(1)

        now = util.utc_now()

        try:
            comment_exp = {"comment" : notes}
            util.update_stored(connection, fname = filename, user = user, date = now, ext="pdf", ftype = "report", status=status, comment=json.dumps(comment_exp))
            connection.close()
            #send email
            if emailto!="":
                try:
                    mail = Email("../smtp.json")
                    s = "Report flagged"
                    f = "AIDA"
                    maildata = [user, status, notes]                
                    text = mail.ok_report_flagged(maildata, filename, etype="report")
                    msg = mail.set_message(s,f,emailto,text,"")
                    mail.send_mail(msg)
                except Exception as e:
                    print(e)
                    error = 2
            
            out = {"error" : error}
        except:
            out = {"error" : 1}          
    else:
        out = {"error" : 1}   
  
    return out

def main(data):
    global e
    e = util.statusMsg()

    plot = data['plot'].value
    if plot == "image":
        out = create_image_pdf(data)
    elif plot == "report":
        out = insert_report_flag(data)      
    else:
        out = create_plot_pdf(data)
    
    print(json.JSONEncoder().encode(out))

if __name__ == "__main__":
    print("Content-Type: application/json")
    print()

    #the cgi library gets vars from html
    data = cgi.FieldStorage()

    main(data)