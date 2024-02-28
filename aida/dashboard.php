<!doctype html>
<html class="fixed">
	<?php 
		$title = "Dashboard";
		include("header.php"); ?>
	<!-- start: page -->
	

	<div class="row">
		<div class="col-xs-12" style="margin-bottom:15px">
			<div class="col-md-6">
			<p><h4>Current Operating Mode: <b><span id="opmode"><?php echo get_opmode();?></span></b></h4></p>
			</div>
			<div class="col-md-6" style = "text-align:right;">
			<p><i>Last access: <?php echo $_SESSION["last_login"];?></i></p>
			</div>
		</div>
		<div class="tabs tabs-primary" id="dash-tabs">
			<ul class="nav nav-tabs <!--nav-justified-->">
				<li class="active">
					<a href="#user-panel" data-toggle="tab">Reports</a>
				</li>
				<li>
					<a href="#history-panel" data-toggle="tab">History</a>
				</li>
				<!--<li>
					<a href="#data-panel" data-toggle="tab">Stored Data</a>
				</li>-->
				<li>
					<a href="#anomalies-panel" data-toggle="tab">Stored Experiments</a>
				</li>              
				<?php if ($_SESSION["role"]=="admin"){?>
					<li>
						<a href="#admin-users-panel" data-toggle="tab">Administration - Users</a>
					</li>
					<li>
						<a href="#admin-settings-panel" data-toggle="tab">Administration - Settings</a>
					</li>              
				<?php } ?>
			</ul>

		<div class="tab-content">
			<div class="tab-pane active" id="user-panel">
				<?php include("user-panel.php");?>

			</div>
			<div class="tab-pane" id="history-panel">
				<?php include("history-panel.php");?>

			</div>
			<!--<div class="tab-pane" id="data-panel">
				<?php include("data-panel.php");?>

			</div>-->
			<div class="tab-pane" id="anomalies-panel">
				<?php include("anomalies-panel.php");?>

			</div>          
			<?php if ($_SESSION["role"]=="admin"){?>
				<div id="admin-users-panel" class="tab-pane">
					<?php include("admin-users-panel.php");?>
				</div>
				<div id="admin-settings-panel" class="tab-pane">
					<?php include("admin-settings-panel.php");?>
				</div>          
          
          
			<?php } ?>

		</div>

	</div>

	<?php include("loader.html"); ?>
	<?php include("footer.php"); ?>
	<?php include("modalbox.php"); show_modal("pwd");?>		
	
			
		<!-- Vendor-->
		<script src="assets/vendor/jquery/jquery.js"></script> 
		<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>
		<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
	<script src="assets/javascripts/lsst/moment.js"></script>
	<script src="assets/javascripts/lsst/moment-timezone.js"></script>  
		<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
		<script src="assets/vendor/magnific-popup/magnific-popup.js"></script>
		<script src="assets/vendor/jquery-placeholder/jquery.placeholder.js"></script>
		<script src="assets/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.js"></script>		
					<!-- Specific Page Vendor -->
		<script src="assets/vendor/select2/select2.js"></script>
		<script src="assets/vendor/jquery-datatables/media/js/jquery.dataTables.js"></script>
		<script src="assets/vendor/jquery-datatables/extras/TableTools/js/dataTables.tableTools.min.js"></script>
  		<script src="assets/vendor/DataTables/datatables.min.js"></script>
		<script src="assets/vendor/ios7-switch/ios7-switch.js"></script>


		<!-- Specific Page Vendor -->
		<script src="assets/vendor/jstree/jstree.js"></script>
		<script src="assets/vendor/pnotify/pnotify.custom.js"></script>
		<!-- PORTLETS -->
		<script src="assets/vendor/jquery-ui/js/jquery-ui-1.10.4.custom.js"></script>
		<script src="assets/vendor/jquery-ui-touch-punch/jquery.ui.touch-punch.js"></script>
		<script src="assets/vendor/store-js/store.js"></script>
		<!-- File upload -->
		<script src="assets/vendor/bootstrap-fileupload/bootstrap-fileupload.min.js"></script>
		<!-- Form validation -->
		<script src="assets/vendor/jquery-validation/jquery.validate.js"></script>

		<!-- IOT -->
		<script src="assets/javascripts/lsst/forms.js"></script>  
		<script src="assets/javascripts/lsst/validation.js"></script>
		<script src="assets/javascripts/lsst/treeview.js"></script>
		<script src="assets/javascripts/lsst/genreport.js"></script>  
	<script src="assets/javascripts/lsst/jqscripts.js"></script>  
		<!-- Theme Base, Components and Settings -->
		<script src="assets/javascripts/theme.js"></script>
		
		<!-- Theme Custom -->
		<script src="assets/javascripts/theme.custom.js"></script>
		
		<!-- Theme Initialization Files -->
		<script src="assets/javascripts/theme.init.js"></script>
		<script src="assets/javascripts/lsst/tab-init.js"></script>
		<script src="assets/javascripts/lsst/tabs.js"></script>

  <script src="assets/vendor/DataTables/Buttons-1.6.5/js/dataTables.buttons.min.js"></script>
		<!-- File Upload -->
		<script src="assets/javascripts/lsst/jquery-progressbar.min.js"></script> 
		<script src="assets/vendor/plupload/js/plupload.full.min.js"></script>
	<!-- Dashboard scripts -->			
	<script src="assets/javascripts/lsst/dashboard.js"></script>

  
</body>	
</html>