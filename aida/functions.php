<?php
if(isset($_POST['action']) && !empty($_POST['action'])) {
    $action = $_POST['action'];
    switch($action) {
		case 'build_options' : {
        	$source = $_POST['source'];
			$usecase = $_POST['usecase'];
			$opmode = $_POST['opmode'];
        	$idx = 	$_POST['idx'];
        	$filename = $_POST['filename'];
         	$res = build_options($source,$usecase,$opmode,$filename,$idx);		
			echo json_encode($res);
          	break;			
		}
      	case 'export_img' : {
        	$img = $_POST['base64data'];
			$name = $_POST['fname'];
			$user = $_POST['user'];
        	$tmp = 	$_POST['imname'];
        	export_img($img,$name,$user,$tmp);
			//$res = export_img($img,$name,$user,$tmp);
			//echo json_encode($res);   	
          	break;        
        }        
      	case 'render_pars' : {
        	$s = $_POST['system'];
        	$o = $_POST['origin'];
			$res = render_pars($s, $o);
			echo json_encode($res);   	
          	break;        
        }
      	case 'get_units' : {
			$tbl = $_POST['o']."_".strtolower($_POST['s'])."_params";
          	$p = $_POST['par'];
			$res = get_units($p, $tbl);
			echo json_encode($res);   	
          	break;
 	    }
      	case 'process_login' : {
      		$u = $_POST['email'];
      		$p = $_POST['p'];
			$res = process_login($u,$p);
          	echo $res;
			break;          	
      	}
		case 'populate_dropdown' : {
			$t = $_POST['table'];
			$c = $_POST['column'];
			$w = $_POST['where'];
			populate_dropdown($t,$c,$w);
			break;
		}
		case 'update_history' : {
			$username = $_POST['username'];
			$msg = $_POST['operation'];
			$in = $_POST['infile'];
			$out = $_POST['out'];
			$conf = $_POST['config'];
			update_history($username, $msg, $in, $out, $conf);
			break;
		}
		case 'fetch_values_subsystem' : {
			$pc = $_POST['cat_val'];
			$pn = $_POST['cat_name'];
          	$f = $_POST['cat_filter'];
			fetch_values_subsystem($pc, $pn, $f);
			break;
		}
		case 'fetch_values' : {
			$pc = $_POST['cat_val'];
			$ps = $_POST['cat_sys'];
			fetch_values($pc, $ps);
			break;
		}
		case 'deletepdf' : {
			$filename = $_POST['file'];
			deletepdf($filename);
			break;
		}
		case 'delete_file' : {
			$filename = $_POST['file'];
			$id = $_POST['id'];
			$path = $_POST['path'];
            $admin = $_POST['user'];
			delete_file($id, $filename, $path, $admin);
			break;
		}
		case 'delete_upload':{
			$filename = $_POST['file'];
			$id = $_POST['id'];
			//remove entry in history table
			remove_history($id);
			//remove file
			unlink("users/config/".$filename);
			//remove entry in config
			remove_configfile_db($filename);
			break;
		}
		case 'update_isrunning':{
			$filename = $_POST['file'];
			$res = update_isrunning($filename);
			echo json_encode($res);
			break;
		}
		case 'manage_user' : {
			$id = $_POST['id'];
			$op = $_POST['op'];
			$user = $_POST['username'];
			$email = $_POST['email'];
			$admin = $_POST['admin'];
			update_user_db($id, $op, $user, $email,$admin);
			break;
		}
		case 'activateuser' : {
			$user = $_POST['username'];
			$newmail = $_POST['newmail'];
			$res = activate1st($user, $newmail);
			echo $res;
			break;
		}		
		
		
		case 'running_reports': {
			$username = $_POST["username"];
			$role = $_POST["role"];
			get_running_reports($username, $role);
			break;
		}
		case 'get_filters': {
			$sys = $_POST["s"];
			$usecase = $_POST["usecase"];
			$result = get_filters($sys, $usecase);
			echo json_encode($result);
			break;
		}        
		case 'show_adu_checkbox': {
			$sys = $_POST["system"];
			$usecase = $_POST["usecase"];
          	$par = $_POST["par"];
			$result = show_adu_checkbox($par, $sys, $usecase);
			echo json_encode($result);
			break;
		}
      	case 'change_pwd':{
      		$user = $_POST["username"];
        	$oldp = $_POST["oldpwd"];
        	$newp = $_POST["newpwd"];      
			$result = change_pwd($user, $oldp, $newp);
			echo json_encode($result);
			break;     
		}
     	case 'reset_pwd':{
      		$email = $_POST["user"];
			$result = reset_pwd($email);
			echo json_encode($result);
			break;          
      	}
      	case 'confirm_pwd_reset':{
      		$email = $_POST["email"];
        	$newp = $_POST["newpwd"];      
			$result = confirm_pwd_reset($email, $newp);
			echo json_encode($result);
			break; 
		}
      	case 'update_opmode':{
        	$newmode = $_POST["new"];    
			$admin = $_POST["user"];  			
			$result = update_opmode($newmode,$admin);
			echo json_encode($result);          
			break; 
		}
      	case 'download_tar':{
        	$f = $_POST["filename"];      
			download_tar($f);
			break; 
		}
      	case 'update_systems':{
        	$data = $_POST["data"];   
			$admin = $_POST["user"]; 			
			$result = update_systems($data,$admin);
			echo json_encode($result);
			break; 
		} 
      	case 'update_genset':{
        	$data = $_POST["data"];      
        	$admin = $_POST["user"];      
			$result = update_genset($data,$admin);
			
			echo json_encode($result);
			break; 
		}
      	case 'smtpconf':{
        	$data = $_POST["data"];
			$admin = $_POST["user"];
			$result = update_smtpset($data,$admin);
			
			echo json_encode($result);
			break; 
		}
      	case 'testsmtp':{
        	$data = $_POST["formset"];
			$user = $_POST["user"];
			$result = test_smtp($data, $user);
			
			echo json_encode($result);
			break; 
		}
      	case 'import_json':{
        	$sys = $_POST["system"];
			$result = read_json_file(strtolower($sys).".conf");
			echo json_encode($result);
			break; 
		}
      	case 'get_allowed_repos':{
        	$sys = $_POST["system"];
        	$origin = $_POST["origin"];
			$result = get_allowed_repos($sys,$origin);
			echo json_encode($result);
			break; 
		}
      	case 'get_parameter_group':{
        	$sys = $_POST["syst"];
        	$origin = $_POST["origin"];
			$subs = $_POST["subs"];
			get_parameter_group($sys,$origin,$subs);
			//$result = get_parameter_group($sys,$origin,$subs);
			//echo json_encode($result);
			break; 
		}		
    }
}

function build_options($source,$usecase,$opmode,$filename,$idx){
	//get repo from opmode
	$source_conf = read_json_file(strtolower($source).".conf");
	$repo = $source_conf[$opmode][$usecase]["repository"];
	//get branch from json file by idx
	$repo_conf = read_json_file("./settings/".$filename);
	$required = $repo_conf[strtolower($source)][$repo][$usecase]["required"];
	$keys = array_keys($required);
	$this_key = $keys[$idx];
	$values = $required[$this_key];
	$inner_keys = array_keys($values);
	if($inner_keys[0]=="values"){
		$list = $values["values"];
	}
	else{
		$list = [];
	}
	//arrange result
	$result = array(strtoupper($this_key) => $list);   
	return $result;
} 



function remove_configfile_db($filename){

	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	$con = new mysqli($host, $user, $password, $dbname, $port, $socket);	
	$sql = "DELETE FROM config_files WHERE filename = '$filename'";
	$result = mysqli_query($con, $sql);	
	mysqli_close($con);
}


function get_plot_title($p){

	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	$con = new mysqli($host, $user, $password, $dbname);	
	$sql = "SELECT plot_title FROM plots WHERE plot_name = '".ucfirst($p)."' LIMIT 1";
	$result = mysqli_query($con, $sql);	


	$value = mysqli_fetch_array($result);
 
  	return $value[0];
}

function get_plots_list(){

	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	$con = new mysqli($host, $user, $password, $dbname);	
	$sql = "SELECT * FROM plots";
	$result = mysqli_query($con, $sql);	
 
  	return $result;
}

function get_units($p, $tbl){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());

	//query
	$sql="SELECT units FROM ".$tbl." WHERE param = '".$p."'";
	$qresult = $con -> query($sql);  
	$row = $qresult->fetch_row();  
    $result = array("units" => $row[0]);   
      
  	return $result;  
  
}

function remove_history($id){

	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	$con = new mysqli($host, $user, $password, $dbname, $port, $socket);	
	$sql = "DELETE FROM history WHERE id = $id";
	$result = mysqli_query($con, $sql);	
	mysqli_close($con);

	return $array;  
  
}


function deletepdf($filename){
	unlink($filename->getRealPath());
				$listfile = fopen('prova.txt', "w") or die("Unable to open file!");
				fwrite($listfile, $filename);
				fclose($listfile);	
	return $filename;
}

function read_json_file($file){
	$strJsonFileContents = file_get_contents($file);
	$strJsonFileContents = str_replace("\\", "/",$strJsonFileContents);
	$array = json_decode($strJsonFileContents, true);

	return $array;
}


function read_config_json($file){
	$array = read_json_file($file);	
	$conf = $array["local_db"];
	return $conf;
}

function read_tmpdir_json($file){
	$array = read_json_file($file);
	$tmpdir = $array["temp_file_dir"];
	
	return $tmpdir;
}



function empty_dir($username){
  	$tmpdir = "users/".$username."/tmp";
	$it = new RecursiveDirectoryIterator($tmpdir, RecursiveDirectoryIterator::SKIP_DOTS);
	$files = new RecursiveIteratorIterator($it,
             RecursiveIteratorIterator::CHILD_FIRST);
	foreach($files as $file) {
		if ($file->isDir()){
			rmdir($file->getRealPath());
		} else {
			unlink($file->getRealPath());
		}
	}
}


function read_admin_json($file){
	$array = read_json_file($file);	
	$admin = $array["admin_email"];
	
	return $admin;
}

function fetch_values($prod_cat, $prod_sys){

	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	$con = new mysqli($host, $user, $password, $dbname, $port, $socket);
	$sql = "SELECT val FROM science_qla_params WHERE (param = '$prod_cat' AND subsystem = '$prod_sys')";
	$result = mysqli_query($con, $sql);
	$msg ='';
	if (mysqli_num_rows($result) > 0){
		while ($row = mysqli_fetch_array($result))
		{
			$val_array = explode(",", $row["val"]);
			foreach ($val_array as $opt){
				$msg .='<option value="'. $opt .'">'. $opt .'</option>';
			}
		}
	}
	else{$msg .="No categories were found!";}
	echo $msg;
	mysqli_close($con);
}

function fetch_values_subsystem($prod_cat, $prod_name, $filter=""){

	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	$con = new mysqli($host, $user, $password, $dbname, $port, $socket);
	$sql = "SELECT param, description FROM ".$prod_name."_params";
	
  	$where_arr = [];
  
    if($prod_cat != "None"){  
     array_push($where_arr, "subsystem = '".$prod_cat."'");
     //$sql = $sql." WHERE subsystem = '".$prod_cat."'";
    }
	if($filter != ""){
	 array_push($where_arr, "extra= '".$filter."'");
	 //$sql.=" AND extra= '".$filter."'";      
   	} 

  	if(count($where_arr)>0){
    	$full_where = implode(" AND ", $where_arr);
    	$sql.= " WHERE ".$full_where;
    }
  
    $sql = $sql." ORDER BY param ASC";
 
	$result = mysqli_query($con, $sql);
	echo '<option value="" disabled selected>Parameter</option>';
	if (mysqli_num_rows($result) > 0){
		while($rs=$result->fetch_assoc()){
			if ($rs['description'] != null){
				$text = $rs['param'].' - '.$rs['description'];
			}
			else{
				$text = $rs['param'];
			}
			echo '<option value="'.$rs['param'].'">'.$text.'</option>';
			}	
        
	}
	else{echo "No categories were found!";}
	mysqli_close($con);	
	
}

function populate_dropdown($table, $column, $where, $distinct=0){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());
  
	//query
	$sql="SELECT id, ".$column." FROM ".$table;
	if (!$where==""){
		//$sql.=' WHERE param="'.$where.'"';
      	$sql.=' WHERE '.$where;
	}

	if($distinct==1){
		$sql.= " GROUP BY ".$column." ORDER BY ".$column;    
    }
 
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
	    // no rows!
		echo "No data found.";
		exit;
	}
	// get usecase from where statement
	$usecase = explode("origin=", $where)[1];
	$usecase = trim($usecase, " '");
	// get current operating mode
	$opmode=strtolower(get_opmode());
	while($rs=$result->fetch_assoc()){
		$isok = false;
		if ($table=="systems"){
			if($usecase!=""){
			//check if systems is enable in current operating mode by checking its settings in configuration file
				try{
					//read <system>.conf file
					$strJsonFileContents = file_get_contents(strtolower($rs[$column]).".conf");
					$strJsonFileContents = str_replace("\\", "/",$strJsonFileContents);
					$array = json_decode($strJsonFileContents, true);
					$el = $array[$opmode][$usecase];
					if($el==""){$isok = false;}
					else{$isok = true;}
				}
				catch(Exception $e){
					$isok = false;
				}
			}
			else{
				$isok = true;
			}
		}
		else{
			$isok = true;
		}
		if($isok){
			echo '<option value="'.$rs[$column].'">'.$rs[$column].'</option>';
		}
	}
}

function get_det_layer($detcoor){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());

	//query
	$sql="SELECT layer FROM hktm_detector_layer WHERE detid=".$detcoor;
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
	    // no rows!
		echo "No data found.";
		exit;
	}
	
	$row = mysqli_fetch_assoc($result);
	$layer = $row['layer'];
	return $layer;
	
	
}

function get_file_list($source, $subsystem, $start, $end){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());	

	//query
	$sql="SELECT * FROM local_files WHERE (data_time >= ".$start." AND data_time <= ".$end." AND data_source = '".$source."' AND subsystem = '".$subsystem."')";
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
	    // no rows!
		echo "No data found.";
		exit;
	}
	
	return $result;	
}

function populate_stats(){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());

	//query
	$sql="SELECT * FROM statistics";
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
	    // no rows!
		echo "No data found.";
		exit;
	}
	
	while($rs=$result->fetch_assoc()){
		echo '<div class="parameters col-md-12">';
		echo '<div class="par-checkbox">';
		echo '<input type="checkbox" class="check" id="'.str_replace("_", "",$rs["stat_name"]).'" name="'.str_replace("_", "",$rs["stat_name"]).'" value="'.$rs["stat_function"].'">'.str_replace("_", " ",$rs["stat_name"]).'</input>';
		if($rs["tooltip"] != ""){
			echo '<div class="stats-tooltip"><img src = "assets/images/tooltip120.png" width = 16/><span class="tooltiptext">'.$rs["tooltip"].'</span></div>';
		}
		echo "<input type='hidden' id='more-".str_replace("_", "",$rs["stat_name"])."' addmore = '".$rs["addmore"]."' value='".$rs["parameters"]."'/>";
		echo '</div>';
	
		echo '</div>';
		echo '</br>';
		}
	
}


// LOGIN FUNCTIONS

function process_login($email,$p){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	$mysqli = new mysqli($host, $user, $password, $dbname);
	sec_session_start();
   if(login($email, $p, $mysqli) == true) {
	  // Login ok
       	return 1;
   } else {
	  // Login failed
		return 0;       
   }
}



function sec_session_start() {
        $session_name = 'euclid_iot_id'; // session name
        $secure = false; // true for https
        $httponly = true; // avoid javascript being able to access session id.
        ini_set('session.use_only_cookies', 1); // Use cookies only
        $cookieParams = session_get_cookie_params(); // Read cookies.
        session_set_cookie_params($cookieParams["lifetime"], $cookieParams["path"], $cookieParams["domain"], $secure, $httponly); 
        session_name($session_name); // set session name
        session_start(); // start php session.
        session_regenerate_id(); // Regenerate session and remove the old one.
}

function login($email, $password, $mysqli) {
   // Using 'prepared' sql statements it will not be possible to carry out a SQL injection attack.
   if ($stmt = $mysqli->prepare("SELECT id, username, password, salt, role, active, last_login FROM members WHERE email = ? LIMIT 1")) { 
      $stmt->bind_param('s', $email); // '$email' parameter binding.
      $stmt->execute(); // execute query.
      $stmt->store_result();
      $stmt->bind_result($user_id, $username, $db_password, $salt, $role, $active, $last); // get query result and set related variables.
      $stmt->fetch();
      $password = hash('sha512', $password.$salt); // password codification.
	  if($stmt->num_rows == 1) { // user exists
         // check if user is not blocked due to too many failed accesses.
         if(checkbrute($user_id, $mysqli) == true) { 
            // Disabled account
            return false;
         } else {
	
 		if ($active == 0) { //Check if user is active
 			return false;	
 		}
         if($db_password == $password) { // Check password.
            // Right Password!
               $user_browser = $_SERVER['HTTP_USER_AGENT']; // Get 'user-agent' parameter for current user
 
               $user_id = preg_replace("/[^0-9]+/", "", $user_id); // against XSS attack
               $_SESSION['user_id'] = $user_id; 
               $username = preg_replace("/[^a-zA-Z0-9_\-]+/", "", $username); // against XSS attack
               $_SESSION['username'] = $username;
			   $_SESSION['role'] = $role;
			   $_SESSION['last_login'] = $last;
			   $_SESSION['LAST_ACTIVITY'] = time();
               $_SESSION['login_string'] = hash('sha512', $password.$user_browser);
               
			    //Insert new last login in DB
			   $current_date = gmdate("Y-m-d H:i:s");
			   $mysqli->query("UPDATE members SET last_login = '".$current_date."' WHERE id = '".$user_id."'");
			   update_history($username, 'Login' , 'NA', 'NA', 'NA');
			   
			   //remove local files from db
			   $mysqli->query("DELETE FROM local_files WHERE username='$username'");
			   //create basic directories if missing			   
           	   if(!is_dir("users/".$username."/tmp")){mkdir("users/".$username."/tmp");}          
			   //Remove all files from temp directory
			   empty_dir($username);
               // Remove files in tmp directory
               $files = preg_grep('~^'.$username.'.*~', scandir("tmp"));
               foreach($files as $file){
				 if(is_file("tmp/".$file)){
					unlink("tmp/".$file);
				 }
               }
			   // Login successful.
               return true;    
         } else {
            // Incorrect Password.
            // Save failed try into DB.
            $now = time();
            $mysqli->query("INSERT INTO login_attempts (user_id, time) VALUES ('$user_id', '$now')");
            return false;
         }
      }
      } else {
         // User does not exist.
         return false;
      }
   }
}

function checkbrute($user_id, $mysqli) {
   // current timestamp
   $now = time();
   // Check all tries in last two hours.
   $valid_attempts = $now - (2 * 60 * 60); 
   if ($stmt = $mysqli->prepare("SELECT time FROM login_attempts WHERE user_id = ? AND time > '$valid_attempts'")) { 
      $stmt->bind_param('i', $user_id); 
      // Execute query
      $stmt->execute();
      $stmt->store_result();
      // Check if there are more than 5 tries.
      if($stmt->num_rows > 5) {
         return true;
      } else {
         return false;
      }
   }
}

function login_check($mysqli) {
   // Check session variables
   if(isset($_SESSION['user_id'], $_SESSION['username'], $_SESSION['login_string'])) {
     $user_id = $_SESSION['user_id'];
     $login_string = $_SESSION['login_string'];
     $username = $_SESSION['username'];     
     $user_browser = $_SERVER['HTTP_USER_AGENT']; // get 'user-agent' string.
     if ($stmt = $mysqli->prepare("SELECT password FROM members WHERE id = ? LIMIT 1")) { 
        $stmt->bind_param('i', $user_id); // '$user_id' parameter binding.
        $stmt->execute(); // Execute query
        $stmt->store_result();
 
        if($stmt->num_rows == 1) { // user exists
           $stmt->bind_result($password); // get result variables.
           $stmt->fetch();
           $login_check = hash('sha512', $password.$user_browser);
           if($login_check == $login_string) {
              // Login OK!!!!
              return true;
           } else {
              //  Login not OK
              return false;
           }
        } else {
            // Login not OK
            return false;
        }
     } else {
        // Login not OK
        return false;
     }
   } else {
     // Login not OK
     return false;
   }
}

// password reset
function reset_pwd($email){ 
  
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];
	$error="";
  	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);
  
    if ($stmt = $mysqli->prepare("SELECT username, active FROM members WHERE email = ? LIMIT 1")) { 
		$stmt->bind_param('s', $email);
        $stmt->execute();
        $stmt->store_result();
      	//check if user exists
		if($stmt->num_rows == 0){
        	$error .= "ERROR! No user is registered with this email address!";
        }
      	else{
            $stmt->bind_result($username,$active);
            $stmt->fetch();
          	//check if user is active
			if($active!=1){
          		$error .= "ERROR! User is not active.";
      		}        
        }
    }
  	else{
      	//error connecting to DB
    	$error .= "ERROR! Impossible to connect to DB. Please retry in few minutes or contact AIDA Admin!";
    }

	if($error==""){
      	//Insert request into pwd temp table
		$email = filter_var($email, FILTER_SANITIZE_EMAIL);
		$email = filter_var($email, FILTER_VALIDATE_EMAIL);      
   		$expFormat = mktime(date("H"), date("i"), date("s"), date("m") ,date("d")+1, date("Y"));      
   		$expDate = date("Y-m-d H:i:s",$expFormat);
   		$key = md5($email);
   		$addKey = substr(md5(uniqid(rand(),1)),3,10);
   		$key = $key . $addKey;
		// Insert Temp Table
		$sql_res = mysqli_query($mysqli, "INSERT INTO pwd_reset_tmp (email, k, expdate) VALUES ('".$email."', '".$key."', '".$expDate."');");
      	if($sql_res==1){
          	//send reset email 
        	$notok = send_reset_email($username, $email, $key);
          	if($notok==1){
              	$error.= "ERROR! Impossible to send password recovery link. Please, contact AIDA Admin.";
            }
          	else{
            	$error.= "Request process confirmed. An email has been sent to you with instructions on how to reset your password.";
            }
        }
      	else{
    		$error .= "ERROR! Impossible to complete your request. Please, try later or contact AIDA Admin.";
        }
    }
 
    mysqli_close($mysqli);
	return array("error" =>$error);
}


function get_flagged($con, $usr){
  	if($usr == "stored"){
		//query	
		$sql="SELECT * FROM stored_files ORDER BY id DESC";
    }else{
      	$sql="SELECT * FROM user_files WHERE username='".$usr."' ORDER BY id DESC";
    }

	$result = $con -> query($sql);
	
	if (!$result) {
		$result = "error";
	}

	return $result;
}


function get_list($con, $type, $statement, $table, $add_stat){

	//query
	switch($statement){
		
		case "exclude":
			$sql="SELECT * FROM ".$table."_files WHERE NOT period = '$type'";
			break;
		case "only":
			$sql="SELECT * FROM ".$table."_files WHERE period = '$type'";
			break;
		case "user":
			$user = $_SESSION['username'];
			$sql="SELECT * FROM ".$table."_files WHERE username = '$user'";
			break;
		default :
			$sql="SELECT * FROM ".$table."_files";
			break;
		}
	
 	if($add_stat!=""){
		
		$sql = $sql." ".$add_stat;
		
	}
	
	
	$sql = $sql." ORDER BY id DESC";

	$result = $con -> query($sql);
	
	if (!$result) {
		$result = "error";
	}

	return $result;
}

function get_reports($con, $type, $statement, $table){
  
	$sql = "SELECT ".$table."_files.*, stored_files.status_exp, stored_files.comment_exp, stored_files.date_exp, stored_files.username as flaguser FROM ".$table."_files LEFT JOIN stored_files ON ".$table."_files.filename=stored_files.filename";  
	switch($statement){
		case "exclude":
			$sql .= " WHERE NOT period = '$type'";
			break;
		case "only":
			$sql .= " WHERE period = '$type'";
			break;
		default :
			$sql.=" ".$statement;
			break;
		}
	
	$sql = $sql." ORDER BY id DESC";

	$result = $con -> query($sql);
	
	if (!$result) {
		$result = "error";
	}

	return $result;
}

function get_tmp_files($con, $usr, $ftype="", $exclude=""){
	$sql="SELECT * FROM local_files WHERE username = '$usr'";
  	if($ftype!=""){
		$sql = $sql." AND filetype = '".$ftype."'";    
    }
  	if($exclude!=""){
		$sql = $sql." AND (NOT filetype = '".$exclude."' OR filetype IS NULL)";    
    }	  
 
  
	$sql = $sql." ORDER BY id DESC";

	$result = $con -> query($sql);
	
	if (!$result) {
		$result = "error";
	}
	return $result;
}

function render_select_files($result){
	while($rs=$result->fetch_assoc()){
		echo "<option value='".$rs['data_source']."'>".$rs['filename']."</option>";      
      
      
    }


}

function render_tmp_files($result,$ftype=""){
	$dir = "users/".$_SESSION['username']."/tmp";  
	while($rs=$result->fetch_assoc()){

		echo "<tr>";
		if($ftype=="upload"){      
          	echo "<td width='70%'>".$rs['filename']."</td>";      
            echo "<td width='20%'>".strtoupper($rs['data_source'])."</td>";      
			echo "<td style='min-width: 160px;' width='10%'><a href='".$dir."/".$rs['filename']."' target='_blank' download><img title='Download File' class='download-icon' src='assets/images/down_min.png'/></a>";
			echo "<a href='analyze-local.php?file=".$rs['filename']."&fmt=".$rs['data_source']."' target='_blank'><img title='Make analysis' class='download-icon' src='assets/images/plot_icon.png'/></a>";          
        }
      	else{
          	echo "<td width='50%'>".$rs['filename']."</td>";			        
            echo "<td>".strtoupper($rs['data_source'])."</td>";
          	if($rs['subsystem']){
              	$val = strtoupper($rs['subsystem']);
            }
          	else{$val = "-";}
          	echo "<td>".$val."</td>"; 
          
          	if($rs['date_start']!=0){
             	$val = gmdate("Y-m-d H:i:s", $rs['date_start']);
            }
          	else{$val = "NA";}
            echo "<td>".$val."</td>";  
          
          	if($rs['date_stop']!=0){
             	$val = gmdate("Y-m-d H:i:s", $rs['date_stop']);
            }
          	else{$val = "NA";}          
            echo "<td>".$val."</td>";           	
        	
			echo "<td style='min-width: 160px;' width='10%'><a href='".$dir."/".strtolower($rs['data_source'])."/".$rs['filename']."' target='_blank' download><img title='Download File' class='download-icon' src='assets/images/down_min.png'/></a>";
			if($rs['filetype']=="image"){
				$onclick_view = "onclick='window.open(\"image-explorer.php?file=".$dir."/".strtolower($rs['data_source'])."/".$rs['filename']."&isflagged=0\", \"Image-Explorer_".$rs['filename']."\", \"width=2048,height=1024\")'";
				echo '<a href="#" '.$onclick_view.'><img src="assets/images/view_img_48.png" width="30" title="View image"/></a>';
			}			
        
        }
      	echo "</td>";
		echo "</tr>";      
    }
  
  
  
}

function render_view_reports($report){
		
	$maindir = "users/";
	$ext = ".pdf";
	while($rs=$report->fetch_assoc()){
		$status = $rs['status_exp'];
      	if(!empty($status)){
      		$status_img = set_status_img($status);
          	$status_cell = "<img src='".$status_img[0]."'/><span style='display:none'>".$status_img[1]."</span>";
          	$comments = json_decode($rs['comment_exp']);
          	$comment_cell = $comments -> {'comment'};
         	//CHECK NULL COMMENT
          
          	$flagdate = $rs['date_exp'];
          	$flaguser = $rs['flaguser'];
          	
        }
      	else{
          	$onclick = "flag_report('".$rs['filename']."','".$rs['period']."')";
        	$status_cell = '<button type="button" class="btn btn-primary btn-xs" style="font-size:9px" onclick="'.$onclick.'">Add Flag</button>';
          	$comment_cell = "-";
          	$flagdate = "-";
          	$flaguser = " - ";
        } 

      
		$dir = $maindir.$rs['filepath'];
		$conf_col = "";
		$dir_conf = $maindir."/config";
		$conf_col = "<td><a href='#' onclick='window.open(\"".$dir_conf."/".$rs['config_file']."\", \"\", \"height=800,width=600\")'>".$rs['config_file']."</a></td>";

		
		echo "<tr>";

		echo "<td><a href='#' onclick='window.open(\"".$dir."/".$rs['filename'].$ext."\", \"\", \"height=800,width=600\")'>".$rs['filename']."</a></td>";
		
		echo "<td>".$rs['upload_date']."</td>";
		echo "<td>".$rs['username']."</td>";
		if($rs['period']<>"ondemand"){
			echo "<td>".$rs['period']."</td>";
		}
		
		echo "<td>".$rs['start_date']."</td>";
		if($rs['end_date'] == ""){
			echo "<td>-</td>";
		}else{
			echo "<td>".$rs['end_date']."</td>";
		}

		
		echo $conf_col;
   		echo "<td style='min-width:52px'>".$status_cell."</td>";      
   		echo "<td>".$flaguser."</td>";
        echo "<td>".$flagdate."</td>";
        echo "<td>".$comment_cell."</td>";      
			$pdf_exist = file_exists($dir."/".$rs['filename'].".pdf");
			if($pdf_exist){			              
				echo "<td style='min-width: 160px;'><a href='".$dir."/".$rs['filename'].".pdf' target='_blank' download><img title='Download as PDF' class='download-icon' src='assets/images/down_pdf_min.png'/></a>";
            }
      		else{
				echo "<td style='min-width: 160px;'><img title='PDF not available' class='download-icon' style='opacity : 0.5' src='assets/images/down_pdf_min.png'/></a>";
            }
			echo "<a href='".$dir."/".$rs['filename'].".xml' target='_blank' download><img title='Download as XML' class='download-icon' src='assets/images/down_xml_min.png'/></a>";		
			echo "<a href='".$dir_conf."/".$rs['config_file']."' target='_blank' download><img title='Download Configuration file' class='download-icon' src='assets/images/down_json_min.png'/></a>";
		echo "</td>";
		echo "</tr>";
	}
}

function render_view_config($conflist){
		
		$maindir = "users/";
		$isrunning = 0;
		
	while($rs=$conflist->fetch_assoc()){

		$dir = $maindir.$rs['filepath'];
		
		echo "<tr>";
		
		//FILENAME
		echo "<td><a href='#' onclick='window.open(\"".$dir."/".$rs['filename']."\", \"\", \"height=800,width=600\")'>".$rs['filename']."</a></td>";
		
		//CREATION DATE
		echo "<td>".$rs['upload_date']."</td>";
		//LAST UPDATE
		echo "<td>".$rs['last_update']."</td>";
		//USER
		echo "<td>".$rs['username']."</td>";
		
		//RECURRENCY (IF PERIODIC REPORT)
		$period = $rs['period'];
		if($period == "custom"){
			$cvalue = $rs['t_window'];
			$period_view = $cvalue."h";
		}
		else{
			$cvalue="";
			$period_view = $period;
		}
		if($rs['iscomplete'] == 1){
			if($period<>"ondemand"){
				if($period == "custom"){
					echo "<td>".$rs['t_window']."h</td>";
				}
				else{
					echo "<td>".$period."</td>";
					
				}
			}
		}
		else{
			
			echo "<td>".$period_view."</td>";
		}
		
		
		if($rs['iscomplete']!=0){
			
			
			//START DATE
			echo "<td>".$rs['original_start_date']."</td>";

			//SAMPLING TYPE AND EVENTUAL VALUE
			$sampling = $rs['sampling'];
			if($rs['sampling'] == "sampled"){
				$sampling = $rs['t_sampling']."h";
			}
			else{
				$sampling = $rs['sampling'];
			}
			echo "<td>".$sampling."</td>";		
			
					
			if($rs['period']=="ondemand"){
				echo "<td>".$rs['t_window']."</td>";
				if($rs['nacq'] > 1){
					$nacq = $rs['nacq']." acquisitions - every ".$rs['t_acq']."h";
				}
				else{
					$nacq = $rs['nacq'];
				}
				echo "<td>".$nacq."</td>";		

				
			}
			//Status cell
			$isrunning = $rs['isrunning'];
			switch($isrunning){
				case 0:{
					echo "<td>idle</td>";
					break;
				}
				case 1:{
					echo "<td style='color:#FF0000; font-weight:bold'>running...</td>";
					break;
				}
				case 2:{
					echo "<td style='color:#FFAA1D; font-weight:bold'>scheduled</td>";
					break;
				}
				case 3:{
					echo "<td style='color:#FFAA1D; font-weight:bold'>paused</td>";
					break;
				}                
			}
		
		}
		//Cell with action icons
		echo "<td><div class='action-btn' style='min-width:105px'>";
		if(basename($_SERVER["SCRIPT_FILENAME"], '.php') <> "list-config" && ($isrunning==0)){
			
			echo "<a href='#' target='_blank' onclick=''><img title='Generate Report' class='download-icon' src='assets/images/play-button.png'/></a>";
		}

		echo "<a href='".$dir."/".$rs['filename']."' target='_blank' download><img title='Download Configuration file' class='download-icon' src='assets/images/down_json_min.png'/></a>";

		
		
		if(($_SESSION['username'] == $rs['username'] || $_SESSION['role'] == 'admin') && ($isrunning==0)){
			
			
			
			echo "<a href='edit-config.php?conf=".$rs['filename']."&p=".$rs['period']."&w=".$cvalue."'><img title='Edit Configuration File' class='download-icon' src='assets/images/man_config_min.png'/></a>";

			echo "<a href='#' onclick = 'delete_file(\"".$rs['id']."\", \"".$rs['filename']."\", \"".$rs['filepath']."\");'><img title='Delete file' class='download-icon' src='assets/images/del_doc_min.png'/></a>";
		}		

		echo "</div></td>";
		echo "</tr>";
	}
}


function render_run_config($conflist){
		
		$maindir = "users/";
		$isrunning = 0;
		
	while($rs=$conflist->fetch_assoc()){

		$dir = $maindir.$rs['filepath'];
		
		echo "<tr>";
		
		//FILENAME
		echo "<td><a href='#' onclick='window.open(\"".$dir."/".$rs['filename']."\", \"\", \"height=800,width=600\")'>".$rs['filename']."</a></td>";
		
		//CREATION DATE
		echo "<td>".$rs['upload_date']."</td>";
		//LAST UPDATE
		echo "<td>".$rs['last_update']."</td>";
		//USER
		echo "<td>".$rs['username']."</td>";
		
		//RECURRENCY (IF PERIODIC REPORT)
		$period = $rs['period'];
		if($period == "custom"){
			$cvalue = $rs['t_window'];
			$period_view = $cvalue."h";
		}
		else{
			$cvalue="";
			$period_view = $period;
		}
		if($rs['iscomplete'] == 1){
			if($period == "custom"){
				echo "<td>".$rs['t_window']."h</td>";
			}
			else{
				echo "<td>".$period."</td>";
				
			}
		}
		else{
			
			echo "<td>".$period_view."</td>";
		}
		
		//START DATE
			echo "<td>".$rs['original_start_date']."</td>";
		//OPERATING MODE
			echo "<td>".$rs['opmode']."</td>";      
		
		//Cell with action icons
		echo "<td><a href='#' onclick='run_from_db(\"".$rs['filename']."\", \"".$period."\", \"".$_SESSION['username']."\", \"".$rs['opmode']."\", 1)'><img title='Generate Report' class='download-icon' src='assets/images/play-button.png'/></a>";

		
		echo "<a href='".$dir."/".$rs['filename']."' target='_blank' download><img title='Download Configuration file' class='download-icon' src='assets/images/down_json_min.png'/></a>";


		echo "</td>";
		echo "</tr>";
	}
}


/*****************************/
function render_view_files($res){

		$maindir = "users/";
		$isuser = False;
		
		$ext = "";

		
	while($rs=$res->fetch_assoc()){

		if($rs['filepath']<>'stored'){
			$isuser = True;
			$dir = $maindir.$rs['filepath']."/stored";
		}
		else{$dir = $maindir.$rs['filepath'];}
		
		echo "<tr>";

		$onclick = "onclick='window.open(\"".$dir."/".$rs['filename']."\", \"\", \"height=800,width=600\")'";
		$href = "#";		
		echo "<td><a href='".$href."' ".$onclick.">".$rs['filename']."</a></td>";
		
		echo "<td>".$rs['date_exp']."</td>";
		if($isuser==False){
			echo "<td>".$rs['username']."</td>";
		}
		echo "<td>".$rs['filetype']."</td>";
		$esimg = set_status_img($rs['status_exp']);	
		echo "<td><img src='".$esimg[0]."'/><span style='display:none'>".$esimg[1]."</span></td>";
		
		echo "</td>";
		
		

		echo "<td><a href='".$dir."/".$rs['filename']."' target='_blank' download><img title='Download file' class='download-icon' src='assets/images/down_min.png'/></a>";
		if($isuser == True || $_SESSION['role'] == 'admin'){
			echo "<a href='#' onclick = 'delete_file(\"".$rs['id']."\", \"".$rs['filename']."\", \"".$rs['filepath']."\");'><img title='Delete file' class='download-icon' src='assets/images/del_doc_min.png'/></a>";
		}
		if($rs['filetype']=="image"){
			if(is_file($dir."/".$rs['parinfo'])) {
				$onclick_view = "onclick='window.open(\"image-explorer.php?file=".$dir."/".$rs['parinfo']."&isflagged=0\", \"Image-Explorer_".$rs['parinfo']."\", \"width=2048,height=1024\")'";
				echo '<a href="#" '.$onclick_view.'><img src="assets/images/view_img_48.png" width="30" title="View image"/></a>';

			}

		}
		
		echo "</td>";
		echo "</tr>";
	}
}

function render_search_select($res, $key){
	mysqli_data_seek($res, 0);
  
  	$items = array();
	while($rs=$res->fetch_assoc()){
      	$info = json_decode($rs['parinfo'], true);
      	switch($key){
          case 'parameter':
            foreach($info as $k => $v) {
         			array_push($items, trim($k," "));
            }
            break;
          case 'system':
            foreach($info as $k => $v) {
            	$data = $v['system'];
        		array_push($items, $data);
            }
        	break;
		  default :
          		array_push($items, $rs[$key]);
        }
    }
	$items = array_unique($items);
	foreach($items as $k){echo '<option value="'.$k.'">'.$k.'</option>';}  
  
}



function render_view_flagged($res, $view){

	$maindir = "users/";
	$isuser = False;
	
	$ext = "";
	
	while($rs=$res->fetch_assoc()){
		
		if($rs['filepath']<>'stored'){
			$isuser = True;
			$dir = $maindir.$rs['filepath']."/stored";
		}
		else{$dir = $maindir.$rs['filepath'];}

      	$fname = $rs['filename'];
      	$user = $rs['username'];
      	$expdate = $rs['date_exp'];
      	$expstatus = $rs['status_exp'];
		$esimg = set_status_img($expstatus);
      	$comments = json_decode($rs['comment_exp'], true);
		$tstart = $rs['exp_tstart'];
		$tstop = $rs['exp_tstop'];
		$exptype = $rs['filetype'];      
		$onclick = "onclick='window.open(\"".$dir."/".$rs['filename']."\", \"\", \"height=800,width=600\")'";      
      
      
      	if($view == "par"){
			$params = json_decode($rs['parinfo'], true);      
      
    	  	if(!empty($params)){
				foreach($params as $key => $val) {
            	  	echo "<tr>";
					$psource = $val['system'];
      	 	       	$pstatus = set_status_img($val['status']);
  	     	       	echo "<td><img src='".$pstatus[0]."'/><span style='display:none'>".$pstatus[1]."</span></td>";
  			      	echo "<td>".$key."</td>";
  		        	echo "<td>".$psource."</td>";
  	         	   	echo "<td style='text-align:left'><a href=\"#\" ".$onclick.">".$fname."</a></td>";
                  	echo "<td><img src='".$esimg[0]."'/><span style='display:none'>".$esimg[1]."</span></td>"; 
	   	  			echo "<td>".$tstart."</td>"; 
	   	  			echo "<td>".$tstop."</td>";
	   	  			echo "<td>".$expdate."</td>";
	   	           	if($isuser==False){
   	  					echo "<td>".$user."</td>";
    	            }
        			$curr_comm = $comments[$key];
					if($curr_comm=="None"){$curr_comm = "";}
	     			echo "<td>".$curr_comm."</td>";

	              	echo "</tr>";
	            }
            }              
        }
      	else{
          	
          	echo "<tr>";
           	echo "<td><img src='".$esimg[0]."'/><span style='display:none'>".$esimg[1]."</span></td>";
			echo "<td><a href=\"#\" ".$onclick.">".$fname."</a></td>";
			echo "<td>".$exptype."</td>";          
	   	  	echo "<td>".$tstart."</td>"; 
	   	  	echo "<td>".$tstop."</td>"; 
	   	  	echo "<td>".$expdate."</td>";
	   	    if($isuser==False){
   	  			echo "<td>".$user."</td>";
    	    }
          	echo "<td style='text-align:left;'>";
          	$hasimg = 1;
          	foreach($comments as $key => $val) {
				if($key != "img"){
                  	switch($rs['filetype']){
						case "image":{
                    		$imgname = $key;
                        	echo $val."<br/>";
                        	break;
                      	}
                      	case "report":{
                      		echo $val."<br/>";
                        	break;                      
                      	}
                  	    default:{
                   		    if($val == "None"){$val = "-";}
                        	echo "<span><b>".$key.": </b></span>".$val."<br/>";                      
                      	}	
                    }
                }
              	else{
                	$hasimg = $val;
                }
            }
          	echo "</td>";
            $view_link="";
			if($rs['plot_id']<>0){
               	$onclick_view = "onclick='window.open(\"view_plot.php?id=".$rs['plot_id']."&s=".$rs['sourcename']."\", \"\",\"height=1024,width=1600\")'";
              	$view_link='<a href="#" '.$onclick_view.'><img src="assets/images/view_plot_48.png" width="30" title="View plot"/></a>';
            }
          	if($rs['filetype']=="image"){
              	if($hasimg==1){
                    $onclick_view = "onclick='window.open(\"image-explorer.php?file=".$dir."/".$imgname."&isflagged=1\", \"Image-Explorer_".$imgname."\", \"width=2048,height=1024\")'";
                    $view_link='<a href="#" '.$onclick_view.'><img src="assets/images/view_img_48.png" width="30" title="View image"/></a>';
                }              
              	else{
              		$view_link="<img title='Image not available on server(s). Analysis on local image.' class='download-icon' style='opacity : 0.5' src='assets/images/view_img_48.png'/>";
                }
         	}
          	echo "<td>".$view_link."</td>";
          	echo "</tr>";
        }
	}
}

function set_status_img($status){
	$imgdir = "assets/images/";

    
	if($status == "Not Defined"){$status = "nd";}
  	$dict =  array(
    "nd" => 0,
    "ok" => 1,
    "warning" => 2,
    "serious" => 3
	);
	$img = $imgdir.$status.".png";
	$imid = $dict[$status];
    return array($img, $imid);

}

function delete_file($id, $filename, $filepath, $admin){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	
	$conn = new mysqli($host, $user, $password, $dbname);
	// Check connection
	if($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	} 

	// sql to delete a record
	if($filepath=="stored" || $filepath=="config" || $filepath=="tempconfig"){
		$tbl = $filepath;
      	$todelete = "users/".$filepath."/".$filename;
	}
	else{
		$tbl = "user";
      	$todelete = "users/".$filepath."/stored/".$filename;
	}
	
 	$sql = "DELETE FROM ".$tbl."_files WHERE id=".$id;

	if ($conn->query($sql) === TRUE) {
		echo "File ".$filename." deleted successfully";
	} else {
		echo "Error deleting file ".$filename." : " . $conn->error ."\nSQL: ".$sql."\nPATH: ".$filepath;
	}



	// remove file from dir
	if (file_exists($todelete)){
		unlink($todelete);
        //update history
        update_history($admin, "Configuration file removed" , 'NA', '{"Filename" : "'.$filename.'"}', 'NA');
	};

	$conn->close();
}

/*****************************/

function get_history_num(){
	
	$config = read_json_file("config.json");
	$history = $config['history'];
	if($history==""){
		$history = 100;
	}
	return $history;
}

function update_history($username, $msg, $input, $output, $expconfig){


	$today = gmdate('Y-m-d H:i:s');
	
	$con = new_conn_from_file("config.json");
	//Check how many records/user are present in db, in order to limit them to 100
	$sql = "SELECT MIN(date_time), COUNT(*) FROM history WHERE username = '$username'";
	$result = $con -> query($sql);
	$row = mysqli_fetch_assoc($result);
	$l = $row['COUNT(*)'];
	$hnum = get_history_num();
	if($l>=$hnum){
		$diff = $l-$hnum+1;
		$sql = "DELETE FROM history WHERE username = '$username' ORDER BY date_time ASC LIMIT ".$diff;
		//remove oldest record
		$result = $con -> query($sql);
	}
	
	$sql="INSERT INTO history (date_time, username, operation, input, output, configuration) VALUES ('$today', '$username', '$msg', '$input', '$output', '$expconfig')";
	
	$result = $con -> query($sql);
	$id = mysqli_insert_id($con);
	
	
	$con->close();
	//store history in files
	$user_str = "[".$today."] : ".$msg;
	$glob_str = "[".$today."][".$username."] : ".$msg;
	if($output != "NA" or $expconfig != "NA"){
		$user_str.=" --- ";
		$glob_str.=" --- ";
	}
	$outstr = array();
	if($output != "NA"){
		array_push($outstr, $output);
	}
	if($expconfig != "NA"){
		array_push($outstr, $expconfig);		
	}
	$user_str.=join(",",$outstr);
	$glob_str.=join(",",$outstr);
	$myfile_usr = file_put_contents("./users/".$username."/history_".$username.".txt", str_replace(array("{","}"),"",$user_str.PHP_EOL) , FILE_APPEND | LOCK_EX);	
	$myfile_gbl = file_put_contents("./users/history.txt", str_replace(array("{","}"),"",$glob_str.PHP_EOL) , FILE_APPEND | LOCK_EX);	
	
	return $id;
}

function update_configlist($file_name, $path, $username, $t, $period, $t_custom, $page, $orig_fname, $iscomplete, $action){

	$today = $t;
	$extension = explode(".", $file_name);
	$ext = end($extension);
	$type = "json";
	$con = new_conn_from_file("config.json");
	
	//open uploaded config file to check integrity
	$strjson = file_get_contents("users/".$path."/".$file_name.""); 
	#check if the file is in a JSON format
	$f = json_decode($strjson, true);
	$err = json_last_error();
	
	$result = true;
	$tbl = $path."_files";
	
	if($err == 0){
		
		//check if all params are well set
		$check = check_general_info($f, $period, $page, $t_custom);
		$e = $check[0];
		if($e == ""){
			$tstart = $check[1];
			$sampling = $check[2];
			$nacq = $check[3];
			$dts = $check[4];
			$dtacq = $check[5];
			$window = $check[6];
			

			
			if($page == "upload" && $period!="ondemand"){
				//modify t_window in config JSON file
				$f["General Info"]["Time Window"] = $window;
				$newJson = json_encode($f, JSON_PRETTY_PRINT);
				file_put_contents("users/".$path."/".$file_name."", $newJson);
			}

			#convert date in timestamp (not UTC) and hours in sec for checking date
			
			$w_sec = $window*3600;
			$ts_sec = strtotime($tstart);
			$now_sec = strtotime($today);
			
			
			
			#calculate $tstop as $tstart + $nacq*($window) + ($nacq-1)*$dtacq
			if($nacq>1){
				$dta_sec = $dtacq*3600;
				$te_sec = $ts_sec + $nacq*($w_sec) + ($nacq-1)*$dta_sec;
			}
			else{
				$te_sec = $ts_sec+$w_sec;
			}
			
			#flag if report generation is running (0 = idle, 1 = running, 2 = scheduled)
			$isrunning = 0;
			
			#if file is not complete, no run
			if($iscomplete == 0 or $action == "save"){
				$isrunning = 0;
			}
			else{
				
				if($period == "ondemand"){
					if($ts_sec<$now_sec && $te_sec<=$now_sec){
						#data already available
						$isrunning = 1;
					}
				}
				else{
					#periodic report run. If running, it means that the daemon is running
					if($ts_sec<=$now_sec){$isrunning=1;}
					else{$isrunning = 2;}
				}
			}
						
			$opmode=get_opmode();			
			if($page == "new" || $page == "upload"){
				$today_utc = gmdate('Y-m-d H:i:s', $now_sec);
				$sql="INSERT INTO $tbl (filename, filepath, username, upload_date, last_update, ext, filetype, period, start_date, original_start_date, sampling, nacq, t_sampling, t_acq, t_window, isrunning, iscomplete, opmode) VALUES ('$file_name', '$path', '$username', '$today', '$today', '$ext', '$type', '$period', '$tstart', '$tstart', '$sampling', '$nacq', '$dts', '$dtacq', '$window', $isrunning, $iscomplete,'$opmode')";
			}
			else {
				$now = gmdate('Y-m-d H:i:s');
				if($period == 'custom'){
					$window = $t_custom;
				}
				$sql="UPDATE $tbl SET last_update = '$now', period = '$period', iscomplete = '$iscomplete', start_date = '$tstart', original_start_date = '$tstart', sampling = '$sampling', nacq = '$nacq', t_sampling = '$dts', t_acq = '$dtacq', t_window = '$window', isrunning = '$isrunning', opmode = '$opmode' WHERE (filename = '$file_name')";

			}
			
			$result = $con -> query($sql);
		}
			
	}

	else{
		$e = "Impossible to read JSON file. Please check syntax.";
		$result = true;
		$isrunning = 0;
		//remove file from directory
		unlink("users/".$path."/".$file_name."");
	}
	$con->close();

	return [$result, $e, $isrunning];
}

function check_general_info($f, $period, $page, $t_custom){
	//check if all parameters are present
	$e="";
	//default null values
	$nacq = "";
	$window = "";
	$tstart = "";
	$sampling = "";
	$dts = "";
	$dtacq = "";
	
	if(isset($f['General Info']['Start Time'])){
		$tstart = $f['General Info']['Start Time'];
		$t = strtotime($tstart);
		$tstart = date('Y-m-d H:i:s',$t);
	}
	
	if($page == "upload"){
		switch($period){
			case "daily":{
				$window = 24;
				break;
			}
			case "weekly":{
				$window = 168;
				break;
			}
			case "monthly":{
				$window = 720;
				break;
			}
			case "ondemand":{
				if(isset($f['General Info']['Time Window'])){
					$window = (float) $f['General Info']['Time Window'];
				}
				break;
			}
			case "custom":{
				$window = (float)$t_custom;
				break;
			}
		}
	}
	else{
		if(isset($f['General Info']['Time Window'])){
			$window = (float) $f['General Info']['Time Window'];
		}
	}
	if(isset($f['General Info']['Sampling'])){
		$sampling = $f['General Info']['Sampling'];
	}
	
	if($period == "ondemand"){
		if(isset($f['General Info']['Number of acquisitions'])){
			$nacq = (int) $f['General Info']['Number of acquisitions'];
		}
	}
	else{$nacq = -1;}
	

	if(($period == "ondemand" && $nacq =="") || $window == "" || $tstart == "" || $sampling == ""){
		$e = "One or more parameters are missing or incorrect. Please check your configuration file.";
	}
	else
	{
		//check tstart value
		if($tstart == "1970-01-01 01:00:00"){
			$e = "Invalid Start Time value. Please check your configuration file.\n";
		}
		//check window value
		if($window<=0){
			$e = $e."Invalid Window value. Please check your configuration file.\n";
		}
	
		//check number of acquisitions value and dtacq if required
		if($period == "ondemand"){
			if($nacq<1){
				$e = $e."Invalid Number of acquisitions value. Please check your configuration file.\n";
			}
			else if($nacq>1){
				if(isset($f['General Info']['Acquisition time step']))
				{
					$dtacq = (float) $f['General Info']['Acquisition time step'];
				}
				else {
					$dtacq="";
				}
				
				if($dtacq =="" || $dtacq<=0){
					$e = $e."Acquisition time step not found or incorrect. Please check your configuration file.\n";
				}
				
			}
			else{$dtacq = 0;}
		}else{$dtacq = 0;}
		//check sampling value and dts if required
		if($sampling=="by time" || $sampling=="by function"){
			if(isset($f['General Info']['Sampling period']))
			{
				$dts = (float) $f['General Info']['Sampling period'];
			}
			else {
				$dts="";
			}
			if($dts ==""){
				$e = $e."Sampling period not found or incorrect. Please check your configuration file.\n";
			}
		}
		else if($sampling == "full"){$dts = 0;}
		else {
			$e = $e."Incorrect Sampling parameter. Please check your configuration file.\n";
			
		}
      	if($sampling=="by function"){
          	if(isset($f['General Info']['Sampling function']))
			{
				$sfunc = $f['General Info']['Sampling function'];
              	if($sfunc != "mean" || $sfunc != "median"){$sfunc == "";}
			}
			else {
				$sfunc= "";
			}
			if($sfunc == ""){
				$e = $e."Sampling function not found or incorrect. Please check your configuration file.\n";
			}
        }

	}	
	
	return [$e, $tstart, $sampling, $nacq, $dts, $dtacq, $window];
}

function checkname($file_name, $p){
	$path = 'users/'.$p.'/';
	$file = $path . $file_name;
	$file_ext = explode('.', $file_name);
	$f = $file_ext[0];
	$file_ext = strtolower(end($file_ext));
	$today = date('Y-m-d H:i:s');
	$todaystr = str_replace(array("-",":"), "", $today);
	$todaystr = str_replace(array(" "), "_", $todaystr);
	
	$filelist = scandir($path);
	$isfile = in_array($file_name, $filelist);

	$changename = 0;
	if($isfile == true){
		$file = $path . $f."_".$todaystr.".".$file_ext;
		$file_name = $f."_".$todaystr.".".$file_ext;
		$changename = 1;
	}
	return [$file_name, $file, $changename];
}

function new_conn_from_file($file){
	$config = read_config_json($file);
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());
	
	return $con;
}


function update_isrunning($file_name){

	$updated = [];
	$con = new_conn_from_file("config.json");
	
	$sql="UPDATE config_files SET isrunning = 1 WHERE (filename = '$file_name')";
			
	$result = $con -> query($sql);

	$updated['res'] = $result;
	return $result;
}		

function list_users($con, $isactive, $statement, $table){
	

	//query
	switch($statement){
		
		case "exclude":
			$sql="SELECT * FROM ".$table." WHERE NOT active = '$isactive'";
			break;
		case "only":
			$sql="SELECT * FROM ".$table." WHERE active = '$isactive'";
			break;
		default :
			$sql="SELECT * FROM ".$table;
			break;
		}
	
	
	$sql = $sql." ORDER BY active ASC";

	$result = $con -> query($sql);
	
	if (!$result) {
		$result = "error";
	}

	return $result;
}

function get_flag_notes($filename, $tbl){
	
	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
  	$filename = str_replace('"',"",$filename);
  	$fname_arr = explode("/",$filename);
  	$fname = end($fname_arr);
  	if($tbl == "stored"){
		$sql = "SELECT username, status_exp, comment_exp FROM stored_files WHERE parinfo = '".$fname."'";
    }
  	else{
      	$sql = "SELECT status_exp, comment_exp FROM user_files WHERE parinfo = '".$fname."' AND username = '".$tbl."'";
    }

	$con = new mysqli($host, $user, $password, $dbname);

	$result = $con -> query($sql);
	
	if (!$result) {
		$result = "error";
	}

	mysqli_close($con);

	return $result;
}


function render_flag_notes($res, $save){

	while($rs=$res->fetch_assoc()){
		
		echo "<tr>";
		//status
        $pstatus = set_status_img($rs['status_exp']);
  	    echo "<td style='max-width:20px'><img src='".$pstatus[0]."' width='18px'/><span style='display:none'>".$pstatus[1]."</span></td>";      
     
		      
		//Username
		if($save=="public"){	      
			echo "<td>".$rs['username']."</td>";
        }
      	//Comments
      	$comments = json_decode($rs['comment_exp'], true);
		foreach ($comments as $key => $value) {
    		echo "<td>".$value."</td>";   
  		}      
		   
		echo "</td>";
		echo "</tr>";
	}

}




function render_view_users($res){
		
	while($rs=$res->fetch_assoc()){
		
		echo "<tr>";
		
		//Username
		echo "<td>".$rs['username']."</td>";
		
		//Email
		echo "<td>".$rs['email']."</td>";
		//Role
		echo "<td>".$rs['role']."</td>";
		
		//Request/Activation/Deactivation date
		echo "<td>".$rs['action_date']."</td>";
		
		//Last login and logout
		if($rs['active']=="1"){
			echo "<td>".$rs['last_login']."</td>";
			echo "<td>".$rs['last_logout']."</td>";
		}
		
		//BUTTONS
		echo "<td>";
		if($rs['active']!="1"){
			//echo "<button class='btn btn-success mr-xs' id = 'activate' >Activate</button>";
			echo "<a href='#' onclick='manage_user(".$rs['id'].", \"active\", \"".$rs['username']."\", \"".$rs['email']."\")'><img title='Activate' class='download-icon' src='assets/images/activate_48.png'/></a>";
		}
		else{
			//echo "<button class='btn btn-warning mr-xs' id = 'deactivate' >Deactivate</button>";
			if($rs['role'] != "admin"){
				echo "<a href='#' onclick='manage_user(".$rs['id'].", \"deactive\", \"".$rs['username']."\", \"".$rs['email']."\")'><img title='Deactivate' class='download-icon' src='assets/images/deactivate_48.png'/></a>";
			}
		}
		if($rs['role'] != "admin" || ($rs['role'] == "admin" && $rs['active']=="0")){
			echo "<a href='#' onclick='manage_user(".$rs['id'].", \"remove\", \"".$rs['username']."\", \"".$rs['email']."\")'><img title='Remove' class='download-icon' src='assets/images/trash_48.png'/></a>";
		}
		echo "</td>";
		echo "</tr>";
	}
}

// Function to delete all files 
// and directories 
function deleteAll($str) { 
      
    // Check for files 
    if (is_file($str)) { 
          
        // If it is file then remove by 
        // using unlink function 
        return unlink($str); 
    } 
      
    // If it is a directory. 
    elseif (is_dir($str)) { 
          
        // Get the list of the files in this 
        // directory 
        $scan = glob(rtrim($str, '/').'/*'); 
          
        // Loop through the list of files 
        foreach($scan as $index=>$path) { 
              
            // Call recursive function 
            deleteAll($path); 
        } 
          
        // Remove the directory itself 
        return @rmdir($str); 
    } 
} 

function activate1st($user, $newmail){
	$error = 0;
	$con = new_conn_from_file("config.json");

	//check if user exists
	$sql="SELECT id FROM members WHERE (username = '$user')";
	$ids = $con -> query($sql);
	$num_rows = mysqli_num_rows($ids);
	if($num_rows==1){
		$sql="UPDATE members SET active = 1 WHERE (username = '$user')";
		$result = $con -> query($sql);	
	
		if($result){

			$dir_err = manage_user_dir($user, "active");
			$error = $dir_err;
			if($dir_err == 0){
				try{
					//modify config.json with new notification email
					$jsonString = file_get_contents('config.json');
					$data = json_decode($jsonString, true);
					$data['admin_email'] = $newmail;
					$newJsonString = json_encode($data);
					file_put_contents('config.json', $newJsonString);
				}
				catch(Exception $e)
				{
					$error = 2;
				}
			}
		}
		else{
			$error=1;
		}
	}
	else{
		$error = 1;
	}
	
	$con -> close();
	
	return $error;	
}


function update_user_db($id, $op, $user, $email, $admin){
	$con = new_conn_from_file("config.json");
	
	//query
	switch($op){
		
		case "active":
			$sql="UPDATE members SET active = 1 WHERE (id = '$id')";
			$hist_word = "activated";
			break;
		case "deactive":
			$sql="UPDATE members SET active = 2 WHERE (id = '$id')";
			$hist_word = "deactivated";			
			break;
		case "remove":
			$sql = "DELETE FROM members WHERE id=".$id;
			$hist_word = "removed";			
			break;
		}

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
	
	
	if($result){
		$dir_err=0;
		if($op!="deactivate"){
			//create/remove directory for activation/deletion
			$dir_err = manage_user_dir($user, $op);
		}
		$mail_err=0;
		if($dir_err == 0){
			//send email
			$mail_err = send_confirmation_email($user, $email, $op);
		}
		//update history
		$hist_op = "User ".$user." ".$hist_word;
		update_history($admin, $hist_op , 'NA', 'NA', 'NA');
		
		
		$error = $dir_err || $mail_err;
	}
	else{
		$error=1;
	}
	$con -> close();
	echo($error);
}

function manage_user_dir($username, $op){

	require("PHPMailer/src/PHPMailer.php");
	require("PHPMailer/src/SMTP.php");
	
	switch($op){
		case "active":
			if (!file_exists('users/'.$username)) {
				mkdir('users/'.$username, 0777, true);
              	mkdir('users/'.$username.'/stored', 0777, true);
              	mkdir('users/'.$username.'/tmp', 0777, true);
				//Create listfiles.html
				$txt = "<ul><li data-jstree='{ \"opened\" : false }' class='folder'>docs<ul></ul></li></ul><ul><li data-jstree='{ \"opened\" : false }' class='folder'>images<ul></ul></li></ul><ul><li data-jstree='{ \"opened\" : false }' class='folder'>temp<ul></ul></li></ul>";
				$listfile = fopen('users/'.$username.'/stored/listfiles.html', "w") or die("Unable to open file!");
				fwrite($listfile, $txt);
				fclose($listfile);

				//create index.html
				$indexfile = fopen('users/'.$username.'/index.html', "w") or die("Unable to open file!");
				fwrite($indexfile, "");
				fclose($indexfile);
              	$indexfile = fopen('users/'.$username.'/stored/index.html', "w") or die("Unable to open file!");
				fwrite($indexfile, "");
				fclose($indexfile);
              	$indexfile = fopen('users/'.$username.'/tmp/index.html', "w") or die("Unable to open file!");
				fwrite($indexfile, "");
				fclose($indexfile);
				//create history file
				$histfile = fopen('users/'.$username.'/history_'.$username.'.txt', "w") or die("Unable to open file!");
				fwrite($histfile, "");
				fclose($histfile);				
			}
		break;
		case "remove":
			deleteAll('users/'.$username);
			break;
	}
	return 0;
}


function get_url(){
    if(isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on')   
         $url = "https://";   
    else  
         $url = "http://";   
    // Append the host(domain name, ip) to the URL.   
    $url.= $_SERVER['HTTP_HOST'];   
    
    // Append the requested resource location to the URL   
    $url.= $_SERVER['REQUEST_URI'];    

	// Remove filename from url
	$parts = explode('/', $url);
	$last = array_pop($parts);
	$parts = array(implode('/', $parts), $last);
  	$url = $parts[0];
	return $url;

}



function send_confirmation_email($username, $email, $op){
	require("PHPMailer/src/Exception.php");	
	//administrator email
	$mail_admin = read_admin_json("config.json");
	//email server configuration
	$configmail = read_json_file("smtp.json");
	$host = $configmail['host'];
	$port = $configmail['port'];
	$user = $configmail['user'];
	$pwd = $configmail['password'];
	
	//Set email subject and body depending on operation done
	switch($op){
		case "active":
			$subject = "Your AIDA account has been activated";
			$msg = "<p>Dear $username,<br/> your registration has been completed and your account is now active. Now you can access to your AIDA dashboard by using the  password you set during registration.</p><p>For any issues or feedback, you can send an email to: <a href='mailto:$mail_admin'>$mail_admin</a>.</p><p>The IOT</p>";
			break;
		case "deactive":
			$subject = "Your AIDA account has been deactivated";
			$msg = "<p>Dear $username,<br/> your AIDA account has been deactivated by AIDA administrator.</p><p>For any details or to re-activate your account, send an email to: <a href='mailto:$mail_admin'>$mail_admin</a>.</p><p>The IOT</p>";
			break;
		case "remove":
			$subject = "Your AIDA account has been removed";
			$msg = "<p>Dear $username,<br/> your AIDA account has been canceled from AIDA database.</p><p>For any details, send an email to: <a href='mailto:$mail_admin'>$mail_admin</a>.</p><p>The IOT</p>";
			break;
	}
	
	

	/* Create a new PHPMailer object. Passing TRUE to the constructor enables exceptions. */
	//$mail = new PHPMailer(TRUE);
	$mail = new PHPMailer\PHPMailer\PHPMailer();

/* Open the try/catch block. */
	$error = 0;
	try {
		$mail->IsSMTP(); // Utilizzo della classe SMTP al posto del comando php mail()
		
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
			$mail->SMTPAuth = true; // Autenticazione SMTP
		}
		$mail->Host = $host;
		$mail->Port = $port;
		if($port==465){
			$mail->SMTPSecure = 'ssl';
		}
		else{
			$mail->SMTPSecure = 'tls';
		}
		$mail->IsHTML(true); 
		$mail->Username = $user; // Nome utente SMTP autenticato
		$mail->Password = $pwd; // Password account email con SMTP autenticato
		
		/*!!!NOTE: GMAIL require to enable unsecure apps*/
					
					
	   /* Set the mail sender. */
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


function send_reset_email($username, $email, $key){

	
	require(__DIR__ ."/PHPMailer/src/PHPMailer.php");
	require(__DIR__ ."/PHPMailer/src/SMTP.php");
	require(__DIR__ ."/PHPMailer/src/Exception.php");	
	//administrator email
	$mail_admin = read_admin_json("config.json");
	//email server configuration
	$configmail = read_json_file("smtp.json");
	$host = $configmail['host'];
	$port = $configmail['port'];
	$user = $configmail['user'];
	$pwd = $configmail['password'];
	
	$url = get_url();  
	$subject = "AIDA Password Recovery";  
  
	$msg='<p>Dear '.$username.',</p>';
	$msg.='<p>Please click on the following link to reset your password.</p>';
	$msg.='<p>-------------------------------------------------------------</p>';
	$msg.='<p><a href="'.$url.'/recovery.php?key='.$key.'&email='.$email.'&action=reset" target="_blank">'.$url.'/recovery.php?key='.$key.'&email='.$email.'&action=reset</a></p>';		
	$msg.='<p>-------------------------------------------------------------</p>';
	$msg.='<p>Please be sure to copy the entire link into your browser. The link will expire after 1 day for security reason.</p>';
	$msg.='<p>If you did not request this forgotten password email, no action is needed, your password will not be reset. However, you may want to log into your account and change your security password as someone may have guessed it.</p>';   	
	$msg.='<p>Thanks,</p>';
	$msg.='<p>The IOT</p>';  

	/* Create a new PHPMailer object. Passing TRUE to the constructor enables exceptions. */
	//$mail = new PHPMailer(TRUE);
	$mail = new PHPMailer\PHPMailer\PHPMailer();

/* Open the try/catch block. */
	$error = 0;
	try {
		$mail->IsSMTP(); // Utilizzo della classe SMTP al posto del comando php mail()
		
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
			$mail->SMTPAuth = true; // Autenticazione SMTP
		}
		$mail->Host = $host;
		$mail->Port = $port;
		if($port==465){
			$mail->SMTPSecure = 'ssl';
		}
		else{
			$mail->SMTPSecure = 'tls';
		}
		$mail->IsHTML(true); 
		$mail->Username = $user; // Nome utente SMTP autenticato
		$mail->Password = $pwd; // Password account email con SMTP autenticato
		
		/*!!!NOTE: GMAIL require to enable unsecure apps*/
					
					
	   /* Set the mail sender. */
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


function get_running_reports($username, $role){
	
	$config = read_config_json("config.json");
	$host = $config['host'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];

	if($role == "admin"){
		$sql = "SELECT id as ID, username as User, period as Period, config_file as 'Config File', start_date as 'Current Report Start Date', exp_status as Progress, pid as Pid FROM running_reports";
		
	}
	else{
		$sql = "SELECT id as ID, period as Period, config_file as 'Config File', start_date as 'Current Report Start Date', exp_status as Progress, pid as Pid FROM running_reports WHERE username = '".$username."'";
	}
	$con = new mysqli($host, $user, $password, $dbname);

	$report = mysqli_query($con, $sql) or die("database error:". mysqli_error($conn));

	$maindir = "users/config";
	mysqli_close($con);

	$data = array();
	while( $rows = mysqli_fetch_assoc($report) ) {
		$cf = $rows["Config File"];
		$ncf = "<a href='#' onclick='window.open(\"".$maindir."/".$cf."\", \"\", \"height=800,width=600\")'>".$cf."</a>";
		$rows["Config File"] = $ncf;


		$status = $rows['Progress'];
			if($status == "-99.0"){
				$status_label = "waiting...";
              	$add_class = "progress-label progress-label-black";
			}
      		else if($status == "-100.0"){
				$status_label = "paused";
              	$add_class = "progress-label progress-label-yellow";
            }
      		else if($status == "-101.0"){
				$status_label = "failed";
              	$add_class = "progress-label progress-label-red";
            }
			else{
				$status_label = $status;
             	$add_class = "";
			}

			$rows["Progress"] =	"<div class='progress'><div class='progress-bar progress-bar-striped progress-bar-animated ".$add_class."' role='progressbar' style='width : ".$status."%;' aria-valuenow='".$status."' aria-valuemin='0' aria-valuemax='100'>".$status_label."</div>	</div>";

			$pid = $rows["Pid"];
		
			$rows["Pid"] = "<div class='action-btn' style='min-width:90px'>";
      		if($role=="admin" && $rows["Period"]!="ondemand"){
              	if($status=="-100.0" ||  $status=="-101.0"){
                  	$rows["Pid"] = $rows["Pid"]."<a href='#' onclick = 'resume_report(".$rows['ID'].", ".$rows['Current Report Start Date'].", \"".$cf."\")'><img title='Resume generation' class='download-icon' src='assets/images/play-button.png'/></a>";
                }
              	else{
              		$rows["Pid"] = $rows["Pid"]."<a href='#' onclick = 'stop_report(".$rows['ID'].", ".$pid.", \"".$cf."\", \"pause\")'><img title='Pause generation' class='download-icon' src='assets/images/pause_doc_min.png'/></a>";
                }
            }

      		else{$rows["Pid"] = "";}
      		
      		if($status=="-100.0" ||  $status=="-101.0"){
              	$title_icon = 'Remove';
              	$img_icon = 'trash_48.png';
            }
      		else{
              	$title_icon = 'Stop generation';
              	$img_icon = 'del_doc_min.png';				
            }
      		$rows["Pid"] = $rows["Pid"]."<a href='#' onclick = 'stop_report(".$rows['ID'].", ".$pid.", \"".$cf."\", \"kill\")'><img title='".$title_icon."' class='download-icon' src='assets/images/".$img_icon."'/></a>";
			$rows["Pid"] = $rows["Pid"]."</div>";
		$data[] = $rows;
	}
	$results = array(
	"sEcho" => 1,
	"iTotalRecords" => count($data),
	"iTotalDisplayRecords" => count($data),
	"aaData" => $data
	);
	file_put_contents("data_php.json", json_encode($results));
	echo json_encode($results);

}


function get_opmode($enabled=true){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());	

	//query
  	if($enabled){
      $sql="SELECT mode FROM operation_modes  WHERE enable=1";
      $result = $con -> query($sql);

      $row = $result->fetch_row();
      $mode = $row[0];
      $res = strtoupper($mode);
	}
  	else{
      $sql="SELECT mode, enable FROM operation_modes";
      $res = $con -> query($sql);
    }
  	return $res;
}

function get_filters($sys, $usecase){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());	

	//query
	$sql="SELECT required_filters, add_filters FROM ".$usecase."_source WHERE name = '".$sys."'";
	$qresult = $con -> query($sql);
	$row = $qresult->fetch_row();
      
    $result = array("required" => $row[0], "additional" => $row[1]);   
      
  	return $result;
}


function show_adu_checkbox($par, $sys, $usecase){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$port = $config['port'];
	$socket = $config['socket'];
	$user = $config['user'];
	$password = $config['password'];
	$dbname = $config['dbname'];
	
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());

	//query
	$sql="SELECT hascalib FROM ".$usecase."_".$sys."_params WHERE param = '".$par."'";
	$qresult = $con -> query($sql);  
	$row = $qresult->fetch_row();  
    $result = array("hascalib" => $row[0]);   
      
  	return $result;  
}


function change_pwd($user, $oldp, $newp){
	
  
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];
	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);  
  
	if ($stmt = $mysqli->prepare("SELECT id, username, password, salt FROM members WHERE username = ? LIMIT 1")) { 
      $stmt->bind_param('s', $user); // '$email' parameter binding.
      $stmt->execute(); // Execute query
      $stmt->store_result();
      $stmt->bind_result($user_id, $username, $db_password, $salt); // get query results and store into variables.
      $stmt->fetch();
      $password = hash('sha512', $oldp.$salt); // password codification.
      if($db_password == $password) {
      // Create random key
      $random_salt = hash('sha512', uniqid(mt_rand(1, mt_getrandmax()), true));
      // Create password with hash key.
      $newpassword = hash('sha512', $newp.$random_salt);
      if ($update_stmt = $mysqli->prepare("UPDATE members SET password=?, salt=? WHERE username = ?")) {    
          $update_stmt->bind_param('sss', $newpassword, $random_salt, $username); 
          // Query execution
          $update_stmt->execute();
		  mysqli_close($mysqli);
          return array("error" => "Password correctly updated.\nPlease, log in again.","logout" => 1);
      }
        else{
          	mysqli_close($mysqli); 
        	return array("error" => "ERROR! Impossible to connect to local DB. Please retry or contact AIDA admin.","logout" => 0);
        }
		
      }
      else{
        mysqli_close($mysqli);
      	return array("error" => "ERROR! Invalid old password. Please, retry", "logout" => 0);
      }
    } else {
         // user does not exist.
      	mysqli_close($mysqli);
        return array("error" => "ERROR! User does not exist.", "logout" => 0);
      }

}


function render_systems($o){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];
	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);

	$sql="SELECT name,enabled FROM systems WHERE origin='".$o."'";  
	$result = $mysqli -> query($sql);
	
	if (!$result) {
		echo "<p>Unable to retrieve info from local DB. Please retry or contact AIDA admin</p>";
	}
  	else{
      	echo "<table class='table systems_info table-bordered table-striped mb-none' id='datatable-systems'>";
		echo '<thead><tr >
		<th scope="col">System</th>
		<th scope="col">Status</th>
		<th scope="col"></th>
	  	</tr></thead>';     
    	while( $rs = mysqli_fetch_assoc($result) ) {
          	$enabled = $rs['enabled'];
			if($enabled==1){
            	$status = '<span class="label label-success">Available</span>';
              	$show = '<button type="button" class="mb-xs mt-xs mr-xs btn btn-sm btn-default" onclick="show_parameters(\''.$rs['name'].'\', \''.$o.'\')">Show parameters</button>';
            }
          	else{
            	$status = '<span class="label label-danger">Unavailable</span>';
				$show = '<span></span>';              
            }
          	echo "<tr>";
          	echo "<td>".$rs['name']."</td>";
          	echo "<td>".$status."</td>";    
          	echo "<td>".$show."</td>";           
          	echo "</tr>";
        }
      	echo "</table>";
    }

    mysqli_close($mysqli);


}

function render_pars($s, $o){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];

	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);

  	$mode = get_opmode();
  
	if($s=="NISP" && $o=="science" && $mode == "NOMINAL"){
    	$stat = " WHERE extra<>'statistics'";
    } 
  	else{
    	$stat = "";
    }
  
  
  
	$sql="SELECT * FROM ".strtolower($o)."_".strtolower($s)."_params".$stat;  
	$result = $mysqli -> query($sql);
	
	if (!$result) {
		$res = array("error" => 1);
	}
  	else{
      	$row = $result->fetch_assoc();
      	$karray = array();
      	foreach($row as $key => $value){
      		array_push($karray, $key);
        }
		$table = "<table class='table params_info table-bordered table-striped mb-none' id='datatable-params'><thead><tr><th scope='col'>Parameter</th>";
      	switch($o){
          case "hktm":
            	$subs = "Subsystem";
            	$hassubs = 1;
            	break;
          case "science":
            	if($s=="QLA"){
            		$subs = "Subsystem";
            		$hassubs = 1;                  
                }
            	else{
            		$subs = "Section";
            		$hassubs = 0;
                }
            	break;
        }

        
        
		$table .="<th scope='col'>".$subs."</th><th scope='col'>Description</th>";
		if(in_array("minval", $karray)){
        	$table .= "<th scope='col'>Soft Min</th><th scope='col'>Soft Max</th>";
        }
		if(in_array("hardmin", $karray)){
        	$table .= "<th scope='col'>Hard Min</th><th scope='col'>Hard Max</th>";
        }      
		if(in_array("val", $karray)){
        	$table .= "<th scope='col'>Values</th>";
        }      
	  	$table .= "</tr></thead>";
		mysqli_data_seek($result,0);      
    	while( $rs = mysqli_fetch_assoc($result) ) {
          	switch($hassubs){
              case 0:
          		$sect = $rs['extra'];
            	break;                
          	  case 1 : 
          		$sect = $rs['subsystem'];
            	break;
            }
        	$table .= "<tr><td>".$rs['param']."</td><td>".$sect."</td><td>".$rs['description']."</td>";
            if(in_array("minval", $karray)){
              	$minval = $rs['minval'];
              	if($minval==-999){$minval="";}
              	$maxval = $rs['maxval'];
              	if($maxval==-999){$maxval="";}              
                $table .= "<td>".$minval."</td><td>".$maxval."</td>";
            }
            if(in_array("hardmin", $karray)){
              	$minval = $rs['hardmin'];
              	if($minval==-999){$minval="";}
              	$maxval = $rs['hardmax'];
              	if($maxval==-999){$maxval="";}               
                $table .= "<td>".$minval."</td><td>".$maxval."</td>";
            }      
            if(in_array("val", $karray)){
              	
                $table .= "<td>".$rs['val']."</td>";
            }           
        	$table .= "</tr>";
        }
     
		$res = array("error" => 0, "table" => $table);
    }

    mysqli_close($mysqli);
  
	return $res;

}


function render_analysis($o){
      
    switch($o){
      case "plots":
        $name_col = 'plot_title';
        $report_name = 'plot_name';
        break;
      case "statistics":
        $name_col = 'stat_name';
        $report_name = 'stat_slug';
        break;
    }
  
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];

	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);

	$sql="SELECT * FROM ".$o. " ORDER BY ".$name_col." ASC";  
	$result = $mysqli -> query($sql);
	
	if (!$result) {
		echo "<p>Unable to retrieve info from local DB. Please retry or contact AIDA admin</p>";
	}
  	else{
		$table = "<table class='table params_info table-bordered table-striped mb-none' id='datatable-analysis'><thead><tr><th scope='col'>Name</th>";
		$table .="<th scope='col'>Report config name</th><th scope='col'>Parameters</th>";      
	  	$table .= "</tr></thead>";
   	while( $rs = mysqli_fetch_assoc($result) ) {
          	if($rs['parameters']!= "") {
			$p_str = json_decode($rs['parameters'], true);
          	$parameters = join(",  ", array_keys($p_str));
            }
          	else{$parameters = "";}
        	$table .= "<tr><td>".$rs[$name_col]."</td><td>".strtolower($rs[$report_name])."</td><td>".$parameters."</td>";
        	$table .= "</tr>";
        }
     
		echo $table;
    }
    mysqli_close($mysqli);
}


function export_img($data, $name, $user, $tmp){
//	$error = 0;

	$tmpdir = 'users/'.$user.'/tmp/'.$tmp;
	if (!file_exists($tmpdir)) {
		mkdir($tmpdir, 0777, true);
    }
    $image = explode('base64,',$data); 
    file_put_contents($tmpdir.'/'.$name.'.jpg', base64_decode($image[1]));

}





// MACHINE LEARNING FUNCTIONS


function populate_ml(){
	$command = 'python scripts/listMlModels.py';
	$result = shell_exec($command); 


$separator = "\r\n";
$line = strtok($result, $separator);
echo '<select name="model" id="model">\n';
  

while ($line !== false) {
    # do something with $line
	
	echo '<option value="'.$line.'">'.$line.'</option>';
    $line = strtok( $separator );

	}	
	
echo '</select>';
	
}


function populate_ml_model(){
	$command = 'python scripts/listMlTrainedModels.py';
	$result = shell_exec($command); 


$separator = "\r\n";
$line = strtok($result, $separator);
echo '<select name="model" id="model">\n';
  

while ($line !== false) {
    # do something with $line
	
	echo '<option value="'.$line.'">'.$line.'</option>';
    $line = strtok( $separator );

	}	
	
echo '</select>';
	
}


function populate_ml_param($model){
	
	
	$command = 'python scripts/formMaker.py '.$model;
	$result = shell_exec($command); 
	echo '<label class="col-md-2 control-label">Configuration of '.$model.'</label> <div class="stat-list col-md-6">'.PHP_EOL;

$separator = "\r\n";
$line = strtok($result, $separator);
  echo '<table>'.PHP_EOL;
while ($line !== false) {
    # do something with $line
	$pieces=explode(" " , $line);
	echo '<tr><td><label for="'.$pieces[0].'"><b>'.$pieces[0].'</b></label></td><td> <input type="text" id="'.$pieces[0].'" name="'.$pieces[0].'" value="'.$pieces[1].'"></td></tr>'.PHP_EOL;
    $line = strtok( $separator );

	}	
echo '</table></div>';	


}




function recovery_form($email, $key){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];

	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);
  	$curDate = date("Y-m-d H:i:s");
 
 	//$query = mysqli_query($mysqli,"SELECT * FROM pwd_reset_tmp WHERE key='".$key."' and `email`='".$email."';");
	$qresult = $mysqli->query("SELECT * FROM pwd_reset_tmp WHERE k='".$key."' and email='".$email."';");
	if(!$qresult){
    	$row="";
    }
  	else{
    	$row = $qresult->num_rows;
    }
	/* Get the number of rows in the result set */
  	//$row = mysqli_num_rows($query);
  	if ($row==""){
  		$res = '<h2>Invalid Link</h2><p>The link is invalid/expired. Either you did not copy the correct link from the email, or you have already used the key in which case it is deactivated.</p>';
		$res .= '<p><a href="recovery.php">Click here</a> to reset password.</p>';
	}else{
		$row = mysqli_fetch_assoc($qresult);
		$expDate = $row['expdate'];
  		if ($expDate >= $curDate){
          $res = '<form method="post" action="" id="updatepwd" name="updatepwd"><input type="hidden" name="action" value="update" />';
          $res .= '<div class="form-group mb-lg"><label class="col-xs-4">Enter New Password:</label><input class="form-control input-lg" type="password" id="pass1" name="pass1" required /></div>';
          $res .= '<div class="form-group mb-lg"><label class="col-xs-4">Re-Enter New Password:</label><input class="form-control input-lg" type="password" id="pass2" name="pass2" required/></div>';
          $res .= '<div class="col-sm-12 text-right"><input type="hidden" id="email" name="email" value="'.$email.'"/><button type="button" id="resetpwd" class="btn btn-primary" onclick="pwd_confirm();">Reset Password</button></div></form>';
        }
    }
  	return $res;
}

function confirm_pwd_reset($email, $newp){
 
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];
	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);  
  
	if ($stmt = $mysqli->prepare("SELECT id, username, password, salt FROM members WHERE email = ? LIMIT 1")) { 
		$stmt->bind_param('s', $email); 
      	$stmt->execute(); 
      	$stmt->store_result();
      	$stmt->bind_result($user_id, $username, $db_password, $salt); 
      	$stmt->fetch();
      	// Create random key
      	$random_salt = hash('sha512', uniqid(mt_rand(1, mt_getrandmax()), true));
      	// Create password with hash key.
      	$newpassword = hash('sha512', $newp.$random_salt);
      	if($update_stmt = $mysqli->prepare("UPDATE members SET password=?, salt=? WHERE username = ?")){    
          	$update_stmt->bind_param('sss', $newpassword, $random_salt, $username); 
          	// Query execution
          	$update_stmt->execute();
          	mysqli_query($mysqli,"DELETE FROM pwd_reset_tmp WHERE email='".$email."';");
		  	mysqli_close($mysqli);
          	return array("error" => "Password correctly updated.");
      	}
      	else{
          	mysqli_close($mysqli); 
        	return array("error" => "ERROR! Impossible to connect to local DB. Please retry or contact AIDA admin.");
      	}
    } else {
      	mysqli_close($mysqli);
        return array("error" => "ERROR! User does not exist.");
    }

}


function select_items_json($opmode, $source, $origin){
	$settings = "";
	if($source != "upload"){  
        // get repository settings	
        $strJsonFileContents = file_get_contents(strtolower($source).".conf");
        $strJsonFileContents = str_replace("\\", "/",$strJsonFileContents);
        $array = json_decode($strJsonFileContents, true);
        $repo = $array[$opmode][$origin]["repository"];

        // open forms json and get settings
        $strJsonFileContents = file_get_contents("settings/forms.json");
        $strJsonFileContents = str_replace("\\", "/",$strJsonFileContents);  
        $data = json_decode($strJsonFileContents, true);

        $settings = $data[strtolower($source)][$repo][$origin];  
    }  
	
	$myfile = fopen("prova.txt", "w") or die("Unable to open file!");
	$txt = $strJsonFileContents;
	fwrite($myfile, $txt);
	fclose($myfile);
	
	return $settings;
}


function update_opmode($new, $admin){
	$old_opmode = get_opmode();
	if(strtoupper($new) != $old_opmode){	
		$config = read_config_json("config.json");
		$host = $config['host'];
		$dbuser = $config['user'];
		$dbpwd = $config['password'];
		$dbname = $config['dbname'];
		
		$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname); 
		$sql = "UPDATE operation_modes SET enable=case when mode='".$new."' then 1 else 0 end";
		$qresult = $mysqli->query($sql);
		mysqli_close($mysqli);

		update_history($admin, "Switched from ".$old_opmode." to ".strtoupper($new)." operating mode" , 'NA', '{"Old" : "'.$old_opmode.'", "New" : "'.strtoupper($new).'"}', 'NA');	
	}
	else{
		$qresult = "None";
	}
	
	return array("error" => $qresult);
	
}


function download_tar($filename){
  header( 'Content-type: archive/tar' );
  header( 'Content-Disposition: attachment; filename="' . basename( $filename ) . '"'  );
  header( 'Content-Transfer-Encoding: binary' );
  header( 'Content-Length: ' . filesize( $filename ) );
  readfile( $filename );

}

function get_systems_plotdelta(){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname); 
	$sql = "SELECT name,origin,plot_delta FROM systems WHERE enabled=1 ORDER BY name ASC";
	$qresult = $mysqli->query($sql);
    mysqli_close($mysqli);	

	render_systems_plotdelta($qresult);
}

function render_systems_plotdelta($systems){
	//get opmode
	$opmode = get_opmode();	
   	while( $rs = mysqli_fetch_assoc($systems) ) {
		$name = $rs['name'];
		$origin = $rs['origin'];
		$plotdelta = $rs['plot_delta'];
		//get config from <system>.conf
		$config = read_json_file(strtolower($name).".conf");

		if($config!=""){
			$opbranch = $config[strtolower($opmode)];
			if($opbranch != ""){
				echo '
				<div class="col-xs-12">
				<label class="col-xs-5 control-label">'.$name.' - '.strtoupper($origin).'</label>
				<div class="col-xs-7"><input name="pd_'.$name.'-'.$origin.'" id="pd_'.$name.'-'.$origin.'" type="number" min="0" class="form-control input-lg" value="'.$plotdelta.'" required/></div>
				</div>';
			}
		}

	}
}


function get_systems_settings($cumulative=True){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);
	if($cumulative){
		$sql = "SELECT name,GROUP_CONCAT(origin) as origin,GROUP_CONCAT(enabled) as enabled FROM systems GROUP BY name ORDER BY name";
	}
	else{
		$sql = "SELECT name, origin, enabled FROM systems ORDER BY name";
	}
	$qresult = $mysqli->query($sql);
    mysqli_close($mysqli);	

	return $qresult;
}

function render_systems_setting($systems){
	//get opmode
	$opmode = get_opmode();	
   	while( $rs = mysqli_fetch_assoc($systems) ) {
		$name = $rs['name'];
		$origin = explode(",",$rs['origin']);
		$enabled = explode(",",$rs['enabled']);
		//get config from <system>.conf
		$config = read_json_file(strtolower($name).".conf");

		if($config==""){
			//missing file
			error_system_json($name,"Missing .conf file");
		}

 		else{
			$opbranch = $config[strtolower($opmode)];
			if($opbranch == ""){
				//missing operating mode key
				error_system_json($name,'Missing configuration for '.$opmode.' operating mode');
			}
			else{
				echo '<tr><td><b>'.$name.'</b></td></tr>';
				for ($i = 0; $i <= sizeof($origin)-1; $i++) {
					//check if origin configuration is set
					$orig_branch = $opbranch[$origin[$i]];
					$disabled = "";
					$checked = "";
					$input_prediv = "";
					$input_postdiv = "";
					$sw_class = "sw_no_tooltip";
					$tooltip = "";
					if($orig_branch==""){
						$disabled = "disabled";
						$input_prediv = '<div class="">';
						$input_postdiv = '</div>';
						$sw_class = "stats-tooltip";
						
						$tooltip = '<span class="tooltiptext">Missing configuration</span>';
						/* error_system_json($name,'Missing configuration', $origin[$i]); */
					}
					else{
						$branch_conf = json_decode($orig_branch);
						if(empty((array)$orig_branch)){
							$disabled = "disabled";
							$sw_class = "stats-tooltip";
							$input_prediv = '<div class="stats-tooltip">';
							$input_postdiv = '<span class="tooltiptext">Missing configuration</span></div>';
							$tooltip = '<span class="tooltiptext">Missing configuration</span>';
							/* error_system_json($name,'Missing configuration', $origin[$i]); */
						}
						else{
							$isenabled = $enabled[$i];
							if($isenabled == "1"){
								$checked = "checked";
							}
						}
					}
							echo '<tr><td></td>';
							echo '<td>'.$origin[$i].'</td>';
							echo '<td>
								<div class="'.$sw_class.'">
								<label class="switch">
									<input name="sw_'.$name.'-'.$origin[$i].'" class="switch-input" type="checkbox" onchange="switch_systems()" '.$checked.' '.$disabled.'/>
									<span class="switch-label" data-on="On" data-off="Off"></span> 
									<span class="switch-handle"></span> 
								</label>
								'.$tooltip.'
								</div>
							</td>';
							echo '</tr>';
				}
			}
		}
	}
}

function error_system_json($name,$msg,$origin=""){
	if($origin==""){
		echo '<tr><td><b>'.$name.'</b></td>';
		echo '<td colspan="2"><div class="stats-tooltip"><img src="assets/images/remove.png" height="35" alt="'.$msg.'"><span class="tooltiptext">'.$msg.'</span></div></td>';
		echo '<td></td>';
		echo '</tr>';
	
	}
	else{
		echo '<tr><td></td>';
		echo '<td>'.$origin.'</td>';
		echo '<td><div class="stats-tooltip"><img src="assets/images/remove.png" height="35" alt="'.$msg.'"><span class="tooltiptext">'.$msg.'</span></div></td>';
		echo '</tr>';
	}
}


function update_systems($data, $admin){
	$out = [];
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];
	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname); 
	$result = True;

	
	//query to get current config
	//check differences with new config
	//add differences to out_hist
	$failed = array();
	$ok = array();	
	foreach($data as $key=>$value)
	{
		$k_split = explode("-", $key, 2);
		$name = $k_split[0];
		$origin = $k_split[1];
		if($value=="true"){
			$enabled = 1;
			$to = "enabled";
			$from = "disabled";
		}else{
			$enabled = 0;
			$from = "enabled";
			$to = "disabled";
		}
		
 		$sql_get = "SELECT enabled FROM systems WHERE name='".$name."' AND origin='".$origin."'";
		$res_query = $mysqli->query($sql_get);
		$rs = mysqli_fetch_assoc($res_query);
		$old_enab = $rs['enabled'];
		if($old_enab != $enabled){
			$sql = "UPDATE systems SET enabled=".$enabled." WHERE name='".$name."' AND origin='".$origin."'";
			$qresult = $mysqli->query($sql);
			if(!$qresult){
				//$result = False;
				//$result[$key] = False;
				$failed[$key] = $from." -> ".$to;				
			}
			else{
				//array_push($ok, $key);
				$ok[$key] = $from." -> ".$to;				
			}
		}
	}
	
	
	if(count($failed)==count($data)){
		$result = False;
	}

	if(count($ok)==0 && count($failed)==0){
		$result = "None";
	}

 	$out_hist = array();
	$final_hist = "NA";
	foreach($ok as $key=>$value){
		array_push($out_hist, strtoupper($key).' : '.$value);
	}
	if(count($out_hist) > 0){
		$final_hist = '{"Updates" : "'.join(",",$out_hist).'"}';
	}


	$failed_hist = array();	
	$final_failed = "NA";	
	foreach($failed as $key=>$value){
		array_push($failed_hist, strtoupper($key).' : '.$value);
	}
	if(count($failed_hist) > 0){
		$final_failed = '{"Failed" : "'.join(",",$failed_hist).'"}';
	}

	if($result){
		update_history($admin, "Systems enabled/disabled" , 'NA', $final_hist, $final_failed);
		
	}	
	
    mysqli_close($mysqli);
	return array("result" => $result);	

}

function update_genset($data, $admin){
	$tmpfile = 'tmp/tmpconf.json';
	$updated = array();
	parse_str($data, $output);
	$config = read_json_file("config.json");
	if($config["offset"] != $output['rep_offset']+0){
		array_push($updated,"Reports offset : ".$config["offset"]." -> ".$output['rep_offset']);
	}
	if($config["history"] != (int)$output['histnum']){
		array_push($updated,"History records : ".$config["history"]." -> ".$output['histnum']);
	}
	if($config["nprocs"] != (int)$output['nprocs']){
		array_push($updated,"Processors number : ".$config["nprocs"]." -> ".$output['nprocs']);
	}
	if($config["admin_email"] != $output['email']){
		array_push($updated,"Communication email : ".$config["admin_email"]." -> ".$output['email']);
	}
	
	$config["offset"] = $output['rep_offset']+0;
	$config["history"] = (int)$output['histnum'];
	$config["nprocs"] = (int)$output['nprocs'];
	$config["admin_email"] = $output['email'];

	//Future: add test email sender???
	
	$jsonerror = 0;	
	$fp = fopen($tmpfile, 'w');
	$written = fwrite($fp, json_encode($config,JSON_PRETTY_PRINT));
	fclose($fp);

	if($written == 4 || $written == false){
		$jsonerror = 1;
	}

	if($jsonerror==0){
		rename("config.json","config.bkp");
		$copied = copy($tmpfile, "config.json");
		if($copied){
			unlink($tmpfile);
			unlink("config.bkp");
		}
		else{
			rename("config.bkp","config.json");
			$jsonerror = 1;
		}
		
	}
	else{
		if(is_file($tmpfile)){
			unlink($tmpfile);
		}
	}

	
	$dberror = 0;
	//query to update plot_delta
	$host = $config["local_db"]['host'];
	$dbuser = $config["local_db"]['user'];
	$dbpwd = $config["local_db"]['password'];
	$dbname = $config["local_db"]['dbname'];
	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname);
	$failed_db = array();
	$pd_num=0;
	$updated_db = array();
	foreach($output as $key=>$value)
	{
		
		$k_split = explode("_", $key);
		$pd = $k_split[0];
		$comp = strcmp($cic, "pd");
		if($pd == "pd"){
			
 	 		$name = explode("-", $k_split[1])[0];
			$origin = explode("-", $k_split[1],2)[1];
			
			//select query to get old value
			$sql_get = "SELECT plot_delta FROM systems WHERE name='".$name."' AND origin='".$origin."'";
			$res_query = $mysqli->query($sql_get);
			$rs = mysqli_fetch_assoc($res_query);
			$old_delta = $rs['plot_delta'];
			if($old_delta != $value){
				$pd_num = $pd_num+1;
			//if old value !=  new value then update db
				$sql = "UPDATE systems SET plot_delta=".$value." WHERE name='".$name."' AND origin='".$origin."'";
				$qresult = $mysqli->query($sql);
				if(!$qresult){
					array_push($failed_db, $name."-".strtoupper($origin." : ".$old_delta." -> ".$value));				
				}
				else{
					//array_push($ok, $key);
					array_push($updated_db, $name."-".strtoupper($origin)." : ".$old_delta." -> ".$value);			
				}				
			}
		}
	}
 	if(count($failed_db)==$pd_num && $pd_num>0){
		$dberror = 1;
	}
	
	$failed = array();
	$out_hist_list = array();
	
	if($jsonerror==1){
		array_push($failed, "Report offset, History records, N.processors, COM email"); 
	}else{
		$out_hist_list = $updated;
	}
	if($dberror==0 && count($updated_db)>0){
		$out_hist_str_db = "Thresholds : ".join(",",$updated_db);
		array_push($out_hist_list, $out_hist_str_db);
	}
	
	if(count($failed_db)>0){
		$failed_str = "Thresholds : ".join(",",$failed_db);
		array_push($failed,$failed_str);
	}

	$out_hist = "NA";
	if(count($out_hist_list)>0){
		$out_hist =	'{"Updates" : "'.join(",",$out_hist_list).'"}';	
	}
	$failed_hist = "NA";
	if(count($failed)>0){
		$failed_hist =	'{"Failed" : "'.join(",",$failed).'"}';	
	}

 	if($dberror==0 || $jsonerror==0){
		update_history($admin, "Webapp settings updated" , 'NA', $out_hist, $failed_hist);
		
	}
	
	if(count($failed)==0 && count($out_hist_list)==0){$jsonerror = 2;}
    mysqli_close($mysqli);
	return array("jsonerr" => $jsonerror, "dberr" => $dberror);
	
	
	
}

function update_smtpset($data,$admin){
	$tmpfile = 'tmp/tmpsmtpconf.json';
	parse_str($data, $output);
	$config = read_json_file("smtp.json");
	//check which confs have been modified
 	$out_hist = array();
	$final_hist = "NA";
	if($config["host"] != $output['conf_host']){
		array_push($out_hist, 'Host : '.$config["host"].' -> '.$output['conf_host']);
	}
	if($config["port"] != (int)$output['conf_port']){
		array_push($out_hist, 'Port : '.$config["port"].' -> '.$output['conf_port']);
	}
	if($config["user"] != $output['conf_user']){
		array_push($out_hist, 'User : '.$config["user"].' -> '.$output['conf_user']);
	}
	if($config["password"] != $output['conf_pwd']){
		array_push($out_hist, 'Password : '.$config["password"].' -> '.$output['conf_pwd']);
	}
	
	if(count($out_hist) > 0){
		$final_hist = '{"Updates" : "'.join(",",$out_hist).'"}';
	}
	
	$config["host"] = $output['conf_host'];
	$config["port"] = (int)$output['conf_port'];
	$config["user"] = $output['conf_user'];
	$config["password"] = $output['conf_pwd'];

	$error = 0;	
	$fp = fopen($tmpfile, 'w');
	$written = fwrite($fp, json_encode($config,JSON_PRETTY_PRINT));
	fclose($fp);

	if($written == 4 || $written == false){
		$error = 1;
	}

 	if($error==0){
		rename("smtp.json","smtp.bkp");
		$copied = copy($tmpfile, "smtp.json");
		if($copied){
			unlink($tmpfile);
			unlink("smtp.bkp");
		}
		else{
			rename("smtp.bkp","smtp.json");
			$error = 1;
		}
		
	}
	else{
		if(is_file($tmpfile)){
			unlink($tmpfile);
		}
	}
	if($error==0){
		update_history($admin, "SMTP configuration updated" , 'NA', $final_hist, 'NA');	
	}
	return array("error" => $error);

}

function test_smtp($data, $to){
//	require("PHPMailer/src/PHPMailer.php");
//	require("PHPMailer/src/SMTP.php");
	require(__DIR__ ."/PHPMailer/src/PHPMailer.php");
	require(__DIR__ ."/PHPMailer/src/SMTP.php");
	require(__DIR__ ."/PHPMailer/src/Exception.php");
	$error = 0;
	parse_str($data, $output);
	$host = $output['conf_host'];
	$port = (int)$output['conf_port'];
	$user = $output['conf_user'];
	$pwd = $output['conf_pwd'];
	$mail_admin = read_admin_json("config.json");
	//get user email
	$config = read_config_json("config.json");
	$dbhost = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];
	
	$mysqli = new mysqli($dbhost, $dbuser, $dbpwd, $dbname); 
	$sql = "SELECT email FROM members WHERE username ='".$to."'";
	$qresult = $mysqli->query($sql);
	if(!$qresult){
		$error = 1;
	}
	else{
		$rs = mysqli_fetch_assoc($qresult);
		$email = $rs['email'];
		
		$subject = "SMTP Testing Email";  
	  
		$msg='<p>Dear '.$to.',</p>';
		$msg.='<p>This is an email to test AIDA SMTP Configuration</p>';
		$msg.='<p>You have received it, then SMTP configuration is ok.</p>';
		$msg.='<br/><p>Thanks,<br/>';
		$msg.='The IOT</p>';  

		/* Create a new PHPMailer object. Passing TRUE to the constructor enables exceptions. */
		//$mail = new PHPMailer(TRUE);
		$mail = new PHPMailer\PHPMailer\PHPMailer();		
		try {
			$mail->IsSMTP(); // Utilizzo della classe SMTP al posto del comando php mail()
			
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
				$mail->SMTPAuth = true; // Autenticazione SMTP
			}
			$mail->Host = $host;
			$mail->Port = $port;
			if($port==465){
				$mail->SMTPSecure = 'ssl';
			}
			else{
				$mail->SMTPSecure = 'tls';
			}
			$mail->IsHTML(true); 
			$mail->Username = $user; // Nome utente SMTP autenticato
			$mail->Password = $pwd; // Password account email con SMTP autenticato
			
			/*!!!NOTE: GMAIL require to enable unsecure apps*/
						
						
		   /* Set the mail sender. */
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
		
	}
	
	
	
    mysqli_close($mysqli);
	return array("error" => $error);

}


function get_cols_from_db($tbl, $cols="*", $stat="",$ordercol=""){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname); 
	$sql = "SELECT ".$cols." FROM ".$tbl;
	if($stat!=""){
		$sql .= " ".$stat;
	}
	if($ordercol!=""){
		$sql.=" ORDER BY ".$ordercol." ASC";		
	}
	$qresult = $mysqli->query($sql);
    mysqli_close($mysqli);	
	
	return $qresult;
}

function get_parameter_group($sys, $origin, $subs){
	$config = read_config_json("config.json");
	$host = $config['host'];
	$dbuser = $config['user'];
	$dbpwd = $config['password'];
	$dbname = $config['dbname'];	
	$mysqli = new mysqli($host, $dbuser, $dbpwd, $dbname); 
 	$sql = "SELECT extra FROM ".$origin."_".strtolower($sys)."_params WHERE subsystem='".$subs."' GROUP BY extra ORDER BY extra ASC";

	$qresult = $mysqli->query($sql);
	$out = "";
	if (mysqli_num_rows($qresult) > 0){
		#$row = $qresult->fetch_row();
 		while ($row = mysqli_fetch_array($qresult))
		{
			$out .= '<option value="'.$row['extra'].'">'.$row['extra'].'</option>';
		}
	}
	else{$out = "No fields were found!";}
    mysqli_close($mysqli);	
	echo $out;
}


?>