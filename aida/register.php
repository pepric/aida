<?php
/* Namespace alias. 
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;*/

include ('functions.php');
require("PHPMailer/src/PHPMailer.php");
require("PHPMailer/src/SMTP.php");
require("PHPMailer/src/Exception.php");
session_start();

if(isset($_POST['captcha_challenge']) && $_POST['captcha_challenge'] == $_SESSION['captcha_text']) {

  #include("config.php");
  $config = read_config_json("config.json");
  $host = $config['host'];
  $user = $config['user'];
  $password = $config['password'];
  $dbname = $config['dbname'];
  $mail_admin = read_admin_json("config.json");


  $mysqli = new mysqli($host, $user, $password, $dbname) 
  or die ('Could not connect to the database server' . mysqli_connect_error());
  $username = str_replace(" ","",$_POST['name']);
  $email = $_POST['email'];
  $role = $_POST['role'];
  $install = $_POST['install'];
  //CHECK USER EXISTING IN DB
  $existmail = check_exist($mysqli, $email, 'email');
  $existuser = check_exist($mysqli, $username, 'username');
  $exist = $existmail || $existuser;


  if($exist == true){
      $error = 1;
  }
  else{
      $error = 0;
      // Get crypted password.
      $password = $_POST['p'];

      // Create random key
      $random_salt = hash('sha512', uniqid(mt_rand(1, mt_getrandmax()), true));
      // Create password with hash key.
      $password = hash('sha512', $password.$random_salt);

      //Request date
      $current_date = gmdate("Y-m-d H:i:s");
      // Insert data in DB
	  if($install==0){
      	if ($insert_stmt = $mysqli->prepare("INSERT INTO members (username, email, password, salt, role, action_date) VALUES (?, ?, ?, ?, ?, ?)")) {    
        	  $insert_stmt->bind_param('ssssss', $username, $email, $password, $random_salt, $role, $current_date); 
          	// Query execution
          	$insert_stmt->execute();
      	}
      	else {$error=2;}
      }
      else{
		//purge table
		$trunc_members = $mysqli->prepare("TRUNCATE TABLE members");
		$trunc_members->execute();  
      	if ($insert_stmt = $mysqli->prepare("INSERT INTO members (username, email, password, salt, role, active, action_date) VALUES (?, ?, ?, ?, ?, ?, ?)")) { 
          	//$active = 1;
			$active = 0;
          	$role = "admin";
        	  $insert_stmt->bind_param('sssssis', $username, $email, $password, $random_salt, $role, $active, $current_date); 
          	// Query execution
          	$insert_stmt->execute();
      	}
      	else {$error=2;}      
      
      }

      if($error==0){
          if($install == 0){
            // SEND MAIL TO ADMIN
            $err_admin = send_admin_email($username, $email, $mail_admin, $role);
            // SEND MAIL TO USER
            $err_user = send_user_email($username, $email, $mail_admin);
            $error_send = $err_admin || $err_user;
          	if($error_send == 1){$error = 3;}
          }
          else{
			$confemail = $_POST['confem'];  
			//send activation email  
            $error_send = send_activation_email($username, $email, $confemail);
            //remove install file
          	//unlink(".install");
          }
      }

  }
  mysqli_close($mysqli);
}
else{$error = 4;}
echo $error;

function send_activation_email($username, $email, $notifemail){
	
	$configmail = read_json_file("smtp.json");
	$host = $configmail['host'];
	$port = $configmail['port'];
	$user = $configmail['user'];
	$pwd = $configmail['password'];
	

	$protocol = isset($_SERVER["HTTPS"]) ? 'https' : 'http';
	$www_arr = explode("/", $_SERVER['PHP_SELF']);
	array_pop($www_arr);
	$path = implode($www_arr);

	$address = $protocol."://".$_SERVER['SERVER_NAME'].":".$_SERVER['SERVER_PORT']."/".$path;	

	
	// subject and message
	$subject = "AIDA Account Confirmation";
	$msg = "<p>Dear ".$username.",<br/> your registration has been submitted. Please, confirm to activate your Admin account by clicking  <a href='".$address."/index.php?user=".$username."&email=".$notifemail."&confirm=1'>here</a>.</p><p>The IOT</p>";

	/* Create a new PHPMailer object. Passing TRUE to the constructor enables exceptions. */
	/* $mail = new PHPMailer(TRUE); */
	$mail = new PHPMailer\PHPMailer\PHPMailer();

/* Open the try/catch block. */
	$error = 0;
//	try {
		$mail->IsSMTP();
		
						//Enable SMTP debugging
		// 0 = off (for production use)
		// 1 = client messages
		// 2 = client and server messages
		$mail->SMTPDebug = 0;
		//Ask for HTML-friendly debug output
		$mail->Debugoutput = 'html';
				
		
		/***** TEMPORARY SOLUTION FOR SMTP ERROR****/
		$mail->SMTPOptions = array(
			'ssl' => array(
				'verify_peer' => false,
				'verify_peer_name' => false,
				'allow_self_signed' => true
			)
		);
		/*********************************************/
		if($pwd==""){
			$mail->SMTPAuth = false; // SMTP Authentication
        }
		else{
			$mail->SMTPAuth = true; // SMTP Authentication
		}      
		$mail->Host = $host;
		$mail->Port = $port;
		$mail->SMTPSecure = 'tls';
		$mail->IsHTML(true); 
		$mail->Username = $user; // SMTP user
		$mail->Password = $pwd; // email account Password
		
		/*!!!NOTE: GMAIL require to enable unsecure apps*/
					
					
	   /* Set the mail sender. */
	   $mail->setFrom($user, "AIDA webapp");

	   /* Add a recipient. */
	   $mail->addAddress($email, $username);

	   /* Set the subject. */
	   $mail->Subject = $subject;

	   /* Set the mail message body. */
	   $mail->Body = $msg;

	   /* Finally send the mail. */
	   $mail->send();
	
	return $error;

}


function send_admin_email($username, $email, $mail_admin, $role){
	
/* 	require(".\PHPMailer\src\Exception.php");
	require(".\PHPMailer\src\PHPMailer.php");
	require(".\PHPMailer\src\SMTP.php"); */

	$configmail = read_json_file("smtp.json");
	$host = $configmail['host'];
	$port = $configmail['port'];
	$user = $configmail['user'];
	$pwd = $configmail['password'];
	
	
	// subject and body
	$subject = "New Registration Request on AIDA";
	$msg = "<p>A new user requested registration in AIDA web app. Please activate user in the DB if authorized.<p><p>Name: ".$username."</p><p>Email: ".$email."</p><p>Role: ".$role."</p>";

	/* Create a new PHPMailer object. Passing TRUE to the constructor enables exceptions. */
	/* $mail = new PHPMailer(TRUE); */
	$mail = new PHPMailer\PHPMailer\PHPMailer();

/* Open the try/catch block. */
	$error = 0;
	try {
		$mail->IsSMTP(); 
		
		//Enable SMTP debugging
		// 0 = off (for production use)
		// 1 = client messages
		// 2 = client and server messages
		$mail->SMTPDebug = 0;
		//Ask for HTML-friendly debug output
		$mail->Debugoutput = 'html';
				
		
		/***** TEMPORARY SOLUTION FOR SMTP ERROR****/
		$mail->SMTPOptions = array(
			'ssl' => array(
				'verify_peer' => false,
				'verify_peer_name' => false,
				'allow_self_signed' => true
			)
		);
		/*********************************************/
		if($pwd==""){
			$mail->SMTPAuth = false; // Autenticazione SMTP
        }
		else{
			$mail->SMTPAuth = true; // Autenticazione SMTP
		}      
		$mail->Host = $host;
		$mail->Port = $port;
		$mail->SMTPSecure = 'tls';
		$mail->IsHTML(true); 
		$mail->Username = $user;
		$mail->Password = $pwd;
		
		/*!!!NOTE: GMAIL requires to enable unsecure apps*/
					
					
	   /* Set the mail sender. */
	   $mail->setFrom($user, "AIDA webapp");

	   /* Add a recipient. */
	   $mail->addAddress($mail_admin, 'AIDA admin');

	   /* Set the subject. */
	   $mail->Subject = $subject;

	   /* Set the mail message body. */
	   $mail->Body = $msg;

	   /* Finally send the mail. */
	   $mail->send();

	}
	catch (Exception $e)
	{
	   /* PHPMailer exception. */
	   //echo $e->errorMessage();

	   $error = 1;

	}
	catch (\Exception $e)
	{
	   /* PHP exception (note the backslash to select the global namespace Exception class). */
	   //echo $e->getMessage();

	   $error = 1;
	}
	
	return $error;

}

function send_user_email($username, $email, $mail_admin){
	
	$configmail = read_json_file("smtp.json");
	$host = $configmail['host'];
	$port = $configmail['port'];
	$user = $configmail['user'];
	$pwd = $configmail['password'];
	
	// subject and body
	$subject = "New Registration Request on RUBIN LSST";
	$msg = "<p>Dear User,<br/> your registration request has been submitted. You will receive the confirm of your activation as soon as possible.</p><p>The IOT</p>";

	/* Create a new PHPMailer object. Passing TRUE to the constructor enables exceptions. */
	/* $mail = new PHPMailer(TRUE); */
	$mail = new PHPMailer\PHPMailer\PHPMailer();

/* Open the try/catch block. */
	$error = 0;
	try {
		$mail->IsSMTP(); 
		
		//Enable SMTP debugging
		// 0 = off (for production use)
		// 1 = client messages
		// 2 = client and server messages
		$mail->SMTPDebug = 0;
		//Ask for HTML-friendly debug output
		$mail->Debugoutput = 'html';
				
		
		/***** TEMPORARY SOLUTION FOR SMTP ERROR****/
		$mail->SMTPOptions = array(
			'ssl' => array(
				'verify_peer' => false,
				'verify_peer_name' => false,
				'allow_self_signed' => true
			)
		);
		/*********************************************/
		
		if($pwd==""){
			$mail->SMTPAuth = false;
        }
		else{
			$mail->SMTPAuth = true;
		} 
		$mail->Host = $host;
		$mail->Port = $port;
		$mail->SMTPSecure = 'tls';
		$mail->IsHTML(true); 
		$mail->Username = $user;
		$mail->Password = $pwd;
		
		/*!!!NOTE: GMAIL require to enable unsecure apps*/
					
					
	   /* Set the mail sender. */
	   /*$mail->setFrom($mail_admin, "AIDA admin");*/
		$mail->setFrom($user, "AIDA admin");

	   /* Add a recipient. */
	   $mail->addAddress($email, $username);

	   /* Set the subject. */
	   $mail->Subject = $subject;

	   /* Set the mail message body. */
	   $mail->Body = $msg;

	   /* Finally send the mail. */
	   $mail->send();
	}
	catch (Exception $e)
	{
	   $error = 1;
	}
	catch (\Exception $e)
	{
	   /* PHP exception (note the backslash to select the global namespace Exception class). */
	   $error = 1;
	}
	
	return $error;
}

function check_exist($con, $val, $col){
	//query
	
	$sql="SELECT * FROM members WHERE $col = '".$val."'";
	$result = $con -> query($sql);
	
	if (!$result = $con->query($sql)) {
		// Oh no! The query failed. 
		echo "Sorry, the web application is experiencing problems.";

		// Again, do not do this on a public site, but we'll show you how
		// to get the error information
		echo "Error: Our query failed to execute and here is why: \n";
		echo "Query: " . $sql . "\n";
		echo "Errno: " . $con->errno . "\n";
		echo "Error: " . $con->error . "\n";
		exit;
	}

	if ($result->num_rows === 0){
	    $exist = false;
	}
	else
	{
		$exist = true;
	}
	
	return $exist;
}

?>