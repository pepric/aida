<!doctype html>
<html class="fixed">
	<head>

		<!-- Basic -->
		<meta charset="UTF-8">

		<title>RUBIN LSST - Password Recovery</title>
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
					<img src="assets/images/vera.png" height="70" alt="RUBIN LSST Password Recovery" />
				</a>

				<div class="panel panel-sign">
					<div class="panel-title-sign mt-xl text-right">
						<h2 class="title text-uppercase text-bold m-none"><i class="fa fa-user mr-xs"></i> Password Recovery</h2>
					</div>
					<div class="panel-body">
                      	<?php
                      		if (isset($_GET["key"]) && isset($_GET["email"]) && isset($_GET["action"]) && ($_GET["action"]=="reset") && !isset($_POST["action"])){
                      			include("functions.php");
                      			$recform = recovery_form($_GET["email"], $_GET["key"]);
                              	echo $recform;
                            }
                      		else{
                      	?>
                              
						<form method="post" id="resetform" name="resetform" action="" novalidate = "novalidate"><!--action="register.php"-->
							<div class="form-group mb-lg">
								<label class="col-xs-4 signup-form">Your E-mail Address</label>
								<input name="email" id="email" type="email" class="form-control input-lg" required />
							</div>
							<div class="row">
								<div class="col-sm-12 text-right">
                                  	<button type="button" id="resetpwd" class="btn btn-primary" onclick="sendreset();">Reset Password</button>
                                  	<button type="button" id="abort" class="btn btn-primary" onclick="window.location.href='index.php';">Back</button>
								</div>
							</div>
						</form>
                      	<?php } ?>
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
			// initialize the validator
			$('#resetform').validate({
			
				highlight: function(element) {
					$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
				},
				success: function(element) {
					$(element).closest('.form-group').removeClass('has-error');
				},
				
				
			});
			// initialize the validator
			$('#updatepwd').validate({
			
				rules : {
					pass1 : {
						pwcheck : true,
						minlength : 8
					},
					pass2 : {
						equalTo : "#pass1"
					}
				},
				
				messages : {
					pass1: {
						pwcheck: "An upper case letter and a digit required",
						minlength: "At least 8 characters required"
					},
				},
			
				highlight: function(element) {
					$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
				},
				success: function(element) {
					$(element).closest('.form-group').removeClass('has-error');
				},
				
				
			});
			
			$.validator.addMethod("pwcheck", function(value) {
				return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) // consists of only these
				&& /[A-Z]/.test(value) // has a lowercase letter
				&& /\d/.test(value) // has a digit
			});		
	
		});
		</script>


	</body>
</html>