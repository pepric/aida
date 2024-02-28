<!doctype html>
<html class="fixed">
	<?php
		$title = "Machine Learning";
		include("header.php"); 

?>

		<div class="col-xs-12" id = "form-div">
			<section class="panel">
				<header class="panel-heading">
					<div class="panel-actions">
						<a href="#" class="fa fa-caret-down"></a>
						<a href="#" class="fa fa-times"></a>
					</div>

					<h2 class="panel-title">Model Selection</h2>
				</header>
				<div class="panel-body">
					<form id="ml_form" class="form-horizontal form-bordered" method="get" action="">
						<label class="col-md-2 control-label">Machine Learning Model</label>
						<div class="stat-list col-md-6">
							<?php populate_ml();?>
							<input type="hidden" name="s" id="hiddenField" value="<?php echo $_GET['s'] ?>" />
						</div>
						<button class="btn btn-primary"  formaction="ml.php" id = "submit_button">Select</button>
						<button class="btn btn-primary"  formaction="modelHelp.php" id = "submit_button" formtarget="_blank">Help</button>
					</form>
				</div>
			</section>
		</div>		
								


		<?php include("footer.php"); ?>
					
		<!-- Vendor-->
		<script src="assets/vendor/jquery/jquery.js"></script> 
		<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>
		<script src="assets/javascripts/lsst/moment.js"></script>
		<script src="assets/javascripts/lsst/moment-timezone.js"></script>
		<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
		<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
		<script src="assets/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.js"></script>
		<script src="assets/vendor/magnific-popup/magnific-popup.js"></script>
		<script src="assets/vendor/jquery-placeholder/jquery.placeholder.js"></script>


		<!-- Form-->
		<script src="assets/vendor/select2/select2.js"></script>
		<script src="assets/vendor/bootstrap-multiselect/bootstrap-multiselect.js"></script>
		<script src="assets/vendor/jquery-maskedinput/jquery.maskedinput.js"></script>
		<script src="assets/vendor/bootstrap-tagsinput/bootstrap-tagsinput.js"></script>
		<script src="assets/vendor/bootstrap-colorpicker/js/bootstrap-colorpicker.js"></script>
		<!--<script src="assets/vendor/bootstrap-timepicker/js/bootstrap-timepicker.js"></script>-->
		<script src="assets/vendor/fuelux/js/spinner.js"></script>
		<script src="assets/vendor/dropzone/dropzone.js"></script>
		<script src="assets/vendor/bootstrap-markdown/js/markdown.js"></script>
		<script src="assets/vendor/bootstrap-markdown/js/to-markdown.js"></script>
		<script src="assets/vendor/bootstrap-markdown/js/bootstrap-markdown.js"></script>
		<script src="assets/vendor/codemirror/lib/codemirror.js"></script>
		<script src="assets/vendor/codemirror/addon/selection/active-line.js"></script>
		<script src="assets/vendor/codemirror/addon/edit/matchbrackets.js"></script>
		<script src="assets/vendor/codemirror/mode/javascript/javascript.js"></script>
		<script src="assets/vendor/codemirror/mode/xml/xml.js"></script>
		<script src="assets/vendor/codemirror/mode/htmlmixed/htmlmixed.js"></script>
		<script src="assets/vendor/codemirror/mode/css/css.js"></script>
		<script src="assets/vendor/summernote/summernote.js"></script>
		<script src="assets/vendor/bootstrap-maxlength/bootstrap-maxlength.js"></script>
		<script src="assets/vendor/ios7-switch/ios7-switch.js"></script> 

		<!-- Form validation -->
		<script src="assets/vendor/jquery-validation/jquery.validate.js"></script>

		<!-- IOT -->
		<script src="assets/javascripts/lsst/ml.js"></script>

		<!-- Theme Base, Components and Settings -->
		<script src="assets/javascripts/theme.js"></script>

		<!-- Theme Custom -->
		<script src="assets/javascripts/theme.custom.js"></script>

		<!-- Theme Initialization Files -->
		<script src="assets/javascripts/theme.init.js"></script>


		<!-- Validation -->
		<script src="assets/javascripts/lsst/validation.js"></script>

		<script src="assets/javascripts/lsst/jqscripts.js"></script>

	</body>
</html>
											