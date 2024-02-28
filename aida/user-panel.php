<div class="panel-body panel-dash">
	<div class="col-md-12">
		<header class="panel-heading">
			<h2 class="panel-title">Reports</h2>
		</header>			
		<div class="col-md-12 dashpanel">
			<div class="col-md-12">
				<section class="panel">
					<header class="panel-heading">
						<h2 class="panel-title">Running Reports Generation</h2>
					</header>
					<div class="panel-body" id="running">
						<!--<div class="col-md-12" style="overflow-x:hidden" id="treeRunning"></div>-->
						<?php /*include("running_reports.php");*/?>
						<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-running">
							<thead>
								<tr >
								<!--<th scope="col">#</th>-->
								<th scope="col">ID</th>
								<?php if($_SESSION["role"] == "admin"){?>
									<th scope="col">User</th>
								<?php }?>
								<th scope="col">Period</th>
								<th scope="col">Config File</th>
								<th scope="col">Current Report Start Date</th>
								<th scope="col">Progress</th>
								<th scope="col"></th>
							  </tr>
							</thead>
						</table>
					</div>
				</section>
			</div>
			<div class="col-md-12">
				<section class="panel">
					<header class="panel-heading">
						<h2 class="panel-title">Flagged Reports</h2>
					</header>
					<div class="panel-body" id="flagged_reports">
						<table class="table tab-reports table-bordered table-striped mb-none" style="width:100%" id="datatable-flag_reports">
							<thead>
								<tr >
									<th scope="col" style="vertical-align:middle">Flag</th>
									<th scope="col" style="vertical-align:middle">Report ID</th>
									<th scope="col" style="vertical-align:middle">Period</th>                              	
									<th scope="col" style="vertical-align:middle">Start Date (UTC)</th>
									<th scope="col" style="vertical-align:middle">End Date (UTC)</th>
									<th scope="col" style="vertical-align:middle"></th>
								  </tr>
							</thead>
						</table>
					</div>
				</section>
			</div>				
				
			<div class="col-md-6">
				<section class="panel">
					<header class="panel-heading">
						<div class="panel-actions" style="top:10px">
							<div class="wait" id="wait_treeReports"><img src="./assets/images/loader_wait.gif" width="58px"/></div>
							<button type="button" class="btn btn-primary" onclick="update_tree('report', '#treeReports', ['pdf','xml'], 1)">Refresh</button>
						</div>
						<h2 class="panel-title">Available Reports</h2>
					</header>
					<div class="panel-body">
						<div class="col-md-12 treeReports" style="overflow-x:hidden" id="treeReports"></div>
					</div>
				</section>
			</div>
			<div class="col-md-6">
				<section class="panel">
					<header class="panel-heading">
						<div class="panel-actions" style="top:10px">
							<div class="wait" id="wait_treeConfig"><img src="./assets/images/loader_wait.gif" width="58px"/></div>
							<button type="button" class="btn btn-primary" onclick="update_tree('config', '#treeConfig', ['json', 'ini'], 1)">Refresh</button>
						</div>
						<h2 class="panel-title">Configuration Files</h2>
					</header>
					<div class="panel-body">
						<div class="col-md-12" style="overflow-x:hidden" id="treeConfig"></div>
					</div>
				</section>
			</div>
		</div>
	</div>
</div>
