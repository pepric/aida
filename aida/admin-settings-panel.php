<div class="panel-body panel-dash">					
  <!-- start: page -->
  <div class="row">
    
	<!--First Column-->
    <div class="col-md-5">
	    <!--Operating Modes Tab-->
		<div class="col-md-12">
		  <section class="panel">
			<header class="panel-heading">
			  <div class="panel-actions">
				<a href="#" class="fa fa-caret-down"></a>
			  </div>
			  <h2 class="panel-title">Operating Modes</h2>
			</header>        
			<div class="panel-body col-md-12 dashpanel">
			  <div class="form-group">
				<label class="col-md-5 control-label" style="padding: 10px;">Select Operating Mode</label>
				<div class="col-md-7">       
				  <select name="opmode" id="opmode_set" class="form-control">
					<?php
					//get opmode
					$result = get_opmode(false); 
					while( $rs = mysqli_fetch_assoc($result)){
					  if(substr($rs['mode'],0,5) != "debug"){
						$selected="";
						if($rs['enable']==1){$selected="selected";}
						echo '<option value="'.$rs['mode'].'" '.$selected.'>'.ucfirst($rs['mode']).'</option>';
					  }
					}

					?>
				  </select>
				  <button id="change_op" type="button" class="btn btn-primary" style="margin-top: -6px;margin-left: 3px;">Change</button>
				</div>
			  </div>
			</div>
		  </section>
		</div>	  
		<!--END Operating Modes Tab--> 	

		<!--App Data Management Tab-->
		<div class="col-md-12">	
	  
		  <section class="panel">
			<header class="panel-heading">
			  <div class="panel-actions">
				<a href="#" class="fa fa-caret-down"></a>
			  </div>
			  <h2 class="panel-title">Web App Settings</h2>
			</header>        
			<div class="panel-body col-md-12 dashpanel">
			  <div class="form-group">
				<label class="col-xs-8 control-label " style="padding: 10px;">General Settings</label>
				<div class="col-xs-4"><a role="button" href="#" tabindex="-1" id="admin_gen_set" data-toggle="modal" data-target="#gen_set" class="btn btn-primary" style="margin-top: 6px;min-width: 78px;">Change</a></div>
				<label class="col-xs-8 control-label " style="padding: 10px;">Edit SMTP</label>
				<div class="col-xs-4"><a role="button" href="#" tabindex="-1" id="admin_smtp_set" data-toggle="modal" data-target="#smtp_set" class="btn btn-primary" style="margin-top: 6px;min-width: 78px;">Change</a></div>			
				<label class="col-xs-8 control-label " style="padding: 10px;">Export Data</label>
				<div class="col-xs-4"><a role="button" href="#" tabindex="-1" id="export_data" data-toggle="modal" data-target="#export" class="btn btn-primary" style="margin-top: 6px;min-width: 78px;">Start</a></div>

			  </div>          
			</div>
		  </section>	  
		  
		</div>	  
	<!--END App Data Management Tab-->  	  
    </div>
    
     <!--Systems Management Tab-->
    <div class="col-md-3">
		<div class="col-md-12">
			<section class="panel">
				<header class="panel-heading">
				  <div class="panel-actions">
					<a href="#" class="fa fa-caret-down"></a>
				  </div>
				  <h2 class="panel-title">Systems</h2>
				</header>        
				<div class="panel-body col-md-12 dashpanel">
					<div class="form-group" >
						<table class="admin_systems" id="tbl_sys">
							<?php 
								$q = get_systems_settings();
								render_systems_setting($q);
							
							?>
						</table>
						<div class="col-xs-12" style="text-align:right"><button id="update_sys" type="button" class="btn btn-primary">Update</button></div>
					</div>         
				</div>
			</section>
		</div>    
	<!--END Systems Management Tab-->    
	</div>
  </div>
</div>























