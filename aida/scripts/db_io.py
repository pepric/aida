#!/usr/bin/python

"""
Database I/O Interface Utilities.

This module provides the dbIO class to manage MySQL database connections and 
execute queries for stored plots, running reports, flagged parameters, user 
accounts, and system configurations.

@package AIDA
@module db_io
"""

import functions as util
import pymysql
import pymysql.cursors
import traceback

class dbIO():
    """Manage database connection lifecycle and data operations for AIDA.

    Parameters
    ----------
    config : dict
        Dictionary containing database connection configuration settings.

    Attributes
    ----------
    config : dict
        Connection parameters dictionary.
    connection : pymysql.connections.Connection or None
        Active PyMySQL connection object.
    """
    
    def __init__(self, config):
        self.config = config
        self.connection = None        

    def _commit_query(self, sql, keep_open = False):
        """Execute and commit an SQL query.

        Parameters
        ----------
        sql : str
            SQL query statement to execute.
        keep_open : bool, optional
            If True, keeps the database connection open (default is False).
        """
        if self.connection is None:
            self.connect()
        #store report in DB
        with self.connection.cursor() as cursor:
            cursor.execute(sql)   
        self.connection.commit()
        if not keep_open:        
            self.close()         
        
    def check_connection(self, keep_open=False):
        """Test whether a database connection can be established.

        Parameters
        ----------
        keep_open : bool, optional
            If True, preserves the active connection instance (default is False).

        Returns
        -------
        locerr : int
            0 if connection succeeded, 1 on failure.
        connection : pymysql.connections.Connection or None
            Established connection instance or None.
        """        
        connection = None        
        try:
            connection = util.connect_db(self.config)
            locerr = 0
            if not keep_open:
                connection.close()
            else:
                self.connection = connection              
        except:
            locerr = 1

        return locerr, connection

    def count_records(self, tbl, statement="", keep_open = False):
        """Count total matching records in a target database table.

        Parameters
        ----------
        tbl : str
            Database table name.
        statement : str, optional
            SQL WHERE clause or filter statement (default is "").
        keep_open : bool, optional
            If True, keeps the connection open (default is False).

        Returns
        -------
        counts : int
            Total number of matching records.
        """
        sql = "SELECT COUNT(*) FROM "+tbl+" " +statement
        if self.connection is None:
            self.connect()
        #commit query
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchone()
        if not keep_open:        
            self.close()
        counts = int(res["COUNT(*)"])
        return counts      
      
    def close(self):
        """Close the active database connection if open."""      
        self.connection.close()
        self.connection = None
        
    def connect(self):
        """Open a new connection to the local database.

        Returns
        -------
        error : int
            0 if successful, 1 on connection failure.
        connection : pymysql.connections.Connection or None
            Active database connection object or None.
        """         
        error, connection = self.check_connection(keep_open = True)
        return error, connection
      
    def get_connection(self):
        """Retrieve current active connection object.

        Returns
        -------
        pymysql.connections.Connection or None
            Active database connection handle.
        """      
        return self.connection

    def get_flagged(self, mode = "exp", archive = "public",keep_open = False):
        """Fetch list of flagged files or experiments.

        Parameters
        ----------
        mode : str, optional
            Query perspective mode ('exp' or 'par', default is 'exp').
        archive : str, optional
            Archive scope ('public', 'report', or specific username, default is 'public').
        keep_open : bool, optional
            If True, keeps connection open (default is False).

        Returns
        -------
        res : list of dict
            List of flagged experiment record dictionaries.
        """

        if archive == "public":
            sql = "SELECT * FROM stored_files ORDER BY id DESC"
        elif archive == "report":
            sql = "SELECT report_files.*, stored_files.status_exp, stored_files.comment_exp, stored_files.date_exp, stored_files.username as flaguser FROM report_files LEFT JOIN stored_files ON report_files.filename=stored_files.filename WHERE stored_files.status_exp IS NOT NULL ORDER BY stored_files.status_exp DESC"      
        else:
            sql = "SELECT * FROM user_files WHERE username='"+archive+"' ORDER BY id DESC"
       
        if self.connection is None:
            self.connect()
        #commit query
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        if not keep_open:        
            self.close()

        return res

    def get_local_files(self, source,tmp_dir, ts = None,te=None,keep_open = False):
        """Fetch list of filenames already cached or downloaded locally.

        Parameters
        ----------
        source : str
            Target data system source name.
        tmp_dir : str
            Temporary working directory identifier.
        ts : str or None, optional
            Search start timestamp string (default is None).
        te : str or None, optional
            Search end timestamp string (default is None).
        keep_open : bool, optional
            If True, keeps connection open (default is False).

        Returns
        -------
        locfiles : list of str
            Filenames matching search criteria.
        """
        sql = "SELECT filename FROM local_files WHERE ("
        if ts is not None and te is not None:
            sql+="date_start <= '"+te+"' AND date_stop >= '"+ts+"' AND "
        sql+="data_source = '"+source+"' AND username  = '"+tmp_dir+"')"

        if self.connection is None:
            self.connect()
        #commit query
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        if not keep_open:        
            self.close()
        locfiles = [f.get('filename') for f in res]
        
        return locfiles

    def get_ml(self, keep_open = False):
        """Fetch list of stored Machine Learning experiment records.

        Parameters
        ----------
        keep_open : bool, optional
            If True, keeps connection open (default is False).

        Returns
        -------
        res : list of dict
            List of ML experiment records.
        """

        sql = "SELECT * FROM stored_ml ORDER BY id DESC"
       
        if self.connection is None:
            self.connect()
        #commit query
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        if not keep_open:        
            self.close()

        return res
        
    def get_opmode(self,keep_open = False):
        """Fetch active operational mode setting.

        Parameters
        ----------
        keep_open : bool, optional
            If True, keeps connection open (default is False).

        Returns
        -------
        res : dict
            Single-item dictionary containing 'mode' key.
        """        
        sql = "SELECT mode FROM operation_modes WHERE enable = 1"
        if self.connection is None:
            self.connect()        
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchone()
        if not keep_open:        
            self.close()
            
        return res    
            
    def get_users(self, status = 1, keep_open = False):
        """Fetch registered users filtered by account status.

        Parameters
        ----------
        status : int, optional
            Filter status code (0: pending, 1: active, 2: deactivated, default is 1).
        keep_open : bool, optional
            If True, keeps connection open (default is False).

        Returns
        -------
        res : list of dict
            List of matching user records.
        """
        sql = "SELECT * FROM members WHERE active = "+str(status);        
        if self.connection is None:
            self.connect()
        #commit query
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        if not keep_open:        
            self.close()

        return res

    def get_report_status(self, runid):
        """Fetch execution status percentage for a target report generation run.

        Parameters
        ----------
        runid : int or str
            Unique run ID of target report job.

        Returns
        -------
        p : float
            Numeric execution progress percentage.
        """            
     
        if self.connection is None:
            self.connect()      
        sql_get = "SELECT exp_status FROM running_reports WHERE id = "+str(runid)
        with self.connection.cursor() as cursor:
            cursor.execute(sql_get)
            perc0 = cursor.fetchone()
        try:
            p = float(perc0['exp_status'])
        except:
            p=0
        return p
      
    def get_running_reports(self, role = "admin", username = "", keep_open = False):
        """Fetch active running report execution records.

        Parameters
        ----------
        role : str, optional
            User role level ('admin' or standard user, default is 'admin').
        username : str, optional
            Filter username when role is not 'admin' (default is "").
        keep_open : bool, optional
            If True, keeps connection open (default is False).

        Returns
        -------
        res : list of dict
            List of running report records.
        """
        sql = "SELECT * FROM running_reports";        
        if role != "admin":
            sql += " WHERE username = '"+username+"'"
        if self.connection is None:
            self.connect()
        #commit query
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        if not keep_open:        
            self.close()

        return res      
      
    def get_systems(self, keep_open = False):
        """Fetch list of distinct system identifiers registered in database.

        Parameters
        ----------
        keep_open : bool, optional
            If True, keeps connection open (default is False).

        Returns
        -------
        out : list of str
            Unique registered system names.
        """      
        sql = "SELECT name FROM systems GROUP BY name"
        out = []
        if self.connection is None:
            self.connect()
        #commit query
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        if not keep_open:        
            self.close()
        #arrange results in a list            
        for item in res:
            out.append(item['name'])

        return out

    def insert_local_file(self, fname, source, user, subsystem = None, tstart = None, tstop = None, ftype = None, keep_open = False):
        """Register newly downloaded local data file entry in database.

        Parameters
        ----------
        fname : str
            Filename.
        source : str
            Data source system identifier.
        user : str
            User who initiated download.
        subsystem : str, optional
            Subsystem identifier name (default is None).
        tstart : str, optional
            Start timestamp (default is None).
        tstop : str, optional
            End timestamp (default is None).
        ftype : str, optional
            File classification type (default is None).
        keep_open : bool, optional
            If True, keeps connection open (default is False).
        """

        sql_newf = "INSERT INTO local_files (filename, data_source, username, filetype) VALUES ('"+fname+"', '"+source+"', '"+user+"', '"+ftype+"')"
        self._commit_query(sql_newf, keep_open)      

    def insert_ml_plot(self, username, modelfile, outfile, recapfile, labels, source, creation, ts, te, config, stats):
        """Insert new Machine Learning experiment record.

        Parameters
        ----------
        username : str
            Generating user's name.
        modelfile : str
            Path to serialized model file.
        outfile : str
            Path to model prediction output file.
        recapfile : str
            Path to summary report file.
        labels : list of str
            List of feature and target parameter labels.
        source : str
            Data system source name.
        creation : str
            Creation timestamp string.
        ts : str
            Data range start timestamp string.
        te : str
            Data range end timestamp string.
        config : dict
            Model and technique configuration settings.
        stats : dict or str
            Evaluation metrics payload.

        Returns
        -------
        plotid : int or None
            Database record ID if successful, None on failure.
        """
        if self.connection is None:
            self.connect()

        tech = config["tech"]
        model = config["model"]
        #convert labels to string
        l = str(labels)[1:-1].replace("'","")        
        #convert stats dict to str
        s = str(stats)
                
        sql = 'INSERT INTO stored_ml (modelfile, outputfile, recapfile, tech, model, labels, source, username, creation, tstart, tstop, stats) VALUES ("'+modelfile+'", "'+outfile+'", "'+recapfile+'", "'+tech+'", "'+model+'", "'+l+'", "'+source+'", "'+username+'", "'+creation+'", "'+ts+'", "'+te+'", "'+s+'")'

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)   
            self.connection.commit()
            plotid = cursor.lastrowid
        except:
            plotid = None
        self.close()
        return plotid
      
    def insert_report_file(self, fname, user, creation, period, configfile, tstart, tstop, keep_open = False):
        """Insert record for a generated report document.

        Parameters
        ----------
        fname : str
            Report PDF filename.
        user : str
            Generating user's name.
        creation : str
            Creation timestamp string.
        period : str
            Report periodicity mode.
        configfile : str
            Configuration filename used for generation.
        tstart : str
            Report data start datetime string.
        tstop : str
            Report data end datetime string.
        keep_open : bool, optional
            If True, keeps connection open (default is False).
        """
        sql_newrep = "INSERT INTO report_files (filename, username, upload_date, period, config_file, start_date, end_date) VALUES ('"+fname+"', '"+user+"', '"+creation+"', '"+period+"', '"+configfile+"', '"+tstart+"', '"+tstop+"')"
        self._commit_query(sql_newrep, keep_open)

    def insert_temp_plot(self, pdata, usecase, plot, username, labels, stats, stat_res, plot_name, ts, te, tokeep):
        """Insert new temporary plot experiment record.

        Parameters
        ----------
        pdata : dict or str
            Plotted data payload.
        usecase : str
            Data origin context.
        plot : str
            Plot type identifier string.
        username : str
            User requesting plot generation.
        labels : list of str
            Labels for plotted parameters.
        stats : str
            Statistical mode ('global' or 'advanced').
        stat_res : str
            JSON formatted statistical results string.
        plot_name : str
            Display name of plot.
        ts : str
            Data start timestamp string.
        te : str
            Data end timestamp string.
        tokeep : int
            Persistence flag (0 for temporary, 1 for permanent).

        Returns
        -------
        plotid : int or None
            Inserted record ID, or None if insert failed.
        """
        if self.connection is None:
            self.connect()

        plot_data = str(pdata).replace("'","\"")
        #convert labels to string
        l = str(labels)[1:-1].replace("'","")
        sql = "INSERT INTO stored_plots (plot_type, usecase, plot_name, username, plot_data, labels, stats_enable, stats_list, tstart, tstop, tokeep) VALUES ('"+plot+"', '"+usecase+"', '"+plot_name+"', '"+username+"', '"+plot_data+"', '"+l+"', '"+stats+"', '"+stat_res+"', '"+ts+"', '"+te+"', "+str(tokeep)+")"

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)   
            self.connection.commit()
            plotid = cursor.lastrowid
        except:
            plotid = None
        self.close()
        return plotid
        
    def remove_running_report(self, runid, keep_open=False):
        """Delete report execution entry from running_reports table.

        Parameters
        ----------
        runid : int or str
            Unique execution record ID.
        keep_open : bool, optional
            If True, keeps connection open (default is False).
        """      
        sql = "DELETE FROM running_reports WHERE id="+ str(runid)      
        self._commit_query(sql, keep_open)
        
    def remove_tmp_data(self, syslist, runid, keep_open = False):
        """Purge temporary experiment tables for listed systems and run ID.

        Parameters
        ----------
        syslist : list of str
            Target systems names.
        runid : int or str
            Target run execution ID.
        keep_open : bool, optional
            If True, keeps connection open (default is False).
        """
        
        for s in syslist:
            sql_remdata = "DELETE FROM "+s.lower()+"_reports_data WHERE runID="+ str(runid)
            self._commit_query(sql_remdata, keep_open=True)
        if not keep_open:            
            self.close()

    def update_config_files(self, configfile, isrunning, start_date=None, keep_open=False):
        """Update report configuration file status flags in database.

        Parameters
        ----------
        configfile : str
            Report configuration filename.
        isrunning : int
            Execution status flag (0: idle, 1: running, 2: scheduled, etc.).
        start_date : str, optional
            Scheduled start date string (default is None).
        keep_open : bool, optional
            If True, keeps connection open (default is False).
        """  
        sql = "UPDATE config_files SET isrunning = "+str(isrunning)
        if start_date is not None:
            sql += ", start_date = '"+start_date+"'"
        sql += " WHERE filename = '"+configfile+"'"      
        self._commit_query(sql, keep_open)      

    def update_progress(self, runid, percent="final"):
        """Update completion progress percentage for a running report job.

        Parameters
        ----------
        runid : int or str
            Unique run ID.
        percent : float or "final", optional
            Percentage increment or "final" to reach 100% (default is "final").
        """
        p = self.get_report_status(runid)

        if p == -99.0:
            p=0.0
        if percent == "final":
            percent = 100.0 - p

        out = p + round(percent,1)

        sql_update = "UPDATE running_reports SET exp_status = "+str(out)+" WHERE id = "+str(runid)
        self._commit_query(sql_update)
        
    def update_running_reports(self, pid, runid, tstart = None, status = None, keep_open = False):
        """Update process ID and progress status for a running report job.

        Parameters
        ----------
        pid : int
            System process ID.
        runid : int or str
            Target run execution ID.
        tstart : str, optional
            Execution start datetime string (default is None).
        status : float or int, optional
            Execution progress value (default is None).
        keep_open : bool, optional
            If True, keeps connection open (default is False).
        """

        if status is None:
            status = 0
        if tstart is not None:
            ts_str = "start_date = '"+tstart+"', "
        else:
            ts_str = ""
        sql = "UPDATE running_reports SET "+ts_str+"exp_status = "+str(status)+", pid = "+str(pid)+" WHERE id = "+str(runid)
        self._commit_query(sql, keep_open)          
