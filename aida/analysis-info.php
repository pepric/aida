<!doctype html>
<html class="fixed">
	<?php
		include('functions.php');
		if(isset($_GET['subj'])){
  			$origin = $_GET['subj'];
          	$err_subj = 0;
		}
        else{
          	$origin = "Analysis";
          	$err_subj = 1;
                            
        }  
  		$title = "Available ".ucfirst($origin);
		include("header.php"); 
  	?>
  		
		<!-- start: page -->
		<div class="row">
			<div class="col-xs-12" id = "analysis-div">
				<section class="panel">
					<header class="panel-heading">
						<h2 class="panel-title"><?php echo ucfirst($origin);?> Info</h2>
					</header>
					<div class="panel-body">
						<?php if($err_subj==0){
								render_analysis($origin);
							}
                      		else{
                            	echo '<p>Unable to get data origin</p>';
                            }
                      	?> 
					</div>
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