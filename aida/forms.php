<?php include("functions.php");

$plot = $_POST["p"];
$origin = $_POST["o"];
$source = $_POST["s"];


class Render{
	
	protected function add_label($id="",$for="",$style="",$class="col-md-2 control-label",$text="Parameters"){
		$res = '<label id="'.$id.'" for="'.$for.'" style="'.$style.'" class="'.$class.'">'.$text.'</label>';
		return $res;
	}
	
	protected function render_bins_div(){
		$div='<div class="form-group" id="bins" style="display:none;">';
		$div .= $this->add_label("","","","col-md-2 control-label","Bin size/Number of Bins");
				/* <label class="col-md-2 control-label">Bin size/Number of Bins</label> */
		$div .=' <div class="col-md-10">
					<div class="col-md-2">
						<div class="form-check form-check-inline">
							<input class="form-check-input" type="radio" name="bintype" id="bintype1" value="binsize" checked>';
		$div .= $this->add_label("","bintype1","","form-check-label"," Bin Size");
							/* <label class="form-check-label" for="bintype1">Bin Size</label> */
		$div .='</div>
					<div class="form-check form-check-inline">
						<input class="form-check-input" type="radio" name="bintype" id="bintype2" value="binnumber">';
		$div .= $this->add_label("","bintype2","","form-check-label"," Number of Bins");
						/* <label class="form-check-label" for="bintype2">Number of Bins</label> */
		$div .='</div>
				</div>
				<div class="col-md-10 ">
					<input type="number" id="binsize" name="binsize" class="form-control" placeholder="Set bin size..." min="0.000000000000001" required></input>
				</div>
			</div>';
		return $div;
	}	

	protected function render_more_btns($add_arg,$display=false){
		$style="";
		if(!$display){
			$style='style="display:none;"';
		}
		$res='<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" '.$style.' id = "addmore" onclick="addmore_btn('.$add_arg.')">Add more...</button>
			  <button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" style="display:none;" id = "remove" onclick="remove_btn()">Remove Last...</button>';
		return $res;
	}

	protected function render_extra_btns($coord, $display){
		
		$div =	'<div style="display:'.$display.'">                             
				<span class ="extra_filters_btn" id="'.$coord.'_extra_filters_btn_show" style="display:none" onclick="show_extra_filters(\''.$coord.'\')"><a>Extra Filters</a></span>
				<span class ="extra_filters_btn" id="'.$coord.'_extra_filters_btn_hide" style="display:none" onclick="hide_extra_filters(\''.$coord.'\')"><a>Hide Extra Filters</a></span>
				</div>';
		return $div;	
	}

	protected function render_partype($coord, $extra,$display=false){
		
		//AGGIUNGERE SUBSYSTEM E FARE QUERY PER FILTRI
		
		$style="";
		if(!$display){
			$style='style="display:none;"';
		}	
		$res = '<select id = "'.$coord.'-partype" name="'.$coord.'-partype" class="form-control" '.$style.' onchange="refresh_params(this)" >
				<option value="" disabled selected>Select Field</option>'.$extra.'</select>';
		return $res;
	}

	protected function render_params_select($coord,$onchange, $display=false, $text="Parameter", $cols=""){
		$style="";
		if(!$display){
			$style='style="display:none;"';
		}

		$res = '<select id = "'.$coord.'-params" name="'.$coord.'-params" class="form-control" '.$style.' onchange="'.$onchange.'" >
					<option value="" disabled selected>'.$text.'</option>'.$cols.'
				</select>';
		return $res;
		
	}

	protected function render_values_select($coord){
		$res = '<select id="'.$coord.'-values" name="'.$coord.'-values" style="display:none"></select>';
		return $res;
	}

	protected function render_main_select($id, $display=false, $onchange="", $disabled_opt="", $all=false, $options=""){
		$style="";
		if(!$display){
			$style='style="display:none;"';
		}
		
		$res='<select id = "'.$id.'" name="'.$id.'" class="form-control" '.$style.' onchange="'.$onchange.'" required >';
		if($disabled_opt != ""){
			$res .= '<option value="" disabled selected>'.$disabled_opt.'</option>';
		}
		if($all){
			$res .= '<option value="ALL">ALL</option>';
		}
		
		if($options != ""){
			$res .= $options; 		
		}
		$res .= '</select>';
		return $res;
		
	}

	protected function render_extra_filters($id, $text, $tag, $style=""){
		$pieces = explode("_", $id);
		$id_label = $pieces[0]."l";
		if($style!=""){
			$span = '<span style="'.$style.'">';
			$end_span='</span>';
		}
		else{
			$span="";
			$end_span="";
		}
		switch($tag){
			case "input" : {
				$type = 'type="text"';
				$cols = "30";
				break;    
			}
			case "textarea" : {
				$type = '';
				$cols = "15";			
				break;    
			}
		}
		$res = $span."<label id=".$id_label." for=".$id.">".$text."</label>";
		$res .= "<".$tag." ".$type." cols=".$cols." id=".$id." name=".$id." value=''></".$tag.">".$end_span;
		return $res;		
	}

	protected function render_adubox($coord, $display){
		$res = '<div style="display:'.$display.'">
					<div id="'.$coord.'-adu_check" style="display:none; margin-right: 30px;">
						<input type="checkbox" id="'.$coord.'-adu_cal" name="'.$coord.'-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span>
						<div class="stats-tooltip">
							<img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
							<div id="units" style="display:none"></div>
					</div>
				</div>';
		return $res;
	}
	
	protected function close_div($n=1){
		$res="";
		$i=1;
		while($i <= $n){
			$res .="</div>";
			$i++;
		}
		return $res;
		
	}
	
	protected function create_div($id,$class="form-group",$style="display:block"){
		$res='<div class="'.$class.'" id="'.$id.'" style="'.$style.'">';
		return $res;
	}
}


/*Plot classes*/
class Trend{

	public function call_source($source, $origin, $settings, $repo_set){
		//Instantiate source class
    	$s = new ReflectionClass(ucfirst($source));
      	$object = $s->newInstanceWithoutConstructor();
		//Render plot form
      	$result = $object -> render_trend_form($origin, $settings, $repo_set);
    	return $result;
    }  
}

class Scatter{
  
	public function call_source($source, $origin, $settings, $repo_set){
		//Instantiate source class
    	$s = new ReflectionClass(ucfirst($source));
      	$object = $s->newInstanceWithoutConstructor();
		//Render plot form
      	$result = $object -> render_scatter_form($origin, $settings, $repo_set);
    	return $result;
    } 

}

class Histogram{
  
	public function call_source($source, $origin, $settings, $repo_set){
		//Instantiate source class
    	$s = new ReflectionClass(ucfirst($source));
      	$object = $s->newInstanceWithoutConstructor();
		//Render plot form
      	$result = $object -> render_hist_form($origin, $settings, $repo_set);
    	return $result;
    } 

}


class Stats{
  
	public function call_source($source, $origin, $settings, $repo_set){
		//Instantiate source class
    	$s = new ReflectionClass(ucfirst($source));
      	$object = $s->newInstanceWithoutConstructor();
		//Render stats form
      	$result = $object -> render_stats_form($origin, $settings, $repo_set);
    	return $result;
    } 

}

class Image{
  
	public function call_source($source, $origin, $settings, $repo_set){
		//Instantiate source class
    	$s = new ReflectionClass(ucfirst($source));
      	$object = $s->newInstanceWithoutConstructor();
		//Render plot form
      	$result = $object -> render_image_form($origin, $settings, $repo_set);
    	return $result;
    } 

}


class EFD extends Render{

	function render_hist_form($origin, $settings, $repo_set){
		$keys = array_keys($repo_set["required"]);       
		ob_start();
       	populate_dropdown($origin."_efd_params", "extra", "", $distinct = 1);
		$extra = ob_get_clean(); 
		$dd = create_option($repo_set, 0);
		//$result='<div class="form-group" id="yparams" style="display:block">';
		$result = $this->create_div("yparams");
		$result.=$this->add_label("y-label","","display:block","col-md-2 control-label","Parameters");
		$result .= $this->create_div("y0-par-form","col-md-10");
		$result .= $this->render_main_select("y0-ic", true, "set_sys_options(this,true)", "Select ".ucfirst($keys[0]), false, $dd);																				
		$result .= $this->render_main_select("y0-sys", false, "set_par_options(this)", "Select Field", false,"");
		$result .= $this->render_params_select("y0", "populate_values(this)");
		$result .= $this->render_values_select("y0");
		$result .= $this->render_extra_btns("y0",$settings["extra"]); 							
		$result .= $this->render_more_btns("1");
		$result .= $this->create_div("y0_extra_filters","col-md-12 extra_filters","display:none");
		$result .= $this->render_extra_filters("y0_DataSetRelease", "DataSetRelease", "input", "display:".$settings["dsr"]);
		$result .= $this->close_div(3);
		$result .= $this->render_bins_div() .'</div>';
    	return $result;
    }
  
	function render_scatter_form($origin, $settings, $repo_set){
		$keys = array_keys($repo_set["required"]);      
		ob_start();
		populate_dropdown($origin."_efd_params", "extra", "extra NOT LIKE 'full_%'", $distinct = 1);
		$extra = ob_get_clean(); 
		$dd = create_option($repo_set, 0);      
		$result = $this->create_div("params");
		$result.=$this->add_label("","","display:block","col-md-2 control-label","X axis parameter");
		$result .= $this->create_div("x-par-form","col-md-10");
		$result .= $this->render_main_select("x-ic", true, "set_sys_options(this,true)", "Select ".ucfirst($keys[0]), false, $dd);																				
		$result .= $this->render_main_select("x-sys", false, "set_par_options(this)", "Select Field", false,"");		

		$result .= $this->render_params_select("x", "populate_values(this)");
		$result .= $this->render_values_select("x");
		$result .= $this->render_extra_btns("x",$settings["extra"]);							
		$result .= $this->create_div("x_extra_filters","col-md-12 extra_filters","display:none");					
		$result .= $this->render_extra_filters("x_DataSetRelease", "DataSetRelease", "input", "display:".$settings["dsr"]);
		$result .= $this->close_div(3);
		
		
		$result .= $this->create_div("yparams");
		$result.=$this->add_label("y-label","","display:block","col-md-2 control-label","Y axis parameters");
					/* <label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label> */
		//$result .= '<div id="y0-par-form" class="col-md-10">';
		$result .= $this->create_div("y0-par-form","col-md-10");
		$result .= $this->render_main_select("y0-ic", true, "set_sys_options(this,true)", "Select ".ucfirst($keys[0]), false, $dd);																				
		$result .= $this->render_main_select("y0-sys", false, "set_par_options(this)", "Select Field", false,"");
		$result .= $this->render_partype("y0", $extra);
		$result .= $this->render_params_select("y0", "populate_values(this)");
		$result .= $this->render_values_select("y0");
		$result .= $this->render_extra_btns("y0",$settings["extra"]);							
		$result .= $this->render_more_btns("1");
		//$result .= '<div id="y0_extra_filters" class="col-md-12 extra_filters" style="display:none">';
		$result .= $this->create_div("y0_extra_filters","col-md-12 extra_filters","display:none");
		$result .= $this->render_extra_filters("y0_DataSetRelease", "DataSetRelease", "input", "display:".$settings["dsr"]);
/* 						<span style="display:'.$settings["dsr"].'">
						<label id="y0l" for="y0_DataSetRelease">DataSetRelease</label><input type="text" cols="30" id="y0_DataSetRelease" name="y0_DataSetRelease" value=""></input>
						</span> */
		$result .= $this->close_div(3);/* '</div> 						
				</div>
			</div>'; */
    	return $result;
    }

	function render_stats_form($origin, $settings, $repo_set){
		$keys = array_keys($repo_set["required"]);       
		ob_start();
       	populate_dropdown($origin."_efd_params", "extra", "", $distinct = 1);
		$extra = ob_get_clean(); 
		$dd = create_option($repo_set, 0);
		//$result='<div class="form-group" id="yparams" style="display:block">';
		$result = $this->create_div("yparams");
		$result.=$this->add_label("y-label","","display:block","col-md-2 control-label","Parameters");
		$result .= $this->create_div("y0-par-form","col-md-10");
		$result .= $this->render_main_select("y0-ic", true, "set_sys_options(this,true)", "Select ".ucfirst($keys[0]), false, $dd);																				
		$result .= $this->render_main_select("y0-sys", false, "set_par_options(this)", "Select Field", false,"");
		$result .= $this->render_params_select("y0", "populate_values(this)");
		$result .= $this->render_values_select("y0");
		$result .= $this->render_extra_btns("y0",$settings["extra"]); 							
		$result .= $this->render_more_btns("1");
		$result .= $this->create_div("y0_extra_filters","col-md-12 extra_filters","display:none");
		$result .= $this->render_extra_filters("y0_DataSetRelease", "DataSetRelease", "input", "display:".$settings["dsr"]);
		$result .= $this->close_div(3);
    	return $result;
    }  
  
	function render_trend_form($origin, $settings, $repo_set){
		$keys = array_keys($repo_set["required"]);  
		ob_start();
		populate_dropdown($origin."_efd_params", "extra", "", $distinct = 1);
		$extra = ob_get_clean();      
		$dd = create_option($repo_set, 0);
		//$result='<div class="form-group" id="yparams" style="display:block">';
		$result = $this->create_div("yparams");
		$result.=$this->add_label("y-label","","display:block","col-md-2 control-label","Y axis parameters");
				/* <label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label> */
		//$result.='<div id="y0-par-form" class="col-md-10">';
		$result .= $this->create_div("y0-par-form","col-md-10");
/* 		$result .= $this->render_main_select("y0-sys", true, "set_params(this,true)", "Select ".ucfirst($keys[0]), false, $dd); */
		$result .= $this->render_main_select("y0-ic", true, "set_sys_options(this,true)", "Select ".ucfirst($keys[0]), false, $dd);
		
		
		$result .= $this->render_main_select("y0-sys", false, "set_par_options(this)", "Select Field", false,"");
		
		
/* 					<select id = "y0-sys" onchange="set_params(this)" class="form-control" >
                      	<option value="" disabled selected>Select '.ucfirst($keys[0]).'</option>'.$dd.'</select>'; */
		
		#METTERE OPZIONE SUBSYSTEM OPPURE IN SET PARAMS  VEDI SET_PARGROUP JAVASCRIPT
		/* $result .= $this->render_partype("y0", $extra); */
		$result .= $this->render_params_select("y0", "populate_values(this)");
		$result .= $this->render_values_select("y0");
		$result .= $this->render_extra_btns("y0",$settings["extra"]);							
		$result .= $this->render_more_btns("1");
		//$result .= '<div id="y0_extra_filters" class="col-md-12 extra_filters" style="display:none">';
		$result .= $this->create_div("y0_extra_filters","col-md-12 extra_filters","display:none");
		$result .= $this->render_extra_filters("y0_DataSetRelease", "DataSetRelease", "input", "display:".$settings["dsr"]);
/* 						<span style="display:'.$settings["dsr"].'">
						<label id="y0l" for="y0_DataSetRelease">DataSetRelease</label><input type="text" cols="30" id="y0_DataSetRelease" name="y0_DataSetRelease" value=""></input>
						</span> */
		$result .= $this->close_div(3);/* '</div> 					
				</div>
			</div>'; */
    	return $result;
    }
}






class Fake{

	function render_hist_form($origin, $settings, $repo_set){
		$keys = array_keys($repo_set["required"]);       
	    if($origin=="hktm"){
			$dd = create_option($repo_set, 0);
			$result='<div class="form-group" id="yparams" style="display:block">
						<label style="display:block" class="col-md-2 control-label" id = "y-label">Parameters</label>
						<div id="y0-par-form" class="col-md-10">
							<select id = "y0-sys" onchange="set_params(this)"  class="form-control" >
                            	<option value="" disabled selected>Select '.ucfirst($keys[0]).'</option>'.$dd.'</select>
							<select id = "y0-params" name="y0-params"  class="form-control" style="display:none" onchange="populate_values(this); show_adu_checkbox(this)" required>
								<option value="" disabled selected>Parameter</option></select>
							<select id="y0-values" name="y0-values" style="display:none"></select>
                            <div style="display:'.$settings["adubox"].'">
                            	<div id="y0-adu_check" style="display:none; margin-right: 30px;">
                                	<input type="checkbox" id="y0-adu_cal" name="y0-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
                                	<div id="units" style="display:none"></div>
								</div>
                            </div>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;" onclick="addmore_btn(1)">Add more...</button>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
						</div>
					</div>
                   	<div class="form-group" id="bins" style="display:none;">
						<label class="col-md-2 control-label">Bin size/Number of Bins</label>
						<div class="col-md-10">
							<div class="col-md-2">
								<div class="form-check form-check-inline">
									<input class="form-check-input" type="radio" name="bintype" id="bintype1" value="binsize" checked>
									<label class="form-check-label" for="bintype1">Bin Size</label>
								</div>
							<div class="form-check form-check-inline">
								<input class="form-check-input" type="radio" name="bintype" id="bintype2" value="binnumber">
								<label class="form-check-label" for="bintype2">Number of Bins</label>
							</div>
						</div>
						<div class="col-md-10 ">
							<input type="number" id="binsize" name="binsize" class="form-control" placeholder="Set bin size..." min="0.000000000000001" required></input>
						</div>
					</div>
				</div>';
    	}
    	else{
			$option1 = create_option($repo_set, 0);
			$option2 = create_option($repo_set, 1);          
			ob_start();
       	 	populate_dropdown($origin."_nisp_params", "extra", "", $distinct = 1);
			$extra = ob_get_clean();			          
    		$result = '<div class="form-group" id="yparams" style="display:block">
						<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
						<div id="y0-par-form" class="col-md-10">
							<select id = "y0-ic" class="form-control" >
                		      	<option value="" disabled selected>Select '.strtoupper($keys[0]).'</option>
                                <option value="ALL">ALL</option>'.$option1.'</select>
							<select id = "y0-sys" onchange="set_params(this)" class="form-control" >
       			               	<option value="" disabled selected>Select '.strtoupper($keys[1]).'</option>
                                <option value="ALL">ALL</option>'.$option2.'</select>                      

							<select id = "y0-partype" name="y0-partype" class="form-control" style="display:none" onchange="refresh_params(this)" >
								<option value="" disabled selected>Parameter filter</option>'.$extra.'
							</select>	
							<select id = "y0-params" name="y0-params" class="form-control" style="display:none" onchange="show_adu_checkbox(this)">
								<option value="" disabled selected>Parameter</option>
							</select>                            
							<select id="y0-values" name="y0-values" style="display:none"></select>
                            <div style="display:'.$settings["adubox"].'">                             
                                <div id="y0-adu_check" style="display:none; margin-right: 30px;">
                                        <input type="checkbox" id="y0-adu_cal" name="y0-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
                                        <div id="units" style="display:none"></div>
                                </div>  
                            </div>
                         	<div style="display:'.$settings["extra"].'">                             
                                <span class ="extra_filters_btn" id="y0_extra_filters_btn_show" style="display:none" onclick="show_extra_filters(\'y0\')"><a>Extra Filters</a></span>
                                <span class ="extra_filters_btn" id="y0_extra_filters_btn_hide" style="display:none" onclick="hide_extra_filters(\'y0\')"><a>Hide Extra Filters</a></span>
							</div>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;" onclick="addmore_btn(2)">Add more...</button>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
     			            <div id="y0_extra_filters" class="col-md-12 extra_filters" style="display:none">
                		    	<label id="y0l" for="y0_pid1">PID</label><textarea cols="15" id="y0_pid1" name="y0_pid1" value=""></textarea>
<!--                   			 	<label for="y0_pid2">PID2</label><input type="text" id="y0_pid2" name="y0_pid2" value="">-->
                		    </div>
						</div>
					</div>
                   	<div class="form-group" id="bins" style="display:none;">
						<label class="col-md-2 control-label">Bin size/Number of Bins</label>
						<div class="col-md-10">
							<div class="col-md-2">
								<div class="form-check form-check-inline">
									<input class="form-check-input" type="radio" name="bintype" id="bintype1" value="binsize" checked>
									<label class="form-check-label" for="bintype1">Bin Size</label>
								</div>
							<div class="form-check form-check-inline">
								<input class="form-check-input" type="radio" name="bintype" id="bintype2" value="binnumber">
								<label class="form-check-label" for="bintype2">Number of Bins</label>
							</div>
						</div>
						<div class="col-md-10 ">
							<input type="number" id="binsize" name="binsize" class="form-control" placeholder="Set bin size..." min="0.000000000000001" required></input>
						</div>
					</div>
				</div>';
    	}
    	return $result;
    }
  
	function render_scatter_form($origin, $settings, $repo_set){
		$keys = array_keys($repo_set["required"]);      
	    if($origin=="hktm"){
			$options = create_option($repo_set, 0);
			$result='<div class="form-group" id="params" style="display:block">
						<label style="display:block" class="col-md-2 control-label" >X axis parameter</label>
						<div id="x-par-form" class="col-md-10">
							<select id = "x-sys" class="form-control" onchange = "set_params(this)" required>
								<option value="" disabled selected>Select X</option>'.$options.'</select>
							<select id = "x-params" name="x-params" class="form-control" style="display:none" onchange="populate_values(this); show_adu_checkbox(this)" required>
								<option value="" disabled selected>Parameter</option>
							</select>
								<select id="x-values" name="x-values" style="display:none"></select>
                                <div style="display:'.$settings["adubox"].'">
		                        	<div id="x-adu_check" style="display:none; margin-right: 30px;">
                    	        		<input type="checkbox" id="x-adu_cal" name="x-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
         	                       		<div id="units" style="display:none"></div>
									</div>
                                </div>
						</div>
					</div>	
					<div class="form-group" id="yparams" style="display:block">
						<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
						<div id="y0-par-form" class="col-md-10">
							<select id = "y0-sys" name="y0-sys" class="form-control" onchange="set_params(this)" required>
                               	<option value="" disabled selected>Select Y</option>'.$options.'</select>
							<select id = "y0-params" name="y0-params" class="form-control" style="display:none" onchange="populate_values(this); show_adu_checkbox(this)" required>
								<option value="" disabled selected>Parameter</option>
							</select>
							<select id="y0-values" name="y0-values" style="display:none"></select>
                            <div style="display:'.$settings["adubox"].'">
                            	<div id="y0-adu_check" style="display:none; margin-right: 30px;">
                               		<input type="checkbox" id="y0-adu_cal" name="y0-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
                                	<div id="units" style="display:none"></div>
								</div>
                            </div>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;" onclick="addmore_btn(1)">Add more...</button>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
						</div>
					</div>';
    	}
    	else{
			$option1 = create_option($repo_set, 0);
			$option2 = create_option($repo_set, 1);          
			ob_start();
       	 	populate_dropdown($origin."_nisp_params", "extra", "", $distinct = 1);
			$extra = ob_get_clean();          
    		$result = '<div class="form-group" id="params" style="display:block">
							<label style="display:block" class="col-md-2 control-label" >X axis parameter</label>
							<div id="x-par-form" class="col-md-10">
								<select id = "x-ic" class="form-control" >
	                		      	<option value="" disabled selected>Select '.strtoupper($keys[0]).'</option>
    	                            <option value="ALL">ALL</option>'.$option1.'</select>
								<select id = "x-sys" onchange="set_params(this)" class="form-control" >
	       			               	<option value="" disabled selected>Select '.strtoupper($keys[1]).'</option>
    	                            <option value="ALL">ALL</option>'.$option2.'</select>
                                <select id = "x-partype" name="x-partype" class="form-control" style="display:none" onchange="refresh_params(this)" >
                                    <option value="" disabled selected>Parameter filter</option>'.$extra.'
                                </select>
								<select id = "x-params" name="x-params" class="form-control" style="display:none" onchange="show_adu_checkbox(this)" required>
									<option value="" disabled selected>Parameter</option>
								</select>
								<select id="x-values" name="x-values" style="display:none"></select>
                            	<div style="display:'.$settings["adubox"].'">                                
                                    <div id="x-adu_check" style="display:none; margin-right: 30px;">
                                        <input type="checkbox" id="x-adu_cal" name="x-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
                                        <div id="units" style="display:none"></div>
                                    </div>
                                </div>
                         	    <div style="display:'.$settings["extra"].'">                                 
                                    <span class ="extra_filters_btn" id="x_extra_filters_btn_show" style="display:none" onclick="show_extra_filters(\'x\')"><a>Extra Filters</a></span>
                                    <span class ="extra_filters_btn" id="x_extra_filters_btn_hide" style="display:none" onclick="hide_extra_filters(\'x\')"><a>Hide Extra Filters</a></span>
                                </div>                                    
                                <div id="x_extra_filters" class="col-md-12 extra_filters" style="display:none">
                		    	<label id="xl" for="x_pid1">PID</label><textarea cols="15" id="x_pid1" name="x_pid1" value=""></textarea>
<!--                    				<label for="x_pid2">PID2</label><input type="text" id="x_pid2" name="x_pid2" value="">-->
                    			</div>
							</div>
						</div>
		                <div class="form-group" id="yparams" style="display:block">
							<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
							<div id="y0-par-form" class="col-md-10">
								<select id = "y0-ic" class="form-control" >
	                		      	<option value="" disabled selected>Select '.strtoupper($keys[0]).'</option>
    	                            <option value="ALL">ALL</option>'.$option1.'</select>
								<select id = "y0-sys" onchange="set_params(this)" class="form-control" >
       			    	           	<option value="" disabled selected>Select '.strtoupper($keys[1]).'</option>
                        	        <option value="ALL">ALL</option>'.$option2.'</select>                       
                                <select id = "y0-partype" name="y0-partype" class="form-control" style="display:none" onchange="refresh_params(this)" >
                                    <option value="" disabled selected>Parameter filter</option>'.$extra.'
                                </select>                                    
								<select id = "y0-params" name="y0-params" class="form-control" style="display:none" onchange="show_adu_checkbox(this)" >
									<option value="" disabled selected>Parameter</option>
								</select>
								<select id="y0-values" name="y0-values" style="display:none"></select>
                            	<div style="display:'.$settings["adubox"].'">                                 
                                    <div id="y0-adu_check" style="display:none; margin-right: 30px;">
                                        <input type="checkbox" id="y0-adu_cal" name="y0-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
                                        <div id="units" style="display:none"></div>
                             	    </div>                                         
                                </div>
                         	    <div style="display:'.$settings["extra"].'">                                
                                    <span class ="extra_filters_btn" id="y0_extra_filters_btn_show" style="display:none" onclick="show_extra_filters(\'y0\')"><a>Extra Filters</a></span>
                                    <span class ="extra_filters_btn" id="y0_extra_filters_btn_hide" style="display:none" onclick="hide_extra_filters(\'y0\')"><a>Hide Extra Filters</a></span>
								</div>
								<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;" onclick="addmore_btn(2)">Add more...</button>
								<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
     			            <div id="y0_extra_filters" class="col-md-12 extra_filters" style="display:none">
                		    	<label id="y0l" for="y0_pid1">PID</label><textarea cols="15" id="y0_pid1" name="y0_pid1" value=""></textarea>
<!--                   			 	<label for="y0_pid2">PID2</label><input type="text" id="y0_pid2" name="y0_pid2" value="">-->
       	   	        			</div>
							</div>
						</div>';
    	}
    	return $result;
    }

	function render_stats_form($origin, $settings, $repo_set){
		$keys = array_keys($repo_set["required"]);      
	    if($origin=="hktm"){
			$result='<div class="form-group" id="yparams" style="display:block">
						<label style="display:block" class="col-md-2 control-label" id = "y-label">Parameters</label>
						<div id="y0-par-form" class="col-md-10">
							<select id = "y0-sys" onchange="set_params(this)" class="form-control" >
                   			   	<option value="" disabled selected>Select '.ucfirst($keys[0]).'</option>';
              
             $result .= create_option($repo_set, 0); 
             $result .= '</select>
							<select id = "y0-params" name="y0-params" class="form-control" style="display:none" onchange="show_adu_checkbox(this)" >
								<option value="" disabled selected>Parameter</option>
							</select>
							<select id="y0-values" name="y0-values" style="display:none"></select>
                            <div style="display:'.$settings["adubox"].'">
              	            	<div id="y0-adu_check" style="display:none; margin-right: 30px;">
	                                <input type="checkbox" id="y0-adu_cal" name="y0-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
 	                                <div id="units" style="display:none"></div>
                            	</div>
							</div>                                
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;" onclick="addmore_btn(1)">Add more...</button>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
						</div>
					</div>';
    	}
    	else{
			ob_start();
       	 	populate_dropdown($origin."_nisp_params", "extra", "", $distinct = 1);
			$extra = ob_get_clean();          
    		$result = '<div class="form-group" id="yparams" style="display:block">
						<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
						<div id="y0-par-form" class="col-md-10">
							<select id = "y0-ic" class="form-control" >
                		      	<option value="" disabled selected>Select '.strtoupper($keys[0]).'</option>
                                <option value="ALL">ALL</option>';
            
			$result .= create_option($repo_set, 0);
            
            $result.='</select>
							<select id = "y0-sys" onchange="set_params(this)" class="form-control" >
       			               	<option value="" disabled selected>Select '.strtoupper($keys[1]).'</option>
                                <option value="ALL">ALL</option>';
          
			$result .= create_option($repo_set, 1);        
          
          
          	$result.='</select>
							<select id = "y0-partype" name="y0-partype" class="form-control" style="display:none" onchange="refresh_params(this)" >
								<option value="" disabled selected>Parameter filter</option>'.$extra.'
							</select>                                
							<select id = "y0-params" name="y0-params" class="form-control" style="display:none" onchange="show_adu_checkbox(this)" >
								<option value="" disabled selected>Parameter</option>
							</select>
							<select id="y0-values" name="y0-values" style="display:none"></select>
                            <div style="display:'.$settings["adubox"].'">                            
                                <div id="y0-adu_check" style="display:none; margin-right: 30px;">
                                        <input type="checkbox" id="y0-adu_cal" name="y0-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
                                        <div id="units" style="display:none"></div>
                                </div>
                            </div> 
                            <div style="display:'.$settings["extra"].'">
								<span class ="extra_filters_btn" id="y0_extra_filters_btn_show" style="display:none" onclick="show_extra_filters(\'y0\')"><a>Extra Filters</a></span>
							    <span class ="extra_filters_btn" id="y0_extra_filters_btn_hide" style="display:none" onclick="hide_extra_filters(\'y0\')"><a>Hide Extra Filters</a></span>
                            </div>                                
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;" onclick="addmore_btn(2)">Add more...</button>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
     			            <div id="y0_extra_filters" class="col-md-12 extra_filters" style="display:none">
                		    	<label id="y0l" for="y0_pid1">PID</label><textarea cols="15" id="y0_pid1" name="y0_pid1" value=""></textarea>
<!--                   			 	<label for="y0_pid2">PID2</label><input type="text" id="y0_pid2" name="y0_pid2" value="">-->
                		    </div>
						</div>
					</div>';
    	}
    	return $result;
    }    
  
  
  
	function render_trend_form($origin, $settings, $repo_set){
		$keys = array_keys($repo_set["required"]);        
	    if($origin=="hktm"){
			$result='<div class="form-group" id="yparams" style="display:block">
						<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
						<div id="y0-par-form" class="col-md-10">
							<select id = "y0-sys" onchange="set_params(this)" class="form-control" >
                   			   	<option value="" disabled selected>Select '.ucfirst($keys[0]).'</option>';
              
             $result .= create_option($repo_set, 0); 
             $result .= '</select>
							<select id = "y0-params" name="y0-params" class="form-control" style="display:none" onchange="populate_values(this); show_adu_checkbox(this)" >
								<option value="" disabled selected>Parameter</option>
							</select>
							<select id="y0-values" name="y0-values" style="display:none"></select>
                            <div style="display:'.$settings["adubox"].'">
                            	<div id="y0-adu_check" style="display:none; margin-right: 30px;">
                            		<input type="checkbox" id="y0-adu_cal" name="y0-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
                                	<div id="units" style="display:none"></div>
								</div>
							</div>                                
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;" onclick="addmore_btn(1)">Add more...</button>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
						</div>
					</div>';
    	}
    	else{
			ob_start();
       	 	populate_dropdown($origin."_nisp_params", "extra", "", $distinct = 1);
			$extra = ob_get_clean(); 
		          
    		$result = '<div class="form-group" id="yparams" style="display:block">
						<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
						<div id="y0-par-form" class="col-md-10">
							<select id = "y0-ic" class="form-control" >
                		      	<option value="" disabled selected>Select '.strtoupper($keys[0]).'</option>
                                <option value="ALL">ALL</option>';
            
			$result .= create_option($repo_set, 0);
            
            $result.='</select>
							<select id = "y0-sys" onchange="set_params(this)" class="form-control" >
       			               	<option value="" disabled selected>Select '.strtoupper($keys[1]).'</option>
                                <option value="ALL">ALL</option>';
          
			$result .= create_option($repo_set, 1);        
          
          
          	$result.='</select>
							<select id = "y0-partype" name="y0-partype" class="form-control" style="display:none" onchange="refresh_params(this)" >
								<option value="" disabled selected>Parameter filter</option>'.$extra.'
							</select>                                
							<select id = "y0-params" name="y0-params" class="form-control" style="display:none" onchange="show_adu_checkbox(this)" >
								<option value="" disabled selected>Parameter</option>
							</select>
							<select id="y0-values" name="y0-values" style="display:none"></select>
                            <div style="display:'.$settings["adubox"].'">                            
                                <div id="y0-adu_check" style="display:none ; margin-right: 30px;">
                                        <input type="checkbox" id="y0-adu_cal" name="y0-adu_cal" value="" onchange="set_units(this)"><span>ADU/Calib</span><div class="stats-tooltip"><img src="assets/images/tooltip120.png" width="16/"><span class="tooltiptext">Check to use calibrated/physical data, uncheck for ADU data</span></div>
                                        <div id="units" style="display:none"></div>
                                </div>
                               </div>                                
                            <div style="display:'.$settings["extra"].'">
								<span class ="extra_filters_btn" id="y0_extra_filters_btn_show" style="display:none" onclick="show_extra_filters(\'y0\')"><a>Extra Filters</a></span>
						    	<span class ="extra_filters_btn" id="y0_extra_filters_btn_hide" style="display:none" onclick="hide_extra_filters(\'y0\')"><a>Hide Extra Filters</a></span>
                            </div>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;" onclick="addmore_btn(2)">Add more...</button>
							<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
     			            <div id="y0_extra_filters" class="col-md-12 extra_filters" style="display:none">
                		    	<label id="y0l" for="y0_pid1">PID</label><textarea cols="15" id="y0_pid1" name="y0_pid1" value=""></textarea>
<!--                   			 	<label for="y0_pid2">PID2</label><input type="text" id="y0_pid2" name="y0_pid2" value="">-->
                		    </div>
						</div>
					</div>';
    	}
    	return $result;
    }  
  
}


class Upload{
	function render_hist_form($origin, $settings, $repo_set){
		$cols = explode(",",$origin);
        $optcols = "";
		foreach($cols as $c){ // iterate cols
          	$optcols .= '<option value="'.$c.'">'.$c.'</option>';
		}       
		$result='<div class="form-group" id="yparams" style="display:block">
					<label style="display:block" class="col-md-2 control-label" id = "y-label">Parameters</label>
					<div id="y0-par-form" class="col-md-10">
						<select id = "y0-params" name="y0-params" class="form-control" required>
							<option value="" disabled selected>Choose parameter...</option>'.$optcols.'
						</select>
						<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" onclick="addmore_btn(1)">Add more...</button>
						<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
					</div>
				</div>               	
                <div class="form-group" id="bins" style="display:none;">
					<label class="col-md-2 control-label">Bin size/Number of Bins</label>
					<div class="col-md-10">
						<div class="col-md-2">
							<div class="form-check form-check-inline">
								<input class="form-check-input" type="radio" name="bintype" id="bintype1" value="binsize" checked>
								<label class="form-check-label" for="bintype1">Bin Size</label>
							</div>
						<div class="form-check form-check-inline">
							<input class="form-check-input" type="radio" name="bintype" id="bintype2" value="binnumber">
							<label class="form-check-label" for="bintype2">Number of Bins</label>
						</div>
					</div>
					<div class="col-md-10 ">
						<input type="number" id="binsize" name="binsize" class="form-control" placeholder="Set bin size..." min="0.000000000000001" required></input>
					</div>
				</div>';

    	return $result;      

    }
  
	function render_scatter_form($origin, $settings, $repo_set){
		$cols = explode(",",$origin);
        $optcols = "";
		foreach($cols as $c){ // iterate cols
          	$optcols .= '<option value="'.$c.'">'.$c.'</option>';
		}       
		$result='<div class="form-group" id="params" style="display:block">
					<label style="display:block" class="col-md-2 control-label" >X axis parameter</label>
					<div id="x-par-form" class="col-md-10">
						<select id = "x-params" name="x-params" class="form-control" required>
							<option value="" disabled selected>Parameter</option>'.$optcols.'
         				</select>
                        <!--<div class="stats-tooltip"><img src = "assets/images/tooltip120.png" width = 16/><span class="tooltiptext">For Trend analysis, select here the datetime column</span></div>-->
					</div>
				</div>	
				<div class="form-group" id="yparams" style="display:block">
					<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
					<div id="y0-par-form" class="col-md-10">
						<select id = "y0-params" name="y0-params" class="form-control" required>
							<option value="" disabled selected>Parameter</option>'.$optcols.'
						</select>
						<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" onclick="addmore_btn(1)">Add more...</button>
						<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
					</div>
				</div>';

    	return $result;
    }

	function render_stats_form($origin, $settings, $repo_set){
		$cols = explode(",",$origin);
        $optcols = "";
		foreach($cols as $c){ // iterate cols
          	$optcols .= '<option value="'.$c.'">'.$c.'</option>';
		}       
		$result='<div class="form-group" id="yparams" style="display:block">
					<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
					<div id="y0-par-form" class="col-md-10">
						<select id = "y0-params" name="y0-params" class="form-control" required>
							<option value="" disabled selected>Parameter</option>'.$optcols.'
						</select>
						<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" onclick="addmore_btn(1)">Add more...</button>
						<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
					</div>
				</div>';

    	return $result;      
    }  
  
	function render_trend_form($origin, $settings, $repo_set){
		$cols = explode(",",$origin);
        $optcols = "";
		foreach($cols as $c){ // iterate cols
          	$optcols .= '<option value="'.$c.'">'.$c.'</option>';
		}       
		$result='<div class="form-group" id="params" style="display:block">
					<label style="display:block" class="col-md-2 control-label" >Datetime column</label>
					<div id="x-par-form" class="col-md-10">
						<select id = "x-params" name="x-params" class="form-control" required>
							<option value="" disabled selected>Parameter</option>'.$optcols.'
         				</select>
                        
					</div>
				</div>	
				<div class="form-group" id="yparams" style="display:block">
					<label style="display:block" class="col-md-2 control-label" id = "y-label">Y axis parameters</label>
					<div id="y0-par-form" class="col-md-10">
						<select id = "y0-params" name="y0-params" class="form-control" required>
							<option value="" disabled selected>Parameter</option>'.$optcols.'
						</select>
						<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" onclick="addmore_btn(1)">Add more...</button>
						<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;" onclick="remove_btn()">Remove Last...</button>
					</div>
				</div>';

    	return $result;
    }

}

function create_option($arr, $id, $type="required",$from_keys=false){
	//render list of options of a select box from an array
	$keys = array_keys($arr[$type]);
	$res = "";	
	if($from_keys){
		foreach(array_keys($arr[$type][$keys[$id]]) as $v){
			$res .= '<option value="'.$v.'">'.$v.'</option>';            
		}		

	}
	else{

		foreach($arr[$type][$keys[$id]]['values'] as $v){
			$res .= '<option value="'.$v.'">'.$v.'</option>';            
		}
	}
	return $res;  
}


/*GET CURRENT OPERATION MODE AND SPECIFIC VIEW SETTINGS*/
$opmode = get_opmode();

switch($opmode){

  case "DEBUG" : {
    	$settings = array(
        	"adubox" => "inline",
          	"extra" => "inline"
        );
        break;
    
    }
  case "NOMINAL" : {
    	$settings = array(
        	"adubox" => "none",        
          	"extra" => "none",        
        );
        break;    
    
    }
  case "CONTINGENCY" : {
    	$settings = array(
        	"adubox" => "none",        
          	"extra" => "none",        
        );
        break;    
    }
  case "COMMISSIONING" : {
    	$settings = array(
        	"adubox" => "none",        
          	"extra" => "none",        
        );
        break;    
    }	
  default:
    {
    	$settings = array(
        	"adubox" => "none",        
          	"extra" => "none",        
        );
        break;    
    }
}


/*SET REPO SETTINGS FOR SELECT ITEMS*/
$repo_set = select_items_json(strtolower($opmode), $source, $origin);

//Instantiate plot class
$plot_cls = new ReflectionClass(ucfirst($plot));
$object = $plot_cls->newInstanceWithoutConstructor();
//Run rendering
$result = $object->call_source($source, $origin, $settings, $repo_set);
echo $result;
?>