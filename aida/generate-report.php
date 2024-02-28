<!doctype html>
<html class="fixed">
	<?php
		$title = "Report Generation";
		include("header.php"); 
	?>
  <span style="display:none" id="opmode"><?php echo get_opmode() ?></span>
	<div class="row">
		<div class="col-xs-12" id = "select-file">
			<section class="panel">
				<header class="panel-heading">
					<div class="panel-actions">
						<a href="#" class="fa fa-caret-down"></a>

					</div>
	
					<h2 class="panel-title">Select Configuration File Origin</h2>
				</header>
				<div class="panel-body">
					<div class="form-group">
						<label class="radio-inline"><input type="radio" name="conf-orig" value="table" checked>Run from Existing Configuration File</label>
						<label class="radio-inline"><input type="radio" name="conf-orig" value="upload" >Upload New Configuration File</label>
					</div>
				</div>
			</section>
		</div>
	
		<div class="col-xs-12" id = "config-table">
			<section class="panel">
				<header class="panel-heading">
					<div class="panel-actions">
						<a href="#" class="fa fa-caret-down"></a>
						<a href="#" class="fa fa-times"></a>
					</div>
	
					<h2 class="panel-title">Generate Report from Existing Configuration File</h2>
				</header>
				
				<div class="panel-body panel-rep">
                  	<?php 
						$result = get_reports($mysqli, "", "WHERE isrunning = 0 AND iscomplete = 1", "config"); 
                  		if($result != "error"){ ?>                  
					<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-personal">
						<thead>
							<tr >
							<!--<th scope="col">#</th>-->
							<th scope="col">Configuration File</th>
							<th scope="col">Creation date</th>
							<th scope="col">Last update</th>
							<th scope="col">Owner</th>
							<th scope="col">Recurrence</th>
							<th scope="col">Start date</th>
							<th scope="col">Operating Mode</th>
							<th scope="col"></th>
						  </tr>
						</thead>										
					<?php 

						render_run_config($result);

					?>
					</table>
               <?php }
                  	else {echo '<p>Unable to retrieve data. Please retry or contact AIDA admin.</p>';}?>					
				</div>
			</section>
		</div>
		
		
		<div class="col-xs-12" id = "config-upload" style="display:none">
			<section class="panel">
				<header class="panel-heading">
					<div class="panel-actions">
						<a href="#" class="fa fa-caret-down"></a>
						<a href="#" class="fa fa-times"></a>
					</div>
	
					<h2 class="panel-title">Upload Configuration File</h2>
				</header>
				<div class="panel-body">
					<form id="upload-form" class="form-horizontal form-bordered" method="" action="">
					
						<div class="form-group">
							<label class="col-md-2 control-label">File Upload</label>
							<div class="col-md-10">
								<div class="fileupload fileupload-new" data-provides="fileupload">
									<div class="input-append">
										<div class="uneditable-input">
											<i class="fa fa-file fileupload-exists"></i>
											<span class="fileupload-preview"></span>
										</div>
										<span class="btn btn-default btn-file">
											<span class="fileupload-exists">Change</span>
											<span class="fileupload-new">Select file</span>
											<input type="file" />
										</span>
										<a href="#" class="btn btn-default fileupload-exists" data-dismiss="fileupload">Remove</a>
									</div>
								</div>
							</div>
						</div>
						<div class="form-group" id="period-div">
							<label class="col-md-2 control-label">Periodicity</label>
							<div class="col-md-10">
								<select name="period" id="period" class="form-control" required style="width: 35%;" onchange="show_custom(this);"> <!--readonly disabled="disabled">-->
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
						
						<div class="form-group" id="hidden-fields"></div>
						
						<div class="col-md-12" style="text-align:right">
							<button type="submit" class="btn btn-primary" id = "submit_btn_upload">Upload & Run</button>
							<button type="reset" class="btn btn-default" >Reset</button>
						</div>
					</form>						
				</div>
			</section>
		</div>
	</div>
	
	<?php include("loader.html"); ?>
</section>		
			

			


	<?php include("footer.php"); ?>
			
	<!-- Vendor-->
	<script src="assets/vendor/jquery/jquery.js"></script> 
	<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>
	<script src="assets/javascripts/lsst/moment.js"></script>
	<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
	<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
	<script src="assets/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.js"></script>
	<script src="assets/vendor/magnific-popup/magnific-popup.js"></script>
	<script src="assets/vendor/jquery-placeholder/jquery.placeholder.js"></script>

	<!-- Form validation -->
	<script src="assets/vendor/jquery-validation/jquery.validate.js"></script>

	<!-- File upload -->
	<script src="assets/vendor/bootstrap-fileupload/bootstrap-fileupload.min.js"></script>
	
	<!-- Specific Page Vendor -->
	<script src="assets/vendor/select2/select2.js"></script>
	<script src="assets/vendor/jquery-datatables/media/js/jquery.dataTables.js"></script>
	<script src="assets/vendor/jquery-datatables/extras/TableTools/js/dataTables.tableTools.min.js"></script>
	<!--<script src="assets/vendor/jquery-datatables-bs3/assets/js/datatables.js"></script>-->
	<script src="assets/vendor/DataTables/datatables.min.js"></script>
	
	<!-- Theme Base, Components and Settings -->
	<script src="assets/javascripts/theme.js"></script>
	
	<!-- Theme Custom -->
	<script src="assets/javascripts/theme.custom.js"></script>
	
	<!-- Theme Initialization Files -->
	<script src="assets/javascripts/theme.init.js"></script>

	<script src="assets/javascripts/lsst/validation.js"></script>
	<script src="assets/javascripts/lsst/tab-init.js"></script>

	<script src="assets/javascripts/lsst/genreport.js"></script>

	<script>
	//datetime fields behavior
	$(document).ready(function () {
		$('#tstart').datetimepicker({
			useCurrent : "day",
			format: 'YYYY-MM-DD HH:mm:ss',

		});
		$('#tend').datetimepicker({
			useCurrent: "day", //Important! See issue #1075
			format: 'YYYY-MM-DD HH:mm:ss'
		});
		$("#tstart").on("dp.change", function (e) {
			$('#tend').data("DateTimePicker").minDate(e.date);
		});
		$("#tend").on("dp.change", function (e) {
			$('#tstart').data("DateTimePicker").maxDate(e.date);
		});	

		$('#dateiconend').on("click", function (){$("#tend").focus()})
		$('#dateiconstart').on("click", function (){$("#tstart").focus()})
	})
	
	//choice between upload and existing file run
	$(document).ready(function(){
		$("input[type='radio']").change(function(){
			if($(this).val()=="upload")
				{
					$("#config-upload").show();
					$("#config-table").hide();
				}
				else
				{
					$("#config-upload").hide();
					$("#config-table").show();
				}
		});
	});
	</script>

</body>
</html>