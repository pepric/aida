<!doctype html>
<html class="fixed">
	<?php 
		$title = "Stored Files";
		include("header.php"); ?>

					<!-- start: page -->
			<div class="row">
				<div class="col-xs-12" id = "user-files">
					<div class="tabs tabs-primary">
						<ul class="nav nav-tabs nav-justified">
							<li class="active">
								<a href="#user" data-toggle="tab">User Files</a>
							</li>
							<li>
								<a href="#global" data-toggle="tab">Global Stored Files</a>
							</li>
							<li>
								<a href="#temp-data" data-toggle="tab">Temporary Files from Repository</a>
							</li>
							<li>
								<a href="#temp-uploaded" data-toggle="tab">Temporary Uploaded Files</a>
							</li>                                      
						</ul>
						<div class="tab-content">
							<div id="user" class="tab-pane active">
								<div class="panel-body panel-rep">
									<?php 
										$result = get_list($mysqli, "", "user", "user",""); 
										if($result !="error"){
									?> 												
										<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-stored-user">
											<thead>
												<tr >
												<!--<th scope="col">#</th>-->
												<th scope="col">File Name</th>
												<th scope="col" >Creation date</th>
												<!--<th scope="col">Start Date</th>
												<th scope="col">End Date</th>-->
												<th scope="col">File Type</th>
												<th scope="col">Flag</th>
												<th scope="col"></th>
											  </tr>
										</thead>
										<?php 
											render_view_files($result);
										?>
										</table>
									<?php }
										else {echo '<p>Unable to retrieve data. Please retry or contact AIDA admin.</p>';}?>
						  
								</div>
							</div>
						  
							<div id="global" class="tab-pane">
								<div class="panel-body panel-rep">
								<?php 
									$result = get_list($mysqli, "", "", "stored",""); 
									if($result !="error"){
								?>                                       
									<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-stored-global">
										<thead>
											<tr >
											<!--<th scope="col">#</th>-->
											<th scope="col">File Name</th>
											<th scope="col" >Creation date</th>
											<th scope="col">Owner</th>
											<!--<th scope="col">Start Date</th>
											<th scope="col">End Date</th>-->
											<th scope="col">File Type</th>
											<th scope="col">Flag</th>
											<th scope="col"></th>
										  </tr>
										</thead>										
									<?php 
										render_view_files($result);
									?>
									</table>
								<?php }
									else {echo '<p>Unable to retrieve data. Please retry or contact AIDA admin.</p>';}?>                                      
								</div>
							</div>
					  
							<div id="temp-data" class="tab-pane">
								<div class="panel-body panel-rep">
								<?php 
									$result = get_tmp_files($mysqli, $_SESSION['username'], $ftype="", $exclude="upload"); 
									if($result !="error"){
								?>                                       
									<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-temp">
										<thead>
											<tr >
											<!--<th scope="col">#</th>-->
											<th scope="col">File Name</th>
											<th scope="col" >System</th>
											<th scope="col">Subsystem</th>
											<th scope="col">Start Date</th>
											<th scope="col">End Date</th>
											<th scope="col"></th>
										  </tr>
										</thead>										
									<?php 
										render_tmp_files($result);
									?>
									</table>
								<?php }
									else {echo '<p>Unable to retrieve data. Please retry or contact AIDA admin.</p>';}?>                                      
								</div>
							</div>
						  
							<div id="temp-uploaded" class="tab-pane">
								<div class="panel-body panel-rep">
								<?php 
									$result = get_tmp_files($mysqli, $_SESSION['username'], $ftype="upload", $exclude=""); 
									if($result !="error"){
								?>                                       
									<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-uploaded">
										<thead>
											<tr >
											<!--<th scope="col">#</th>-->
											<th scope="col" >File Name</th>
											<th scope="col" >Format</th>
											<th scope="col" ></th>
										  </tr>
										</thead>										
									<?php 
										render_tmp_files($result,$ftype="upload");
									?>
									</table>
								<?php }
									else {echo '<p>Unable to retrieve data. Please retry or contact AIDA admin.</p>';}?>                                      
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

	</body>
</html>