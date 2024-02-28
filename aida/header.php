<?php
	if(isset($_GET['error'])){
		exit("<script type='text/javascript'>alert('Error Logging In! Please retry');
								window.location.href='index.php';
								</script>");
	}
	if(!@include_once('functions.php')) {
		include('functions.php');	
	}	
	
	#include("config.php");
	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	
	$mysqli = new mysqli($host, $user, $password, $dbname)
	or die ('Could not connect to the database server' . mysqli_connect_error());;
	sec_session_start();
	$homeurl = 'index.php';                               
	$homepage = "";
	$dash="dashboard.php";
	$path = $_SERVER['REQUEST_URI'];
	$current_array = explode("/", $path);
	$currentpage = end($current_array);
	$check = login_check($mysqli);

	if ($currentpage == $homepage or $currentpage == $homeurl){
		$ishome=true;
	}else{$ishome = false;}

	// for debug: $check = true
	if($check== true or $ishome==true) {
 
			include("header.html");
				if($ishome==false){
					if ($currentpage == $dash){
						include("sidebar.php");
						$dashcls = "";

					}
					else
					{
						$dashcls = "nodash";
					}


					echo '<section role="main" class="content-body '.$dashcls.'">
					<header class="page-header '.$dashcls.'">
						<h2 id="plot-title">'.$title.'</h2>
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
      
   $current =  explode("?", $currentpage);  
   if($current[0]!="view_plot.php"){   
   		header("location: not-logged.php");
   }
   else{
		include("header.html");     
     
     
     
     
     
     
   		$tolog = 1; 
   }
}?>