<?php
	include('functions.php');
	#include("config.php");
	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	sec_session_start();
	// Save logout event in DB
	$mysqli = new mysqli($host, $user, $password, $dbname);
	$username = $_SESSION['username'];
	$current_date = gmdate("Y-m-d H:i:s");
	//history table
	update_history($username, 'Logout' , 'NA', 'NA', 'NA');
	
	//users table
	$mysqli->query("UPDATE members SET last_logout = '".$current_date."' WHERE username= '".$username."'");
	
	// Remove temporary local files
	$mysqli->query("DELETE FROM local_files WHERE username='$username'");
	$mysqli->query("DELETE FROM stored_plots WHERE (username='$username' AND tokeep=0)");
	empty_dir($username);
	
	// Remove files in tmp directory
	$files = preg_grep('~^'.$username.'.*~', scandir("tmp"));
	foreach($files as $file){
		if(is_file("tmp/".$file)){
			unlink("tmp/".$file);
		}			
	}

// Destroy session
	$_SESSION = array();
	// Get session parameters
	$params = session_get_cookie_params();
	// Delete current cookies
	setcookie(session_name(), '', time() - 42000, $params["path"], $params["domain"], $params["secure"], $params["httponly"]);
	// Delete session
	session_destroy();
	header('Location: ./');
?>