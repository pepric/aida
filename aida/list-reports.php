<!doctype html>
<html class="fixed">
	<?php 
		$title = "Reports";
		include("header.php"); ?>

		<!-- start: page -->
			<div class="row">
				<div class="col-xs-12" id = "periodic-reports">
					<section class="panel">
						<header class="panel-heading">
							<div class="panel-actions">
								<a href="#" class="fa fa-caret-down"></a>
								<a href="#" class="fa fa-times"></a>
							</div>
			
							<h2 class="panel-title">Periodic Reports List</h2>
						</header>
						<div class="panel-body panel-rep">
						<?php 
							$result = get_reports($mysqli, "ondemand", "exclude", "report");
							if($result !="error"){
						?> 										
								<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-report-per">
									<thead>
										<tr >
										<!--<th scope="col">#</th>-->
										   
										<th scope="col">Report</th>
										<th scope="col">Creation date</th>
										<th scope="col">Owner</th>
										<th scope="col">Recurrence</th>
										<th scope="col">Start date</th>
										<th scope="col">End date</th>
										<th scope="col">Config file</th>
										<th scope="col">Flag</th>                                                       
										<th scope="col">Flag Creator</th>
										<th scope="col">Flag Date</th>
										<th scope="col">Flag Comments</th>                                                      
										<th scope="col"></th>
									  </tr>
									</thead>
						
								<?php 
									render_view_reports($result);
								?>
								</table>
	<?php }
		else {echo '<p>Unable to retrieve Reports data from local DB. Please retry or contact AIDA admin.</p>';}?>										
						</div>
					</section>
				</div>
				<div class="col-xs-12" id = "ondemand-reports">
					<section class="panel">
						<header class="panel-heading">
							<div class="panel-actions">
								<a href="#" class="fa fa-caret-down"></a>
								<a href="#" class="fa fa-times"></a>
							</div>
			
							<h2 class="panel-title">On-Demand Reports List</h2>
						</header>
						<div class="panel-body panel-rep">
						<?php 
							$result = get_reports($mysqli, "ondemand", "only", "report"); 
							if($result !="error"){
						?>                                      
								<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-report-ond">
									<thead>
										<tr >
										<!--<th scope="col">#</th>-->

										<th scope="col">Report</th>
										<th scope="col">Creation date</th>
										<th scope="col">Owner</th>

										<th scope="col">Start date</th>
										<th scope="col">End date</th>
										<th scope="col">Config file</th>
										<th scope="col">Flag</th>                                                        
										<th scope="col">Flag Creator</th>
										<th scope="col">Flag Date</th>
										<th scope="col">Flag Comments</th>                                                       
										<th scope="col"></th>
									  </tr>
									</thead>										
								<?php 
									render_view_reports($result);
								?>
								</table>
	<?php }
		else {echo '<p>Unable to retrieve Reports data from local DB. Please retry or contact AIDA admin.</p>';}?>	                                      
						</div>
					</section>
				</div>
			</div>
						
		<?php include("loader.html"); ?>
		</section>
		<?php include("modalbox.php"); show_modal("report");?>
		<?php include("footer.php"); ?>
		<?php include("base_scripts.html"); ?>
		<?php include("form_scripts.html"); ?>	

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
		
		<script src="assets/javascripts/lsst/tab-init.js"></script>
        <!-- Validation -->
        <script src="assets/javascripts/lsst/validation.js"></script>
	<script>
	$("input[type='radio'][name=repflag]").change(function(){
		$('#input-descr').val('');
		if($(this).val()!="nd")
			{
//				populate_flags();
				$("#description").show();
//				$("#parflag").show();
				$("#alert-email").show();
				
			}
		else
			{
				$("#description").hide();
//				$("#parflag").hide();
              	$("#email-to").val('')
				$("#alert-email").hide();
			}
	});
      
//automatic refresh page
setTimeout(function(){
  location = '';
}, 300000); 

	</script>
	</body>
</html>