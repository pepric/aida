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