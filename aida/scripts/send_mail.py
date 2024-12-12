#!/usr/bin/python

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import functions as util

class Email():

    def __init__(self, smtpfile):
        smtpconf = self.get_smtp_data(smtpfile)
        if smtpconf['host'] != "":
            self.host = smtpconf['host']
            self.port = smtpconf['port']
            self.user = smtpconf['user']
            self.pwd = smtpconf['password']
        else:
            #Error
            pass

    def error_img_text(self, maildata, error = "N/A"):
        text = """\
    <html>
      <body>
        <p>The generation of requested analysis by AIDA is failed:</p>
        <p>
        Experiment : Statistics on """+str(maildata[0]).upper()+""" images<br/>
        Source : """+maildata[1]+"""<br/>
        Involved Files : """+maildata[5][1:-1]+"""<br/>"""
        
        text +="""  
      
        
        </p>
        <p style="font-weight:bold; font-decoration:underline">Error : """+error+"""
        <br/>
        <p><span>Please, contact AIDA admin to report the error</span></p>
      </body>
    </html>
    """
        return text



    def error_plot_text(self, maildata, error = "N/A"):
        text = """\
    <html>
      <body>
        <p>The generation of requested plot by AIDA is failed:</p>
        <p>
        Experiment : """+str(maildata[0])+"""<br/>
        Data Origin : """+maildata[1].upper()+""" - """+maildata[2]+"""<br/>"""
        
        if maildata[3][0]!="None":
            text += """X Parameter: """+maildata[3][0]+"""<br/>"""
        pars = maildata[3][1:]
        p_text = ",".join(pars)     
        text += """Y Parameter(s) : """+p_text+"""<br/>"""        
        text += """        
        Date Range : """+maildata[4]+""" - """+maildata[5]+"""<br/>"""
        
        stats = maildata[6]
        if len(stats) > 0:
            slist = str(maildata[6].keys())
            s = slist.replace("'","").replace("dict_keys([","").replace("])","").replace("_"," ")
        else:
            s = "None"
        
        text +="""  
        Statistics : """+s+"""<br/>        
        
        </p>
        <p style="font-weight:bold; font-decoration:underline">Error : """+error+"""
        <br/>
        <p><span>Please, contact AIDA admin to report the error</span></p>
      </body>
    </html>
    """
        return text
      
    def error_report_text(self, maildata, period, error = "N/A"):
        text = """\
    <html>
      <body>
        <p>The generation of report by AIDA is failed:</p>
        <p style="font-weight:bold; font-decoration:underline">SUMMARY</p>
        <p>
        Run ID : """+str(maildata[4])+"""<br/>
        Type : """+period+"""<br/>
        Configuration File : """+maildata[0]+"""<br/>
        Date Range : """+maildata[1]+""" - """+maildata[2]+"""

        </p>
        <br/>
        <p><span style="font-weight:bold;">Encountered error: </span>"""+error+"""      
        </p>
      </body>
    </html>
    """
        return text        
          
    def get_smtp_data(self, smtpfile):
        try:
            # get report config data from json
            fileobj = open(smtpfile, "r")
            jsonstr = fileobj.read()
            fileobj.close()
            #convert input string to json object
            mailconfig = json.loads(jsonstr)
        except:
            mailconfig = {"host" : ""}
            
        return mailconfig

    def ok_report_flagged(self, maildata, filename="", etype="plot"):
        user = maildata[0]
        status = maildata[1].upper()
        comment_exp = maildata[2]
        text = """\
        <html>
            <body>
                <p>A new """+etype+""" has been flagged in AIDA repository by user """+user+""".</p>
                <p>For additional info, please contact """+user+""" directly.</p>
                <br/>"""
        if filename != "":
            text +="""<b>Report Name :</b> """+filename+"""<br/>"""
        text +="""<p><b>Status:</b> """+status+"""<br/>"""

        if isinstance(comment_exp, str):
            text +="""<b>Comments :</b> """+comment_exp+"""<br/>"""
        elif isinstance(comment_exp, dict):
            for k in comment_exp:
                text +="""<b>Comment on """+k+""" :</b> """+comment_exp[k]+"""<br/>"""
                
        text+="""</p></body></html>"""
        return text      
      
      
    def ok_flagged(self, maildata, filename="", etype="plot"):
        user = maildata[0]
        save = maildata[1].upper()
        source = maildata[2].upper()
        status = maildata[3].upper()
        comment_exp = maildata[4]
        text = """\
        <html>
            <body>
                <p>A new """+etype+""" has been flagged and stored in AIDA repository by user """+user+""". It has been stored in the """+save+""" archive.</p>
                <p>For additional info, please contact """+user+""" directly.</p>
                <br/>"""
        if filename != "":
            text +="""<b>Filename :</b> """+filename+"""<br/>"""
        text +="""<p><b>System:</b> """+source+"""<br/>
                <b>Status:</b> """+status+"""<br/>"""

        if isinstance(comment_exp, str):
            text +="""<b>Comments :</b> """+comment_exp+"""<br/>"""
        elif isinstance(comment_exp, dict):
            for k in comment_exp:
                text +="""<b>Comment on """+k+""" :</b> """+comment_exp[k]+"""<br/>"""
                
        text+="""</p></body></html>"""
        return text

    def ok_img_text(self, maildata, plotid, source):
        webappdir = util.repConfig().data['webapp_dir']    
        ploturl = "http://"+maildata[4]+"/"+webappdir+"/view_results.php?id="+str(plotid)+"&s="+source        
        
        text = """\
    <html>
      <body>
        <p>A new image analysis has been performed by AIDA:</p>
        <p style="font-weight:bold; font-decoration:underline">SUMMARY</p>
        <p>
        Experiment : Statistics on """+str(maildata[0]).upper()+""" images<br/>
        Source : """+source+"""<br/>
        Involved Files : """+maildata[5][1:-1]+"""<br/>"""
        
        text +="""
        </p>
        
        <p>Click <a href='"""+ploturl+"""'>here</a>  to view results.</p>
      </body>
    </html>
    """
        return text

      
    def ok_plot_text(self, maildata, plotid, source):
        webappdir = util.repConfig().data['webapp_dir']    
        ploturl = "http://"+maildata[7]+"/"+webappdir+"/view_plot.php?id="+str(plotid)+"&s="+source        
        
        text = """\
    <html>
      <body>
        <p>A new data analysis has been performed by AIDA:</p>
        <p style="font-weight:bold; font-decoration:underline">SUMMARY</p>
        <p>
        Experiment : """+str(maildata[0])+"""<br/>
        Data Origin : """+maildata[1].upper()+""" - """+maildata[2]+"""<br/>"""
        
        if maildata[3][0]!="None":
            text += """X Parameter: """+maildata[3][0]+"""<br/>"""
        pars = maildata[3][1:]
        p_text = ",".join(pars)     
        text += """Y Parameter(s) : """+p_text+"""<br/>"""        
        
        
        text += """        
        Date Range : """+maildata[4]+""" - """+maildata[5]+"""<br/>"""
        
        stats = maildata[6]
        if len(stats) > 0:
            slist = str(maildata[6].keys())
            s = slist.replace("'","").replace("dict_keys([","").replace("])","").replace("_"," ")
        else:
            s = "None"
        
        text +="""  
        Statistics : """+s+"""<br/>        
        
        </p>
        
        <p>Click <a href='"""+ploturl+"""'>here</a>  to view results.</p>
      </body>
    </html>
    """
        return text
      
    def ok_report_text(self, maildata, period, fullfile, pdf_ok):
        if pdf_ok:
            p_pdf = """<p>Click <a href='"""+fullfile+""".pdf' download='"""+fullfile+""".pdf'>here</a>  to download it in PDF version or visit AIDA portal to list available reports</p>"""       
        else:
            p_pdf = """PDF version is not available. Contact AIDA admin for further info."""
        
        text = """\
    <html>
      <body>
        <p>A new report has been generated by AIDA:</p>
        <p style="font-weight:bold; font-decoration:underline">SUMMARY</p>
        <p>
        Run ID : """+str(maildata[6])+"""<br/>
        Type : """+period+"""<br/>
        Report File Name : """+maildata[0]+"""<br/>
        Creation Date : """+maildata[2]+"""<br/>
        Owner : """+maildata[1]+"""<br/>
        Date Range : """+maildata[4]+""" - """+maildata[5]+"""
        
        
        </p>
      
        <p>Click <a href='"""+fullfile+""".xml' download='"""+fullfile+""".xml'>here</a>  to download it in XML version or visit AIDA portal to list available reports</p>"""+p_pdf+"""
     
      </body>
    </html>
    """
        return text
      
    def send_mail(self, message):
        if self.port==465:
            server=smtplib.SMTP_SSL(self.host, self.port)
        else:
            server = smtplib.SMTP(self.host, self.port)
            server.ehlo()
            server.starttls()
        if self.pwd != "":        
            server.login(self.user, self.pwd)

        TO = [message['To']]
        CC = message["CC"].split(",")                             
        server.sendmail(self.user, TO+CC, message.as_string())
        server.quit()      
      
    def set_message(self, subject, fromuser, touser, text, cc=""):
        message = MIMEMultipart("alternative")
        message['Subject'] = subject
        message["From"] = fromuser
        message["To"] = touser
        if isinstance(cc,list):
            message["CC"] = ",".join(cc)
        else:
            message["CC"] = cc                            
        part = MIMEText(text, "html")   
        message.attach(part)
        
        return message
        
    def stop_report_text(self, user, errorlist, runid):
        text = """\
    <html>
      <body>
        <p>Report generation with RUNID = """+str(runid)+""" has been stopped by """+user+""".</p>"""
        if errorlist['error'] == 2:        
            text += """<p style="font-weight:bold; font-decoration:underline">WARNINGS</p>
    <p>"""+errorlist['msg']+"""</p>"""
      
        text += """<p>For further info, please contact """+user+"""</p>
     
      </body>
    </html>
    """
        return text        
        