	<?php include("header.php");
  		//redirect to dashboard if logged
		if($check == true){   
			exit("<script type='text/javascript'>window.location.href='dashboard.php';</script>");
   		}
	?>	
	
	<div class="row">
		<div class="col-md-12">
			<div class="panel-body panel-body-index">
				<div class="first-panel col-md-12">
					<div class = "col-md-2"></div>
					<div class = "description col-md-8">
					<!--	<p style="margin-top:20px"><img src="assets/images/logoAIDA.png" height="150" alt="" /></p>-->
						<h2>What is AIDA?</h2>
						<p>AIDA is a Rubin LSST monitoring, analysis & visualization web app fully accessible through network connection</p>
					</div>
					<div class = "col-md-2"></div>
				</div>
									
				<div class="second-panel col-md-12">
					<div class = "col-md-2"></div>
					<div class = "description col-md-8">
						<h2>Main Functionalities</h2>
						<ul>
							<li>Monitoring report generation and delivery
								<ul>
									<li>periodic report generation on a pre-defined parameter list and delivery of the link to remote archives;</li>
									<li>on demand customised report generation on a user selected parameter list, locally stored;</li>
								</ul>
							</li>
							<li>Visualization
								<ul>
									<li>series of plots on user selected parameters/data products and ranges
										<ul>
											<li>dynamic histograms, scatter plots, trend plots</li>
										</ul>
									</li>
									<li>observed images (static view and dynamic windowing)</li>
								</ul>
							</li>
							<li>Statistics
								<ul>
									<li>base (default) estimators (automatically produced with the plots)
										<ul>
											<li>mean, median, RMS, σ, variance, min-max, MAD, NMAD, kurtosis, skewness, ...</li>
										</ul>
									</li>
									<li>special estimations (tables/images)
										<ul>
											<li>mode, percentiles, map counting, thresholding maps, biweight, σ-clipping, ...</li>
										</ul>
									</li>
								</ul>
							</li>
						</ul>
					</div>
					<div class = "col-md-2"></div>
				</div>
			</div>
		</section>
	</div>
<?php include("modalbox.php"); show_modal("loginerr");?>					<!-- end: page -->
</section>
</div>
</section>

<?php include("footer.php"); ?>

<!-- Vendor-->
<script src="assets/vendor/jquery/jquery.js"></script> 
<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script>
<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
<!-- Theme Base, Components and Settings -->
<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
<script src="assets/javascripts/theme.js"></script>
<!-- Theme Custom -->
<script src="assets/javascripts/theme.custom.js"></script>
<!-- Theme Initialization Files -->
<script src="assets/javascripts/theme.init.js"></script>

<script>  
	$("#password").keypress(function(event) { 
		if (event.keyCode === 13) { 
			$("#loginbtn").click(); 
		} 
	});
  

  
  
  
</script> 
</body>
</html>

		
</div>