<!doctype html>
<html class="fixed">
	<?php 
		$title = "Configuration Files";
		include("header.php"); ?>
			<!-- start: page -->
				<div class="row">
					<div class="col-xs-12" id = "periodic-reports">
						<div class="tabs tabs-primary">
							<ul class="nav nav-tabs nav-justified">
								<li class="active">
									<a href="#periodic" data-toggle="tab">Periodic Configuration Files</a>
								</li>
								<li>
									<a href="#ondemand" data-toggle="tab">On-Demand Configuration Files</a>
								</li>
								<li>
									<a href="#uncomplete" data-toggle="tab">Uncompleted Configuration Files</a>
								</li>
							</ul>
							<div class="tab-content">
								<div id="periodic" class="tab-pane active">
									<div class="panel-body panel-rep">
									<?php 
										$result = get_list($mysqli, "ondemand", "exclude", "config","AND iscomplete = 1");
										if($result !="error"){
									?> 												
										<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-periodic">
											<thead>
												<tr >
												<!--<th scope="col">#</th>-->
												<th scope="col">Configuration File</th>
												<th scope="col">Creation date</th>
												<th scope="col">Last update</th>
												<th scope="col">Owner</th>
												<th scope="col">Recurrence</th>
												<th scope="col">Start date</th>
												<th scope="col">Sampling</th>
												<th scope="col">Report Generation Status</th>
												<th scope="col"></th>
											  </tr>
											</thead>
											<?php 
												 
												render_view_config($result);

											?>
										</table>
										<?php }
											else {echo '<p>Unable to retrieve Configuration Files data from local DB. Please retry or contact AIDA admin.</p>';}?>											
									</div>
								</div>
								<div id="ondemand" class="tab-pane">
									<div class="panel-body panel-rep">
									<?php 
										$result = get_list($mysqli, "ondemand", "only", "config","AND iscomplete = 1");
										if($result !="error"){
									?>                                               
										<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-ondemand">
											<thead>
												<tr >
												<!--<th scope="col">#</th>-->
												<th scope="col">Configuration File</th>
												<th scope="col">Creation date</th>
												<th scope="col">Last update</th>
												<th scope="col">Owner</th>
												<th scope="col">Start date</th>
												<th scope="col">Sampling</th>
												<th scope="col">Window (h)</th>
												<th scope="col">Repetitions</th>
												<th scope="col">Report Generation Status</th>
												<th scope="col"></th>
											  </tr>
											</thead>										
										<?php 

											render_view_config($result);

										?>
										</table>
									<?php }
										else {echo '<p>Unable to retrieve Configuration Files data from local DB. Please retry or contact AIDA admin.</p>';}?>                                              
									</div>
								</div>
								<div id="uncomplete" class="tab-pane">
									<div class="panel-body panel-rep">
								<?php 
									$result = get_list($mysqli, "", "user", "config","AND iscomplete = 0"); 
									if($result !="error"){
								?>                                               
										<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-uncomplete">
											<thead>
												<tr >
												<!--<th scope="col">#</th>-->
												<th scope="col">Configuration File</th>
												<th scope="col">Creation date</th>
												<th scope="col">Last update</th>
												<th scope="col">Owner</th>
												<th scope="col">Recurrence</th>
												<th scope="col"></th>
											  </tr>
											</thead>										
										<?php 
											render_view_config($result);
										?>
										</table>
									<?php }
										else {echo '<p>Unable to retrieve Configuration Files data from local DB. Please retry or contact AIDA admin.</p>';}?>                                              
									</div>
								</div>
							</div>
						</div>							
					</div>
				</div>
		</section>
						


		<?php include("footer.php"); ?>
		
		<!-- Vendor-->
		<script src="assets/vendor/jquery/jquery.js"></script> 
		<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>
		<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
		<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
		<script src="assets/vendor/bootstrap-datepicker/js/bootstrap-datepicker.js"></script>
		<script src="assets/vendor/magnific-popup/magnific-popup.js"></script>
		<script src="assets/vendor/jquery-placeholder/jquery.placeholder.js"></script>

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
		<script src="assets/javascripts/lsst/tabs.js"></script>

		<script>

		//automatic refresh page
		setTimeout(function(){
		  location = '';
		}, 300000);

		</script>
	</body>
</html>