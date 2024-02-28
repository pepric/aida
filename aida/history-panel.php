<div class="panel-body panel-dash">
			<div class="col-md-12 ">
		
				<header class="panel-heading">
					<div class="panel-actions" style="top:10px">
                      	<div class="wait" id="wait_history"><img src="./assets/images/loader_wait.gif" width="58px"/></div>
						<button type="button" class="btn btn-primary" onclick="refresh_history()">Refresh</button>
					</div>                  
					<h2 class="panel-title">History</h2>
				</header>
				<div class="col-md-12 dashpanel">
					<div class="col-md-12">
						<section class="panel">
							<header class="panel-heading">
								<!--<div class="panel-actions" style="top:10px">
									<div class="wait" id="wait_treeUserHist"><img src="./assets/images/loader_wait.gif" width="58px"/></div>
									<button type="button" class="btn btn-primary" onclick="update_history('','treeUserHist');">Refresh</button>
								</div>-->
								<div class="panel-actions" style="top:10px">
									<button type="button" class="btn btn-primary" onclick="download_history('<?php echo $_SESSION['username'];?>')">Download Full User History</button>
								</div> 								
								<h2 class="panel-title">User</h2>

							</header>
							<div class="panel-body">
								<div class="moredata" id="moredata">"+morecontent+"</div>
								<div class="col-md-12" id="treeUserHist"></div>
							
							</div>
						</section>
					</div>
					<?php 
						if ($_SESSION["role"]=="admin"){
							$global = "";
						}
						else
						{
							$global = "display : none;";
						}
					?>
					
						<div class="col-md-12" style="<?php echo $global;?>">
							<section class="panel">
								<header class="panel-heading">
									<!--<div class="panel-actions" style="top:10px">
										<div class="wait" id="wait_treeGlobalHist"><img src="./assets/images/loader_wait.gif" width="58px"/></div>
										<button type="button" class="btn btn-primary" onclick="update_history('global','treeGlobalHist');">Refresh</button>
									</div>-->
									<div class="panel-actions" style="top:10px">
										<button type="button" class="btn btn-primary" onclick="download_history()">Download Full History</button>
									</div> 									
									<h2 class="panel-title">Global</h2>
								</header>
								<div class="panel-body">
									<div class="col-md-12" id="treeGlobalHist"></div>
								
								</div>
							</section>
						</div>
					
				</div>

			</div>


</div>