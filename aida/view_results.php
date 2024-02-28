<!doctype html>
<html class="fixed">
	<?php
  		$tolog = 0;
		$title = "View Plot";
		include("header.php"); ?>

		<?php if($tolog==0){?>
  
		<!-- start: page -->
		<?php include("plotcontainer.php"); ?>
		<div class="row">
			<div class="col-xs-12" id = "form-div">
				<section class="panel">
					<div class="panel-body" style="display:none">
						<form id="detector_form" class="form-horizontal form-bordered" method="" action="" novalidate = "novalidate">
							<div class="form-group" id="hidden-fields">
								<input type="hidden" name="det-type" id = "det-type" value="None"></input>
								<input type="hidden" name="n_ypar" id = "n_ypar" value=1></input>
								<input type="hidden" name="plot_type" id = "plot_type" value="" disabled></input>
								<input type="hidden" name="stats_enable" id = "stats_enable" value="global" disabled></input>
								<input type="hidden" name="stats_list" id = "stats_list" value=""></input>
								<input type="hidden" name="hktm_source" id = "hktm_source" value="<?php echo $_GET['s']; ?>"></input>
								<input type="hidden" name="usecase" id = "usecase" value="" disabled></input>
								<span id="plotdata" ></span>
								<?php 
									if(isset($_GET['id'])){$id = $_GET['id'];} else {$id="none";}?> 									
								<input type="hidden" name="plotid" id = "plotid" value="<?php echo $id; ?>" disabled></input>
							</div>
						</form>
					</div>
				</section>
			</div>
		</div>
		<?php include("loader.html"); ?>
		<canvas id="canvas"></canvas>
		<div id="plot_img" style="display:none"><img id = "png_img"></img></div>
		<?php include("modalbox.php"); show_modal("exp");?>
		


		<?php } else {?>
		<div class="row">
			<div class="col-xs-12" id = "form-div">
				<section class="panel">
					<div class="panel-body">
						<h2>You must be logged to view plot. Please, login in a separate tab and then refresh this page.</h2>
					</div>
				</section>
			</div>
		</div>
		<?php } ?>
	</section>

	<?php include("footer.php"); ?>
	<?php include("base_scripts.html"); ?>
	<?php include("form_scripts.html"); ?>	
	<script src="assets/vendor/jquery-datatables/media/js/jquery.dataTables.js"></script>
	<script src="assets/vendor/jquery-datatables/extras/TableTools/js/dataTables.tableTools.min.js"></script>
	<script src="assets/vendor/DataTables/datatables.min.js"></script>

	<!-- IOT -->
	<script src="assets/javascripts/lsst/plots.js"></script>
	<script src="assets/javascripts/lsst/forms.js"></script>	
	<!-- Validation -->
	<script src="assets/javascripts/lsst/validation.js"></script>
	
	<!-- Theme Base, Components and Settings -->
	<script src="assets/javascripts/theme.js"></script>
	
	<!-- Theme Custom -->
	<script src="assets/javascripts/theme.custom.js"></script>
	
	<!-- Theme Initialization Files -->
	<script src="assets/javascripts/theme.init.js"></script>
	
	<script src="assets/javascripts/lsst/jqscripts.js"></script>


<script>
	document.addEventListener("DOMContentLoaded", function(){
      	var id = document.getElementById("plotid").value
		if(id != "none"){
		   	$.ajax({
			method : 'POST',
           	datatype    : 'json',
			url : 'scripts/cs_interface.py',
			data : {
				plotid: id,
	           	action : "view_plot_from_db",
			},
			beforeSend: function(){
				// Show loader image container
				$("#loader").show();
			},              
			success : function(response){
              	//update title
               	$('#plot-title').text(response['plot_name']);
              	var plot = response['plot_type']
				var usecase = response['usecase']
				var user = response['username']
               	// get output data
				var jsondata = JSON.parse(response['plot_data'])

				if(jsondata["errstatus"]==0 && jsondata["datastatus"]==0){
						// get labels
						var labels = response['labels'].split(",")
						var flist = response['stats_list'].split(",")
						var source = response['stats_enable']

						document.getElementById("plot_type").value = plot
 						document.getElementById("modal-labels").value = response['labels']
						document.getElementById("modal-tstart").value = response['tstart']     
						document.getElementById("modal-tstop").value = response['tstop']
						document.getElementById("plotdata").innerHTML = response['plot_data']
						document.getElementById("usecase").value = usecase
						document.getElementById("img_op").value = response['plot_type']
						
						render_img_stats(jsondata, labels, plot, flist)
						render_img_files_tbl(jsondata, labels, plot, user, flist,source)   
				}
				else{
					var msg = jsondata["msg"].replace(/_RETCHAR_/g,"\n")
					alert(msg)
					window.close()
				}
            },
			complete:function(data){
				var tabstats = document.getElementById("tab-stats1")
                if(tabstats.style.display == "none"){hide_pdf()}

				$("#loader").hide();
			}
	});

          
        }      	
		else{
        	alert("Unable to get plot id. Please check url.")
        }
    	
  
    });




</script>

</html>
</body>