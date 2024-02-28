<!doctype html>
<html class="fixed">
	<?php
		$title = "Statistical Analysis";
		include("header.php"); 
/*		include("stats_panel.php");*/
		include("plotcontainer.php");
	?>
		<div class="row">
			<div class="col-xs-12" id = "form-div">
				<section class="panel">
					<header class="panel-heading">
						<div class="panel-actions">
							<a href="#" class="fa fa-caret-down"></a>
							<a href="#" class="fa fa-times"></a>
						</div>
						<h2 class="panel-title">Statistics</h2>
					</header>
					<div class="panel-body">
						<form id="detector_form" class="form-horizontal form-bordered" method="" action="">
							<div class="form-group">
								<label class="col-md-2 control-label">Data source</label>
								<div class="col-md-6">
									<select name="hktm_source" id="hktm_source" class="form-control" required>
										<option value="" disabled selected>Select Data source</option>
										<?php populate_dropdown("systems", "name", "enabled=1 AND origin='".$_GET['s']."'");?>
									</select>
								</div>
							</div>
							<div class="form-group" id="daterange" style="display:none; float:left">
								<label class="col-md-2 control-label">Date range (UTC)</label>
								<div class="col-md-8">
									<div class='input-daterange input-group date' >
										<span class="input-group-addon" id="dateiconstart">
											<span class="glyphicon glyphicon-calendar"></span>
										</span>
										<input type='text' class="form-control indate" name="tstart" id="tstart" required />
									</div>
									<div class='input-daterange input-group date' >
										<span class="input-group-addon" id="dateiconend">
											<span class="glyphicon glyphicon-calendar"></span>
										</span>
										<input type='text' class="form-control indate" name="tend" id="tend" required />
									</div>
								</div>
							</div>
							<div class="form-group" id="hidden-fields">
								<input type="hidden" name="det-type" id = "det-type" value="None"></input>
								<input type="hidden" name="n_ypar" id = "n_ypar" value=1></input>
								<input type="hidden" name="plot_type" id = "plot_type" value="stats" disabled></input>
								<input type="hidden" name="stats_enable" id = "stats_enable" value="advanced" disabled></input>
								<input type="hidden" name="stats_list" id = "stats_list" value=""></input>
								<input type="hidden" name="usecase" id = "usecase" value="<?php echo $_GET['s']; ?>" disabled></input>
								<span id="plotdata" ></span>
							</div>
						</form>                                          
						<form id="stats_form" class="form-horizontal form-bordered" method="" action="">
							<div class="form-group" id="stats" style="display:none;">
								<label class="col-md-2 control-label">Statistical Tools</label>
								<div class="stat-list col-md-6">
									<input type="checkbox" id="checkThemAll">Select/Deselect All</input>
									<?php populate_stats();?>
								</div>
							</div>
						</form>
						<div class="col-md-12" style="text-align:right">
						<button class="btn btn-primary" id = "submit_button">Submit</button>
						<button type="reset" class="btn btn-default" onClick="window.location.reload();">Reset</button>
						</div>
					</div>
				</section>
			</div>
		</div>

		<?php include("loader.html"); ?>
		<div id="plot_img" style="display:none"><img id = "png_img"></img></div>
		<?php include("modalbox.php"); show_modal("exp");?>
	</section>						

	<?php include("footer.php"); ?>
	<?php include("base_scripts.html"); ?>			
	<?php include("form_scripts.html"); ?>
	<script src="assets/vendor/jquery-datatables/media/js/jquery.dataTables.js"></script>
	<script src="assets/vendor/jquery-datatables/extras/TableTools/js/dataTables.tableTools.min.js"></script>
	<script src="assets/vendor/DataTables/datatables.min.js"></script>
	<!-- IOT -->
	<script src="assets/javascripts/lsst/plots.js"></script>
	
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