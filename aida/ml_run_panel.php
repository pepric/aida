					<!-- start: page -->
						<?php include("plotcontainer.php"); ?>
					
					
					
					
						<div class="row">
							<div class="col-xs-12" id = "form-div">
								<section class="panel">
									<header class="panel-heading">
										<div class="panel-actions">
											<a href="#" class="fa fa-caret-down"></a>
											<a href="#" class="fa fa-times"></a>
										</div>
						
										<h2 class="panel-title">Machine Learning</h2>
									</header>
									<div class="panel-body">
										<form id="detector_form" class="form-horizontal form-bordered" method="" action="">
										<!--<form class="form-horizontal form-bordered" method="post" action="result.php">-->
											<div class="form-group">
												<label class="col-md-2 control-label">Data source</label>
												<div class="col-md-6">
													<!--<select data-plugin-selectTwo class="form-control populate">-->
													<select name="hktm_source" id="hktm_source" class="form-control" required>
														<option value="" disabled selected>Select Data source</option>
																								<?php /*populate_dropdown($_GET['s']."_source", "name", "enabled=1");*/
											populate_dropdown("systems", "name", "enabled=1 AND origin='".$_GET['s']."'");


										?>
														
														<?php /*populate_dropdown($_GET['s']."_source", "name", ""); */?>
													</select>
													<!--</select>-->
												</div>
											</div>
											
											<!--<div class="form-group" id="sys" style="display:none;">
												<label class="col-md-2 control-label">Subsystem</label>
												<div class="col-md-6">
													<select id = "subsystem" onchange="set_qla_params(this.value)"></select>
												</div>
											</div>-->
									<div class="panel-body">

										<form id="ml_form" class="form-horizontal form-bordered" method="get" action="">
												<label class="col-md-2 control-label">Machine Learning Model</label>
												<div class="stat-list col-md-6">
													<?php populate_ml_model();?>
													<input type="hidden" name="s" id="hiddenField" value="<?php echo $_GET['s'] ?>" />

											</div>
											<div class="form-group" id="yparams" style="display:none; float:left">
												<label style="display:block" class="col-md-2 control-label" id = "y-label">Features</label>
												<div id="y0-par-form" class="col-md-10">
													<select id = "y0-sys" onchange="set_params(this)" class="form-control"></select>
													<select id = "y0-params" name="y0-params" style="display:none" onchange="populate_values(this)" class="form-control">
														<option value="" disabled selected>Parameter</option>
														<?php //populate_dropdown("hktm_qla_params", "param", ""); ?>
													</select>
													<select id="y0-values" name="y0-values" style="display:none"></select>
													
													<button type="button" class="mb-xs mt-xs mr-xs btn btn-primary btn-sm" id = "addmore" style="display:none;">Add more...</button>
													
													<button type="button" class="mb-xs mt-xs mr-xs btn btn-danger btn-sm" id = "remove" style="display:none;">Remove Last...</button>
													<!--</select>-->
												</div>
											</div>
											<div class="form-group" id="params" style="display:none; float:left">
												<label style="display:block" class="col-md-2 control-label" >Label</label>
												<div id="x-par-form" class="col-md-10">
													<select id = "x-sys" class="form-control" onchange = "set_params(this)" required></select>
													<select id = "x-params" name="x-params" class="form-control" style="display:none" onchange="populate_values(this)" required>
														<option value="" disabled selected>Parameter</option>
													</select>
													<select id="x-values" name="x-values" style="display:none"></select>

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
												<input type="hidden" name="plot_type" id = "plot_type" value="scatter" disabled></input>
												<input type="hidden" name="stats_enable" id = "stats_enable" value="global" disabled></input>
												<input type="hidden" name="stats_list" id = "stats_list" value=""></input>
												<input type="hidden" name="usecase" id = "usecase" value="<?php echo $_GET['s']; ?>" disabled></input>
												<input type="hidden" name="model" id = "model" value="<?php echo $_GET['model']; ?>" disabled></input>
											</div>
										</form>
											
											 

							
										<form id="stats_form" class="form-horizontal form-bordered" method="" action="">
													<?php populate_ml_param($_GET['model']);
													echo '<a href="modelHelp.php?model='.$_GET['model'].'" target="_blank"><b>'.$_GET['model'].' Help</b></a>';
													?>
										</form>
										<form id="splitting" class="form-horizontal form-bordered" method="" action="">

										 <div class="stat-list col-md-6">										
										 <label class="col-md-2 control-label">Train - Test Split</label> <div class="stat-list col-md-6">

										  <input type="range" min="1" max="100" value="70" class="slider" id="traintest">
										  <p>Percentage of data to be used as Train: <span id="outtraintest"></span></p>
										  
										<label for="splitRandomState"><b>Random Seed for the Split</b></label> <input type="text" id="splitRandomState" name="splitRandomState" value="None">
										</div>
										</form>

										<script>
										var slider = document.getElementById("traintest");
										var output = document.getElementById("outtraintest");
										output.innerHTML = slider.value;

										slider.oninput = function() {
										  output.innerHTML = this.value;
										}
										</script>

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
				<?php include("modalbox.php"); ?>
			</section>	
			