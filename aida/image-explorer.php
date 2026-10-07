<?php
/**
 * Image Explorer JS9 Main View.
 *
 * Renders the main container page for the JS9 web-based astronomical FITS image viewer,
 * loading JS9 dependencies, plugins, and custom styles.
 *
 * @package    AIDA
 * @subpackage Views\Images
 * @author     Giuseppe Riccio
 * @version    1.1.0
 */
?>
<!doctype html>
<html class="fixed">
	<?php 
		$title = "Image Explorer";
		include("header-js9.php"); ?>
					<!-- start: page -->
						<?php include("js9_app.php"); ?>
	<?php include("footer.php"); ?>
	
	<!-- IOT -->
	<script src="assets/javascripts/lsst/treeview.js"></script>

	<!-- Theme Base, Components and Settings -->
	<script src="assets/javascripts/theme.js"></script>
	
	<!-- Theme Custom -->
	<script src="assets/javascripts/theme.custom.js"></script>
	
	<!-- Theme Initialization Files -->
	<script src="assets/javascripts/theme.init.js"></script>

	</body>
</html>