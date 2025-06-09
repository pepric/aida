<!doctype html>
<html class="fixed">
	<?php
		$title = "Analyze Local Data";
		include("header.php"); 
	?>
		<script src="assets/vendor/jquery/jquery.js"></script> 
		<script src="assets/vendor/jquery-browser-mobile/jquery.browser.mobile.js"></script> 
		<script src="assets/javascripts/lsst/jquery-progressbar.min.js"></script>  
		<script src="assets/vendor/plupload/js/plupload.full.min.js"></script>


<script>
    // Upload Form
    $(function() {
        // Settings ////////////////////////////////////////////////
        var uploader = new plupload.Uploader({
            runtimes : 'html5,html4', // Set runtimes, here it will use HTML5, if not supported will use html4, etc.
            browse_button : 'pickfiles', // The id on the select files button
            multi_selection: false, // Allow to select one file each time
            container : 'uploader', // The id of the upload form container
            multipart_params :
            {
                'user' : document.getElementById("session-user").innerHTML
            },          
            //max_file_size : '100kb', // Maximum file size allowed
            url : 'upload_chunk.php', // The url to the upload.php file
    		chunk_size: '10mb',          
            //flash_swf_url : 'js/plupload.flash.swf', // The url to thye flash file
            //silverlight_xap_url : 'js/plupload.silverlight.xap', // The url to the silverlight file
            //filters : [ {title : "Table files", extensions : "csv,fits,txt"} ] // Filter the files that will be showed on the select files window
        });
 
        // Start Upload ////////////////////////////////////////////
        // When the button with the id "#uploadfiles" is clicked the upload will start
        $('#uploadfiles').click(function(e) {
            uploader.start();
            e.preventDefault();
        });
 
        uploader.init(); // Initializes the Uploader instance and adds internal event listeners.
 
        // Selected Files //////////////////////////////////////////
        // When the user select a file it wiil append one div with the class "addedFile" and a unique id to the "#filelist" div.
        // This appended div will contain the file name and a remove button
        uploader.bind('FilesAdded', function (up, files) {
            var fileCount = up.files.length,
                i = 0,
                ids = $.map(up.files, function (item) { return item.id; });

            for (i = 0; i < fileCount-1; i++) {
                uploader.removeFile(uploader.getFile(ids[i]));
            }

            $.each(files, function(i, file) {
              $('#file-preview').html(file.name)
            });
        });      
      

        // Error Alert /////////////////////////////////////////////
        // If an error occurs an alert window will popup with the error code and error message.
        // Ex: when a user adds a file with now allowed extension
        uploader.bind('Error', function(up, err) {
            reset = alert("Impossible to upload file: " + err.file.name +". Please retry.");
          	if(reset){}
			else{window.location.reload()}; 
            up.refresh(); // Reposition Flash/Silverlight
         
        });
 
        // Remove file button //////////////////////////////////////
        // On click remove the file from the queue
/*        $('a.removeFile').live('click', function(e) {
            uploader.removeFile(uploader.getFile(this.id));
            $('#'+this.id).remove();
            e.preventDefault();
        });*/
 
        // Progress bar ////////////////////////////////////////////
        // Add the progress bar when the upload starts
        // Append the tooltip with the current percentage
        uploader.bind('UploadProgress', function(up, file) {
            var progressBarValue = up.total.percent;
            $('#progressbar').fadeIn().progressbar({
                value: progressBarValue
            });
            // set colors for progressbar
            $("#progressbar").css({ 'background': 'url(assets/images/bg_progress_cccccc_1x100.png) #ffffff repeat-x 50% 50%', 'float': 'left', 'width': '30%', "margin-top": "5px"});
            $("#progressbar > div").css({ 'background': 'url(assets/images/bar_progressbar_0088cc_500x100.png) #cccccc repeat-x 50% 50%', 'border' : '1px solid #0088cc' });          
            $('#progressbar .ui-progressbar-value').html('<span class="progressTooltip">' + up.total.percent + '%</span>');
        });
 
        // Close window after upload ///////////////////////////////
        uploader.bind('UploadComplete', function(up, file) {
            
          		$('#upfile-preview').html(uploader.files[0].name)
				read_uploaded_file(uploader.files[0].name);           

				       
        });      
      
        // If checkbox is checked when the upload is complete it will close the window
/*        uploader.bind('UploadComplete', function() {
            if ($('.upload-form #checkbox').attr('checked')) {
                $('.upload-form').fadeOut('slow');
            }
        });
 
        // Close window ////////////////////////////////////////////
        // When the close button is clicked close the window
        $('.upload-form .close').on('click', function(e) {
            $('.upload-form').fadeOut('slow');
            e.preventDefault();
        });*/
 
    }); // end of the upload form configuration
</script>  
  
  
  
  
  
  
  
	<?php include("plotcontainer.php"); ?>  
	<div class="row">
		<div class="col-xs-12" id = "choice-div" >
			<section class="panel">
				<header class="panel-heading">
					<div class="panel-actions">
						<a href="#" class="fa fa-caret-down"></a>
						<a href="#" class="fa fa-times"></a>
					</div>
	
					<h2 class="panel-title">Select Data File</h2>
				</header>
				<div class="panel-body">
					<div class="form-group">
						<label class="radio-inline"><input type="radio" name="conf-orig" value="table" checked>Load Existing Temporary File</label>
						<label class="radio-inline"><input type="radio" name="conf-orig" value="upload" >Upload New File</label>
					</div>
				</div>
			</section>
		</div>              
              
		<div class="col-xs-12" id = "config-table">
			<section class="panel">
				<header class="panel-heading">
					<div class="panel-actions">
						<a href="#" class="fa fa-caret-down"></a>
						<a href="#" class="fa fa-times"></a>
					</div>
	
					<h2 class="panel-title">Load Existing Temporary File</h2>
				</header>              
				<div class="panel-body panel-rep">
                  	<form id="loadfile-form" class="form-horizontal form-bordered" method="" action="">
						<div class="form-group" id="filesel">
							<label class="col-md-2 control-label">File to Analyze</label>
							<div class="col-md-10">
                              	<div style="float:left;">
                                  <select id = "stored_file" class="form-control select_file" required>
                                    <option value="" disabled selected>Select...</option>
                                    <?php 
                                    $result = get_tmp_files($mysqli, $_SESSION['username'], $ftype="upload");

                                    if($result != "error"){render_select_files($result);}
                                    ?>					

                                  </select>
                              </div>
                                <div class="up-btn">
                                  <a class="btn btn-default" id="loadfile" href="#">Load</a>
                                </div>                              
                            </div>

						</div>
                  </form>
				</div>
			</section>
		</div>              
		<div class="col-xs-12" id = "config-upload" style="display:none">
			<section class="panel">
				<header class="panel-heading">
					<div class="panel-actions">
						<a href="#" class="fa fa-caret-down"></a>
						<a href="#" class="fa fa-times"></a>
					</div>
	
					<h2 class="panel-title" id="title-conf">Upload New File</h2>
				</header>              
              
				<div class="panel-body">
                  	<form id="upload-form" class="form-horizontal form-bordered" method="" action="">
                  		<div class="upload-form form-group" id="uploader">
							<label class="col-md-2 control-label">Select File to Upload</label>
							<div class="col-md-10">
                              	<div class="fileupload">

										<select id = "filefmt" class="form-control filefmt" required>
                                      		<option value="fits" selected>FITS</option>                                          
                                      		<option value="csv">CSV</option>
                                      		<!--<option value="ascii">TXT</option>-->
                                      	</select>                                      

                                    <!-- File List -->
                                    <div id="filelist" class="uneditable-input cb filelist">

                                                <i class="fa fa-file fileupload-exists"></i>
                                                <span id="file-preview" class="fileupload-preview"></span>
                                    </div>

                                    <!-- Select & Upload Button -->
                                    <div class="up-btn">
                                        <a class="btn btn-default" id="pickfiles" href="#">Browse</a>
                                        <a class="btn btn-default" id="uploadfiles" href="#">Upload</a>
                                    </div>
                                    <div id="hasheader" style="display:none; padding:5px; float: left; margin-right:10px">
                                  	 	<input type="checkbox" id="csvheader" name="csvheader" style="float: left; margin: 5px;" checked><span>Header(Y/N)</span>
                                    </div>                                  
                                    <!-- Progress Bar -->
                                    <div id="progressbar"></div>
                              	</div>
							</div>
						</div>
                      	<div class="form-group" id="okupload" style="display:none">
							<label class="col-md-2 control-label">Uploaded File</label>
							<div class="col-md-10" style="margin-top:10px">
                              	<span id="upfile-preview" style="margin-right:10px"></span><span class="label label-success">Success</span>
							</div>                          
                        </div>
						<div class="form-group" id="opselection" style="display:none">
							<label class="col-md-2 control-label">Analysis to perform</label>
							<div class="col-md-10">                          
								<select id = "op" class="form-control" required>
									<option value="" disabled selected>Select...</option>
    	                        	<option value="histogram">Histogram</option>                                  
	                            	<option value="scatter">Scatter plot</option>                                          
        	                    	<option value="stats">Statistics</option>
	                            	<option value="trend">Trend Analysis</option>                                  
            	                </select>  							
                            </div>
						</div>				
						<div class="form-group" id="hidden-fields">
							<input type="hidden" name="cols" id = "cols" value=""></input>
							<input type="hidden" name="n_ypar" id = "n_ypar" value=1></input>
							<input type="hidden" name="stats_enable" id = "stats_enable" value="global" disabled></input>
							<input type="hidden" name="stats_list" id = "stats_list" value=""></input>          
							<input type="hidden" name="plot_type" id = "plot_type" value="upload" disabled></input>
							<input type="hidden" name="fmt_field" id = "fmt_field" value="<?php if(isset($_GET['fmt'])){echo $_GET['fmt'];}else{echo "";} ?>" disabled></input>
  							<input type="hidden" name="file_field" id = "file_field" value="<?php if(isset($_GET['file'])){echo $_GET['file'];}else{echo "";} ?>" disabled></input>
          					<span id="plotdata" ></span>
						</div>
					</form>
      

						<form id="stats_form" class="form-horizontal form-bordered" method="" action="">
							<div class="form-group" id="stats" style="display:none;">
								<label class="col-md-2 control-label">Statistical Tools</label>
								<div class="stat-list col-md-6">
									<input type="checkbox" id="checkThemAll">Select/Deselect All</input>
									<?php populate_stats();?>
								</div>
							</div>
						</form> 
      
 						<div class="col-md-12" style="text-align:right">
							<button class="btn btn-primary" id="advanced_a" onclick="set_advanced_stats()" style="display:none">Advanced Statistics</button>
							<button class="btn btn-primary"  id="global_a" style="display:none" onclick="set_global_stats()">Default Statistics</button>                          
							<button type="submit" class="btn btn-primary" id = "submit_btn_upl_op" style="display:none">Submit</button>
							<button id="btn-reset" type="reset" class="btn btn-default" onclick="window.location.reload()">Reset</button>
						</div>     
				</div>
			</section>
		</div>
	</div>
	
	<?php include("loader.html"); ?>
</section>		
			

			


	<?php include("footer.php"); ?>
	<?php include("form_scripts.html"); ?>			
		<!-- Vendor-->

		<script src="assets/javascripts/lsst/moment.js"></script>
		<script src="assets/vendor/bootstrap/js/bootstrap.js"></script>
		<script src="assets/vendor/nanoscroller/nanoscroller.js"></script>
		<script src="assets/vendor/bootstrap-datetimepicker/js/bootstrap-datetimepicker.js"></script>
		<script src="assets/vendor/magnific-popup/magnific-popup.js"></script>
		<script src="assets/vendor/jquery-placeholder/jquery.placeholder.js"></script>

		<!-- Form validation -->
		<script src="assets/vendor/jquery-validation/jquery.validate.js"></script>

		<!-- File upload -->
		<script src="assets/vendor/bootstrap-fileupload/bootstrap-fileupload.min.js"></script>
		
		<!-- Specific Page Vendor -->
		<script src="assets/vendor/select2/select2.js"></script>
		<script src="assets/vendor/jquery-datatables/media/js/jquery.dataTables.js"></script>
		<script src="assets/vendor/jquery-datatables/extras/TableTools/js/dataTables.tableTools.min.js"></script>
		<!--<script src="assets/vendor/jquery-datatables-bs3/assets/js/datatables.js"></script>-->
		<script src="assets/vendor/DataTables/datatables.min.js"></script>
		
		<!-- Theme Base, Components and Settings -->
		<script src="assets/javascripts/theme.js"></script>
		
		<!-- Theme Custom -->
		<script src="assets/javascripts/theme.custom.js"></script>
		
		<!-- Theme Initialization Files -->
		<script src="assets/javascripts/theme.init.js"></script>


		<!-- Examples -->
		<script src="assets/javascripts/lsst/validation.js"></script>
		<script src="assets/javascripts/lsst/tab-init.js"></script>
		
		<script src="assets/javascripts/lsst/plots.js"></script>	
		<script src="assets/javascripts/lsst/plots_utils.js"></script>		
	
		<script src="assets/javascripts/lsst/jqscripts.js"></script>

		<script>

	$(document).ready(function(){
			$("input[type='radio'][name=conf-orig]").change(function(){
				if($(this).val()=="upload")
					{

						$("#config-upload").show();
						$("#config-table").hide();
						
					}
					else
					{
						$("#config-upload").hide();
						$("#config-table").show();
					}
			});
		});
          
	$('#filefmt').on('change', function (){
      	var fmt = document.getElementById("filefmt").value
    	if(fmt == "csv"){
        	$('#hasheader').css('display','inline-block');
        }
      	else{
        	$('#hasheader').css('display','none');
        }
    
    })          

	$('#op').on('change', function (){
      		var plot = document.getElementById('op').value
            var cols = document.getElementById('cols').value
			//remove previous generated fields
            if($("#params").length > 0){
             	$("#params").remove();
            }            
            if($("#bins").length > 0){
             	$("#bins").remove();
            }
            if($("#yparams").length > 0){
             	$("#yparams").remove();
            }      
			if(plot != "stats"){
                $('#advanced_a').show()
                document.getElementById('stats_enable').value = 'global'
              	$('#global_a').hide()
                $('#stats').hide()
            }
			$.ajax({
				   //Build form
				   method:"POST",
				   url: 'forms.php',
				   data:{
					   p : plot,
					   o : cols,
					   s : "upload"
				   },
				   success :	function(resultdata){
                  		$( resultdata ).insertBefore( "#hidden-fields" );
						if(plot != "stats"){
                          $('#advanced_a').show()
                          document.getElementById('stats_enable').value = 'global'
                        }
                     	else{
                          $('#advanced_a').hide()
             			  document.getElementById('stats_enable').value = 'advanced'
                          set_advanced_stats()
                        }
                    	if($("#bins").length > 0){
                           	$("#bins").show();
							set_bins()
                           }
                     	$("#n_ypar").val(1)
						$("#submit_btn_upl_op").show()

					}
              
			});
	});
		

$(document).ready(function() {
		//file upload
        $('#loadfile').on('click', function(event) {
          	var filetype = $("#stored_file").val()

            if(filetype == null){
				alert("Please, select a valid file")          
            } 
          	else{

	            var farr = filetype.split("_")
              
    	        {
        	    	var fmt = farr[0]
            		if(farr.length>0){
                		var hslug = farr[1]
                    	if(hslug=="noheader"){
                          var header=0
                          $('input[name="csvheader"]').prop("checked",false)
                          }
  	              }
    	          	else{
        	        	var header = 1
                         $('input[name="csvheader"]').prop("checked",true)
                        
     	           }
        	    }
                var e = document.getElementById('stored_file')
                var filename = e.options[e.selectedIndex].text
                $('#upfile-preview').html(filename)
                $("#filefmt").val(fmt)
                read_uploaded_file(filename, fmt, header, "local");

            //alert(filename)
            
            }
            
        })
})
          
$(document).ready(function() {
		//form validation
        $('#submit_btn_upl_op').on('click', function(event) {
            document.getElementById('stats_tab').setAttribute('onclick','onclick_stats()')
			var ny = document.getElementById("n_ypar").value
			var plot = document.getElementById("op").value
			if(plot == "histogram"){
				var bintype = $('input[name=bintype]:checked').val();
				if(bintype=="binnumber"){
					$('#binsize').rules("add", {digits : true, min :2})
				}
				else
				{
					$('#binsize').rules("remove");
				}
			}
		
			for(var i=0; i<ny; i++){
				// adding rules for elements


				$('#y'+i+'-params').each(function() {
					$(this).rules("add", 
						{
							required: true
						})
				}); 


			}
            // prevent default submit action         
            event.preventDefault();

            // test if form is valid 
            if($('#upload-form').validate().form()) {
              	var stats = $("#stats_enable").val();	
				var go = true
    
				if(stats=="advanced"){
					var stats_list = document.getElementById("stats_list").value;
					if(stats_list==""){
						go = confirm("No statistical operation selected! Proceed anyway?")							
					}
				}
              	if(go==true){
                  	//run analysis
					run_upload_py(event)
                }
            }

        })
		
		// initialize the validator
        $('#upload-form').validate({
			

			binsize : {
				required : true
			},
			
			
			
			highlight: function(element) {
				$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
			},
			success: function(element) {
				$(element).closest('.form-group').removeClass('has-error');
			},
			
			
		});

})

          
document.addEventListener("DOMContentLoaded", function(){
    var filename = document.getElementById('file_field').value
    var filetype = document.getElementById('fmt_field').value
    
	var exists = false
    if(filename!=""){
		if(filetype != ""){   
          $('#stored_file  option').each(function(){
            if (this.text == filename) {
              exists = true;
            }
          });
          if(exists){
            $("#stored_file").find("option[text='"+filename+"']").attr("selected", true);
           
            var farr = filetype.split("_")

            {
              var fmt = farr[0]
              if(farr.length>0){
                var hslug = farr[1]
                if(hslug=="noheader"){
                  var header=0
                   $('input[name="csvheader"]').prop("checked",false)
                  }
              }
              else{
                var header = 1
                 $('input[name="csvheader"]').prop("checked",true)
                }
            }
            $('#fmt_field').val(farr[0])
            $('#upfile-preview').html(filename)
            //console.log(fmt)
            read_uploaded_file(filename, fmt, header, "local")
            $('#btn-reset').css("display","none")            
          }
          else{
              alert("Error! Option not found")
          }
        }
      	else{
        	alert("Error! Missing file format")
        }
      }
    

});          
		
		</script>

</body>
</html>