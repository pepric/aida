#!/usr/bin/python

"""
Plot Rendering and Chart Export Utilities.

This module provides classes for generating histogram, scatter, and trend 
plots using Matplotlib for report generation and XML export.

@package AIDA
@module plots
"""

import numpy as np
import ast
import h5py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from io import BytesIO
from svglib.svglib import svg2rlg
from math import ceil
from os import environ, path
environ['MPLCONFIGDIR'] = './tmp/'
import matplotlib
import reportutils as ru
matplotlib.use('Agg')
environ['HOME'] = '/'
from matplotlib.ticker import MaxNLocator
import functions as util

class Histogram():
    """Histogram chart generation class for report rendering.

    Attributes
    ----------
    name : str
        Display name of the plot type.
    linewidth : float
        Line width for histogram edges.
    edgecolor : str
        Color string for bar edges.
    ptype : str
        Plot type identifier string.
    splitplot : int
        Plot layout split mode flag.
    vs : str
        Comparison axis identifier.
    xlabel : str or None
        X-axis label string.
    """
    def __init__(self):
        #name to display
        self.name = "Histogram"
        #width of line connection points on plot
        self.linewidth = 0.5
        self.edgecolor = "#333333"
        #plot type in XML
        self.ptype = "histogram"
        #flag to indicate if single and/or multi plots must be created
        #0 no multiplot, 1 only multiplot or single plot if n params = 1, 2 both single and multi plot
        self.splitplot = 1
        self.vs = ""
        self.xlabel = None
        
    def arrange_data_plot(self, resdict, par):
        """Rearrange data dictionary into plottable structure.

        Parameters
        ----------
        resdict : dict
            Input result data dictionary.
        par : str
            Target parameter identifier.

        Returns
        -------
        plotdata : list of dict
            Formatted plot data structures.
        labels : list of str
            Extracted labels list.
        nodatapar : list of str
            List of parameters with no data available.
        """
        labels = []
        plotdata = []
        nodatapar = []

        for ka, va in resdict.items():
            edges = va['edges']
            counts = va['counts']
            labels.append(ka)
            #check if parameter has data            
            if isinstance(edges,str) or isinstance(counts,str):                     
                nodatapar.append(ka)
                plotdata.append({"x" : [], "y" : []})                           
            else:             
                plotdata.append({"x" : edges, "y" : counts})

        if labels == nodatapar:
            plotdata = []
        return plotdata, labels, nodatapar      

    def create_plot_output(self, ET, y0, par, currop, addlist, acquid, fromfile, extrapars, h5add, h5resfile, h5group):
        """Generate histogram output dataset and append XML nodes.

        Parameters
        ----------
        ET : module
            ElementTree module reference.
        y0 : dict
            Primary Y parameter dataset dictionary.
        par : str
            Parameter identifier name.
        currop : Element
            XML operation element node.
        addlist : list of str
            Additional parameter names list.
        acquid : str
            Acquisition ID string.
        fromfile : bool
            Flag indicating whether plot is saved from file.
        extrapars : dict
            Extra configuration options.
        h5add : str
            HDF5 additional data file path.
        h5resfile : str
            HDF5 results output file path.
        h5group : Group
            HDF5 target output group node.

        Returns
        -------
        plotdict : dict
            Histogram results mapping dictionary.
        nodata : bool
            True if additional data is missing.
        warning : bool
            Warning status flag.
        """
        plotdict = {}
        opbranch = extrapars["opbranch"]
        iswidth, binval = ru.get_bins(opbranch)

        #name of binning parameter
        try:
            opbranch["Bin Size"]
            binname = "Bin Size"
        except:
            binname = "Number of Bins"
        curr_bin = ET.SubElement(currop, "setting")
        curr_bin.text = str(binval)
        curr_bin.set("param", binname)
       
        if y0['vals'].shape[0] > 0:
            if iswidth == 1:
                b = np.arange(min(y0['vals']), max(y0['vals']) + binval, binval)
            else:
                b = int(binval)

            counts, edges = np.histogram(y0['vals'], bins=b)
            ET.SubElement(currop, "data").text = h5resfile            
            counts = list(counts)
            edges = list(edges)
            h5group.create_dataset("counts", data=counts)
            h5group.create_dataset("edges", data=edges)            
        else:
            counts = "No Data available"
            edges = "No Data available"          
            ET.SubElement(currop, "counts").text = str(counts)
            ET.SubElement(currop, "edges").text = str(edges)
            
        if fromfile:
            plotdict.update({par : {"counts" : counts, "edges" : edges}})               
            
        nodata = False
        hf = h5py.File(h5add,"r")        
        for p in addlist:
            curr_add = ET.SubElement(currop, "additional")
            curr_add.set("param", p)
            vals = hf[p]["acquisition_"+acquid]['vals']
            if vals.shape[0] > 0 and vals.shape[0] > 0:
                if iswidth == 1:
                    b = np.arange(min(vals), max(vals) + binval, binval)
                else:
                    b = int(binval)                    
                counts, edges = np.histogram(vals, bins=b)
                counts = list(counts)
                edges = list(edges)
                ET.SubElement(curr_add, "data").text = h5resfile
                if "additional" not in h5group.keys():
                    g = h5group.create_group("additional")
                else:
                    g = h5group["additional"]
                addp = g.create_group(p)
                addp.create_dataset("counts", data=counts)     
                addp.create_dataset("edges", data=edges)                
            else:
                warning = True                                       
                counts = "No Data available"
                edges = "No Data available"
                nodata = True
                ET.SubElement(curr_add, "counts").text = counts           
                ET.SubElement(curr_add, "edges").text = edges
            if fromfile:
                plotdict.update({p : {"counts" : counts, "edges" : edges}})
        hf.close()

        return plotdict, nodata, False      
                                            
    def multi_plot(self, data, labels, nodata, filename = ""):
        """Render multi-panel histogram grid layout.

        Parameters
        ----------
        data : list
            Plot data dictionaries list.
        labels : list of str
            Parameter labels list.
        nodata : list of str
            Missing data parameters list.
        filename : str, optional
            Output filename prefix (default is "").

        Returns
        -------
        drawing : list
            List of ReportLab drawings or creation boolean flags.
        """
        drawing = []
        img_x_plot = 4
        img_x_row = int(img_x_plot/2)
        ny = len(labels)
        npages = ceil(float(ny)/img_x_plot)
        yksplitted = np.array_split(labels, npages)     
        for i in range(npages):
            fig = plt.figure(figsize=(9,5), dpi=100)
            curr_labels = yksplitted[i]
            for j,l in enumerate(curr_labels):
                ax = plt.subplot(2,img_x_row, j+1)
                ax.set_title(l, fontdict={'fontsize': 10})
                if l in nodata:
                    bins = []
                    counts = []
                else:
                    parpos = labels.index(l)
                    bins = data[parpos]["x"]
                    counts = data[parpos]["y"]
                if len(counts) > 0:
                    h = plt.hist(bins[:-1], bins, weights=counts, edgecolor= self.edgecolor, linewidth=self.linewidth)
                else:
                    ax.text(0.33, 0.5, 'No Data Available', fontsize='large')               
                
                ax.set_xticks(bins)
                if len(counts)>0:
                    self.set_axes(plt,ax)
                else:
                    ax.axes.xaxis.set_ticks([])
                    ax.axes.yaxis.set_ticks([])
                plt.tight_layout()
            if filename == "":                
                imgdata = BytesIO()
                fig.savefig(imgdata, format='svg')
                imgdata.seek(0)  # rewind the data
            
                drawing.append(svg2rlg(imgdata))
                del imgdata
                plt.close(fig)
            else:
                plt.savefig(filename+"__"+str(i+1)+".png", format = "png")
                plt.close()
                if path.isfile(filename+"__"+str(i+1)+".png"):
                    drawing.append(True)
                else:
                    drawing.append(False)
        return drawing 
        
    def set_axes(self, plt, ax):
        """Apply custom axis styles and formatting to Matplotlib plot.

        Parameters
        ----------
        plt : module
            Matplotlib.pyplot module.
        ax : Axes
            Matplotlib axis instance.
        """
        ax.set_facecolor('#e5ecf6')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#333333')
        ax.spines['left'].set_color('#333333')
        ax.tick_params(colors='#333333')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))        
        plt.xticks(fontsize = 10, rotation=45, ha="right")          
        plt.yticks(fontsize = 10)   
    
    def single_plot(self, data, labels, nodata, filename = ""):
        """Render single histogram chart.

        Parameters
        ----------
        data : list
            Plot data list.
        labels : list of str
            Parameter labels list.
        nodata : list of str
            Missing data parameters list.
        filename : str, optional
            Output filename prefix (default is "").

        Returns
        -------
        drawing : Drawing or list
            ReportLab drawing or creation status list.
        """
        drawing = []        
        fig = plt.figure(figsize=(8.5,5), dpi=100)
        ax = fig.add_subplot(1,1,1)
        axlabels=[]
        l = labels[0]
        if l in nodata:
            bins = []
            counts = []
        else:
            bins = data[0]['x']
            counts = data[0]['y'] 
        if len(counts) > 0:
            h = plt.hist(bins[:-1], bins, weights=counts, edgecolor= self.edgecolor, linewidth=self.linewidth)
        else:
            ax.text(0.33, 0.5, 'No Data Available', fontsize='large')

        #set axes
        ax.set_xticks(bins)        
        self.set_axes(plt,ax)
        plt.tight_layout()
        if filename == "":      
            imgdata = BytesIO()
            fig.savefig(imgdata, format='svg')
            imgdata.seek(0)  # rewind the data
            drawing=svg2rlg(imgdata)
            del imgdata
            plt.close(fig)
        else:
            plt.savefig(filename+"__0.png", format = "png")
            plt.close()
            if path.isfile(filename+"__0.png"):
                drawing.append(True)
            else:
                drawing.append(False)            
        return drawing

class Scatter():
    """Scatter plot chart generation class for report rendering.

    Attributes
    ----------
    name : str
        Display name of the plot type.
    linewidth : float
        Line width for scatter markers.
    ptype : str
        Plot type identifier string.
    splitplot : int
        Plot layout split mode flag.
    vs : int
        VS parameter index.
    xlabel : str or None
        X-axis label string.
    """
    def __init__(self):
        #name to display
        self.name = "Scatter Plot"
        #width of line connection points on plot
        self.linewidth = 0
        #plot type in XML
        self.ptype = "scatter"
        #flag to indicate if single and/or multi plots must be created
        #0 no multiplot, 1 only multiplot or single plot if n params = 1, 2 both single and multi plot
        self.splitplot = 0
        self.vs = 0
        self.xlabel = None
        
    def arrange_data_plot(self, resdict, par):
        """Rearrange data dictionary into scatter plot structure.

        Parameters
        ----------
        resdict : dict
            Input result data dictionary.
        par : str
            Target parameter identifier.

        Returns
        -------
        plotdata : list of dict
            Formatted scatter plot data structures.
        labels : list of str
            Extracted labels list.
        nodatapar : list of str
            List of parameters with no data available.
        """
        labels = []
        plotdata = []
        nodatapar = []
        for ka, va in resdict.items():
            x = va['X']['vals']
            y = va['vals']
            labels.append(ka)
            if isinstance(x,str) or isinstance(y,str):
                nodatapar.append(ka)
                plotdata.append({"x" : [], "y" : []})                
            else:             
                plotdata.append({"x" : x, "y" : y})            
        
        if labels == nodatapar:
            plotdata = []       
        return plotdata, labels, nodatapar

    def create_plot_output(self, ET, y0, par, currop, addlist, acquid, fromfile, extrapars, h5add, h5resfile, h5group):
        """Generate scatter plot output dataset and append XML nodes.

        Parameters
        ----------
        ET : module
            ElementTree module reference.
        y0 : dict
            Primary Y parameter dataset dictionary.
        par : str
            Parameter identifier name.
        currop : Element
            XML operation element node.
        addlist : list of str
            Additional parameter names list.
        acquid : str
            Acquisition ID string.
        fromfile : bool
            Flag indicating whether plot is saved from file.
        extrapars : dict
            Extra configuration options.
        h5add : str
            HDF5 additional data file path.
        h5resfile : str
            HDF5 results output file path.
        h5group : Group
            HDF5 target output group node.

        Returns
        -------
        plotdict : dict
            Scatter results mapping dictionary.
        nodata_add : bool
            True if additional parameter data is missing.
        nodata_x : bool
            True if X parameter data is missing.
        """
        plotdict = {}
        x = extrapars["x"]
        hf = h5py.File(h5add,"r")
        try:
            xdata = hf[x]['acquisition_'+acquid]
        except:
            xdata={"dates":np.empty(0),"values":np.empty(0)}
        nodata_x = False
        nodata_add = False        
        self.xlabel = extrapars["xlabel"]
        # convert x data strings into lists
        xfinal, y0final = ru.data_intersect(xdata, y0)
    
        if len(xfinal)>0 and len(y0final)>0:
            ET.SubElement(currop, "data").text = h5resfile 
            xfinal = [float(v) for v in xfinal]
            xml_ytext = y0final
            xml_xtext = h5resfile
            h5group.create_dataset("values", data=y0final)
            h5group.create_dataset("X", data=xfinal)
            x4plot = xfinal
        else:
            xml_ytext = "No Data available"
            xml_xtext = "No Data available"
            x4plot = xml_xtext
            ET.SubElement(currop, "values").text = str(xml_ytext)
     
        curr_xpar = ET.SubElement(currop, "X")
        curr_xpar.set("param", x)
        curr_xpar.text = str(xml_xtext)         

        if fromfile:
            plotdict.update({par : {"X" : {"name" : x, "vals" : x4plot}, "vals" : xml_ytext}})
        for p in addlist:
            addv = hf[p]["acquisition_"+acquid]
            xfinal, yafinal = ru.data_intersect(xdata, addv)
            curr_add = ET.SubElement(currop, "additional")
            curr_add.set("param", p)
            if len(xfinal)>0 and len(yafinal)>0:
                xfinal = [float(v) for v in xfinal]
                ET.SubElement(curr_add, "data").text = h5resfile              
                xml_ytext = yafinal
                xml_xtext = xfinal
                if "additional" not in h5group.keys():
                    g = h5group.create_group("additional")
                else:
                    g = h5group["additional"]
                addp = g.create_group(p)
                addp.create_dataset("X", data=xfinal)     
                addp.create_dataset("values", data=yafinal)
            else:
                warning = True 
                xml_ytext = "No Data available"
                xml_xtext = "No Data available"            
                nodata_add = True            
                ET.SubElement(curr_add, "values").text = str(xml_ytext)
                ET.SubElement(curr_add, "X").text = str(xml_xtext)            
            if fromfile:
                plotdict.update({p : {"X" : {"name" : x, "vals" : xml_xtext}, "vals" : xml_ytext}})
                
        if xdata['dates'].shape[0] == 0:
            nodata_x = True
         
        hf.close()           
        return plotdict, nodata_add, nodata_x        
        
    def multi_plot(self, data, labels, nodata, filename=""):
        """Unused multi-plot stub for scatter layout."""
        pass #NOT USED FOR SCATTER PLOT HERE
        
    def set_axes(self, plt, ax):
        """Apply custom axis styles and formatting to scatter plot.

        Parameters
        ----------
        plt : module
            Matplotlib.pyplot module.
        ax : Axes
            Matplotlib axis instance.
        """
        ax.set_facecolor('#e5ecf6')
        if self.xlabel is not None:
            ax.set_xlabel(self.xlabel)
            ax.xaxis.label.set_color('#333333')        
        plt.grid(color='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#333333')
        ax.spines['left'].set_color('#333333')
        ax.tick_params(colors='#333333')
        try:
            ax.yaxis.get_major_formatter().set_useOffset(False)
        except:
            pass
        try:
            ax.xaxis.get_major_formatter().set_useOffset(False)        
        except:
            pass
        plt.xticks(fontsize = 8, rotation=45, ha="right")
        plt.yticks(fontsize = 8)    

    def single_plot(self, data, labels, nodata, filename = ""):
        """Render single scatter plot chart.

        Parameters
        ----------
        data : list
            Plot data list.
        labels : list of str
            Parameter labels list.
        nodata : list of str
            Missing data parameters list.
        filename : str, optional
            Output filename prefix (default is "").

        Returns
        -------
        drawing : Drawing or list
            ReportLab drawing or creation status list.
        """
        drawing = []
        fig = plt.figure(figsize=(9,5.5), dpi=100)
        ax = fig.add_subplot(1,1,1)
        axlabels=[]
       
        for i,d in enumerate(labels):
            if d not in nodata:
                #get data
                ylabel = d
                ydata = data[i]["y"]
                xdata = data[i]["x"]
            else:
                ylabel = d+" - No Data"
                ydata = []
                xdata = []              
            #create plot
            scatter = plt.plot(xdata, ydata, label = ylabel, linewidth=self.linewidth)
            plt.setp(scatter, marker = "o", ms = 2)
        #set axes
        self.set_axes(plt,ax)
        plt.tight_layout()
        if len(labels) > 3:
            lgd = plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",mode="expand", borderaxespad=0.5, ncol=3)
        else:
            lgd = plt.legend(loc='best', borderaxespad=0.5, prop={'size': 8})        

        if filename == "":
            imgdata = BytesIO()
            fig.savefig(imgdata, format='svg', bbox_extra_artists=(lgd,), bbox_inches='tight', pad_inches=0)
            imgdata.seek(0)  # rewind the data
            drawing=svg2rlg(imgdata)
            del imgdata
            plt.close(fig)
        else:
            fig.savefig(filename+"__0.png", format = "png", bbox_extra_artists=(lgd,), bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            if path.isfile(filename+"__0.png"):
                drawing.append(True)
            else:
                drawing.append(False)            
        return drawing

class Trend():
    """Trend analysis time-series chart generation class.

    Attributes
    ----------
    name : str
        Display name of the plot type.
    linewidth : float
        Line width for time-series trend lines.
    ptype : str
        Plot type identifier string.
    splitplot : int
        Plot layout split mode flag.
    vs : str
        Comparison axis identifier ("time").
    xlabel : str or None
        X-axis label string.
    """
    def __init__(self):
        #name to display
        self.name = "Trend Analysis"
        #width of line connection points on plot
        self.linewidth = 0.5
        #plot type in XML
        self.ptype = "trend"
        #flag to indicate if single and/or multi plots must be created
        #0 no multiplot, 1 only multiplot or single plot if n params = 1, 2 both single and multi plot
        self.splitplot = 2
        self.vs = "time"
        self.xlabel = None
        
    def arrange_data_plot(self, resdict, par):
        """Rearrange data dictionary into time-series trend structure.

        Parameters
        ----------
        resdict : dict
            Input result data dictionary.
        par : str
            Target parameter identifier.

        Returns
        -------
        plotdata : list of dict
            Formatted trend plot data structures.
        labels : list of str
            Extracted labels list.
        nodatapar : list of str
            List of parameters with no data available.
        """
        labels = []
        plotdata = []
        nodatapar = []
    
        for ka, va in resdict.items():
            x = va['dates']
            y = va['vals']
            labels.append(ka)             
            if isinstance(x,str) or isinstance(y,str):
                nodatapar.append(ka)
                plotdata.append({"x" : [], "y" : []})                
            else:             
                plotdata.append({"x" : x, "y" : y})

        if labels == nodatapar:
            plotdata = []
        return plotdata, labels, nodatapar
      
    def create_plot_output(self, ET, y0, par, currop, addlist, acquid, fromfile, extrapars, h5add, h5resfile, h5group):
        """Generate time-series trend output dataset and append XML nodes.

        Parameters
        ----------
        ET : module
            ElementTree module reference.
        y0 : dict
            Primary Y parameter dataset dictionary.
        par : str
            Parameter identifier name.
        currop : Element
            XML operation element node.
        addlist : list of str
            Additional parameter names list.
        acquid : str
            Acquisition ID string.
        fromfile : bool
            Flag indicating whether plot is saved from file.
        extrapars : dict
            Extra configuration options.
        h5add : str
            HDF5 additional data file path.
        h5resfile : str
            HDF5 results output file path.
        h5group : Group
            HDF5 target output group node.

        Returns
        -------
        plotdict : dict
            Trend results mapping dictionary.
        nodata : bool
            True if additional data is missing.
        warning : bool
            Warning status flag.
        """
        plotdict = {}              
        if y0['dates'].shape[0] > 0:
            ET.SubElement(currop, "data").text = h5resfile
            xplot = y0['dates']
            yplot = y0['vals']
            xplot, yplot = (list(t) for t in zip(*sorted(zip(xplot, yplot))))            
            h5group.create_dataset("dates", data=xplot)
            h5group.create_dataset("values", data=yplot)
        else:
            ET.SubElement(currop, "dates").text = "No Data available"
            ET.SubElement(currop, "values").text = "No Data available"
            xplot = "No Data available"
            yplot = "No Data available"
        if fromfile:
            plotdict.update({par : {"dates" : xplot, "vals" : yplot}})

        nodata = False
        hf = h5py.File(h5add,"r")       
        for p in addlist:
            curr_add = ET.SubElement(currop, "additional")
            curr_add.set("param", p)
            try:
                dates = hf[p]["acquisition_"+acquid]['dates']
            except:
                dates = np.empty(0)
            if dates.shape[0] > 0:
                vals = hf[p]["acquisition_"+acquid]['vals']
                ET.SubElement(curr_add, "data").text = h5resfile
                dates = dates[:]
                vals = [float(v) for v in vals]
                dates, vals = (list(t) for t in zip(*sorted(zip(dates, vals))))                            
                if "additional" not in h5group.keys():
                    g = h5group.create_group("additional")
                else:
                    g = h5group["additional"]
                addp = g.create_group(p)
                addp.create_dataset("dates", data=dates)     
                addp.create_dataset("values", data=vals)                 
            else:
                nodatatxt = "No Data available"
                ET.SubElement(curr_add, "dates").text = nodatatxt
                ET.SubElement(curr_add, "values").text = nodatatxt
                dates = nodatatxt
                vals = nodatatxt
                nodata = True
                
            if fromfile:
                plotdict.update({p : {"dates" : dates, "vals" : vals}})
        hf.close()

        return plotdict, nodata, False
      
    def multi_plot(self, data, labels, nodata, filename = ""):
        """Render multi-panel trend plot grid layout.

        Parameters
        ----------
        data : list
            Plot data dictionaries list.
        labels : list of str
            Parameter labels list.
        nodata : list of str
            Missing data parameters list.
        filename : str, optional
            Output filename prefix (default is "").

        Returns
        -------
        drawing : list
            List of ReportLab drawings or creation boolean flags.
        """
        drawing = []
        img_x_plot = 4
        img_x_row = int(img_x_plot/2)
        ny = len(labels)
        npages = ceil(float(ny)/img_x_plot)
        yksplitted = np.array_split(labels, npages)     
        for i in range(npages):
            fig = plt.figure(figsize=(9,5.5), dpi=100)
            curr_labels = yksplitted[i]
            for j,l in enumerate(curr_labels):
                ax = plt.subplot(2,img_x_row, j+1)
                ax.set_title(l, fontdict={'fontsize': 10})
                if l in nodata:
                    xdata = []
                    ydata = []
                else:
                    parpos = labels.index(l)
                    xdata = [datetime.utcfromtimestamp(ts) for ts in data[parpos]["x"]]
                    ydata = data[parpos]["y"][:]
                if len(xdata) > 0:
                    trend = plt.plot(xdata, ydata, label = l, linewidth=self.linewidth)
                    plt.setp(trend, marker = "o", ms = 1)
                else:
                    ax.text(0.33, 0.5, 'No Data Available', fontsize='large')               
                
                if len(xdata)>0:
                    self.set_axes(plt,ax)
                else:
                    ax.axes.xaxis.set_ticks([])
                    ax.axes.yaxis.set_ticks([])
                plt.tight_layout()
            if filename == "":              
                imgdata = BytesIO()
                fig.savefig(imgdata, format='svg')
                imgdata.seek(0)  # rewind the data

                drawing.append(svg2rlg(imgdata))
                del imgdata
                plt.close(fig)
            else:
                plt.savefig(filename+"__"+str(i+1)+".png", format = "png")
                plt.close()
                if path.isfile(filename+"__"+str(i+1)+".png"):
                    drawing.append(True)
                else:
                    drawing.append(False)                
        return drawing

    def set_axes(self, plt, ax):
        """Apply concise date formatting and custom axis styles to trend plot.

        Parameters
        ----------
        plt : module
            Matplotlib.pyplot module.
        ax : Axes
            Matplotlib axis instance.
        """
        ax.set_facecolor('#e5ecf6')
        plt.grid(color='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#333333')
        ax.spines['left'].set_color('#333333')
        ax.tick_params(colors='#333333')
        try:
            locator = mdates.AutoDateLocator(minticks=3, maxticks=10)
            formatter = mdates.ConciseDateFormatter(locator, formats = ['%Y', '%b', '%d', '%H:%M', '%H:%M:%S', '%S'], zero_formats=['', '%Y-%b-%d', '%b', '%Y-%b-%d', '%Y-%b-%d\n%H:%M', '%H:%M'], show_offset = False)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            ax.yaxis.get_major_formatter().set_useOffset(False)
        except:
            pass
        plt.xticks(fontsize = 8, rotation=45, ha="right")
        plt.yticks(fontsize = 8)
        
    def single_plot(self, data, labels, nodata, filename = ""):
        """Render single time-series trend chart.

        Parameters
        ----------
        data : list
            Plot data list.
        labels : list of str
            Parameter labels list.
        nodata : list of str
            Missing data parameters list.
        filename : str, optional
            Output filename prefix (default is "").

        Returns
        -------
        drawing : Drawing or list
            ReportLab drawing or creation status list.
        """
        drawing = []      
        fig = plt.figure(figsize=(9,5.5), dpi=100)
        ax = fig.add_subplot(1,1,1)
        axlabels=[]
        for i,d in enumerate(labels):
            if d not in nodata:
                ylabel = d
                ydata = data[i]["y"][:]
                xdata = [datetime.utcfromtimestamp(ts) for ts in data[i]["x"]]
            else:
                ylabel = d+" - No Data"
                ydata = []
                xdata = []
            #create plot
            trend = plt.plot(xdata, ydata, label = ylabel, linewidth=self.linewidth)
            plt.setp(trend, marker = "o", ms = 2)
       #set axes
        self.set_axes(plt,ax)
        plt.tight_layout()
        if len(labels) > 3:
            lgd = plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",mode="expand", borderaxespad=0.5, ncol=3)
        else:
            lgd = plt.legend(loc='best', borderaxespad=0.5, prop={'size': 8})
        
        if filename == "":      
            imgdata = BytesIO()
            fig.savefig(imgdata, format='svg', bbox_extra_artists=(lgd,), bbox_inches='tight', pad_inches=0)
            imgdata.seek(0)  # rewind the data
            drawing=svg2rlg(imgdata)
            del imgdata
            plt.close(fig)
        else:
            plt.savefig(filename+"__0.png", format = "png", bbox_extra_artists=(lgd,), bbox_inches='tight', pad_inches=0)
            plt.close()
            if path.isfile(filename+"__0.png"):
                drawing.append(True)
            else:
                drawing.append(False)            
        return drawing