<?php
	include("functions.php");
	$out=[];
	$file_name = $_POST['file'];
	$text = $_POST['jsontext'];
	$period = $_POST['period'];
	$username = $_POST['user'];
	$path = $_POST['path'];
	$page = $_POST['page'];
	$t_custom = $_POST['cust_val'];
	$action = $_POST['action'];
	
  	$file_ext = explode('.', $file_name);
	$fname = $file_ext[0];
	$file_ext = strtolower(end($file_ext));
		
	$today = date('Y-m-d H:i:s');
	$todaystr = str_replace(array("-",":"), "", $today);
	$todaystr = str_replace(array(" "), "_", $todaystr);

		
	//Try to upload
		if($page == "new"){
			$newname = checkname($file_name, $path);
			$fname = $newname[0];
			$file = $newname[1];
			$changename = $newname[2];
		}
 		else
		{
			$fname = $file_name;
			$file = 'users/'.$path.'/'.$file_name;
			$changename = 0;
		}


		//save file
		$f = fopen($file, 'w');
		fwrite($f, $text);
		fclose($f);

		//check if file has been saved
		$filelist = scandir("users/".$path);
		$isfile = in_array($fname, $filelist);
		
		if($isfile){
			if($changename==0){
				$out['msg'] = 'All OK';
				$out['status'] = 'success';
			}
			else{
				$out['msg'] = 'A file with name '.$file_name." already exists. The new file has been changed in ".$fname;
				$out['status'] = 'warning';
			}
		}else{
			$out['msg'] = 'Unable to create the file on repository. Try later. If the problem persists please contact AIDA admin.';
			$out['status'] = 'failed';
		}
		
		// Try to update DB and check file integrity
		if($out['status'] != 'failed'){
			$r = update_configlist($fname, $path, $username, $today, $period, $action, $t_custom, $page, $file_name);
			$conn_err =$r[0];
			$data_err = $r[1];
 			if($conn_err == false){
				
				//check connection
				$out['status']='failed';
				$out['msg'] = "Impossible to store configuration data in the local DB. Try later. If the problem persists please contact AIDA admin.";

				
			}
			else if($data_err <> ""){
				//check file integrity
				$out['status']='failed';
				$out['msg'] = $data_err;
			}
			else
			{
				$msg = "Created ".$period." config file";
				
				
				//Remove temporary file if new run has been created
				if($page == "edit"){
					$con = new_conn_from_file("config.json");
					$sql1 = "SELECT id FROM tempconfig_files WHERE (filename = '$fname')";
					$res1 = $con -> query($sql1);
					$row = mysqli_fetch_assoc($res1);
					$id = $row['id'];
					delete_file($id, $file_name, 'tempconfig');
			
					
					$con->close();
				}
			}
			$out['file']=$fname;
		}
		
	echo json_encode($out);
?>