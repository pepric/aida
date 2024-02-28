<div class="row" id = "imgdata_container" style="display:none;">
	<div class="col-xs-12">
		<div class="tab-content" style="min-height: 400px; height: auto;">
			<div id="imgfiles_tab" >
                <div class="col-md-12">
                    <section class="panel">		
						<header class="panel-heading">
						  <div class="panel-actions">
							<a href="#" class="fa fa-caret-down"></a>
							<a href="#" class="fa fa-times"></a>
						  </div>
						  <h2 class="panel-title">Images list</h2>
						</header>			
						<div class="panel-body col-md-12 dashpanel">
						  <table class="table tab-reports table-bordered table-striped mb-none" id="img_filelist"></table>          
                        </div>
                    </section>
                </div>
				<div class="col-md-12" style="text-align:right">
					<select id="img_op" class="form-control img-op" required>
					   <option value="" disabled selected>Select Operation</option>
					   <option value="difference">Difference Stats</option>
					</select>						
					<button class="btn btn-primary" id = "img_stats_submit" >Submit</button>
				</div>
			</div>
			<input type="hidden" name="img_files_container" id = "img_files_container" value=""></input>
			<input type="hidden" name="diff_A" id = "diff_A" value=""></input>
			<input type="hidden" name="diff_B" id = "diff_B" value=""></input>
			<input type="hidden" name="source_exp" id = "source_exp" value=""></input>
			<div style="clear:both"></div>
		</div>
	</div>
</div>