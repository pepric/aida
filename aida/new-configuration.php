<!doctype html>
<html class="fixed">
	<?php 
		$title = "New Report Configuration";
		include("header.php"); ?>
	
	<!-- start: page -->
	
		<div class="row">
			<div class="col-xs-12" id = "form-div">
				<section class="panel">
					<header class="panel-heading">
						<div class="panel-actions">
							<a href="#" class="fa fa-caret-down"></a>
							<a href="#" class="fa fa-times"></a>
						</div>
		
						<h2 class="panel-title">Basic Configuration Settings</h2>
					</header>
					<div class="panel-body">
						<form id="config_form" class="form-horizontal form-bordered" method="" action="" novalidate = "novalidate">
							<div class="form-group" id="period-div">
								<label class="col-md-2 control-label">Periodicity</label>
								<div class="col-md-10">
									<select name="period" id="period" class="form-control" required style="width: 35%;" onchange="show_custom(this);">
										<option value="daily">Daily</option>
										<option value="weekly">Weekly</option>
										<option value="monthly">Monthly</option>
										<option value="custom">Periodic Custom</option>
										<option value="ondemand" selected>On Demand</option>
										
									</select>
								</div>
							</div>
							<div class="form-group" id="custom-group" style="display:none">
								<label class="col-md-2 control-label">Custom Period (decimal hours)</label>
								<div class="col-md-10">
									<input type="number" name="custom" id = "custom" min="0" step="0.1" style="width: 35%;"></input>
								</div>
							</div>
							<div class="form-group" id="daterange">
								<label class="col-md-2 control-label">Start Date (UTC)</label>
								<div class="col-md-8">
									<div class='input-daterange input-group date' >
										
										<span class="input-group-addon" id="dateiconstartc">
											<span class="glyphicon glyphicon-calendar"></span>
										</span>
										<input type='text' class="form-control indate" name="tstartconf" id="tstartconf" required />
									</div>
								</div>
							</div>
							<div class="form-group" id="sampling-group">
								<label class="col-md-2 control-label">Sampling</label>
								<div class="col-md-10">
									<!--<select data-plugin-selectTwo class="form-control populate">-->
									<select name="sampling" id="sampling" class="form-control" onchange="show_dts(this)" required style="width: 35%;" readonly disabled>
										<option value="full" selected>Full</option>
										<option value="by time">By Time</option>
                                      	<option value="by function">By Function</option>
									</select>
									<!--</select>-->
								
								</div>
							</div>
							<div class="form-group" id="dts-group" style="display:none">
								<label class="col-md-2 control-label">Sampling Period (decimal hours)</label>
								<div class="col-md-10">
									<input type="number" name="dts" id = "dts" placeholder="Set sampling period..." min="0" step="0.1" style="width: 35%;"></input>
								</div>
							</div>
							<div class="form-group" id="sfunc-group" style="display:none">
								<label class="col-md-2 control-label">Sampling function</label>
								<div class="col-md-10">
									<select name="sampling" id="sfunc" class="form-control" style="width: 35%;">
										<option value="mean" selected>Mean</option>
										<option value="median">Median</option>
                                      	<!--<option value="biweight mean">Biweight Mean</option>-->
									</select>
								</div>
							</div>
							<div class="form-group" id="window-group" style="display:none">
								<label class="col-md-2 control-label">Time Window (decimal hours)</label>
								<div class="col-md-10">
									<input type="number" name="window" id = "window" placeholder="Set window amplitude..." min="0" step="0.1" style="width: 35%;"></input>
								</div>
							</div>
							<div class="form-group" id="nacq-group" style="display:none">
								<label class="col-md-2 control-label">Number of Acquisitions</label>
								<div class="col-md-10">
									<input type="number" name="nacq" id = "nacq" placeholder="Set number of acquisitions..." min="1" style="width: 35%;" onchange="show_dtacq(this)" ></input>
								</div>
							</div>
							<div class="form-group" id="dtacq-group" style="display:none; border-bottom: 1px solid #eff2f7 !important; padding-bottom: 15px !important; margin-bottom: 15px; !important">
								<label class="col-md-2 control-label">Acquisition time step (decimal hours)</label>
								<div class="col-md-10">
									<input type="number" name="dtacq" id = "dtacq" placeholder="Set step..." min="0" step="0.1" style="width: 35%;"></input>
								</div>
							</div>
						</form>
						<form id="editor_form" class="form-horizontal form-bordered" method="" action="" novalidate = "novalidate">
							<div class="form-group" id="editor" style="display:none">
								<label class="col-md-2 control-label">Configuration Editor</label>
								<div class="col-md-10" id="editor-div">
									<textarea id="code-area"></textarea>
								
								
								</div>
							</div>
							<div class="form-group" id="filename" style="display:none">
								<label class="col-md-2 control-label">JSON File Name</label>
								<div class="col-md-10">
									<input type="text" id="infile" style="width: 35%;" value="config.json" required></input>
								</div>
							</div>
				
							
							<div class="form-group" id="hidden-fields">
								<!--<input type="hidden" name="period" id = "period" value="ondemand"></input>-->
								<input type="hidden" name="page" id = "page" value="new"></input>
							</div>
						</form>
						<div class="col-md-12" style="text-align:right">
							<button class="btn btn-primary" id = "submit_temp" style="display:none">Store Temporary JSON</button>
							<button class="btn btn-primary" id = "complete_config" style="display:none">Save Completed JSON</button>
							<button class="btn btn-primary" id = "run_config" style="display:none">Generate Report</button>
							<button class="btn btn-primary" id = "submit_config" >Generate Configuration JSON</button>
							<button type="reset" class="btn btn-default" onClick="window.location.reload();">Reset</button>
						</div>
						
					</div>
				</section>
			</div>
		</div>
		<?php include("loader.html"); ?>
		<canvas id="canvas"></canvas>
		<div id="plot_img" style="display:none"><img id = "png_img"></img></div>
		
		<?php include("modalbox.php"); ?>
	</section>
						


	<?php include("footer.php"); ?>
	<?php include("base_scripts.html"); ?>
	<?php include("form_scripts.html"); ?>	
 

	<!-- IOT -->
	<script src="assets/javascripts/lsst/plots.js"></script>
	
	<!-- Validation -->
	<script src="assets/javascripts/lsst/validation.js"></script>
	
	<!-- Theme Base, Components and Settings -->
	<script src="assets/javascripts/theme.js"></script>
	
	<!-- Theme Custom -->
	<script src="assets/javascripts/theme.custom.js"></script>
	
	<!-- Theme Initialization Files -->
	<script src="assets/javascripts/theme.init.js"></script>

	
	<script src="assets/javascripts/lsst/jqscripts.js"></script>
	
	<script src="assets/javascripts/lsst/genreport.js"></script>

	<script>
	$(document).ready(function(){
		// show/hide form fields according with user choices
		var curr = document.getElementById("period").value;
		var wingroup = document.getElementById("window-group");
		var nacqgroup = document.getElementById("nacq-group");
		var win = document.getElementById("window");
		var nacq = document.getElementById("nacq");
		
		if(curr == "ondemand"){
			wingroup.setAttribute("style","display:block");
			win.setAttribute("required","");
			nacqgroup.setAttribute("style","display:block");
			nacq.setAttribute("required","");
		}

		$("#period").change(function(){
			if($(this).val() == "ondemand"){
				wingroup.setAttribute("style","display:block");
				win.setAttribute("required","");
				nacqgroup.setAttribute("style","display:block");
				nacq.setAttribute("required","");
				
			
			}
			else{
				
				
				var dtacqgroup = document.getElementById("dtacq-group");
				var dtacq = document.getElementById("dtacq");
				wingroup.setAttribute("style","display:none");
				win.removeAttribute("required","");
				nacqgroup.setAttribute("style","display:none");
				nacq.removeAttribute("required","");
				dtacqgroup.setAttribute("style","display:none");
				dtacq.removeAttribute("required","");
				dtacq.value = "";
				
			}
		});

	});
	
		$(document).ready(function () {
		//init datetime picker
		var period = document.getElementById('period').value;
		conf0 = {
			useCurrent : "day",
			timeZone : "UTC",
			format: 'YYYY-MM-DD HH:mm:ss',
		}
		if(period == "ondemand"){
			conf0['maxDate']='now'
		}
		$('#tstartconf').datetimepicker(conf0);
		
		//set new datetime when ondemand
		$('#period').on('change', function() {
		  var period = this.value;
		  conf1 = {
			useCurrent : "day",
			timeZone : "UTC",
			format: 'YYYY-MM-DD HH:mm:ss',
			}
		  if(period == "ondemand"){
			conf1['maxDate']='now'
			}
		  $('#tstartconf').datetimepicker('destroy');
		  $('#tstartconf').datetimepicker(conf1);

		});

	$('#dateiconstartc').on("click", function (){$("#tstartconf").focus()})
	});
	
	
	</script>



</html>
</body>