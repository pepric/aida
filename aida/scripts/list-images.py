#!/usr/bin/python

"""
Image Directory Listing Generator for JS9 Viewer.

This module scans user directories for FITS and PNG image files and generates 
an HTML nested list tree structure for display with JS9 viewer integration.

@package AIDA
@module list-images
"""

import cgi, cgitb 
cgitb.enable()  # for troubleshooting
import glob
import os

def main(data):
    """Scan target user directory for image files and export HTML tree view file.

    Parameters
    ----------
    data : cgi.FieldStorage
        HTTP request payload containing main directory path.
    """
    dir = data['maindir'].value
    listfile = [os.path.basename(x) for x in glob.glob('../users/'+dir+"/*.fits")]
    listfile = listfile + [os.path.basename(x) for x in glob.glob('../users/'+dir+"/*.png")]
    listhtml = "<ul><li>"+dir+"<ul>"
    jstreetag='"icon":"fa fa-file"'
    
    for fname in listfile:
        f = "users/"+dir+"/"+fname
        onclick = 'javascript:JS9.Load("'+f+'", {scale:"log", colormap:"grey"});'
        listhtml += "<li data-jstree='{"+jstreetag+"}'><a onclick='"+onclick+"'>"+fname+"</a></li>"
    listhtml += "</ul></li></ul>"
    with open('../users/'+dir+"/listfiles.html", "w") as filename:
        filename.write(listhtml)
    
    print(listhtml)

if __name__ == "__main__":
    #print("Content-Type: text/plain;charset=utf-8")
    print("Content-Type: application/json")
    print()

    #the cgi library gets vars from html
    data = cgi.FieldStorage()

    main(data)
