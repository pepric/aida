<!doctype html>
<html class="fixed">
	<?php include("header.php"); ?>
	<?php include("functions.php");?>

			<div class="inner-wrapper">
				<?php include("sidebar.php"); ?>

				<section role="main" class="content-body">
					<header class="page-header">
						<h2>Dashboard</h2>
					</header>

					<!-- start: page -->
						<div class="row">
							<div class="col-xs-12">
								<section class="panel">
									<header class="panel-heading">
										<div class="panel-actions">
											<a href="#" class="fa fa-caret-down"></a>
											<a href="#" class="fa fa-times"></a>
										</div>
						
										<h2 class="panel-title">Select Data to Plot</h2>
									</header>
									<div class="panel-body">
										<h3>RISULTATI</h3>
										<?php
										
										$plot = $_POST['plot_type'];
										$n_ypar = $_POST['n_ypar'];
										
										echo "PLOT: ".$plot."</br>";
										echo "N PARAMS: ".$n_ypar."</br>";
										
										
										$source = $_POST['hktm_source'];
										echo "SOURCE: ".$source."</br>";
										/*$subsystem = $_POST['hktm_qla'];
										echo "SUBSYSTEM: ".$subsystem."</br>";
										
										$xrow = $_POST['x-det-row'];
										$xcol = $_POST['x-det-col'];
										if(isset($_POST['x-quadrant'])){
											$xquad = $_POST['x-quadrant'];
											$xdetector = 'CCD_'.$xrow.'-'.$xcol;
											if ($xquad !=""){
												$xdetector.="['".$xquad."']";
											}
										}
										else{
											$xlayer=get_det_layer($xrow.$xcol);
											$xdetector = 'DET_'.$xrow.$xcol.'['.$xlayer.']';
										}
										echo 'X-DETECTOR: '.$xdetector."</br>";
										
										$yrow = $_POST['y-det-row'];
										$ycol = $_POST['y-det-col'];
									
										if(isset($_POST['y-quadrant'])){
											$yquad = $_POST['y-quadrant'];
											$ydetector = 'CCD_'.$yrow.'-'.$ycol;
											if ($yquad !=""){
												$ydetector.="['".$yquad."']";
											}
										}
										else{
											$ylayer=get_det_layer($yrow.$ycol);
											$ydetector = 'DET_'.$yrow.$ycol.'['.$ylayer.']';
										}
										echo 'Y-DETECTOR: '.$ydetector."</br>";





										$xpar = $_POST['x-params'];
										$xval = $_POST['x-values'];
										
										echo "X PARAMS: ".$xpar."</br>";
										echo "X VALUES: ".$xval."</br>";
										
										$ypar = $_POST['y-params'];
										$yval = $_POST['y-values'];
										
										echo "Y PARAMS: ".$ypar."</br>";
										echo "Y VALUES: ".$yval."</br>";

										$tstart = $_POST['tstart'];
										$tend = $_POST['tend'];
										
										$tstart = DateTime::createFromFormat('m/d/Y', $tstart);
										$tstart = date_format($tstart, 'Ymd');
										
										$tend = DateTime::createFromFormat('m/d/Y', $tend);
										$tend = date_format($tend, 'Ymd');
										
										echo "START TIME: ".$tstart."</br>";
										echo "END TIME: ".$tend."</br>";
							
										
										// QUERY TO DB FOR LOCAL LIST FILES
										$result = get_file_list($source, $subsystem, $tstart, $tend);
										$listfile = array();
										//$timefile = array();
										while($rs=$result->fetch_assoc()){
											$listfile[] = $rs;
											//$listfile[] = $rs['filename'];
											//$timefile[] = $rs['data_time'];
											//echo $rs['filename'].' - ' .$rs['data_time'].'</br>';
										}
										
										$data = json_encode($listfile);
										print $data;
										
										*/
										
										//echo $listfile[0];
										//echo $timefile[0];
										
										
										
										
										?>
										
									</div>
								</section>
							</div>
						</div>
						<div class="row">
							<div class="col-xs-12">
								<section class="panel">
									<header class="panel-heading">
										<div class="panel-actions">
											<a href="#" class="fa fa-caret-down"></a>
											<a href="#" class="fa fa-times"></a>
										</div>
						
										<h2 class="panel-title">Scatter Plot</h2>
									</header>
									<div class="panel-body">
										<div id = "plot"></div>
									</div>
								</section>
							</div>
						</div>
						

		</section>
						

	
	<?php include("footer.php"); ?>
	<script>
    $(document).ready(function() {
        function updateMsg() {
    $.ajax({
        type: "POST",
        url: "/prova.py",
        data: {'test': <?php echo $plot;?>},
        cache: false,
		success: function(returndata){
                    $("#plot").html(returndata);
               }
    });
    }});

	</script>
</html>