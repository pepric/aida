/**
 * Application Dashboard Controller and DataTables Manager.
 *
 * Handles dashboard tab initialization, periodic DataTables auto-reloading (running processes,
 * flagged reports, ML experiments, pending/active/deactivated users), flagged anomaly filtering,
 * file uploader initialization (Plupload), and administrative system/SMTP settings AJAX handlers.
 *
 * @package    AIDA
 * @subpackage JS\Dashboard
 * @author     Giuseppe Riccio
 * @version    1.1.0
 */

/**
 * DOM Load Initialization:
 * Loads navigation file trees (user, stored, reports, configs),
 * retrieves active history logs, and prevents form submission on Enter key in password fields.
 */
$(document).ready(function(){
	var name = document.getElementById("session-user").innerHTML;
	get_tree(name, "#treeUser", [], 1)
	get_tree("stored", "#treeStored", [], 1)
	get_tree("report", "#treeReports", ["xml","pdf"], 1)
	get_tree("config", "#treeConfig", ["json", "ini"], 1)
	get_history(name, "treeUserHist");
	get_history("global", "treeGlobalHist");
	
	$("#pwdin").keypress(function(event) { 
		if (event.keyCode === 13) { 
			return false
		} 
	});	
});	

/**
 * Periodic Refresh Timer:
 * Polls to refresh user and global history logs every 3 minutes.
 */
setInterval(function(){
	refresh_history();
}, 180000);

/**
 * Opens a page in a new browser tab with the current operating mode appended as a query parameter.
 *
 * @param {string} page Target URL path.
 */
function open_tab(page){
	var opmode = document.getElementById("opmode").innerHTML.toLowerCase()
	window.open(page+'?opmode='+opmode,'_blank');
	
	
}

/**
 * Formats flag image elements into text strings for CSV export.
 *
 * @param {string} data HTML content string containing flag image.
 * @param {string} type Render type context (e.g., 'exportcsv').
 * @returns {string} Plain text flag status.
 */
function render_flag(data, type){
	if (type === "exportcsv") {
		data = data.replace('<img src="assets/images/nd.png"><span style="display:none">0</span>', "Not Defined");
		data = data.replace('<img src="assets/images/ok.png"><span style="display:none">1</span>', "Ok");
		data = data.replace('<img src="assets/images/warning.png"><span style="display:none">2</span>', "Warning");
		data = data.replace('<img src="assets/images/serious.png"><span style="display:none">3</span>', "Serious");
		return data;
	}
	return data;        
}

/**
 * Prompts the user for logout confirmation and redirects to logout.php.
 */
function logout(){
	var r = confirm("You are logging out. Are you sure?");
	if (r == true) {
	  location.href='logout.php';
	}
}

/**
 * Running Reports DataTables:
 * Configures displayed columns based on user role (Admin vs. User),
 * initializes the table, and triggers automatic AJAX polling every 5 seconds.
 */
$( document ).ready(function() {
	var role = document.getElementById("session-role").innerHTML
	var user = document.getElementById("session-user").innerHTML

	if(role == "admin"){
		var cols = [
			{ mData: 'ID' } ,
			{ mData: 'User' } ,
			{ mData: 'Period' },
			{ mData: 'Config File' },
			{ mData: 'Current Report Start Date' },
			{ mData: 'Progress' },
			{ mData: 'Pid' },
		]
		var notorder = 6
	}
	else
	{
		var cols = [
			{ mData: 'ID' } ,
			{ mData: 'Period' },
			{ mData: 'Config File' },
			{ mData: 'Current Report Start Date' },
			{ mData: 'Progress' },
			{ mData: 'Pid' },
		]
		var notorder = 5
	}

	var table = $('#datatable-running').DataTable( {
		"ajax": {
			"type": "POST",
          	"url": "scripts/cs_interface.py",
			"data": {
				"username": user,
				"role" : role,
				"action" : "running_reports"
			}
		},
      	autoWidth : false,
		"language": {"emptyTable": "No Running Processes"},
		"order": [[ 0, 'desc' ]],
		"bPaginate":true,
		"bProcessing": false,
		"pageLength": 10,
		"columns": cols,
      	"columnDefs" :[ {orderable:false, targets : [notorder]}]
	});
	setInterval( function () {
	table.ajax.reload(null, false);
	}, 5000 );
});
  
/**
 * Flagged Reports DataTables:
 * Initializes the table for flagged reports/anomalies and schedules a refresh every 10 minutes.
 */ 
$( document ).ready(function() {
		var cols = [
			{ mData: 'Flag' } ,
			{ mData: 'Report' },
			{ mData: 'Period' },
			{ mData: 'Start Date (UTC)' },
			{ mData: 'End Date (UTC)' },
			{ mData: 'Actions' },
		]  
 
	var freptable = $('#datatable-flag_reports').DataTable( {
		"ajax": {
			"type": "POST",
          	"url": "scripts/cs_interface.py",
			"data": {
				"action" : "flagged_reports",
			}
		},
      	autoWidth : false,
		"language": {"emptyTable": "No Flagged Reports"},
      	"columns": cols,
      	"columnDefs" :[ {orderable:false, targets : [5]}]
	});
	setInterval( function () {
	freptable.ajax.reload(null, false);
	}, 600000);
}); 


/**
 * Machine Learning Experiments DataTables:
 * Initializes the table for saved ML models in the database, refreshing every 10 minutes.
 */
$( document ).ready(function() {
		var cols = [
			{ mData: 'ID' } ,
			{ mData: 'ML Technique' },
			{ mData: 'Model' },
			{ mData: 'Data Source' },
			{ mData: 'Dates Interval' },
			{ mData: 'User' },
			{ mData: 'Generation Date' },
			{ mData: 'Actions' },
		]  
 
	var freptable = $('#datatable-ml_stored').DataTable( {
		"ajax": {
			"type": "POST",
          	"url": "scripts/cs_interface.py",
			"data": {
				"action" : "mlstored",
			}
		},
      	autoWidth : false,
		"language": {"emptyTable": "No Machine Learning experiments stored into DB"},
      	"columns": cols,
      	"columnDefs" :[ {orderable:false, targets : [7]}]
	});
	setInterval( function () {
	freptable.ajax.reload(null, false);
	}, 600000);
}); 


/**
 * Administrative User Management DataTables (Pending, Active, Deactivated):
 * Three blocks populating their respective DataTables and scheduling hourly updates (3600000 ms).
 */
$( document ).ready(function() {
		var cols = [
			{ mData: 'Username' } ,
			{ mData: 'E-Mail' },
			{ mData: 'Role' },
			{ mData: 'Request Date' },
			{ mData: 'Actions' },
		]  
 
	var pendingtable = $('#datatable-pending').DataTable( {
		"ajax": {
			"type": "POST",
          	"url": "scripts/cs_interface.py",
			"data": {
				"action" : "users_tables",
				"status" : 0
			}
		},
      	autoWidth : false,
		"language": {"emptyTable": "No Pending Requests"},
      	"columns": cols,
      	"columnDefs" :[ {orderable:false, targets : [4]}]
	});
	setInterval( function () {
	pendingtable.ajax.reload(null, false);
	}, 3600000);
});
  
 //refresh active users table 
$( document ).ready(function() {
		var cols = [
			{ mData: 'Username' } ,
			{ mData: 'E-Mail' },
			{ mData: 'Role' },
			{ mData: 'Activation Date' },
			{ mData: 'Last Login' },
			{ mData: 'Last Logout' },
			{ mData: 'Actions' },
		]  
 
	var activetable = $('#datatable-active').DataTable( {
		"ajax": {
			"type": "POST",
          	"url": "scripts/cs_interface.py",
			"data": {
				"action" : "users_tables",
				"status" : 1
			}
		},
      	autoWidth : false,
      	"columns": cols,
      	"columnDefs" :[ {orderable:false, targets : [6]}]
	});
	setInterval( function () {
	activetable.ajax.reload(null, false);
	}, 3600000);
});

 //refresh deactivated users table 
$( document ).ready(function() {
		var cols = [
			{ mData: 'Username' } ,
			{ mData: 'E-Mail' },
			{ mData: 'Role' },
			{ mData: 'Deactivation Date' },
			{ mData: 'Actions' },
		]  
 
	var activetable = $('#datatable-removed').DataTable( {
		"ajax": {
			"type": "POST",
          	"url": "scripts/cs_interface.py",
			"data": {
				"action" : "users_tables",
				"status" : 2
			}
		},
      	autoWidth : false,
		"language": {"emptyTable": "No Deactivated Users"},
      	"columns": cols,
      	"columnDefs" :[ {orderable:false, targets : [4]}]
	});
	setInterval( function () {
	activetable.ajax.reload(null, false);
	}, 3600000);
});

/**
 * Page-Level Periodic Refresh Timers:
 * Regenerates file trees, flag tables, and history logs every 10 minutes.
 */
$( document ).ready(function() {
	  //refresh config files and reports trees
  	  update_tree('config', '#treeConfig', ['json', 'ini'], 1)
  	  setInterval(update_tree, 600000, 'config', '#treeConfig', ['json', 'ini'], 1);
  	  setInterval(update_tree, 600000, 'report', '#treeReports', ['pdf','xml'], 1);
	  // refresh flagged tables
  	  build_flagged_tables()
  	  setInterval(build_flagged_tables, 600000);
	  // refresh history
	  setInterval(refresh_history, 600000);
  
});

/**
 * Fetches flagged anomaly data via AJAX and initializes or refreshes DataTables.
 */
function build_flagged_tables(){

  	  var tbl = ['datatable-anomalies','datatable-anomalies1','datatable-anomalies2','datatable-anomalies3']
      $.ajax({
          'url': "scripts/cs_interface.py",
          'method': "POST",
			"data": {
				"action" : "flagged_tables",
				"tbl" : tbl,
				"user" : document.getElementById("session-user").innerHTML
			}
      }).done( function(results) {
			for(var i=0;i<tbl.length;i++){
              	if($.fn.DataTable.isDataTable('#'+tbl[i])){
					$('#'+tbl[i]).DataTable().destroy();                
                }
            	var cols = init_flagged(tbl[i], results[tbl[i]])
				build_flagged_filters(cols, tbl[i], results[tbl[i]])
            	$('#tbl_loading'+i).hide()
            }
      }) 
}

/**
 * Initializes a DataTable instance for a flagged anomaly table.
 *
 * @param {string} divid Container table ID.
 * @param {Array}  data  Dataset array to populate.
 * @returns {Array} Columns configuration array.
 */
function init_flagged(divid, data){
	var filenames={
      	"datatable-anomalies" : "flagged_parameters_public",
    	"datatable-anomalies1" : "flagged_parameters_private",
      	"datatable-anomalies2" : "flagged_experiments_public",
      	"datatable-anomalies3" : "flagged_experiments_private"
    }
  	var cols = []
	var tbl = document.getElementById(divid)
	var namerow = tbl.rows[0]
    var targets = []
    var notorder = []
    for (var j = 0, col; col = namerow.cells[j]; j++) {
    	colname = col.innerHTML
		if(colname!=""){
        	
          	if(colname.includes("Flag")){
            	targets.push(j)
            }
          	if(colname=="Comments"){
            	notorder.push(j)
				cols.push({mData : colname, className : "td-left"})
            }
			else{
				cols.push({mData : colname})
			}
        }
		else
		{
			cols.push({mData : "Actions"})
			notorder.push(j)
		}
    }

	var t_flag = $('#'+divid).DataTable( {

			"aaData": data,
			"dom" : "row <'col-sm-2'l><'col-sm-4'B><'col-sm-6'f>"+"rtip",
          	"language": {"emptyTable": "No Flagged Experiments", "buttons":{"colvis" : "Filter columns", "csv" : "Export"}},
			"order": [[ 0, 'desc' ]],
			"bPaginate":true,
			"bProcessing": false,
			"pageLength": 10,
          	"buttons" : [
						{ extend: 'colvis', className:"btn btn-primary", postfixButtons: [ 'colvisRestore' ]},  					
              			{ extend: 'csv', className: 'btn btn-primary', title: filenames[divid], fieldBoundary: '', exportOptions: { orthogonal: "exportcsv", columns: ':visible'} },
            ],
            "columns": cols,
          	"columnDefs" :[ {targets : targets, render:render_flag},{orderable:false, targets : notorder}]
	});
	
	return cols
}

/**
 * Populates dropdown filter controls based on flagged DataTable column values.
 *
 * @param {Array}  cols Column definitions array.
 * @param {string} tbl  Table ID.
 * @param {Array}  data Source data array.
 */
function build_flagged_filters(cols, tbl, data){

	const select_map = {
		"Parameter" : "par_select",
		"System" : "sys_select",
		"Experiment" : "exp_select",
		"User" : "user_select",
		"Experiment Start Date (UTC)" : "datestart_select",
		"Experiment Stop Date (UTC)" : "dateend_select",
		"Generation Date (UTC)" : "gen_select",
		"Exp Type" : "exptype_select"
	}
	var dtbl_id = tbl.replace("datatable-anomalies","")

	for(var i=0; i<cols.length; i++){
		var c = cols[i]['mData']
		var list = []
		for(var j=0;j<data.length;j++){
			var curr_data = data[j]
			if(!c.includes("Flag") && c!="Comments"){
				var curr_val = curr_data[c]
				if(!list.includes(curr_val)){
					list.push(curr_val)
				}
			}
		}
		list.sort()
		curr_div = select_map[c]
		if(curr_div!=null){
			select = document.getElementById(curr_div+dtbl_id)
			for(let el in list){
				var opt = document.createElement('option');
				if(list[el].startsWith("<a")){
					var text = list[el].split(">")[1].slice(0,-4)
					opt.value = text;
					opt.innerHTML = text;
				}
				else{
				  opt.value = list[el];
					opt.innerHTML = list[el];
				}
				select.appendChild(opt);    
			}			
		}
	}
}


$(document).ready(function() { 
	$('#admin_remrepo_set').click(function() { 
		reset_repo_modal()
	});

});

/**
 * Resets repository modal selection dropdowns and hides input fields.
 */
function reset_repo_modal(){
	$('#form_settings').hide()
	$('#form_opmode').hide()
	$('#repo_opmode').val("")
	$('#form_origin').hide()
	$('#repo_origin').val("")
	$('#repo_source').val("")
	
}

$(document).ready(function() { 
	$('input[type="radio"]').click(function() { 
		var inputValue = $(this).attr("value"); 
		var targetBox = $("." + inputValue); 
		$(".anomalies").not(targetBox).hide(); 
		$(targetBox).show(); 
	}); 
}); 

/**
 * Applies a column search filter on a DataTable instance.
 *
 * @param {string}          tbl Table ID.
 * @param {HTMLSelectElement} sel Select element triggering the filter.
 * @param {number}          col Target column index.
 */ 
function filter_table(tbl, sel, col){
	var table = $('#'+tbl).DataTable()
	table.columns(col).search( sel.value ).draw();
}  

/**
 * Resets all select filters for a specific anomaly table.
 *
 * @param {string|number} id Anomaly table ID suffix.
 */
function reset_filters(id){
	var n = 0;
    $("#filters"+id).find("select").each(function () { // there is no such thing as input[type=select] 
        this.value = ""; // this is a <select>
		filter_table('datatable-anomalies'+id, this, n);
     	n = n+1;
    });
}
 
/**
 * Upload Form (Plupload Engine):
 * Initializes the chunked uploader for backup archives (10MB chunks),
 * handles extension validation, progress bar rendering, and completion callbacks.
 */
$(function() {
	// Settings ////////////////////////////////////////////////
	var uploader = new plupload.Uploader({
		runtimes : 'html5,html4', // Set runtimes, here it will use HTML5, if not supported will use html4, etc.
		browse_button : 'pickfiles', // The id on the select files button
		multi_selection: false, // Allow to select one file each time
		container : 'uploader', // The id of the upload form container
		multipart_params :
		{
			'user' : document.getElementById("session-user").innerHTML,
			'path' : 'tmp'
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
		if(window.location.href.split("/").slice(-1)=="dashboard.php"){
			
			upload_backup(uploader.files[0].name);
		}
		else{
			read_uploaded_file(uploader.files[0].name);
		}					
	});      
}); // end of the upload form configuration 

/**
 * Handles UI toggle events for system state switches.
 */
function switch_systems(){

      var isChecked = $(this).is(':checked');
      var selectedData;
      var $switchLabel = $('.switch-label');

      if(isChecked) {
        selectedData = $switchLabel.attr('data-on');
      } else {
        selectedData = $switchLabel.attr('data-off');
      }
}

/**
 * AJAX Handler - Save Monitored Systems Settings:
 * Collects active toggle switch states and sends the update request to the backend.
 */
$(document).ready(function() {

	$('#update_sys').on("click", function(){
		$("#loader").show();	
		//var params = $("#tbl_sys").serialize();
		var params = $("#tbl_sys :input")
		var sysdata = {}
		for(var i=0; i<params.length; i++){
			var el = params[i]
			var name = el.name.split("_")[1]
			var check =  el.checked
			sysdata[name] = check
		}

 	  $.ajax({
		method:"POST",
		url:"functions.php",
		data:{
		  action : "update_systems",
		  data : sysdata,
		  user : document.getElementById("session-user").innerHTML
		},
 		success:function(data){
			data = JSON.parse(data)
			var msg
			switch(data['result']){
			  case true:
			  {
				msg="Enabled systems updated successfully."
				break;
			  }
			  case false:
			  {
				msg="ERROR! Impossible to update systems enabled. Please retry later or contact AIDA admin."
				break;			
			  }
			  case "None":
			  {
				msg="INFO: Systems unchanged. Nothing to do."  
				break;			  
			  }
			  
			  
			}			
			box = alert(msg)
			if(box){} else {
				$("#loader").hide();
				location.reload()
			} 			
		}
	  });
	})
})

/**
 * AJAX Handler and Validation - Save General Web App Settings (General Settings Modal).
 */
$(document).ready(function() {
	$('#gen_set-btn').on('click', function(event) {
		$('#histnum').rules("add", {digits : true})
		$('#nprocs').rules("add", {digits : true})
	// prevent default submit action         
		event.preventDefault();
		// test if form is valid 
		if($('#update_genset').validate().form()) {
			$("#loader").show();
			$('#gen_set').modal('hide');
			var formdata = $('#update_genset').serialize()
			//ajax to store settings
			  $.ajax({
				method:"POST",
				url:"functions.php",
				data:{
				  action : "update_genset",
				  data : formdata,
				  user : document.getElementById("session-user").innerHTML
				},
				success:function(data){

					var res = JSON.parse(data)
					var jsonerr = res['jsonerr']
					console.log(jsonerr)
					var dberr = res['dberr']
					if(jsonerr == 2){
						alert("INFO: No change in web app settings. Nothing to do.")
					}
					else{
						if(jsonerr==0 && dberr==0){
							alert("Settings updated successfully!")
							location.reload()
						}
						else{
							var msg = "Error updating settings!\n"
							if(jsonerr){
								msg += " - Impossible to save configuration file\n"
							}
							if(dberr){
								msg += " - Impossible to store Time Window Thresholds in local db"
							}						
							alert(msg)
							location.reload()
						}
					}
				}
			  });
		}	
	});
	
	// initialize the validator
	$('#update_genset').validate({
	
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
});

/**
 * AJAX Handler and Validation - SMTP Configuration (SMTP Settings Modal).
 */
$(document).ready(function() {
	$('#smtp_set-btn').on('click', function(event) {
	// prevent default submit action         
		event.preventDefault();
		// test if form is valid 
		if($('#smtpconf').validate().form()) {
			$("#loader").show();

			$('#smtp_set').modal('hide');
 			var formdata = $('#smtpconf').serialize()
			//ajax to store settings
			  $.ajax({
				method:"POST",
				url:"functions.php",
				data:{
				  action : "smtpconf",
				  user : document.getElementById("session-user").innerHTML,
				  data : formdata,
				},
				success:function(data){
					var res = JSON.parse(data)
					var err = res['error']
					if(err==0){
						alert("Settings updated successfully!")
						location.reload()
					}
					else{
						var msg = "Error updating SMTP settings!\nImpossible to store SMTP configuration file"					
						alert(msg)
						location.reload()
					}
				}
			  });
		}	
	});
	
	// initialize the validator
	$('#smtpconf').validate({
	
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
		
		
	});
});

/**
 * AJAX Handler - Send Test SMTP Email.
 */
$(document).ready(function() {
	$('#smtp_test-btn').on('click', function(event) {
	// prevent default submit action         
		event.preventDefault();
		// test if form is valid 
		if($('#smtpconf').validate().form()) {
			$("#loader").show();
 			var formdata = $('#smtpconf').serialize()
			console.log(formdata)
			var user = document.getElementById("session-user").innerHTML
			console.log(user)
			//ajax to store settings
			  $.ajax({
				method:"POST",
				url:"functions.php",
				data:{
				  action : "testsmtp",
				  formset : formdata,
				  user : user
				},
				success:function(results){
					var res = JSON.parse(results)
					var err = res['error']
					if(err==0){
						alert("A test email has been sent to your address. If not receive it in few minutes, please check your settings or contact AIDA admin!")
					}
					else{
						//var msg = "Error sending test email!\nPlease, check your settings and retry."	
						var msg = err
						alert(msg)
					}
					$("#loader").hide();
				}
			  });
		}	
	});
	
	// initialize the validator
	$('#smtpconf').validate({
	
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
});

/**
 * Displays a PNotify notification pop-up containing report information.
 *
 * @param {string} repname   Report name.
 * @param {string} repstatus Report status ('ok', 'warning', 'serious', 'nd').
 */
function show_rep_info(repname, repstatus){
	const status_map = {"ok" : "success", "warning" : "warning", "serious" : "error", "nd" : "dark"}
	var reptype = status_map[repstatus]
	var addcl = "ui-pnotify-no-icon"
	if(reptype == "dark"){
		addcl =  addcl + " notification-dark"
	}
	var t = document.getElementById(repname).innerHTML
	new PNotify({
		title: repname,
		text: t,
		type: reptype,
		addclass : addcl,
		icon: false
	});
}

/**
 * Displays a PNotify notification pop-up containing detailed user or global history entry.
 *
 * @param {string|number} id   History entry ID.
 * @param {string}        list Scope identifier ('global' or 'user').
 */
function show_hist_info(id, list){
	var addcl = "ui-pnotify-no-icon notification-dark"
    var id_prefix
    if(list=="global"){
        id_prefix = "hg"
    }
    else{
        id_prefix = "hu"
    }
	var t = document.getElementById("more-"+id_prefix+"-"+id).innerHTML
	var title = document.getElementById(id_prefix+id).innerHTML
	new PNotify({
		title : title,
		text: t,
		type: "dark",
		addclass : addcl,
		icon: false
	});
}

/**
 * Triggers a browser file download for user or global history text files.
 *
 * @param {string} [el="full"] User identifier or 'full' for global history.
 */
function download_history(el="full"){
	var link = document.createElement("a");
	var name, uri
	if(el=="full"){
		name = "history.txt"
		uri = "users/history.txt"
	}
	else{
		name = "history_"+el+".txt"
		uri = "users/"+el+"/history_"+el+".txt"
	}
	link.download = name;
	link.href = uri;
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);
	delete link;	
}