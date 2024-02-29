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
 
## Main AIDA functionalities
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

## Browser compatibility
In terms of web browser compatibility, IODA has been tested and validated on:
* Chrome v118;
* Microsoft Edge v114;
* Firefox v114;
* Opera v100;
 
# Installation Procedure
The installation of the AIDA package on the AIDAHM is automated by exploiting the docker virtualization technology.
AIDA is developed as a double container, i.e. two standardized software units, respectively, the web application and the
local database, allowing to isolate the application environment from the rest of the hosting machine.

**NOTE**: A third docker container is provided, containing a simple database with fake data only for demonstrative purposes. To access to different data repositories, it is needed to write the required I/O code for interfacing AIDA with external DBs.

In this repository, the AIDA code directory is provided, together with the dumps of the two MySQL databases (AidaDB and FakeDB), for a manual installation. However, it is **STRONGLY** suggested to use the procedure described below, that requires the files located into the *installation* folder

## Docker Configuration
1. Install Docker (https://docs.docker.com/engine/install/) and Docker-Compose (https://docs.docker.com/compose/install/). For instance, using Linux Ubuntu, it can be done using the following command line:
<pre>
sudo apt install docker docker-compose -y
</pre>
2. Download the complete AIDA files package (**"_installation_"** folder):
  * **docker-compose.yml** , the file defining the inner relations of the docker containers;
  * **Dockerfile** , the docker configuration;
  * **aidaCodeXX.tar.gz** , containing the AIDA code;
  * **apache2.conf** needed for setting the environment of apache in the docker container (the file should be in the same folder of Dockerfile and could not be deleted);
  * **php.ini** needed for setting the environment of php in the docker container (the file should be in the same folder of Dockerfile and could not be deleted);
  * **aidaDBXX.tar.gz** , containing an empty pre-configured DB.
  * **AidaDBFakeXX.tar.gz** , containing the fake data DB.
3. Uncompress the compressed files for DBs and code:
  * The name of the three directories (for DBs and code, respectively) can be arbitrarily set. But it is important to make the three directories case sensitive. This is particularly required in case of an OS not case sensitive (such as MS Windows). To do that, there is a specific command line. For instance, in MS Windows, by running a powershell as administrator:
<pre>
fsutil.exe file SetCaseSensitiveInfo <YourLocalFolder>/ioda enable
fsutil.exe file SetCaseSensitiveInfo <YourLocalFolder>/mysqlData enable
fsutil.exe file SetCaseSensitiveInfo <YourLocalFolder>/mysqlFakeData enable
</pre>
  * In Linux you need to uncompress the folder as root to correctly preserve the ownership of the code directory ( @sudo tar -xvzf aidaCodeXXtar.gz ).
4. Specify the location (**ABSOLUTE PATH**) of the uncompressed folders (DBs and code) in docker-compose.yml;
5. Change, if needed, the exposed ports for AIDA (web application and SQL) in docker-compose.yml. This is required only if you already are exposing different services on the default ports (80 for AIDA and 3306 for SQL);
6. Launch docker-compose using your docker-compose.yml. This could depend on the OS. On Ubuntu:
  * From the folder where you downloaded docker-compose.yml **AND** Dockerfile launch: 
<pre>
docker-compose up –d --build
</pre> 
  * If you want to automatically launch AIDA at each machine reboot, you have to configure your machine to do that, for example by using the _crontab_ on Ubuntu.

## First Access Configuration
Once installed, AIDA can be accessed by any web browser at the dedicated address. On first access, an introductory page is shown in order to start the definition of some primary settings:

![first_install](https://github.com/pepric/aida/assets/50458987/69aab471-7c50-48bc-9ecf-2ee46e4ea066)

By clicking on _“START INSTALLATION”_ button, a multi-step configuration wizard starts.

### Backup import
At this stage, the user can import a backup previously created on a previous AIDA instance (Figure 3). This optional step
can be skipped by clicking on the ”Skip” button. 

![backup_1](https://github.com/pepric/aida/assets/50458987/7e8d1a69-d4f3-4391-8d4e-617374ba26ed)

To import an existing backup (as a tar.gz archive), the user can easily
browse the local machine and upload it. Once uploaded, the user can select the sections to import. 

![backup_2](https://github.com/pepric/aida/assets/50458987/7e722797-06fd-40b3-8cad-85227467d81d)

If the option “SMTP settings” is not checked, then the AIDA SMTP server should be configured (see below). 

If the option “Users” is not checked, then the first AIDA administrator should be registered (see below). 

If import step is skipped, then both SMTP server and first administrator should be defined in next steps.

### Mail server configuration
In order to send e-mails to the users (communications and analysis results), AIDA requires access to a mail server.

If not already imported, SMTP server data must be defined by filling this form with server name, port, username and, if need, the password.

**NOTE**: it is strongly suggested to **NOT** use the Google SMTP because of its strict policy on external apps.

![smtp](https://github.com/pepric/aida/assets/50458987/bbaf46c7-4c7b-455d-86ca-c08ca9fc4fb5)

### First administrator registration
First user data must be inserted into the AIDA DB by filling the related form. The user can use its own email address in order to receive AIDA notifications on new user registration and generated reports, or use a different one by acting on the related checkbox.

![first_admin](https://github.com/pepric/aida/assets/50458987/f6784292-8f7d-4389-ab1d-6251133d09ed)

Once the form is submitted, if all the inserted data are correct, the user will receive an activation email to confirm its email address. By confirming, AIDA will be opened into a new tab notifying the completion of installation procedure.

![mail_active](https://github.com/pepric/aida/assets/50458987/1aa84782-c867-4133-b6c8-b038424a51b7)





