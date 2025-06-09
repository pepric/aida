#!/usr/bin/python

import functions as util
import pymysql
import pymysql.cursors
import traceback

class dbIO():
    """ Class implementing utilities and queries for local database interface"""
    def __init__(self, config):
        """dbIO init
        Parameters
        ---------
        config : dict,
            dictionary containing connection parameters
            
        Attributes
        ---------
        config : dict,
            dictionary containing connection parameters
        connection : class or None,
            connection class by pymysql if not None
        """            
       
        self.config = config
        self.connection = None        

    def _commit_query(self, sql, keep_open = False):
        """ Commit a query
        Parameters
        ---------
        sql : str,
            query to commit,
        keep_open : boolean,
            if True, keep the connection open for next operation
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
        """ Check if a connection can be opened
        Parameters
        ---------
        keep_open : boolean,
            if True, keep the connection open for next operation
            
        Returns
        --------
        locerr : 0 or 1,
            it is 0 if the connection can be opened, 1 otherwise
        connection : class
            connection class by pymysql if opened, None otherwise
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
        """ Get number of records in defined DB table with conditions defined by statement.
        Parameters
        ---------
        tbl : string,
            table to query
        statement : string,
            statement of query
        keep_open : boolean,
            if True, keep the connection open for next operation

        Returns
        ---------
        counts : int,
            number of records
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
        """Close connection"""      
        self.connection.close()
        self.connection = None
        
    def connect(self):
        """Open a new connection to local DB
        Returns
        --------
        error : 0 or 1,
            it is 0 if the connection can be opened, 1 otherwise
        connection : class
            connection class by pymysql if opened, None otherwise
        """         
        error, connection = self.check_connection(keep_open = True)
        return error, connection
      
    def get_connection(self):
        """Return the current connection"""      
        return self.connection

    def get_flagged(self, mode = "exp", archive = "public",keep_open = False):
        """ Get list of flagged experiment from DB.
        Parameters
        ---------
        mode : string, "exp" or "par"
            query by "experiment" or by "parameter"
        archive: string, "stored" or "user"
            query public archive or private archive
        keep_open : boolean,
            if True, keep the connection open for next operation

        Returns
        ---------
        res : list of dictionaries,
            list of dicts containing flagged experiments records
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
        """ Get list of data files already downloaded for analysis.
        Parameters
        ---------
        source : str,
                system source under analysis    
        tmp_dir : str,
                user temporary directory to search in 
        ts : int or None,
            timestamp of search start date
        te : int or None,
            timestamp of search end date
        keep_open : boolean,
            if True, keep the connection open for next operation

        Returns
        ---------
        locfiles : list,
            list of stored files
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
        
    def get_opmode(self,keep_open = False):
        """ Get the current operation mode.
        Parameters
        ---------
        keep_open : boolean,
            if True, keep the connection open for next operation

        Returns
        ---------
        res : dict,
            single entry dictionary, {"mode" : <current operational mode>}
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
        """ Get list of users from DB.
        Parameters
        ---------
        status : int,
            0 to select "pending", 1 for "active" or 2 for "deactive" users
        keep_open : boolean,
            if True, keep the connection open for next operation

        Returns
        ---------
        res : list of dictionaries,
            list of dicts containing users records
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
        """Get status of current report record within running_reports table in local DB
        
        Parameters
        ----------
        runid : int or str,
            id of the current experiment
            
        Returns
        --------
        p : float,
            exp_status value from local DB
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
        """ Get running report list from DB.
        Parameters
        ---------
        keep_open : boolean,
            if True, keep the connection open for next operation
        role : string,
            if "admin", get all the results, otherwise get only user running reports

        Returns
        ---------
        res : list of dictionaries,
            list of dicts containing running reports records
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
        """ Get available systems from DB.
        Parameters
        ---------
        keep_open : boolean,
            if True, keep the connection open for next operation

        Returns
        ---------
        out : list,
            the list of available systems
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
        """Insert a new downloaded file into the local DB
        
        Parameters
        ---------
        fname : str,
            name of file
        source : str,
            system source of file
        subsystem : str, optional
            subsystem source of file. Default is None            
        user : str,
            user who downloaded file
        tstart : str, optional
            start time in file. Default is None
        tstop : str, optional
            end time in file.  Default is None
        keep_open : boolean,
            if True, keep the connection open for next operation
        """

        sql_newf = "INSERT INTO local_files (filename, data_source, username, filetype) VALUES ('"+fname+"', '"+source+"', '"+user+"', '"+ftype+"')"
        self._commit_query(sql_newf, keep_open)      
      
    def insert_report_file(self, fname, user, creation, period, configfile, tstart, tstop, keep_open = False):
        """Insert a new report file into the local DB
        
        Parameters
        ---------
        fname : str,
            name of report file
        user : str,
            user who run the report generation
        creation : str,
            report creation date
        period : "ondemand", "daily", "weekly", "monthly" or "custom"
            report periodicity
        configfile : str,
            name of report configuration file
        tstart : str,
            start time of report
        tstop : str,
            end time of report
        keep_open : boolean,
            if True, keep the connection open for next operation
        """
        sql_newrep = "INSERT INTO report_files (filename, username, upload_date, period, config_file, start_date, end_date) VALUES ('"+fname+"', '"+user+"', '"+creation+"', '"+period+"', '"+configfile+"', '"+tstart+"', '"+tstop+"')"
        self._commit_query(sql_newrep, keep_open)

    def insert_temp_plot(self, pdata, usecase, plot, username, labels, stats, stat_res, plot_name, ts, te, tokeep):
        """Insert a new temporary plot experiment into the local DB
        
        Parameters
        ---------
        pdata : dict,
            data to plot as retrieved by get_data
        usecase: "htkm" or "science", string
            data origin
        plot : str,
            plot to generate
        username : str,
            user who request the plot
        labels : list,
            list of plotted parameters
        period : "ondemand", "daily", "weekly", "monthly" or "custom"
            report periodicity
        stats : "global" or "advanced", string
            type of statistical analysis requested
        stat_res : dict,
            results of statistical analysis
        plot_name : str,
            displayed name of plot
            
        Returns
        --------
        plotid : int,
            row id of stored record in DB
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
        """Remove a report generation from running reports table
        
        Parameters
        ---------
        runid : int or str,
            id of the current experiment
        keep_open : boolean,
            if True, keep the connection open for next operation
        """      
        sql = "DELETE FROM running_reports WHERE id="+ str(runid)      
        self._commit_query(sql, keep_open)
        
    def remove_tmp_data(self, syslist, runid, keep_open = False):
        """Remove temporary experiment data from local DB
        
        Parameters
        ----------
        confreport : list
            list of systems involved in current experiment
        runid : int or str,
            id of the current experiment
        keep_open : boolean,
            if True, keep the connection open for next operation        
        """
        
        for s in syslist:
            sql_remdata = "DELETE FROM "+s.lower()+"_reports_data WHERE runID="+ str(runid)
            self._commit_query(sql_remdata, keep_open=True)
        if not keep_open:            
            self.close()

    def update_config_files(self, configfile, isrunning, start_date=None, keep_open=False):
        """Update config file record within config_files table in local DB
        
        Parameters
        ----------
        configfile : str,
            name of report configuration file
        isrunning : int,
            running status of related report generation (0 = idle, 1 = running, 2 = scheduled),
        start_date : str,
            If not None, start date for report generation        
        keep_open : boolean,
            if True, keep the connection open for next operation        
        """  
        sql = "UPDATE config_files SET isrunning = "+str(isrunning)
        if start_date is not None:
            sql += ", start_date = '"+start_date+"'"
        sql += " WHERE filename = '"+configfile+"'"      
        self._commit_query(sql, keep_open)      

    def update_progress(self, runid, percent="final"):
        """Update progress percentage of current report record within running_reports table in local DB
        
        Parameters
        ----------
        runid : int or str,
            id of the current experiment
        percent : float or "final",
            if float, the percentage to add to the previous status. If "final", percent is set in order to reach 100%
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
        """Update current report record within running_reports table in local DB
        
        Parameters
        ----------
        pid : int,
            program id for current report generation experiment
        runid : int or str,
            id of the current experiment.
        tstart : str, optional
            If not None, start date of report acquisition. Default is None
        status : str, optional
            If not None, starting percentage of report generation. Default is None
        keep_open : boolean, optional
            if True, keep the connection open for next operation. Default is False.     
        """

        if status is None:
            status = 0
        if tstart is not None:
            ts_str = "start_date = '"+tstart+"', "
        else:
            ts_str = ""
        sql = "UPDATE running_reports SET "+ts_str+"exp_status = "+str(status)+", pid = "+str(pid)+" WHERE id = "+str(runid)
        self._commit_query(sql, keep_open)          
