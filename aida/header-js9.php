<?php
	if(isset($_GET['error'])){
		exit("<script type='text/javascript'>alert('Error Logging In! Please retry');
								window.location.href='index.php';
								</script>");
	}
	include('functions.php');
	#include("config.php");
	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	$dash="dashboard.php";	
	$mysqli = new mysqli($host, $user, $password, $dbname);
	sec_session_start();
	$homeurl = 'index.php';                               
	$homepage = "";
	$path = $_SERVER['REQUEST_URI'];
	$current_array = explode("/", $path);
	$currentpage = end($current_array);
	$check = login_check($mysqli);
	if ($currentpage == $homepage or $currentpage == $homeurl){
		$ishome=true;
	}else{$ishome = false;}

	// for debug: $check = true
	if($check== true or $ishome==true) {?>
 

 
	<head>

		<!-- Basic -->
		<meta charset="UTF-8">

		<title>RUBIN LSST - AIDA</title>
		<meta name="keywords" content="HTML5 Admin Template" />
		<meta name="description" content="RUBIN LSST - AIDA">
		<meta name="author" content="LSST">

		<!-- Mobile Metas -->
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
		<link rel="icon" href="assets/images/logo_aida.png">
        <!--link rel="icon" href="assets/images/left_smallLogoAIDA.png">-->
		<!-- Web Fonts  -->
		<link href="http://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700,800|Shadows+Into+Light" rel="stylesheet" type="text/css">

		<!-- Vendor CSS -->
		<link rel="stylesheet" href="assets/vendor/bootstrap/css/bootstrap.css" />
		<link rel="stylesheet" href="assets/vendor/font-awesome/4.7/css/font-awesome.min.css">
		<!--<link rel="stylesheet" href="assets/vendor/font-awesome/css/font-awesome.css" />-->
		<link rel="stylesheet" href="assets/vendor/magnific-popup/magnific-popup.css" />
		<link rel="stylesheet" href="assets/vendor/bootstrap-datepicker/css/datepicker3.css" />

		<!-- Specific Page Vendor CSS -->
		<link rel="stylesheet" href="assets/vendor/jquery-ui/css/ui-lightness/jquery-ui-1.10.4.custom.css" />
		<link rel="stylesheet" href="assets/vendor/select2/select2.css" />
		<link rel="stylesheet" href="assets/vendor/bootstrap-multiselect/bootstrap-multiselect.css" />
		<link rel="stylesheet" href="assets/vendor/morris/morris.css" />
		<link rel="stylesheet" href="assets/vendor/bootstrap-tagsinput/bootstrap-tagsinput.css" />
		<link rel="stylesheet" href="assets/vendor/bootstrap-colorpicker/css/bootstrap-colorpicker.css" />
		<link rel="stylesheet" href="assets/vendor/bootstrap-timepicker/css/bootstrap-timepicker.css" />
		<link rel="stylesheet" href="assets/vendor/dropzone/css/basic.css" />
		<link rel="stylesheet" href="assets/vendor/dropzone/css/dropzone.css" />
		<link rel="stylesheet" href="assets/vendor/bootstrap-markdown/css/bootstrap-markdown.min.css" />
		<link rel="stylesheet" href="assets/vendor/summernote/summernote.css" />
		<link rel="stylesheet" href="assets/vendor/summernote/summernote-bs3.css" />
		<link rel="stylesheet" href="assets/vendor/codemirror/lib/codemirror.css" />
		<link rel="stylesheet" href="assets/vendor/codemirror/theme/monokai.css" />
		<link rel="stylesheet" href="assets/vendor/jstree/themes/default/style.css" />
		<!-- Tables CSS -->
      	<link rel="stylesheet" href="assets/vendor/DataTables/datatables.min.css" />		
		<!-- Theme CSS -->
		<link rel="stylesheet" href="assets/stylesheets/theme.css" />
      
		<!-- Theme Custom CSS -->
		<link rel="stylesheet" href="assets/stylesheets/theme-custom.css">
		<!-- Skin CSS -->
		<link rel="stylesheet" href="assets/stylesheets/skins/default.css" />


		<!-- JS9  -->
<script src="assets/javascripts/lsst/fits.js" type="text/javascript" charset="utf-8"></script>
    
<script type="text/javascript">
  var FITS = astro.FITS;
</script>	
  <link type="text/css" rel="stylesheet" href="js9/js9support.css">
  <link type="text/css" rel="stylesheet" href="js9/js9.css">
  <link rel="apple-touch-icon" href="js9/images/js9-apple-touch-icon.png">
  <script type="text/javascript" src="js9/js9prefs.js"></script>
  <script type="text/javascript" src="js9/js9support.js"></script>
	<!--<script type="text/javascript" src="js9/js9.js"></script>-->
  <!--<script type="text/javascript" src="js9/js9support.min.js">-->
  <!--<script type="text/javascript" src="js9/js9.min.js"></script>-->
  <script type="text/javascript" src="js9/js9.js"></script>
  
  <script type="text/javascript" src="js9/js9plugins.js"></script>

      <!-- JS9 IOT CUSTOM -->
      <link rel="stylesheet" href="assets/stylesheets/js9_custom.css" />


		<!-- Head Libs -->
		<script src="assets/vendor/modernizr/modernizr.js"></script>


	<!-- Specific Page Vendor -->
		<script src="assets/vendor/select2/select2.js"></script>
		<script src="assets/vendor/jquery-datatables/media/js/jquery.dataTables.js"></script>
		<script src="assets/vendor/jquery-datatables/extras/TableTools/js/dataTables.tableTools.min.js"></script>
  		<script src="assets/vendor/DataTables/datatables.min.js"></script>
		
	
 
<script src="assets/javascripts/lsst/image-explorer.js"></script>

		<!-- Vendor
		<script src="assets/vendor/jquery/jquery.js"></script> -->
		<script src="assets/vendor/jquery-validation/jquery.validate.js"></script>  
		<!--<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>-->
		<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
		<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
		<!-- Specific Page Vendor -->
		<script src="assets/vendor/jstree/jstree.js"></script>


		
		<!-- LSST Libs -->
		<!--<script src="scripts/echarts.min.js"></script>-->
		<script src="assets/javascripts/lsst/plotly-latest.min.js"></script>
		<script src="assets/javascripts/lsst/iot.js"></script>
		
		<!-- Login libs -->
		<script type="text/javascript" src="assets/javascripts/lsst/sha512.js"></script>
		<script type="text/javascript" src="assets/javascripts/lsst/forms.js"></script>
		<script src="assets/javascripts/lsst/html2canvas.min.js"></script>		

	</head>
	<body>

		<section class="body">

			<!-- start: header -->
			<header class="header">
				<div class="logo-container">
					<a class="logo">
						<div class="logo-img"><img src="assets/images/logo_aida.png" height="100" alt="" /></div>
						<div class="logo-title"><p class="title">AIDA</p><span class="tagline">Advanced Infrastructure for Data Analysis</span></div>
						<div class="lsst-img"><img src="assets/images/logo_aida.png" height="100" alt="" /></div>
					</a>
				</div>
			

			</header>
			<!-- end: header -->

			<div class="inner-wrapper">
			<?php   
				if($ishome==false){
				echo '<section role="main" class="content-body nodash">
				<header class="page-header nodash">
					<h2>'.$title.'</h2>
					<div class="right-wrapper pull-right">
					</div>';
					include("login.php");
					echo '</header>';
				} else {
						echo '<section role="main" class="content-body-index">';
						echo '<header class="page-header page-header-index">';
						include("login.php");
						echo "</header>";
				}
			?>
			
<?php
} else {
   header("location: not-logged.php");
}?>