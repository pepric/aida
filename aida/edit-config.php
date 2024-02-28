<!doctype html>
<html class="fixed">
	<?php 
		$title = "Edit Configuration File";
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
		
						<h2 class="panel-title">Edit Configuration</h2>
					</header>
					<div class="panel-body">


						
						<form id="editor_form" class="form-horizontal form-bordered" method="" action="" novalidate = "novalidate">
							<div class="form-group" id="filename">
								<label class="col-md-2 control-label">JSON File Name</label>
								<div class="col-md-10">
									<input type="text" id="infile" style="width: 35%;" value="<?php echo $_GET['conf'];?>" readonly></input>
								</div>
							</div>
							<div class="form-group" id="period-div">
								<label class="col-md-2 control-label">Periodicity</label>
								<div class="col-md-10">
									<select name="period" id="period" class="form-control" required style="width: 35%;" readonly disabled="disabled">
										<option value="weekly">Weekly</option>
										<option value="monthly">Monthly</option>
										<option value="custom">Periodic Custom</option>
										<option value="ondemand">On Demand</option>
										
									</select>
								</div>
							</div>
							<div class="form-group" id="custom-group" style="display:none">
								<label class="col-md-2 control-label">Custom Period (decimal hours)</label>
								<div class="col-md-10">
									<input type="number" name="custom" id = "custom" min="0" step="0.1" style="width: 35%;"></input>
								</div>
							</div>
						
							<div class="form-group" id="editor">
								<label class="col-md-2 control-label">Configuration Editor</label>
								<div class="col-md-10" id="editor-div">
									<textarea id="code-area"></textarea>
								
								
								</div>
							</div>
							
				
							
							<div class="form-group" id="hidden-fields">
								<input type="hidden" name="page" id = "page" value="edit"></input>
							</div>
						</form>
						<div class="col-md-12" style="text-align:right">
							<button class="btn btn-primary" id = "submit_temp">Update Temporary JSON</button>
							<button class="btn btn-primary" id = "complete_config">Save Completed JSON</button>
							<button class="btn btn-primary" id = "run_config">Generate Report</button>
							<button type="reset" class="btn btn-default" onClick="window.location.href='list-config.php';">Abort</button>
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
		//visualize additional setting when custom interval is selected
		$(document).ready(function(){
		var url = window.location.href;
		var params = url.split('&');
		var period = params[1].split('=')[1]
		if(period=="custom"){
			var win = params[2].split('=')[1]
		}
		
		$("#period option[value="+period+"]").attr('selected', 'selected');
		var curr = document.getElementById("period");
		if(curr.value == "custom"){
			var custom = document.getElementById("custom");
			custom.setAttribute("value",win);
		}
		show_custom(curr)
		
	})
	
	$(document).ready(function(){
		generate_from_file();
	})
	
	</script>
	
</html>
</body>