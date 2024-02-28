<!doctype html>
<html class="fixed">
	<?php
		include('functions.php');  
  		$title = "Image Analysis";
		include("header.php"); 
  	?>
  		
		<!-- start: page -->
		<?php include("imagedatacontainer.php"); ?>
		<div class="row">
			<div class="col-xs-12" id = "form-div">
				<section class="panel">
					<header class="panel-heading">
						<div class="panel-actions">
							<a href="#" class="fa fa-caret-down"></a>
							<a href="#" class="fa fa-times"></a>
						</div>
						<h2 class="panel-title">Select Data to Plot</h2>
					</header>
					<div class="panel-body">
						<form id="detector_form" class="form-horizontal form-bordered" method="" action="" novalidate = "novalidate">
							<div class="form-group">
								<label class="col-md-2 control-label">Data source</label>
								<div class="col-md-6">
									<select name="sys_source" id="sys_source" class="form-control" required>
										<option value="" disabled selected>Select Data source</option>
										<?php /*populate_dropdown($_GET['s']."_source", "name", "enabled=1");*/
											populate_dropdown("systems", "name", "enabled=1 AND origin='image'");


										?>
									</select>
								</div>
							</div>
                            <div class="form-group" id="daterange" style="display:none">
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
                                <input type="hidden" name="n_ypar" id = "n_ypar" value=1></input>
                                <input type="hidden" name="plot_type" id = "plot_type" value="image-analysis" disabled></input>
                                <input type="hidden" name="stats_enable" id = "stats_enable" value="global" disabled></input>
                                <input type="hidden" name="stats_list" id = "stats_list" value=""></input>
                                <input type="hidden" name="usecase" id = "usecase" value="image" disabled></input>
                                <span id="plotdata" ></span>
                            </div>
                        </form>


						<div class="col-md-12" style="text-align:right">
							<button class="btn btn-primary" id = "submit_img_button" >Next</button>
							<button type="reset" class="btn btn-default" onClick="window.location.reload();">Reset</button>
						</div>
					</div>
				</section>
			</div>
		</div>

		<?php include("loader.html"); ?>
		<canvas id="canvas"></canvas>
		<div id="plot_img" style="display:none"><img id = "png_img"></img></div>
			<!--<button class="btn btn-default" onClick="prova()">Marker to Red</button>-->
			<?php include("modalbox.php"); show_modal("exp");?>
	</section>
						


	<?php include("footer.php"); ?>
	<?php include("base_scripts.html"); ?>
	<?php include("form_scripts.html"); ?>	
	<script src="assets/vendor/jquery-datatables/media/js/jquery.dataTables.js"></script>
	<script src="assets/vendor/jquery-datatables/extras/TableTools/js/dataTables.tableTools.min.js"></script>
	<!--<script src="assets/vendor/jquery-datatables-bs3/assets/js/datatables.js"></script>-->
	<script src="assets/vendor/DataTables/datatables.min.js"></script>

	<!-- IOT -->
	<script src="assets/javascripts/lsst/forms.js"></script>	
	<!-- Validation -->
	<script src="assets/javascripts/lsst/validation.js"></script>
	
	<!-- Theme Base, Components and Settings -->
	<script src="assets/javascripts/theme.js"></script>
	
	<!-- Theme Custom -->
	<script src="assets/javascripts/theme.custom.js"></script>
	
	<!-- Theme Initialization Files -->
	<script src="assets/javascripts/theme.init.js"></script>

	
	<script src="assets/javascripts/lsst/image-analysis.js"></script>

</html>
</body>