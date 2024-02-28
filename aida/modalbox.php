<?php

function show_modal($case){
  switch ($case){
    case "report":
      echo '<!-- Modal to store report into db as flagged -->						
  <div class="modal fade" id="store_report" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                  <h3 id="myModalLabel">Report flagging options</h3>
              </div>
              <div class="modal-body">

                  <form id="modal-form">
                      <div class="form-group" >
						<div class="form-group" >
							<label class="radio-inline" style="width:20%">Report Filename</label>                        
                            <input type="text" id="fname" style="width:79%" disabled></input>
                      	</div>
						<div class="form-group" >
                        	<label class="radio-inline" style="width:20%">Flag Creator</label>
                            <input type="text" id="fcreator" style="width:79%" disabled></input>
                      	</div>
					</div>


                      <h4>Flag your report</h4>
                      <div class="form-group">
                          <label class="radio-inline"><input type="radio" id="nd" name="repflag" value="nd" checked>Not Defined</label>
                          <label class="radio-inline"><input type="radio" name="repflag" value="ok">Ok</label>
                          <label class="radio-inline"><input type="radio" name="repflag" value="warning">Warning</label>
                          <label class="radio-inline"><input type="radio" name="repflag" value="serious">Serious</label>
                      </div>
                      <div class="form-group" id="description" style="display:none">
                      	<textarea style="width : 100%" rows="5" id = "input-descr" class="form-control" placeholder="Comments:"></textarea>
                      </div>




                      <div class="form-group" style="display:none" id="alert-email">
                          <input type="email" style="width : 100%" id = "email-to" class="form-control" placeholder="Send alert email to:">
                      </div>

                  </form>


                 <input type="hidden" id="period">
<!--                   <input type="hidden" id="modal-labels">
                  <input type="hidden" id="modal-tstart">
                  <input type="hidden" id="modal-tstop">-->
              </div>
              <div class="modal-footer">
                  <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
                  <button id="store-rep-btn" class="btn btn-primary" data-dismiss="modal">Confirm</button>

              </div>
          </div>
      </div>
  </div>';
      break;                        

    case "img" :
      echo '<!-- Modal to store image into db as flagged -->						
  <div class="modal fade" id="store_img" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                  <h3 id="myModalLabel">Image storing options</h3>
              </div>
              <div class="modal-body">

                  <form id="modal-form">
                      <div class="form-group" >
                          <select id="mode" style="width: 70%; margin-bottom:10px">
                              <option value="private">Private Archive</option>
                              <option value="public">Public Archive</option>
                          </select>
                          <input type="checkbox" id="downloadpdf">Download a copy</input>


							<select name="hktm_source" id="hktm_source" style="width: 70%;" required>
								<option value="" disabled selected>Select Data source</option>';
							populate_dropdown("systems", "name", "enabled=1",1);
							
      echo'	<option value="Other">Other</option></select>
					</div>


                      <h4>Flag your image</h4>
                      <div class="form-group">
                          <label class="radio-inline"><input type="radio" id="nd" name="optflag" value="nd" checked>Not Defined</label>
                          <label class="radio-inline"><input type="radio" name="optflag" value="ok">Ok</label>
                          <label class="radio-inline"><input type="radio" name="optflag" value="warning">Warning</label>
                          <label class="radio-inline"><input type="radio" name="optflag" value="serious">Serious</label>
                      </div>
                      <div class="form-group" id="description" style="display:none">
                      	<textarea style="width : 100%" rows="5" id = "input-descr" class="form-control" placeholder="Comments:"></textarea>
                      </div>




                      <div class="form-group" style="display:none" id="alert-email">
                          <input type="email" style="width : 100%" id = "email-to" class="form-control" placeholder="Send alert email to:">
                      </div>

                  </form>


<!--                  <input type="hidden" id="n_exp">
                  <input type="hidden" id="modal-labels">
                  <input type="hidden" id="modal-tstart">
                  <input type="hidden" id="modal-tstop">-->
              </div>
              <div class="modal-footer">
                  <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
                  <button id="store-img-btn" class="btn btn-primary" data-dismiss="modal">Confirm</button>

              </div>
          </div>
      </div>
  </div>';
      break;        

    case "exp":
      echo '<!-- Modal to store Experiment in PDF -->						
  <div class="modal fade" id="store_pdf" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                  <h3 id="myModalLabel">Experiment results storing options</h3>
              </div>
              <div class="modal-body">

                  <form id="modal-form">
                      <div class="form-group" >
                          <select id="mode" style="width: 70%; margin:0 40px 30px 0">
                              <option value="private">Private Archive</option>
                              <option value="public">Public Archive</option>
                          </select>
                          <input type="checkbox" id="downloadpdf">Download a copy</input>
                      </div>

                      <h4>Flag your experiment</h4>
                      <div class="form-group">
                          <label class="radio-inline"><input type="radio" id="nd" name="optflag" value="nd" checked>Not Defined</label>
                          <label class="radio-inline"><input type="radio" name="optflag" value="ok">Ok</label>
                          <label class="radio-inline"><input type="radio" name="optflag" value="warning">Warning</label>
                          <label class="radio-inline"><input type="radio" name="optflag" value="serious">Serious</label>
                          <!--<select id="flag" style="width: 70%">
                              <option value="nd" selected>Not Defined</option>
                              <option value="ok">Ok</option>
                              <option value="warning">Warning</option>
                              <option value="serious">Serious</option>
                          </select>-->
                      </div>
                      <div class="form-group" id="description" style="display:none"></div>




                      <div class="form-group" style="display:none" id="alert-email">
                          <input type="email" style="width : 100%" id = "email-to" class="form-control" placeholder="Send alert email to:">
                      </div>

                  </form>



                  <input type="hidden" id="n_exp">
                  <input type="hidden" id="modal-labels">
                  <input type="hidden" id="modal-tstart">
                  <input type="hidden" id="modal-tstop">
                  <input type="hidden" id="modal-pid">
				  <input type="hidden" id="img_op">				  
              </div>
              <div class="modal-footer">
                  <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
                  <button id="store-btn" class="btn btn-primary" data-dismiss="modal">Confirm</button>
                  <!-- inserire validation email -->
              </div>
          </div>
      </div>
  </div>';
      break;

    case "loginerr":
      echo '<!-- Modal to show login errors -->						
  <div class="modal fade" id="loginerr" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                  <h3 id="myModalLabel">Error!</h3>
              </div>
              <div class="modal-body">
					<h4>Error logging in! Invalid username and/or password. Please retry</h4>
              </div>
              <div class="modal-footer">
                  <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
              </div>
          </div>
      </div>
  </div>';        

      break; 

    case "pwd":
      echo '<!-- Modal to change password -->						
  <div class="modal fade" id="pwd" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                  <h3 id="myModalLabel">Change Your Password</h3>
              </div>
              <div class="modal-body">
                  <form id="modal-pwd">
                      <div class="form-group">
							<label class="pwd-inline">Old Password :</label><input type="password" id = "oldpwd" class="form-control pwd-input" required>
                            <div style="clear:both;"></div>
							<label class="pwd-inline">New Password :</label><input type="password" id = "newpwd" name="newpwd" class="form-control pwd-input" required>
                            <div style="clear:both;"></div>
							<label class="pwd-inline">Confirm New Password :</label><input type="password" id = "checkpwd" name="checkpwd" class="form-control pwd-input" required>                            
                      </div>
                  </form>

              </div>
              <div class="modal-footer">
                  <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
                  <button id="change-pwd" class="btn btn-primary">Confirm</button>

              </div>
          </div>
      </div>
  </div>';
      break;

  }



}
?>



<div class="modal fade" id="export" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">Export App Data</h3>
      </div>
      <div class="modal-body">
        <h4>Select Info to Export</h4>
        <form id="modal-form">
          <div class="form-group" >
            <div class="col-xs-12"><label class="col-xs-5 control-label">Users</label><div class="col-xs-2"><input type="checkbox" id="exp_users" checked/></div></div>
            <div class="col-xs-12"><label class="col-xs-5 control-label ">Reports</label><div class="col-xs-2"><input type="checkbox" id="exp_reports" checked/></div></div>            
            <div class="col-xs-12"><label class="col-xs-5 control-label ">Report Configuration Files</label><div class="col-xs-2"><input type="checkbox" id="exp_repconf" checked/></div></div>
            <div class="col-xs-12"><label class="col-xs-5 control-label ">Stored Experiments</label><div class="col-xs-2"><input type="checkbox" id="exp_stored" checked/></div></div>
            <div class="col-xs-12"><label class="col-xs-5 control-label ">Systems Configurations</label><div class="col-xs-2"><input type="checkbox" id="exp_sys" checked/></div></div>
            <div class="col-xs-12"><label class="col-xs-5 control-label ">History</label><div class="col-xs-2"><input type="checkbox" id="exp_history" checked/></div></div>    
            <div class="col-xs-12"><label class="col-xs-5 control-label ">SMTP settings</label><div class="col-xs-2"><input type="checkbox" id="exp_smtp" checked/></div></div>                
          </div>
        </form>                
    </div>
    <div class="modal-footer">
      <button id="export-btn" class="btn btn-primary" data-dismiss="modal">Confirm</button>
      <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
    </div>
  </div>
</div>
</div>

<div class="modal fade" id="import" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">Import App Data</h3>
      </div>
      <div class="modal-body">
        <h3><strong>ATTENTION! Backup files not correctly exported could cause SERIOUS APP MALFUNCTIONING</strong></h3><br/><br/>
        <h4>Select File to Import (tar.gz)</h4>
        
        <form id="upload-backup" class="form-horizontal form-bordered" method="" action="">
          <div class="upload-form form-group" id="uploader">

            <div class="col-md-12">
              <div class="fileupload">
                                   

                <!-- File List -->
                <div id="filelist" class="uneditable-input bkp-file filelist">

                  <i class="fa fa-file fileupload-exists"></i>
                  <span id="file-preview" class="fileupload-preview"></span>
                </div>

                <!-- Select & Upload Button -->
                <div class="up-btn">
                  <a class="btn btn-default" id="pickfiles" href="#">Browse</a>
					<a class="btn btn-default" id="uploadfiles" href="#">Upload</a>				  
                </div>
				
				<!-- Progress Bar -->
				<div id="progressbar"></div>
              </div>
            </div>
          </div>
			<div class="form-group" id="okupload" style="display:none">
				<div class="col-xs-12" style="margin-top:10px">
					<span id="upfile-preview" style="margin-right:10px"></span><span class="label label-success">Success</span>
					<span id="upfile-remove" style="margin-right:10px"></span><img src="assets/images/remove.png" style="cursor:pointer;width: 19px;" onclick="remove_upfile()"/>					
				</div>                          
			</div>
			
          <div class="form-group" id="import_items" style="display:none">
			<h4 style="margin-left: 15px;">Select Items to import</h4>
            <div class="col-xs-12" id="check_0"><label class="col-xs-5 control-label bkp-label">Users</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_users"/></div></div>
            <div class="col-xs-12" id="check_1"><label class="col-xs-5 control-label bkp-label">Reports</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_reports"/></div></div>            
            <div class="col-xs-12" id="check_2"><label class="col-xs-5 control-label bkp-label">Report Configuration Files</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_repconf"/></div></div>
            <div class="col-xs-12" id="check_3"><label class="col-xs-5 control-label bkp-label">Stored Experiments</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_stored"/></div></div>
            <div class="col-xs-12" id="check_4"><label class="col-xs-5 control-label bkp-label">Systems Configurations</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_sys"/></div></div>
            <div class="col-xs-12" id="check_5"><label class="col-xs-5 control-label bkp-label">History</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_history"/></div></div>    
            <div class="col-xs-12" id="check_6"><label class="col-xs-5 control-label bkp-label">SMTP settings</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_smtp"/></div></div>                
          </div>			
			<div class="form-group" id="hidden-fields">
				<input type="hidden" name="cols" id = "cols" value=""></input>
				<input type="hidden" name="impfile" id = "impfile" value=""></input>
			</div>			
        </form>        
      </div>
      <div class="modal-footer">
      	<button id="import-btn" class="btn btn-primary" data-dismiss="modal" style="display:none">Confirm</button>        
        <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
      </div>
    </div>
  </div>
</div>

<!-- Modal to invite to close tab after first installation -->						
  <div class="modal fade" id="modal-install" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <h3 id="myModalLabel">Registration complete!</h3>
              </div>
              <div class="modal-body" id="reg-comp-ok">
					<!--<h4 ></h4>-->
              </div>
              <div class="modal-footer"></div>
          </div>
      </div>
  </div>
  
<!-- Modal installation complete -->						
  <div class="modal fade" id="modal-complete" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

      <div class="modal-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <h3 id="myModalLabel">Installation complete!</h3>
              </div>
              <div class="modal-body">
				  <div class="row">
					<div class="col-md-8" id="inst-compl">
					</div>
					<div class="col-md-4">
						<img src="assets/images/minilogoAIDA.png" height="160px" style="margin-top: 20px;"alt="">
					</div>
				  </div>			  

					<!--<h4 ></h4>-->
              </div>
              <div class="modal-footer">
					<button class="btn btn-primary" data-dismiss="modal" aria-hidden="true" onclick="window.location.href = 'index.php'">OK</button>
			  </div>
          </div>
      </div>
  </div>  
 

 
<!-- Modal Change Settings -->
<div class="modal fade" id="gen_set" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">Web App Settings</h3>
      </div>
      <div class="modal-body admin-settings">
		<form method="post" id="update_genset" name="update_genset" action="" novalidate = "novalidate">
			<?php
				$config = read_json_file("config.json");
				$offset = $config['offset'];
				$history = $config['history'];
				$nprocs = $config['nprocs'];
				$admin_email = $config['admin_email'];
			?>	

			<div class="col-xs-12">
			
				<div class="form-group mb-lg">
					<label class="col-xs-5">Reports Offset (hours)</label>
					<div class="col-xs-7"><input name="rep_offset" id="rep_offset" type="number" min="0" class="form-control" value="<?php echo $offset;?>" required /></div>
				</div>

				<div class="form-group mb-lg">
					<label class="col-xs-5">History records per user</label>
					<div class="col-xs-7"><input name="histnum" id="histnum" type="number" min="0" class="form-control" value="<?php echo $history;?>" required /></div>
				</div>

				<div class="form-group mb-lg">
					<label class="col-xs-5">Processors per system</label>
					<div class="col-xs-7"><input name="nprocs" id="nprocs" type="number" min="1" class="form-control" value="<?php echo $nprocs;?>" required /></div>
				</div>

				<div class="form-group mb-lg">
					<label class="col-xs-5">Communications E-mail</label>
					<div class="col-xs-7"><input name="email" id="email" type="email" class="form-control" value="<?php echo $admin_email;?>" required /></div>				
				</div>
				

			</div>			
			<div class="form-group mb-lg">

					<label class="col-xs-12">Time Window Threshold for Offline Plots (hours)</label>
					<?php get_systems_plotdelta();?>
			</div>
		</form>
      </div>
      <div class="modal-footer">
      	<button id="gen_set-btn" class="btn btn-primary">Confirm</button>
      
		<button class="btn" data-dismiss="modal" aria-hidden="true">Abort</button>
      </div>
    </div>
  </div>
</div>

<!-- Modal Change SMTP -->
<div class="modal fade" id="smtp_set" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">SMTP Settings</h3>
      </div>
      <div class="modal-body admin-settings">
		<form method="post" id="smtpconf" name="smtpconf" action="" novalidate = "novalidate">
			<?php
				$config = read_json_file("smtp.json");
				$host = $config['host'];
				$port = $config['port'];
				$user = $config['user'];
				$password = $config['password'];
			?>	
			
				<div class="form-group mb-lg">
					<label class="col-xs-5">Host</label>
					<div class="col-xs-7"><input name="conf_host" id="conf_host" type="text" class="form-control" value="<?php echo $host;?>" required /></div>
				</div>

				<div class="form-group mb-lg">
					<label class="col-xs-5">Port</label>
					<div class="col-xs-7"><input name="conf_port" id="conf_port" type="number" min="1" class="form-control" value="<?php echo $port;?>" required /></div>
				</div>

				<div class="form-group mb-lg">
					<label class="col-xs-5">User</label>
					<div class="col-xs-7"><input name="conf_user" id="conf_user" type="text" class="form-control" value="<?php echo $user;?>" required /></div>
				</div>

				<div class="form-group mb-lg">
					<label class="col-xs-5">Password (optional)</label>
					<div class="col-xs-7"><input name="conf_pwd" id="conf_pwd" type="text" class="form-control" value="<?php echo $password;?>"/></div>				
				</div>
		</form>
      </div>
      <div class="modal-footer">
		<button id="smtp_test-btn" class="btn btn-primary">Test SMTP</button>
      	<button id="smtp_set-btn" class="btn btn-primary">Confirm</button>
      
		<button class="btn" data-dismiss="modal" aria-hidden="true">Abort</button>
      </div>
    </div>
  </div>
</div>

<!-- Modal Change Repo Config -->
<div class="modal fade" id="repo_set" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">

  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">Repository settings</h3>
      </div>
      <div class="modal-body admin-settings">
		<form method="post" id="repoconf" name="repoconf" action="" novalidate = "novalidate">
			<?php
				//get all data required for building form
				$opmode = get_opmode(false);
				
				$systems = get_cols_from_db("systems","name, GROUP_CONCAT(origin) as origin, GROUP_CONCAT(enabled) as enabled","GROUP BY name","name");	
				$en_status = [];
				while( $rs = mysqli_fetch_assoc($systems)){
					$s = strtolower($rs['name']);
					$o = explode(",", $rs['origin']);
					$e = explode(",", $rs['enabled']);
					$en_or = [];
					for ($i = 0; $i <= sizeof($o)-1; $i++) {

						
						if($e[$i]==1){
							array_push($en_or,$o[$i]);
						}
					}
					$en_status[$s] = $en_or;
					
				}
				echo "<input id='en_status' type='hidden' value='".json_encode($en_status)."'/>";

				
			?>
				<div class="form-group mb-sm" id="form_source">
					<label class="col-xs-6">System</label>
					<div class="col-xs-6">
					<select name="repo_source" id="repo_source" class="form-control" onchange="import_json(this.value)" required>
						<option value="" disabled selected>Select</option>
						<?php
							mysqli_data_seek($systems, 0);
							while( $rs = mysqli_fetch_assoc($systems)){
								echo '<option value="'.$rs['name'].'">'.$rs['name'].'</option>';
							}
						?>
					</select>
					</div>	
				</div>			
				<div class="form-group mb-xs" id="form_opmode" style="display:none">
					<label class="col-xs-6">Operational Mode</label>
					<div class="col-xs-6">
						<select name="repo_opmode" id="repo_opmode" class="form-control" onchange="show_origin(this.value)" required></select>
					</div>
				</div>
				<div class="form-group mb-xs" id="form_origin" style="display:none">
					<label class="col-xs-6">Data origin</label>
					<div class="col-xs-6">
						<select name="repo_origin" id="repo_origin" class="form-control" onchange="show_repo_settings(this.value)" required></select>
					</div>
				</div>


				<div class="form-group mb-xs" id="form_settings" style="display:none">
					<div class="form-group mb-xs">
						<label class="col-xs-6">No. of simultaneous DB accesses</label>
						<div class="col-xs-6">
							<input name="repo_nprocs" id="repo_nprocs" type="number" min="1" value="" class="form-control" required></select>
						</div>
					</div>
					<div class="form-group mb-xs">
						<label class="col-xs-6">Repository</label>
						<div class="col-xs-6">
							<select name="repo_repo" id="repo_repo" class="form-control" onchange="set_repofiles(this)" required></select>
						</div>
					</div>					
					

					<div class="form-group mb-xs">
						<label class="col-xs-6">Repository Type</label>
						<div class="col-xs-6">
							<select name="repo_type" id="repo_type" class="form-control" required>
								<option value="file">Files</option>
								<option value="db">Database</option>							
							</select>

						</div>
					</div>
					<div class="form-group mb-xs">
						<label class="col-xs-6">Files Repository</label>
						<div class="col-xs-6">	
							<input name="repo_files" id="repo_files" type="text" class="form-control" value="" disabled readonly />
							<input id='repomap' type='hidden' value=''/>							
						</div>
					</div>
				
					<div class="form-group mb-xs">
						<label class="col-xs-12">Metadata DB Settings</label>

							<div class="form-group mb-xs">
								<label class="col-xs-6" style="padding-left:50px">Host</label>
								<div class="col-xs-6"><input name="repo_meta_host" id="repo_meta_host" type="text" class="form-control" value="" required /></div>
							</div>

							<div class="form-group mb-xs">
								<label class="col-xs-6" style="padding-left:50px">Port</label>
								<div class="col-xs-6"><input name="repo_meta_port" id="repo_meta_port" type="number" min="1" class="form-control" value="" required /></div>
							</div>

							<div class="form-group mb-xs">
								<label class="col-xs-6" style="padding-left:50px">User</label>
								<div class="col-xs-6"><input name="repo_meta_user" id="repo_meta_user" type="text" class="form-control" value="" required /></div>
							</div>

							<div class="form-group mb-xs">
								<label class="col-xs-6" style="padding-left:50px">Password</label>
								<div class="col-xs-6"><input name="repo_meta_pwd" id="repo_meta_pwd" type="text" class="form-control" value="" required /></div>				
							</div>
							<div class="form-group mb-xs">
								<label class="col-xs-6" style="padding-left:50px">DB Name</label>
								<div class="col-xs-6"><input name="repo_meta_dbname" id="repo_meta_dbname" type="text" class="form-control" value="" required /></div>				
							</div>
							<div class="form-group mb-xs">
								<label class="col-xs-6" style="padding-left:50px">DB Table</label>
								<div class="col-xs-6"><input name="repo_meta_table" id="repo_meta_table" type="text" class="form-control" value="" required /></div>				
							</div>
							<div class="form-group mb-xs">
								<label class="col-xs-6" style="padding-left:50px">Extra Statement</label>
								<div class="col-xs-6"><input name="repo_meta_condition" id="repo_meta_condition" type="text" class="form-control" value=""/></div>				
							</div>							
					</div>
				</div>
		</form>
      <input type="hidden" value="" id="json_config"/>  
        
      </div>
      <div class="modal-footer">
      	<button id="smtp_set-btn" class="btn btn-primary">Confirm</button>
		<button class="btn" data-dismiss="modal" aria-hidden="true">Abort</button>
      </div>
    </div>
  </div>
</div>