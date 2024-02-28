<?php
include("functions.php");

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['files'])) {
        $errors = [];
		$extensions = ['json'];
		$username = $_POST['username'];
		$period = $_POST['period'];
		$t_custom = $_POST['t_custom'];
		$file_name = $_FILES['files']['name'][0];
		$file_tmp = $_FILES['files']['tmp_name'][0];
		$file_type = $_FILES['files']['type'][0];
		$file_size = $_FILES['files']['size'][0];

		$file_ext = explode('.', $file_name);
		$f = $file_ext[0];
		$file_ext = strtolower(end($file_ext));
		
		$today = gmdate('Y-m-d H:i:s');
		$todaystr = str_replace(array("-",":"), "", $today);
		$todaystr = str_replace(array(" "), "_", $todaystr);
		
		//check file extension
		if ($file_type=="") {
					$file_type = $file_ext;
			}
		if (!in_array($file_ext, $extensions)) {
			$errors['msg'] = 'Extension not allowed: ' . $file_name . ' (' . $file_type . ')';
			$errors['status'] = 'failed';
		}
		
		//Try to upload
		if (empty($errors)) {
			$newname = checkname($file_name, "config");
			$file_name = $newname[0];
			$file = $newname[1];
			$changename = $newname[2];

			$uploaded = move_uploaded_file($file_tmp, $file);
			
			if($uploaded){
				#load file content
				if($changename==0){
					$errors['msg'] = 'All OK';
					$errors['status'] = 'success';
					$errors['filename'] = $file_name;

				}
				else{
					$errors['msg'] = 'A file with name '.$_FILES['files']['name'][0]." already exists. The new file has been changed in ".$file_name;
					$errors['status'] = 'warning';
					$errors['filename'] = $file_name;

				}
			}else{
				$errors['msg'] = 'Unable to upload the file. Try later. If the problem persists please contact AIDA admin.';
				$errors['status'] = 'failed';
			}
		}
		
		// Try to update DB and check file integrity
		if($errors['status'] != 'failed'){
			$r = update_configlist($file_name, "config", $username, $today, $period, $t_custom, "upload", $_FILES['files']['name'][0], 1, "upload");
			$conn_err =$r[0];
			$data_err = $r[1];
			$isrunning = $r[2];
			if($conn_err == false){
				//check connection
				$errors['status']='failed';
				$errors['msg'] = "Impossible to store configuration data in the local DB. Try later. If the problem persists please contact AIDA admin.";
			}
			else if($data_err <> ""){
				$errors['status']='failed';
				$errors['msg'] = $data_err;
			}
			else
			{
				$id = update_history($username, "Uploaded config file. Report generation launched.", 'NA', '{"period" : "'.ucfirst($period).'", "configuration file" : "'.$file_name.'"}','NA');
				$errors['histid'] = $id;
				$errors['isrunning'] = $isrunning;
			}
		}
		
		echo json_encode($errors);
	}
}
?>