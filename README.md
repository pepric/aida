# About AIDA
AIDA is a portable and modular web application, designed to provide an efficient and intuitive software infrastructure to support monitoring of data acquiring systems over time, diagnostics and both scientific and engineering data quality analysis, particularly suited for astronomical instruments.

The AIDA design was mainly focused on the following goals:
* Daily mission operations, for instruments health assessment and reporting:
  * Monitoring and verifying the nominal quality of data;
  * Production of  user-defined reports (automatic and/or on-demand);
* Short/Mid/Long term activities, to investigate and report instruments behaviour over time:
  * Analysis of instruments HouseKeeping/TeleMetry (HK/TM) trends;
  * Analysis of instruments systematic effects;
  * Detection and analysis of instrumental features, degradation and anomalies;
* Data Analysis:
  *  Basic and on-demand advanced statistics for data correlation and quality assessment;
  *  Machine/Deep Learning based classification/regression on data.

In the following we will use the term **AIDAHM**, referring to a generic hosting machine on which AIDA is
installed and running
 
Main AIDA functionalities are:

* Instrument monitoring, report generation and delivery
  * Periodic report production on a predefined parameter list and delivery to remote archives;
  * On demand customized report production, based on user selected systems and parameters, stored in the AIDAHM filesystem;
* Visualization/Exploration
  *  Plots generation on user selected systems and parameters;
  *  Dynamically navigable histograms, scatter plots, trend analyses;
  *  Observed/diagnostic images visualization and analysis:
    *  Static view, dynamic navigation, statistics and cut-outs creation;
    *  Advanced operations on images (Mosaic visualization, statistics on composed image) (**IN PROGRESS**)
*  Statistics estimation:
  *   Default estimators, automatically produced with the plots from tabular data:
    *    mean, median, RMS, standard deviation, variance, minimum, maximum, MAD, NMAD, kurtosis, skewness;
  *   Special estimations (tables/images);
    *  mode, percentiles, biweight, σ-clipping; skewness;
  *  Machine/Deep Learning based classification/regression/prediction on local data (**IN PROGRESS**).
*  Additional features:
  *  Flagging System: association of a semaphore-like flag to each kind of experiment, to indicate its status and generate a related PDF report, summarizing its results and flags;
  *  Local Data Analysis: generation of plots on data and visualize/analyze images uploaded from local machine;
  *  Users and System Management:
      * online user registration to be confirmed by administrators;
      *  user password recovery system
      *  administration management:
        *  enable, disable or remove users;
        *  set Operating Mode (Nominal, Commissioning, Contingency);
        *  enable/disable and configure systems to monitor;
        *  set web app configuration (SMTP server, number of processors to use…);
  *  Logging System: each operation performed is logged into local DB;
  *  Easy Step-by-step Installation Procedure;
  *  Customizable plots graphics;
  *  Data backup system    
 
# Prerequisites

# Installation Procedure
