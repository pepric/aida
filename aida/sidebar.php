<!-- start: sidebar -->
				<aside id="sidebar-left" class="sidebar-left">
				
					<div class="sidebar-header">
						<div class="sidebar-toggle hidden-xs" data-toggle-class="sidebar-left-collapsed" data-target="html" data-fire-event="sidebar-left-toggle">
							<i class="fa fa-bars" aria-label="Toggle sidebar"></i>
						</div>
					</div>
				
					<div class="nano">
						<div class="nano-content">
							<div class="sidebar-title">General Info</div>
						
							<nav id="menu" class="nav-main" role="navigation">
								<ul class="nav nav-main">
                                  
									<li class="nav-parent">
										<a>
											<i class="fa fa-info-circle" aria-hidden="true"></i>
											<span>Systems Info</span>
										</a>
                                      	<ul class="nav nav-children">
                                          <li>
                                              <a href="system-info.php?subj=hktm" target="_blank">
                                                  <span>HKTM Parameters</span>
                                              </a>
                                          </li>
										</ul>
									</li>                                  
									<li class="nav-parent">
										<a>
											<i class="fa fa-info-circle" aria-hidden="true"></i>
											<span>Analysis Info</span>
										</a>
                                      	<ul class="nav nav-children">
                                          <li>
                                              <a href="analysis-info.php?subj=plots" target="_blank">
                                                  <span>Available Plots</span>
                                              </a>
                                          </li>
                                          <li>
                                              <a href="analysis-info.php?subj=statistics" target="_blank">
                                                  <span>Available Statistics</span>
                                              </a>
                                          </li>
										</ul>
									</li>                                   
								</ul>
							</nav>
                          
                          
                          
                          
							<hr class="separator" />
							<div class="sidebar-title">Local Data</div>
						
							<nav id="menu" class="nav-main" role="navigation">
								<ul class="nav nav-main">
									<li>
										<a href="analyze-local.php" target="_blank">
											<i class="fa fa-search" aria-hidden="true"></i>
											<span>Analyze Local Data</span>
										</a>
									</li>
									<li>
										<a href="list-local.php" target="_blank">
											<i class="fa fa-eye" aria-hidden="true"></i>
											<span>View Local Data</span>
										</a>
									</li>
								</ul>
							</nav>

							<hr class="separator" />
							<div class="sidebar-title">HKTM</div>
						
							<nav id="menu" class="nav-main" role="navigation">
								<ul class="nav nav-main">
									<li class="nav-parent">
										<a>
											<i class="fa fa-line-chart" aria-hidden="true"></i>
											<span>New Plot</span>
										</a>
                                      	<ul class="nav nav-children">
                                      	<?php  
                                      		$plot = get_plots_list();
                                      		while ($row = mysqli_fetch_array($plot))
                                            {
												$ptitle = $row['plot_title'];
                                                $pname = $row['plot_name'];
                                              	echo '<li><a href="generate-plot.php?plot='.strtolower($pname).'&s=hktm" target="_blank">'.$ptitle.'</a></li>';
                                            }	
                                     	?>
										</ul>
									</li>
									<li>
										<a href="statistics.php?s=hktm" target="_blank">
											<i class="fa fa-calculator" aria-hidden="true"></i>
											<span>Statistics</span>
										</a>
									</li>
								<!--	<li class="nav-parent">
										<a>
											<i class="fa fa-cogs" aria-hidden="true"></i>
											<span>Machine Learning</span>
										</a>
										<ul class="nav nav-children">
											<li>
												<a href="ml_train.php?s=hktm" target="_blank">
													 Train
												</a>
											</li>
											<li>
												<a href="under_construction.php" target="_blank">
													 Apply
												</a>
											</li>
										</ul>
									</li>	-->								
								</ul>
							</nav>
							
							<hr class="separator" />
					
							<div class="sidebar-title">Images</div>
							
							<nav id="menu" class="nav-main" role="navigation">
								<ul class="nav nav-main">
									<li>
										<a href="image-explorer.php" target="_blank">
											<i class="fa fa-eye" aria-hidden="true"></i>
											<span>Image Explorer</span>
										</a>
									</li>
								<!--	<li>
										<a href="image-analysis.php" target="_blank">
											<i class="fa fa-calculator" aria-hidden="true"></i>
											<span>Image Analysis</span>
										</a>
									</li>	-->								
								</ul>
							</nav>

							<hr class="separator" />
							<div class="sidebar-title">Reports</div>
							
							<nav id="menu" class="nav-main" role="navigation">
								<ul class="nav nav-main">
									<li>
										<a href="new-configuration.php" target="_blank">
											<i class="fa fa-edit" aria-hidden="true"></i>
											<span>New Configuration</span>
										</a>
									</li>									
									<li>
										<a href="generate-report.php" target="_blank">
											<i class="fa fa-calendar" aria-hidden="true"></i>
											<span>Generate Report</span>
										</a>
									</li>									
									<li>
										<a href="list-reports.php" target="_blank">
											<i class="fa fa-list-ul" aria-hidden="true"></i>
											<span>List Reports</span>
										</a>
									</li>
									<li>
										<a href="list-config.php" target="_blank">
											<i class="fa fa-list-ul" aria-hidden="true"></i>
											<span>Configuration Files</span>
										</a>
									</li>
								</ul>
							</nav>
                          <div class="version"><p>v0.4</p></div>
					</div>
				                      	
				</aside>
				<!-- end: sidebar -->
				