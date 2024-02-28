<!doctype html>

<?php
	if(file_exists(".install")){
		$firstinst = 1;
	}
    else{
    	$firstinst = 0;
    }


?>



<html class="fixed">
	<head>

		<!-- Basic -->
		<meta charset="UTF-8">

		<title>RUBIN LSST - User Registration</title>
		<meta name="keywords" content="HTML5 Admin Template" />
		<meta name="description" content="Porto Admin - Responsive HTML5 Template">
		<meta name="author" content="okler.net">

		<!-- Mobile Metas -->
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />

		<!-- Web Fonts  -->
		<link href="http://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700,800|Shadows+Into+Light" rel="stylesheet" type="text/css">

		<!-- Vendor CSS -->
		<link rel="stylesheet" href="assets/vendor/bootstrap/css/bootstrap.css" />
		<link rel="stylesheet" href="assets/vendor/font-awesome/css/font-awesome.css" />
		<link rel="stylesheet" href="assets/vendor/magnific-popup/magnific-popup.css" />
		<link rel="stylesheet" href="assets/vendor/bootstrap-datepicker/css/datepicker3.css" />

		<!-- Theme CSS -->
		<link rel="stylesheet" href="assets/stylesheets/theme.css" />

		<!-- Skin CSS -->
		<link rel="stylesheet" href="assets/stylesheets/skins/default.css" />

		<!-- Theme Custom CSS -->
		<link rel="stylesheet" href="assets/stylesheets/theme-custom.css">

		<!-- Head Libs -->
		<script src="assets/vendor/modernizr/modernizr.js"></script>
	
	
		<!-- Login libs -->
		<script type="text/javascript" src="assets/javascripts/lsst/sha512.js"></script>
		<script type="text/javascript" src="assets/javascripts/lsst/forms.js"></script>
				

	</head>
	<body>
		<!-- start: page -->
		<section class="body-sign">
			<div class="center-sign">
				<a href="index.php" class="logo pull-left">
					<img src="assets/images/vera.png" height="70" alt="RUBIN LSST Registration" />
				</a>

				<div class="panel panel-sign">
					<div class="panel-title-sign mt-xl text-right">
						<h2 class="title text-uppercase text-bold m-none"><i class="fa fa-user mr-xs"></i> Sign Up</h2>
					</div>
					<div class="panel-body">
						<form method="post" id="signupform" name="signupform" action="" novalidate = "novalidate"><!--action="register.php"-->
							<div class="form-group mb-lg">
								<label class="col-xs-4 signup-form">Name</label>
								<input name="name" id="name" type="text" class="form-control input-lg" required />
							</div>

							<div class="form-group mb-lg">
								<label class="col-xs-4 signup-form">E-mail Address</label>
								<input name="email" id="email" type="email" class="form-control input-lg" required />
							</div>
							
							<div class="form-group mb-lg">
								<label class="col-xs-4 signup-form">Role</label>
                              
                              	<?php if($firstinst==0){?>
									<select name="role" id="role" class="form-control input-lg" style="width:57%" required />
										<option value="user">User</option>
										<option value="admin">Administrator</option>
									</select>
                          		<?php }else{ ?>
                          			<input name="role" id="role" type="text" value="Administrator" class="form-control input-lg" disabled selected/>
                          		<?php } ?>
							</div>

							<div class="form-group mb-none">
								<div class="row">
									<div class="col-sm-12 mb-lg">
										<label class="col-xs-4 signup-form">Password</label>
										<input name="password" id="password" type="password" class="form-control input-lg" required />
									</div>
								</div>
							</div>
							
							<div class="form-group mb-none">
								<div class="row">
									<div class="col-sm-12 mb-lg">
										<label class="col-xs-4 signup-form" style="padding-top:0px">Password Confirmation</label>
										<input name="password_confirm" id="password_confirm" type="password" class="form-control input-lg" required />
									</div>
								</div>
							</div>
                            <div class="form-group mb-lg">
                              <label for="captcha">Please Enter the Captcha Text</label><i class="fa fa-refresh refresh-captcha"></i><br>
                                <img src="captcha.php" alt="CAPTCHA" class="captcha-image">
                                <input type="text" id="captcha" name="captcha_challenge" pattern="[A-Z]{6}" required>
                            </div>
                      		<input type="hidden" name="firstinst" id="firstinst" value="<?php echo $firstinst;?>" />
							<div class="row">
								<div class="col-sm-12 text-right">
									<button type="button" id="signup" class="btn btn-primary" onclick="requestnewuser(this.form);">Sign Up</button>
								</div>
							</div>

						</form>
					</div>
					<div id="loader" style="display:none"><img src="assets/images/loading_blue.gif" /></div>
				</div>

			</div>
		</section>
		<!-- end: page -->

		<!-- Vendor -->
		<script src="assets/vendor/jquery/jquery.js"></script>
		<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>
		<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
		<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
		<script src="assets/vendor/bootstrap-datepicker/js/bootstrap-datepicker.js"></script>
		<script src="assets/vendor/magnific-popup/magnific-popup.js"></script>
		<script src="assets/vendor/jquery-placeholder/jquery.placeholder.js"></script>
		<!-- IOT -->
 
		<script src="assets/javascripts/lsst/validation.js"></script>
	

		<!-- Form validation -->
		<script src="assets/vendor/jquery-validation/jquery.validate.js"></script>
		<!-- Theme Base, Components and Settings -->
		<script src="assets/javascripts/theme.js"></script>
		
		<!-- Theme Custom -->
		<script src="assets/javascripts/theme.custom.js"></script>
		
		<!-- Theme Initialization Files -->
		<script src="assets/javascripts/theme.init.js"></script>

		<script>
			$(document).ready(function() {          
				var refreshButton = document.querySelector(".refresh-captcha");
				refreshButton.onclick = function() {
				  document.querySelector(".captcha-image").src = 'captcha.php?' + Date.now();
				}
			});
		</script>
	</body>
</html>