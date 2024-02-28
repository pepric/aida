<?php
	include("functions.php");
	$out=[];
	$file_name = $_POST['file'];
	$text = $_POST['jsontext'];
	$period = $_POST['period'];
	$username = $_POST['user'];
	//$path = $_POST['path'];
	$iscomplete = $_POST['iscomplete'];
	$path = "config";
	$page = $_POST['page'];
	$t_custom = $_POST['cust_val'];
	$action = $_POST['action'];
	//$extensions = ['json'];
		
  	$file_ext = explode('.', $file_name);
	$fname = $file_ext[0];
	$file_ext = strtolower(end($file_ext));
		
	$today = gmdate('Y-m-d H:i:s');
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
				$out['msg'] = 'A file with name '.$file_name." already exists. The new file has been changed in ".$fname.". ";
				$out['status'] = 'warning';
			}
		}else{
			$out['msg'] = 'Unable to create the file on repository. Try later. If the problem persists please contact AIDA admin.';
			$out['status'] = 'failed';
		}
		
		// Try to update DB and check file integrity
		if($out['status'] != 'failed'){
			$r = update_configlist($fname, $path, $username, $today, $period, $t_custom, $page, $file_name, $iscomplete, $action);
			$conn_err =$r[0];
			$data_err = $r[1];
			$isrunning = $r[2];
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
				if($page == "edit"){
					$msg = "Updated ".$period." config file. ";
				}
				else{
					$msg = "Created ".$period." config file. ";
				}
				if($isrunning==0){
                  	if($iscomplete=="1"){
                  		$msg .= "Configuration completed.";
                    }
                  	else{
                    	$msg .= "Config not completed.";
                    }
                }
             	else{
                	$msg .= "Report generation launched.";}
             	

				update_history($username, $msg , 'NA', '{"period": "'.ucfirst($period).'", "configuration file" : "'.$fname.'"}', 'NA');

			}
			$out['file']=$fname;
			$out['isrunning']=$isrunning;
		}
		
	echo json_encode($out);
?>