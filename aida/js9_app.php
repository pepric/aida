<div class="row">
	<div>
		<section class="panel">
			<div class="js9-panel-body">
				<div class="col-md-8">
					<div class="JS9Menubar" data-usermenus="false" data-js9id="*" data-width="100%" ></div>
					<!--<div class="JS9Toolbar"></div>-->
					<div class="JS9" data-width="100%"></div>
					<div style="margin-top: 2px;">
						<div class="JS9Colorbar" data-js9id="*" data-width="100%"></div>
					</div>
				</div>
				<div class = "col-md-4" style="padding-left : 0">
					<div class = "col-md-6">
						<div class="JS9Magnifier" data-width="100%" data-height="230"></div> <!--data-width=100%???-->
					</div>
					<div class = "col-md-6">
						<div class="JS9Panner" data-width="100%" data-height="230"></div>
					</div>
					<div class = "col-md-6 imginfo">
						<div class="drag-handle" style="margin-top: 15px;">Info</div>                      
						<div class="JS9Info" data-width="100%"></div>
					</div>
                  	<div class="col-md-6 filetree">
						<div class="drag-handle" style="margin-top: 15px;">Navigation</div>
						<div class = "col-md-12 iottree">
							<div class="col-md-12" style="overflow-x:auto" id="treeImg"></div>                          
                        </div>
                    </div>
                  
					<div class = "col-md-12 newpanel" style="margin-top:20px;">
						<button class="btn btn-primary js9-btn" id="new-js9-panel" onclick="open_panel()">Open new panel</button>
                      	<button class="btn btn-primary js9-btn" id="flag_img" onclick="flag_image()">Flag image</button>

					</div>
                  	<?php
                  		if(isset($_GET['file'])){
							$val = '"'.$_GET['file'].'"';
						}
                  		else
                        {
                        	$val = 'None';
                        }
                  	?>
                  	<input type="hidden" id="img_file" value=<?php echo $val;?>>
                  	<?php
                  		if(isset($_GET['isflagged'])){
							$isf = $_GET['isflagged'];
						}
                  		else
                        {
                        	$isf = 0;
                        }
                  	?>
                  	<input type="hidden" id="isflagged" value=<?php echo $isf;?>>
                  	<input type="hidden" id="canvas_error" value=0>
				</div>
				<div class="col-md-8" style="padding-top: 15px;">		
					<div class="col-md-3 imexam" id="js9_3dPlot">
						<div class="ImExam3dPlot" data-js9id="*"></div>
					</div>
					<div class="col-md-3 imexam" id="js9_XProj">
						<div class="ImExamXProj" data-js9id="*" ></div>
					</div>
					<div class="col-md-3 imexam" id="js9_YProj">
						<div class="ImExamYProj" data-js9id="*" ></div>
					</div>
					<div class="col-md-3 imexam" id="js9_Histogram">
						<div class="ImExamHistogram" data-js9id="*" ></div>
					</div>
					<div class="col-md-3 imexam" id="js9_EncEnergy">
						<div class="ImExamEncEnergy" data-js9id="*" ></div>
					</div>
					<div class="col-md-3 imexam" id="js9_RadialProj">
						<div class="ImExamRadialProj" data-js9id="*" ></div>
					</div>
					<div class="col-md-6 imexam" id="js9_RegionStats">
						<div class="ImExamRegionStats" data-js9id="*"></div>
					</div>
				</div>
			
				<!-- list of stored files.-->
				<div class="col-md-4" id = "iottree">
					<div id="flag_notes">
					  <div class="drag-handle"  style="margin-top: 15px;">Flags Info</div>
					  <div class = "col-md-12 infoflag">
						<p id="flags_info_title" style="text-align:center; width:100%; margin: 10px 0 0px;"></p>
						<table class="table flagtable tab-imgflag table-bordered mb-none" style="margin-top: 10px; font-size : 12px" id="datatable-notes-public">
							<thead>
								<tr><th colspan="3">Public Flags</th></tr>
								<tr>
									<th scope="col" style="width:10%">Flag</th>
									<th scope="col" style="width:30%">User</th>
									<th scope="col" style="width:60%">Notes</th>                                      
								</tr>
							</thead>						
						</table>
						<table class="table flagtable tab-imgflag table-bordered mb-none" style="margin-top: 10px; font-size : 12px" id="datatable-notes-private">
							<thead>
								<tr><th colspan="3">Personal Flags</th></tr>
								<tr>
									<th scope="col" style="width:10%">Flag</th>
									<th scope="col" style="width:60%">Notes</th>                                      
								</tr>
							</thead>						
						</table>					
					  </div>
					</div>
				</div>
			</div>
		</section>
	</div>
  	<?php include("loader.html"); ?>
	<?php include("modalbox.php"); show_modal("img");?>	
	

</div>



      
<script> 
  function testcanvas(){
  	var divs = ["JS9", "js9_3dPlot", "js9_XProj", "js9_YProj", "js9_Histogram", "js9_EncEnergy", "js9_RadialProj", "js9_RegionStats"]
	for (let i = 0; i < divs.length; i++) {
      	if(i>0){
        var textdiv = "ImExam"+divs[i].split("_")[1]
      	document.getElementById(textdiv).innerHTML = '<p style="padding: 20px 0px 0px 20px; margin: 0px">No region selected<br></p>'
        }
		//exportAndSaveCanvas(divs[i])
	}  
  }

</script>  