<!doctype html>
<html class="fixed">
	<?php
		include('functions.php');  
  		$title = strtoupper($_GET['subj'])." - Available Systems";
		include("header.php"); 
  	?>
  		
		<!-- start: page -->
		<div class="row">
			<div class="col-xs-4" id = "systems-div">
				<section class="panel">
					<header class="panel-heading">
						<h2 class="panel-title">Systems Info</h2>
					</header>
					<div class="panel-body">
						<?php if(isset($_GET['subj'])){
  								$origin = $_GET['subj'];
								render_systems($origin);
							}
                      		else{
                            	echo '<p>Unable to get data origin</p>';
                            
                            }
                      	?> 
						
					</div>
				</section>
			</div>
			<div class="col-xs-8" id = "parinfo-div" style="display : none">
				<section class="panel">
					<header class="panel-heading">
						<div class="panel-actions">
							<!--<a href="#" class="fa fa-caret-down"></a>-->
							<a href="#" class="fa fa-times-circle-o" onclick="$('#parinfo-div').css('display','none')"></a>
						</div>
						<h2 class="panel-title" id="parinfo-title"></h2>
					</header>
					<div class="panel-body" id="parinfo-tbl"></div>
				</section>
			</div>          
          
          
		</div>

	</section>
						


	<?php include("footer.php"); ?>
	<?php include("base_scripts.html"); ?>
	<script src="assets/vendor/jquery-datatables/media/js/jquery.dataTables.js"></script>
	<script src="assets/vendor/jquery-datatables/extras/TableTools/js/dataTables.tableTools.min.js"></script>
  	<script src="assets/vendor/DataTables/datatables.min.js"></script>
	
	<!-- Theme Base, Components and Settings -->
	<script src="assets/javascripts/theme.js"></script>
	
	<!-- Theme Custom -->
	<script src="assets/javascripts/theme.custom.js"></script>
	
	<!-- Theme Initialization Files -->
	<script src="assets/javascripts/theme.init.js"></script>
	<script src="assets/javascripts/lsst/tab-init.js"></script>
	
	<script src="assets/javascripts/lsst/jqscripts.js"></script>
 


</html>
</body>