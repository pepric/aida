<?php include("header.html");
	if(!@include_once('functions.php')) {
		include('functions.php');	
	}
	echo '<section role="main" class="content-body-index">';
	echo '<header class="page-header page-header-index">';

	echo "</header>";?>
	<span class="name" id="session-user" style="display:none;">1stInstall</span>
	<span class="name" id="confirm" style="display:none;"><?php if(isset($_GET['confirm'])){echo $_GET['confirm'];} else {echo 0;} ?></span>
	<span class="name" id="activation" style="display:none;"><?php if(isset($_GET['user'])){echo $_GET['user'];} else {echo 0;} ?></span>
	<span class="name" id="newmail" style="display:none;"><?php if(isset($_GET['email'])){echo $_GET['email'];} else {echo 0;} ?></span>						
	<div class="row justify-content-center" >
		<div class="col-md-12">
			<div class="panel-body panel-body-index" id="main_inst">
				<div class="first-panel col-md-12">
					<div class = "col-md-2"></div>
					<div class = "description col-md-8 col-md-offset-4">
					<!--	<p style="margin-top:20px"><img src="assets/images/logoAIDA.png" height="150" alt="" /></p>-->	
						<h2>Welcome to AIDA installation</h2>
						<p>Once installation process is started, you will be able to define a minimum group of settings, required to correctly start AIDA. You can also upload a data backup previously downloaded from another AIDA installation.</p>
						<br/>
						<p>
							<button class="btn btn-primary btn-lg " onclick="start_install();">START INSTALLATION</button>
						</p>
					</div>
					<div class = "col-md-2"></div>
				</div>
			</div>

			<!-- ADMIN SECTION -->			
			<div class="panel-body panel-body-index" id="1streg_form" style="display:none">
				<div class="first-panel col-md-12">
					<div class = "col-md-2"></div>
					<div class = "description col-md-8">
						<div class="col-md-2"></div>
						<div class="col-md-8">						
							<h2 style="margin-bottom:30px">First Admin registration</h2>
						</div>
						<div class="col-md-2" style="text-align:right; padding: 23px;">
							<button class="btn btn-danger" id = "upload_skip" onclick="abort_install()">Abort</button>
						</div>						
						<div class="col-auto">
							<form method="post" id="signupform" name="signupform" action="" novalidate = "novalidate">
								<table class="reg_tbl">
									<tr>
										<td class="tbl_label"><label>Name </label></td>
										<td class="tbl_field"><input name="name" id="name" type="text" class="form-control input-lg" required /></td>
									</tr>								
									<tr>
										<td class="tbl_label"><label>E-mail Address </label></td>
										<td class="tbl_field"><input name="email" id="email" type="email" class="form-control input-lg" required /></td>
									</tr>
									<tr>
										<td class="tbl_label"><label>Use same email for notifications </label></td>
										<td class="tbl_field"><input class="form-check-input" type="checkbox" value="" id="notificationemail" checked>
									</tr>									
									<tr id="tr_noti" style="display:none">
										<td class="tbl_label"><label>Notification E-mail</label></td>
										<td class="tbl_field"><input name="notiemail" id="notiemail" type="email" class="form-control input-lg" /></td>
									</tr>									
									<tr>
										<td class="tbl_label"><label>Role </label></td>
										<td class="tbl_field"><input name="role" id="role" type="text" value="Administrator" class="form-control input-lg" disabled selected /></td>
									</tr>
									<tr>
										<td class="tbl_label"><label>Password </label></td>
										<td class="tbl_field"><input name="password" id="password" type="password" class="form-control input-lg" required /></td>
									</tr>
									<tr>
										<td class="tbl_label"><label>Password Confirmation </label></td>
										<td class="tbl_field"><input name="password_confirm" id="password_confirm" type="password" class="form-control input-lg" required /></td>
									</tr>
									<tr>
										<td class="tbl_label"><label>Please Enter the Captcha Text </label><i class="fa fa-refresh refresh-captcha"></i> </td>
										<td class="tbl_field">
											<img src="captcha.php" alt="CAPTCHA" class="captcha-image">
										</td>
									</tr>
									<tr>
										<td class="tbl_label"><label></label></td>
										<td class="tbl_field">
											<input type="text" id="captcha" class="form-control input-lg" name="captcha_challenge" pattern="[A-Z]{6}" required>
										</td>
									</tr>
								</table>
								<input type="hidden" name="firstinst" id="firstinst" value="1" />							
								<div class="col-md-12 text-right">
									<!--<button class="btn btn-primary" id = "1streg_submit" onclick="registration(this.form)">Finish</button>-->
									<button class="btn btn-primary" id = "1streg_submit" onclick="requestnewuser(this.form)">Submit</button>
									<button type="reset" class="btn btn-default" onclick="backtab('1streg')">Back</button>
								</div>
						</form>				
						</div>
					</div>
					<div class = "col-md-2"></div>
					<hr>
				</div>
			</div>

			<!-- SMTP SECTION -->
			<div class="panel-body panel-body-index" id="smtpconf_form" style="display:none">
				<div class="first-panel col-md-12">
					<div class = "col-md-2"></div>
					<div class = "description col-md-8">
					
						<div class="col-md-2"></div>
						<div class="col-md-8">						
							<h2 style="margin-bottom:30px">Mail server configuration</h2>
						</div>
						<div class="col-md-2" style="text-align:right; padding: 23px;">
							<button class="btn btn-danger" id = "upload_skip" onclick="abort_install()">Abort</button>
						</div>					

						<?php
							$config = read_json_file("smtp.json");
							$host = $config['host'];
							$port = $config['port'];
							$user = $config['user'];
							$password = $config['password'];
						?>
						
						<form id="smtpconf" class="form-horizontal form-bordered" method="" action="" novalidate = "novalidate">
							<div class="col-auto">
								<table class="smtp_tbl">
									<tr>
										<td class="tbl_label"><label>Host </label></td>
										<td class="tbl_field"><input type="text" id="conf_host" value="<?php echo $host;?>" required /></td>
									</tr>
									<tr>
										<td class="tbl_label"><label>Port </label></td>
										<td class="tbl_field"><input type="number" id="conf_port" value="<?php echo $port;?>" required /></td>
									</tr>								
									<tr>
										<td class="tbl_label"><label>User </label></td>
										<td class="tbl_field"><input type="text" id="conf_user" value="<?php echo $user;?>" required /></td>
									</tr>
									<tr>
										<td class="tbl_label"><label>Password (optional)</label></td>
										<td class="tbl_field"><input type="text" id="conf_pwd" value="<?php echo $password;?>" /></td>
									</tr>								
								</table>
							</div>

						
						</form>
						<div class="col-md-12" style="text-align:right">
							<button class="btn btn-primary" id = "smtpconf_submit" onclick="validate_install('smtpconf')">Submit</button>
							<button type="reset" class="btn btn-default" onclick="backtab('smtpconf')">Back</button>
						</div>
					</div>
					<div class = "col-md-2"></div>
					<hr>
				</div>
			</div>
	
			<!-- UPLOAD SECTION -->
			<div class="panel-body panel-body-index" id="import_bkp" style="display:none">
				<div class="first-panel col-md-12">			
					<div class = "col-md-2"></div>
					<div class = "description col-md-8">
						<div class="col-md-2"></div>
						<div class="col-md-8">						
							<h2 style="margin-bottom:30px">Import Backup (Optional)</h2>
						</div>
						<div class="col-md-2" style="text-align:right; padding: 23px;">
							<button class="btn btn-primary" id = "upload_skip" onclick="skip_upload()">Skip</button>
						</div>
						<div class="col-md-12">
							<p>Upload a data backup from another AIDA version.</p>
							<p><strong>ATTENTION! Backup files not correctly exported could cause SERIOUS APP MALFUNCTIONING</strong></p>
						</div>
						<div class = "col-md-12" style="margin-top:20px">
							<form id="upload-backup" class="form-horizontal" method="" action="">
								<div class="upload-form form-group" id="uploader">
									<div class="col-md-8 col-md-offset-4">
										<div class="fileupload">
											<!-- File List -->
											<div id="filelist" class="uneditable-input bkp-file filelist">
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
				
								<div class="col-md-4 col-md-offset-4" id="import_items" style="display:none">
									<h4 style="margin-left: 15px;">Select Items to import</h4>
									<div class="col-xs-12" id="check_0"><label class="col-xs-10 control-label bkp-label">Users</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_users"/></div></div>
									<div class="col-xs-12" id="check_1"><label class="col-xs-10 control-label bkp-label">Reports</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_reports"/></div></div>            
									<div class="col-xs-12" id="check_2"><label class="col-xs-10 control-label bkp-label">Report Configuration Files</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_repconf"/></div></div>
									<div class="col-xs-12" id="check_3"><label class="col-xs-10 control-label bkp-label">Stored Experiments</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_stored"/></div></div>
									<div class="col-xs-12" id="check_4"><label class="col-xs-10 control-label bkp-label">Systems Configurations</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_sys"/></div></div>
									<div class="col-xs-12" id="check_5"><label class="col-xs-10 control-label bkp-label">History</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_history"/></div></div>    
									<div class="col-xs-12" id="check_6"><label class="col-xs-10 control-label bkp-label">SMTP settings</label><div class="col-xs-2 bkp-input"><input type="checkbox" id="imp_smtp"/></div></div>                
								</div>			


								<div class="form-group" id="hidden-fields">
									<input type="hidden" name="cols" id = "cols" value=""></input>
									<input type="hidden" name="impfile" id = "impfile" value=""></input>
									<input type="hidden" name="nextform" id = "nextform" value=""></input>
								</div>
								
							</form>
							<div class="col-md-12" id="btn-div" style="text-align:right; display:none">
								<button class="btn btn-primary" id = "import-btn">Import</button>
								<button type="reset" class="btn btn-default" onclick="window.location.reload()">Back</button>
							</div>							
						</div>
					</div>
				</div>
			</div>
		</section>
	</div>




<?php include("loader.html"); ?>
<?php include("footer.php"); ?>
<?php include("modalbox.php"); ?>
<!-- Vendor-->
<script>

var refreshButton = document.querySelector(".refresh-captcha");
console.log(refreshButton)
refreshButton.onclick = function() {
  document.querySelector(".captcha-image").src = 'captcha.php?' + Date.now();
}

</script>


<script src="assets/vendor/jquery/jquery.js"></script> 
<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>
<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
<!-- Theme Base, Components and Settings -->
<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
<script src="assets/javascripts/lsst/moment.js"></script>
<script src="assets/javascripts/lsst/moment-timezone.js"></script> 
<script src="assets/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.js"></script>
<!-- File upload -->
<script src="assets/vendor/bootstrap-fileupload/bootstrap-fileupload.min.js"></script>
<!-- Form validation -->
<script src="assets/vendor/jquery-validation/jquery.validate.js"></script>

<!-- IOT -->
<script src="assets/javascripts/lsst/forms.js"></script>  
<script src="assets/javascripts/lsst/validation.js"></script>
<script src="assets/javascripts/lsst/jqscripts.js"></script> 



<script src="assets/javascripts/theme.js"></script>
<!-- Theme Custom -->
<script src="assets/javascripts/theme.custom.js"></script>
<!-- Theme Initialization Files -->
<script src="assets/javascripts/theme.init.js"></script>
<!-- File Upload -->
<script src="assets/javascripts/lsst/jquery-progressbar.min.js"></script> 
<script src="assets/vendor/plupload/js/plupload.full.min.js"></script>
<script src="assets/javascripts/lsst/install.js"></script>