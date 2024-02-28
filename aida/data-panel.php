<div class="panel-body panel-dash">

			<div class="col-md-12 ">
				<header class="panel-heading">
					<div class="panel-actions" style="top:10px">
						<button type="button" class="btn btn-primary" onclick="update_tree('', '#treeUser', [], 1); update_tree('stored', '#treeStored', [], 1)">Refresh</button>
					</div>
					<h2 class="panel-title">Stored Experiments</h2>
				</header>
				<div class="col-md-6 dashpanel">
					<section class="panel">
						<header class="panel-heading">
							<div class="panel-actions" style="top:10px">
								<div class="wait" id="wait_treeUser"><img src="./assets/images/loader_wait.gif" width="58px"/></div>
							
							</div>
							<h2 class="panel-title">User</h2>
						</header>
						<div class="panel-body">
							<div class="col-md-12" style="overflow-x:hidden" id="treeUser"></div>
					
						</div>
					</section>
					
				
				</div>
				<div class="col-md-6 dashpanel">
					<section class="panel">
						<header class="panel-heading">
							<div class="panel-actions" style="top:10px">
								<div class="wait" id="wait_treeStored"><img src="./assets/images/loader_wait.gif" width="58px"/></div>
							
							</div>
							<h2 class="panel-title">Public</h2>
						</header>
						<div class="panel-body">
							
							<div class="col-md-12" style="overflow-x:hidden" id="treeStored"></div>
						
						</div>
					</section>				
				</div>
			</div>

</div>