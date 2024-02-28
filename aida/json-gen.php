<?php
include("functions.php");
error_reporting(0);
if(isset($_POST['action']) && !empty($_POST['action'])) {
	$action = $_POST['action'];
	//generate report configuration file from form or upload
	switch($action) {
		case 'new_from_form' : {
			$myfilename = "config_template.json";
			if(file_exists($myfilename)){
				$res = file_get_contents($myfilename);
				$err = 0;
			}
			else{
				$res = "Impossible to load JSON template file. Please contact AIDA admin.";
				$err = 1;
			}
			if($err == 0){
				//get configuration values
				$period = $_POST['period'];
				$t = str_replace(" ", "T", $_POST['tstart']);
				$sampling = $_POST['sampling'];
				$dts = $_POST['dts'];
				$sfunc = $_POST['sfunc'];
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
						$window = $_POST['t_window'];
						break;
					}
					case "custom":{
						$window = $_POST['dtcustom'];
						break;
					}
				}
				$nacq = $_POST['nacq'];
				$dtacq = $_POST['dtacq'];
				$general = '"Start Time": "'.$t.'",
	"Time Window": '.$window.',';
				if($period == "ondemand"){$general = $general.'
	"Number of acquisitions": '.$nacq.',';
				}
				$general = $general.'
	"Sampling": "'.$sampling.'"';
			if($dts != ""){
				$general = $general.',
	"Sampling period" : '.$dts;
			}
			if($sampling == "by function"){
				$general = $general.',
	"Sampling function" : "'.$sfunc.'"';
			}
			if($dtacq != ""){$general = $general.',
	"Acquisition time step" : '.$dtacq;}

				$result = get_systems_settings();
				#create json string to append in template
				$sysstr = array();
				while ($row = mysqli_fetch_array($result))
				{
					$name = $row['name'];
					$origin = explode(",", $row['origin']);;
					$enabled = explode(",", $row['enabled']);;
					$str_origin="";
					$orig_array = array();
					for($i=0; $i<count($origin);$i++){
						$curr_o = $origin[$i];
						$curr_e = $enabled[$i];
						if($curr_e==1){		//calibration exclusion is temporary
							array_push($orig_array,$curr_o);
						}
					}
					for($i=0; $i<count($orig_array);$i++){
							$str_origin .= "\t\t";
							$str_origin .= '"'.strtoupper($orig_array[$i]).'"	:	{}';
							if($i!=count($orig_array)-1){$str_origin.=",";}
							$str_origin.="\n";							
					}
					if($str_origin!=""){
						$s0 = '"'.$name.'"	:	{';
						if($name!="QLA"){
							$s0 .= "\n";
							$s0 .= $str_origin;
							$s0 .= "\t}";
						}else{
						   $s0 .= "}"; 
						}
						array_push($sysstr, $s0);
					}
				}
				$sysjson = implode(",\n\t", $sysstr);
				$res = str_replace('"Info" : ""', $general, $res);
				$res = str_replace('"SYSTEM" : ""', $sysjson, $res);
				break;
			}
		}
		case 'load_from_file' : {
			$myfilename =$_POST['filename'];
			$path = "users/tempconfig";
			if(file_exists("users/tempconfig/".$myfilename)){
				$res = file_get_contents("users/tempconfig/".$myfilename);
				$err = 0;
			}
			else if(file_exists("users/config/".$myfilename)){
				$res = file_get_contents("users/config/".$myfilename);
				$err = 0;
			}
			else{
				$res = "Impossible to load temporary configuration file. Please contact AIDA admin.";
				$err = 1;
			}
			break;
		}
	}
	echo $res;
}

?>