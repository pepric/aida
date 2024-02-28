<div class="row" id = "plot_container" style="display:none;">
	<div class="col-xs-12">
		<div class="tabs tabs-primary">
			<ul class="nav nav-tabs <!--nav-justified-->"> 
				<li id="tab1" style="display : none";>
					<a href="#plot_tab" data-toggle="tab" class="text-center" onclick="onclick_plot()"></a>
				</li>
				<li id="tab-stats1">
					<a id="stats_tab" href="#plot_stats" data-toggle="tab" class="text-center" onclick="onclick_stats()" ></a>
				</li>
				<li id="tab-files1">
					<a href="#plot_files" data-toggle="tab" class="text-center" onclick="onclick_files()" >Files</a>
				</li>
			</ul>
			<div class="tab-content" style="min-height: 400px; height: auto;">
				<div id="plot_tab" class="tab-pane">
                  	<div id="plot_image" class="col-xs-12">
						<div id="chartContainer" style="display:none;"></div>
						<!--<div id = "plot"></div>-->
                  		<div id="linkContainer" style="display:none;"></div>
                  	</div>
				<?php include("custom_plot.php");?>
				</div>

				<div id="plot_stats" class="tab-pane"></div>
				<div id="plot_files" class="tab-pane"></div>              
				<div style="clear:both"></div>
				<div id = "stats_results" style="display:none"></div>
			</div>
		</div>
	</div>
</div>