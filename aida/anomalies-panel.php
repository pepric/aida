<div class="panel-body panel-dash">
	<div class="col-md-12 ">
		<header class="panel-heading">

			<h2 class="panel-title" style="float:left; margin-right:20px">Stored Experiments</h2>
            <div class="form-group">
				<label class="radio-inline"><input type="radio" name="flagtbl" value="exp" checked>By Experiment</label>
				<label class="radio-inline"><input type="radio" name="flagtbl" value="par" >By Parameter</label>
			</div>          	
		</header>
		<div class="col-md-12 dashpanel anomalies par" style="display : none">
			<section class="panel">
				<header class="panel-heading">
					<h2 class="panel-title">Public Archive</h2>
				</header>
				<div class="panel-body" id="anomalies">
					<table class="table tab-reports table-bordered table-striped mb-none" style="width:100%" id="datatable-anomalies">
						<thead>
							<tr >
                              	<th scope="col" style="vertical-align:middle">Flag</th>
								<th scope="col" style="vertical-align:middle">Parameter</th>
								<th scope="col" style="vertical-align:middle">System</th>
                              	
                              	<th scope="col" style="vertical-align:middle">Experiment</th>
								<th scope="col" style="vertical-align:middle">Exp Flag</th>                              	
                              	<th scope="col" style="vertical-align:middle">Experiment Start Date (UTC)</th>
                              	<th scope="col" style="vertical-align:middle">Experiment Stop Date (UTC)</th>
								<th scope="col" style="vertical-align:middle">Generation Date (UTC)</th>
								<th scope="col" style="vertical-align:middle">User</th>
								
								<th scope="col">Comments</th>
							  </tr>
						</thead>
                    </table>	
                  <div id="tbl_loading0" class="tbl-loading"><p>Loading...</p></div>					
                 
					<div class="col-md-3" style="margin-bottom : 5px; padding-left:0; padding-right:0"><h4 style="float: left;margin-right: 20px;">Filters</h4>
                    	<button type="reset" class="btn btn-primary" onClick="reset_filters('');">Reset</button>
                  	</div>
                      <div id="filters">
                   	<div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">
                  		<select id="status_select" onchange='filter_table("datatable-anomalies", this,0)'>
							<option value="">by Flag</option>
							<option value=0>Not Defined</option>
							<option value=1>Ok</option>
                          	<option value=2>Warning</option>
                            <option value=3>Serious</option>
						</select>
                    
                    	<select id="par_select" onchange='filter_table("datatable-anomalies", this, 1)'>
                  			<option value="">By Parameter</option>
                        </select>
                    
                    	<select id="sys_select" onchange='filter_table("datatable-anomalies", this, 2)'>
                  			<option value="">By System</option>
                        </select>
                    </div>
                    <div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">  
                        <select id="exp_select" onchange='filter_table("datatable-anomalies", this, 3)'>
                  			<option value="">by Experiment</option>
                        </select>      
                  		<select id="expstatus_select" onchange='filter_table("datatable-anomalies", this, 4)'>
							<option value="">by Exp Flag</option>
							<option value=0>Not Defined</option>
							<option value=1>Ok</option>
                          	<option value=2>Warning</option>
                            <option value=3>Serious</option>
						</select>                    
                    	<select id="user_select" onchange='filter_table("datatable-anomalies", this, 8)'>
                  			<option value="">By User</option>
                        </select>
                    </div>
                    <div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">                      
                    	<select id="datestart_select" onchange='filter_table("datatable-anomalies", this, 5)'>
                  			<option value="">By Start Date</option>
                        </select>                      
                    	<select id="dateend_select" onchange='filter_table("datatable-anomalies", this, 6)'>
                  			<option value="">By End Date</option>
                        </select>                         
                    	<select id="gen_select" onchange='filter_table("datatable-anomalies", this, 7)'>
                  			<option value="">By Experiment Date</option>
                        </select>                       
                    </div>
                  </div>
				</div>
			</section>
		</div>
		
      	<div class="col-md-12 dashpanel anomalies par" style="display : none" >
			<section class="panel">
				<header class="panel-heading">
					<h2 class="panel-title">Personal Archive</h2>
				</header>
				<div class="panel-body" id="anomalies">
					<table class="table tab-reports table-bordered table-striped mb-none" style="width:100%" id="datatable-anomalies1">
						<thead>
							<tr >
                              	<th scope="col" style="vertical-align:middle">Flag</th>
								<th scope="col" style="vertical-align:middle">Parameter</th>
								<th scope="col" style="vertical-align:middle">System</th>
                              	<th scope="col" style="vertical-align:middle">Experiment</th>
                              	<th scope="col" style="vertical-align:middle">Exp Flag</th>    
                              	<th scope="col" style="vertical-align:middle">Experiment Start Date (UTC)</th>
                              	<th scope="col" style="vertical-align:middle">Experiment Stop Date (UTC)</th>
								<th scope="col" style="vertical-align:middle">Generation Date (UTC)</th>
								<th scope="col" style="vertical-align:middle">Comments</th>

							  </tr>
						</thead>
                 		</table>
                  <div id="tbl_loading1" class="tbl-loading"><p>Loading...</p></div>					
					<div class="col-md-3" style="margin-bottom : 5px; padding-left:0; padding-right:0"><h4 style="float: left;margin-right: 20px;">Filters</h4>
                    <button type="reset" class="btn btn-primary" onClick="reset_filters(1);">Reset</button></div>
                      <div id="filters1">
                   	<div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">
                  		<select id="status_select1" onchange='filter_table("datatable-anomalies1", this,0)'>
							<option value="">by Flag</option>
							<option value=0>Not Defined</option>
							<option value=1>Ok</option>
                          	<option value=2>Warning</option>
                            <option value=3>Serious</option>
						</select>
                    
                    	<select id="par_select1" onchange='filter_table("datatable-anomalies1", this, 1)'>
                  			<option value="">By Parameter</option>
                        </select>
                    
                    	<select id="sys_select1" onchange='filter_table("datatable-anomalies1", this, 2)'>
                  			<option value="">By System</option>
                        </select>
                    </div>
                    <div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">  
                        <select id="exp_select1" onchange='filter_table("datatable-anomalies1", this, 3)'>
                  			<option value="">by Experiment</option>
                        </select>      
                  		<select id="expstatus_select1" onchange='filter_table("datatable-anomalies1", this, 4)'>
							<option value="">by Exp Flag</option>
							<option value=0>Not Defined</option>
							<option value=1>Ok</option>
                          	<option value=2>Warning</option>
                            <option value=3>Serious</option>
						</select>                    
                    </div>
                    <div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">                      
                    	<select id="datestart_select1" onchange='filter_table("datatable-anomalies1", this, 5)'>
                  			<option value="">By Start Date</option>
                        </select>                      
                    	<select id="dateend_select1" onchange='filter_table("datatable-anomalies1", this, 6)'>
                  			<option value="">By End Date</option>
                        </select>                         
                    	<select id="gen_select1" onchange='filter_table("datatable-anomalies1", this, 7)'>
                  			<option value="">By Experiment Date</option>
                        </select> 
                        </div>
				</div>
			</section>
		</div>
      
		<div class="col-md-12 dashpanel anomalies exp">
			<section class="panel">
				<header class="panel-heading">
					<h2 class="panel-title">Public Archive</h2>
				</header>
				<div class="panel-body" id="anomalies">
					<table class="table tab-reports table-bordered table-striped mb-none" style="width:100%" id="datatable-anomalies2">
						<thead>
							<tr >
                              	<th scope="col">Flag</th>
								<th scope="col">Experiment</th>
                              	<th scope="col">Exp Type</th>
                              	<th scope="col">Experiment Start Date (UTC)</th>
                              	<th scope="col">Experiment Stop Date (UTC)</th>
								<th scope="col">Generation Date (UTC)</th>
								<th scope="col">User</th>
								<th scope="col">Comments</th>
								<th scope="col" style="vertical-align:middle"></th>
							  </tr>
						</thead>
					</table>
					<div id="tbl_loading2" class="tbl-loading"><p>Loading...</p></div>					                  
                                   
					<div class="col-md-3" style="margin-bottom : 5px; padding-left:0; padding-right:0"><h4 style="float: left;margin-right: 20px;">Filters</h4>
                    <button type="reset" class="btn btn-primary" onClick="reset_filters(2);">Reset</button></div>
                  	<div id="filters2">
                   	<div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">
                  		<select id="status_select2" onchange='filter_table("datatable-anomalies2", this,0)'>
							<option value="">by Flag</option>
							<option value=0>Not Defined</option>
							<option value=1>Ok</option>
                          	<option value=2>Warning</option>
                            <option value=3>Serious</option>
						</select>
                        <select id="exp_select2" onchange='filter_table("datatable-anomalies2", this, 1)'>
                  			<option value="">by Experiment</option>
                        </select>
                        <select id="exptype_select2" onchange='filter_table("datatable-anomalies2", this, 2)'>
                  			<option value="">by Exp Type</option>
                        </select>                      
                   
                    </div>
                    <div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">                      
                    	<select id="datestart_select2" onchange='filter_table("datatable-anomalies2", this, 3)'>
                  			<option value="">By Start Date</option>
                        </select>                      
                    	<select id="dateend_select2" onchange='filter_table("datatable-anomalies2", this, 4)'>
                  			<option value="">By End Date</option>
                        </select>                         
                    	<select id="gen_select2" onchange='filter_table("datatable-anomalies2", this, 5)'>
                  			<option value="">By Experiment Date</option>
                        </select>                           
                        <select id="user_select2" onchange='filter_table("datatable-anomalies2", this, 6)'>
                  			<option value="">By User</option>
                        </select>                          
                      </div>
				</div>
				</div>
			</section>
		</div>
		
      	<div class="col-md-12 dashpanel anomalies exp">
			<section class="panel">
				<header class="panel-heading">
					<h2 class="panel-title">Personal Archive</h2>
				</header>
				<div class="panel-body" id="anomalies">
					<table class="table tab-reports table-bordered table-striped mb-none" style="width:100%" id="datatable-anomalies3">
						<thead>
							<tr >
                              	<th scope="col">Flag</th>
								<th scope="col">Experiment</th>
								<th scope="col">Exp Type</th>                              
                              	<th scope="col">Experiment Start Date (UTC)</th>
                              	<th scope="col">Experiment Stop Date (UTC)</th>
								<th scope="col">Generation Date (UTC)</th>
								<th scope="col">Comments</th>
								<th scope="col" style="vertical-align:middle"></th>
							  </tr>
						</thead>
					</table>
                  	<div id="tbl_loading3" class="tbl-loading"><p>Loading...</p></div>					
                  	<div class="col-md-3" style="margin-bottom : 5px; padding-left:0; padding-right:0"><h4 style="float: left;margin-right: 20px;">Filters</h4>
                    <button type="reset" class="btn btn-primary" onClick="reset_filters(3);">Reset</button></div>
                  	<div id="filters3">
                   	<div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">
                  		<select id="status_select3" onchange='filter_table("datatable-anomalies3", this,0)'>
							<option value="">by Flag</option>
							<option value=0>Not Defined</option>
							<option value=1>Ok</option>
                          	<option value=2>Warning</option>
                            <option value=3>Serious</option>
						</select>
                        <select id="exp_select3" onchange='filter_table("datatable-anomalies3", this, 1)'>
                  			<option value="">by Experiment</option>
                        </select>
                        <select id="exptype_select3" onchange='filter_table("datatable-anomalies3", this, 2)'>
                  			<option value="">by Exp Type</option>
                        </select>                        
                   
                    </div>
                    <div class="col-md-12" style="margin-bottom : 5px; padding-left:0; padding-right:0">                      
                    	<select id="datestart_select3" onchange='filter_table("datatable-anomalies3", this, 3)'>
                  			<option value="">By Start Date</option>
                        </select>                      
                    	<select id="dateend_select3" onchange='filter_table("datatable-anomalies3", this, 4)'>
                  			<option value="">By End Date</option>
                        </select>                         
                    	<select id="gen_select3" onchange='filter_table("datatable-anomalies3", this, 5)'>
                  			<option value="">By Experiment Date</option>
                        </select>                           
                     
                      </div>
				</div>
				</div>
			</section>
		</div>            
	</div>
</div>