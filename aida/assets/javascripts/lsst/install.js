$(document).ready(function() {
    $('#header-right').hide()
	$("#header-right").append("<span id='session-user'>1stInstall</span>");
});

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
				upload_backup(uploader.files[0].name);
        });      
    }); // end of the upload form configuration
	
	
function start_install(){
	//Initialize installation	
	//AJAX call to truncate tables and remove existing directories
	$("#loader").show();
	$.ajax({
		url: "scripts/backup.py",
		method      : 'POST',
		datatype	: 'json',
		data : {
			"action" : "flush"
		},
		success:function()
		{
			$("#loader").hide();						
			$('#main_inst').hide()
			$('#import_bkp').show()
		}
	})			
}

function backtohome(el,reset){
	if(reset){
		window.location.reload()
		
	}else{
		$(el).hide()
		$('#main_inst').show()
	}
}

function next_confdb(){
	
	var toimport = $('#import_bkp').val()
	if(toimport==1){
		$('#db_conf').hide()
		$('#import_conf').show()
	}
	else{
		alert("TODO")
		
	}
	
	
}

$("#email").keyup(function() {
    $("#notiemail").val( this.value );
});

$(document).ready(function() {
	$("#notificationemail").change(function(){
        if($(this).is(":not(:checked")) {
            $("#notiemail").prop("required", true);
			$("#tr_noti").show()
        }
		else{
			$("#notiemail").prop("required", false);
			$("#tr_noti").hide()
			
		}
		
	});
});

function registration(yourform){
	$("#loader").show();
	var addmsg = ""
	var notification = document.getElementById("notiemail").value
	event.preventDefault();
	//
	$.ajax({
		url: "scripts/backup.py",
		method : 'POST',
		data : {
			"action" : "notification",
			"email" : notification
		},
	   success:function(res){
			var error = res['error']
			if(error==1){
				addmsg = "\nWARNING! Impossible to set notification email. You can set it from admin dashboard successively.\n\nNow you can close this page."
			}
			requestnewuser(yourform, addmsg)
		},
	});
}

document.addEventListener("DOMContentLoaded", function() {
    let confirm = document.getElementById("confirm").innerHTML
	let activation = document.getElementById("activation").innerHTML
	let email = document.getElementById("newmail").innerHTML
	if(confirm == 1 && activation != 0 && email!=0){
		$("#loader").show();
		//CODE FOR ACTIVATING EMAIL
		$.ajax({
			url: "functions.php",
			method      : 'POST',
			datatype	: 'json',
			data : {
				"username" : activation,
				"newmail" : email,
				"action" : "activateuser"
			},
			success:function(res){
				if(res==1){
					alert("ERROR! Impossible to activate user. Please contact AIDA support team.")
					$("#loader").hide();				
				}
				else{
					var addmsg = "\n"
					if(res==2){
						addmsg = "\nWARNING! Impossible to set notification email. You can set it from admin dashboard successively."
					}					
					clean_installation(addmsg)
				}
			},
			error:function(){
				alert("ERROR! Impossible to activate user. Please contact AIDA support team.")
				$("#loader").hide();
			}
		})		
	}
});

function clean_installation(addmsg="\n"){
	$("#loader").show();	
	$.ajax({
		url: "scripts/backup.py",
		method      : 'POST',
		datatype	: 'json',
		data : {
			action : "clean"
		},
	   success:function(res)
		{
			document.getElementById('inst-compl').innerHTML='<p style="min-height: 40px;">'+addmsg+'</p><p class="inst-compl">May the plots be with you...<p>'
			$("#loader").hide();
			$('#modal-complete').modal('show');
		}
	})	
}

function skip_upload(){
	var toform=["smtpconf_form", "1streg_form"]
	$("#nextform").val(toform)
	showtab(toform,0)
}