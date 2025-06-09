<!doctype html>
<html class="fixed">

<?php
// redirect to installation if not yet done
if (!file_exists("users/ready.log")) {	
    include("install.php");
} else {
?>
	
<head>
	<!-- Basic -->
	<meta charset="UTF-8">

	<title>RUBIN LSST - AIDA</title>
	<meta name="keywords" content="HTML5 Admin Template" />
	<meta name="description" content="RUBIN LSST - AIDA">
	<meta name="author" content="RUBIN LSST">

	<!-- Mobile Metas -->
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />

	<!-- Web Fonts  -->
	<link href="http://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700,800|Shadows+Into+Light" rel="stylesheet" type="text/css">

	<!-- Vendor CSS -->
	<link rel="stylesheet" href="assets/vendor/bootstrap/css/bootstrap.css" />
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	<link rel="stylesheet" href="assets/vendor/magnific-popup/magnific-popup.css" />
	<link rel="stylesheet" href="assets/vendor/bootstrap-datetimepicker/css/bootstrap-datetimepicker.css" />

	<!-- Specific Page Vendor CSS -->
	<link rel="stylesheet" href="assets/vendor/jquery-ui/css/ui-lightness/jquery-ui-1.10.4.custom.css" />
	<link rel="stylesheet" href="assets/vendor/select2/select2.css" />
	<link rel="stylesheet" href="assets/vendor/bootstrap-multiselect/bootstrap-multiselect.css" />
	<link rel="stylesheet" href="assets/vendor/morris/morris.css" />
	<link rel="stylesheet" href="assets/vendor/bootstrap-tagsinput/bootstrap-tagsinput.css" />
	<link rel="stylesheet" href="assets/vendor/bootstrap-colorpicker/css/bootstrap-colorpicker.css" />
	<!--<link rel="stylesheet" href="assets/vendor/bootstrap-timepicker/css/bootstrap-timepicker.css" />-->
	<link rel="stylesheet" href="assets/vendor/dropzone/css/basic.css" />
	<link rel="stylesheet" href="assets/vendor/dropzone/css/dropzone.css" />
	<link rel="stylesheet" href="assets/vendor/bootstrap-markdown/css/bootstrap-markdown.min.css" />
	<link rel="stylesheet" href="assets/vendor/summernote/summernote.css" />
	<link rel="stylesheet" href="assets/vendor/summernote/summernote-bs3.css" />
	<link rel="stylesheet" href="assets/vendor/codemirror/lib/codemirror.css" />
	<link rel="stylesheet" href="assets/vendor/codemirror/theme/monokai.css" />
	<link rel="stylesheet" href="assets/vendor/jstree/themes/default/style.css" />
	<!-- Tables CSS -->
	<link rel="stylesheet" href="assets/vendor/select2/select2.css" />
	
	<!-- File Upload CSS -->
	<link rel="stylesheet" href="assets/vendor/bootstrap-fileupload/bootstrap-fileupload.min.css" />
	
	<!-- Theme CSS -->
	<link rel="stylesheet" href="assets/stylesheets/theme.css" />

	<!-- Skin CSS -->
	<link rel="stylesheet" href="assets/stylesheets/skins/default.css" />

	<!-- Theme Custom CSS -->
	<link rel="stylesheet" href="assets/stylesheets/theme-custom.css">

	<!-- Head Libs -->
	<script src="assets/vendor/modernizr/modernizr.js"></script>

	<!-- lsst Libs -->
	<script src="assets/javascripts/lsst/FileSaver.js"></script>
	<script src="assets/javascripts/lsst/plotly-latest.min.js"></script>
	<script src="assets/javascripts/lsst/iot.js"></script>
	
	<!-- Login libs -->
	<script type="text/javascript" src="assets/javascripts/lsst/sha512.js"></script>
	<script type="text/javascript" src="assets/javascripts/lsst/forms.js"></script>
	
 
	</head>
	<body>
		<section class="body">

			<!-- start: header -->
			<header class="header">
				<div class="logo-container">
					<a href="index.php" class="logo">
						<div class="logo-img"><img src="assets/images/logo_aida.png" height="100" alt="" /></div>
						<div class="logo-title"><p class="title">AIDA</p><span class="tagline">Advanced Infrastructure for Data Analysis
						</span></div>
						<div class="lsst-img"><img src="assets/images/lsst_logonew.png" height="100" alt="" /></div>
					</a>
				</div>
			</header>
			<!-- end: header -->

			<div class="inner-wrapper">
			<?php   
				$check = false;
				echo '<section role="main" class="content-body-index">';
				echo '<header class="page-header page-header-index">';
				include("login.php");
				echo "</header>";
				
			?>
				<div class="row">
					<div class="col-md-12">
							<div class="panel-body panel-body-index">
								<div class="col-md-12" style="margin-top:200px;">
									<div class = "col-md-2"></div>
									<div class = "description col-md-8">
										<h2>You are not authorized to access this page!</h2>
										<p>Please login or <a href="signup.html">submit your registration request </a></p>
									</div>
									<div class = "col-md-2"></div>
								</div>
							

							</div>
						</section>
					</div>
					
				</div>
			</div>
					<!-- end: page -->
		</section>
	<footer class = "page-footer">
			<div class = "col-md-2"></div>
			<div class = "col-md-2">
				<h3>Useful Links</h3>
				<ul>
					<li><a href="https://rubinobservatory.org/" target="_blank">Rubin-LSST Official</a></li>
					<li><a href="https://www.lsst.org/scientists/in-kind-program" target="_blank">Rubin-LSST In-Kind Program</a></li>
					<li><a href="https://rubinobservatory.org/for-scientists/resources/community-forum" target="_blank">Rubin Community Forum</a></li>
					<li><a href="https://www.inaf.it/" target="_blank">INAF</a></li>
				</ul>
			</div>
			<div class = "col-md-4 logodiv">
				<h3>AIDA is a Rubin - LSST project for monitoring, analysis & visualization</h3>
				<div class="logos">
					<img src="assets/images/INAF_logo.png" height="100" alt="">
					<img src="assets/images/vera.png" height="100" alt="">
                    <img src="assets/images/lsstred.png" height="100" alt="">
				</div>
			</div>
			<div class = "col-md-2">
				<h3>Credits & Contacts</h3>
				<p>For infos and technical support:</p>
				<ul>
					<li><a href="mailto://giuseppe.riccio@inaf.it">G. Riccio - giuseppe.riccio@inaf.it</a></li>
					<li><a href="mailto://massimo.brescia@inaf.it">M. Brescia - massimo.brescia@inaf.it</a></li>
					<li><a href="mailto://stefano.cavuoti@gmail.com">S. Cavuoti - stefano.cavuoti@gmail.com</a></li>
				</ul>
			</div>
			<div class = "col-md-2"></div>

		</footer>
			<!-- Vendor-->
		<script src="assets/vendor/jquery/jquery.js"></script> 
		<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>
		<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
		<!-- Theme Base, Components and Settings -->
		<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>  
		<script src="assets/javascripts/theme.js"></script>
		<!-- Theme Custom -->
		<script src="assets/javascripts/theme.custom.js"></script>
		<!-- Theme Initialization Files -->
		<script src="assets/javascripts/theme.init.js"></script>
  
        <script>  
          $("#password").keypress(function(event) { 
              if (event.keyCode === 13) { 
                  $("#loginbtn").click(); 
              } 
          }); 
     	 </script> 
		 
	</body>
	
</html>
<?php } ?>