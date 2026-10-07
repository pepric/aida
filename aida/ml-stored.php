<?php
/**
 * Stored Machine Learning Experiments Dashboard Panel View.
 *
 * Renders the dashboard panel table listing executed Machine Learning experiments,
 * including technique, model type, data source, date range, user, generation date, and download links.
 *
 * @package    AIDA
 * @subpackage Views\MachineLearning
 * @author     Giuseppe Riccio
 * @version    1.1.0
 */
?>
<div class="panel-body panel-dash">
	<div class="col-md-12">
		<header class="panel-heading">
			<h2 class="panel-title">Machine Learning Experiments</h2>
		</header>			
		<div class="col-md-12 dashpanel">
			<div class="col-md-12">
				<section class="panel">
					<div class="panel-body" id="mlexp">
						<!--<div class="col-md-12" style="overflow-x:hidden" id="treeRunning"></div>-->
						<?php /*include("running_reports.php");*/?>
						<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-ml_stored">
							<thead>
								<tr >
								<!--<th scope="col">#</th>-->
								<th scope="col">ID</th>
								<th scope="col">ML Technique</th>
								<th scope="col">Model</th>
								<th scope="col">Data Source</th>
								<th scope="col">Dates Interval</th>
								<th scope="col">User</th>
								<th scope="col">Generation Date</th>
								<th scope="col"></th>
							  </tr>
							</thead>
						</table>
					</div>
				</section>
			</div>
		</div>
	</div>
</div>
