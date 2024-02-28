function check_connection(){
	var error = 0
  	$.ajax({
		url         : "scripts/cs_interface.py",
		method      : 'POST',
		datatype	: 'json',
      	data		: {action : "check_connection"},
      	success		: function(response){	
			error = response['error']	
        }
    });
 	return error
}

function show_dts(select){
	var chosen = select.options[select.selectedIndex].value; 
	var dtsg = document.getElementById("dts-group")
	var dts = document.getElementById("dts")
	var sgfunc = document.getElementById("sfunc-group")
	var sfunc = document.getElementById("sfunc")	
	if(chosen!="full"){
		dtsg.style.display = "block";
		dts.setAttribute("required", "required");
	}
	else
	{
		dtsg.style.display = "none";
		dts.removeAttribute("required");
	}
	if(chosen=="by function"){
		sgfunc.style.display = "block";
		sfunc.setAttribute("required", "required");
	}
	else
	{
		sgfunc.style.display = "none";
		sfunc.removeAttribute("required");
	}
}

function show_dtacq(select){
	var n = select.value; 
	var dtacqg = document.getElementById("dtacq-group")
	var dtacq = document.getElementById("dtacq")
	if(n>"1"){
		dtacqg.style.display = "block";
		dtacq.setAttribute("required", "required");
	}
	else
	{
		dtacqg.style.display = "none";
		dtacq.removeAttribute("required");
	}
}

function show_custom(select){
	var n = select.value; 
	var customg = document.getElementById("custom-group")
	var custom = document.getElementById("custom")
	if(n == "custom"){
		customg.style.display = "block";
		custom.setAttribute("required", "required");
	}
	else
	{
		customg.style.display = "none";
		custom.removeAttribute("required");
	}
}


function generate_editor(){
	$.ajax({
		method : 'POST',
		url : 'json-gen.php',
		data : {
			action : 'new_from_form',
			tstart : document.getElementById("tstartconf").value,
			sampling : document.getElementById("sampling").value,
			dts : document.getElementById("dts").value,
			sfunc : document.getElementById("sfunc").value,          
			t_window : document.getElementById("window").value,
			nacq : document.getElementById("nacq").value,
			dtacq : document.getElementById("dtacq").value,
			dtcustom : document.getElementById("custom").value,
			period : document.getElementById("period").value
		},
		datatype    : 'json',
		success     : function(response){
			//Hide form 
			document.getElementById("period").setAttribute("readonly","")
			document.getElementById("custom-group").setAttribute("style", "display:none")
			document.getElementById("daterange").setAttribute("style", "display:none")
			document.getElementById("sampling-group").setAttribute("style", "display:none"),
            document.getElementById("sfunc-group").setAttribute("style", "display:none"),
			document.getElementById("dts-group").setAttribute("style", "display:none"),
			document.getElementById("window-group").setAttribute("style", "display:none"),
			document.getElementById("nacq-group").setAttribute("style", "display:none"),
			document.getElementById("dtacq-group").setAttribute("style", "display:none")
			
			//Show and Hide buttons
			$("#submit_config").hide();
			$("#submit_temp").show();
			$("#complete_config").show();
			$("#run_config").show();
			
			//Create Editor
			var div = document.getElementById("editor");
			div.setAttribute("style", "display : block");
			var editor = CodeMirror.fromTextArea(document.getElementById('code-area'), {
				mode: "text/javascript",
				lineNumbers: true,
			});
			
			editor.setSize(null, 600)
			editor.setValue(response)
			editor.save()
			editor.on("change", function() {
				editor.save()
			})

			//Show file name input
			$("#filename").show();
		},
	});
}

function generate_from_file(){
	$.ajax({
		method : 'POST',
		url : 'json-gen.php',
		data : {
			action : 'load_from_file',
			filename : document.getElementById("infile").value,
		},
		datatype    : 'json',
		success     : function(response){
			//Create Editor
			var div = document.getElementById("editor");
			div.setAttribute("style", "display : block");
			var editor = CodeMirror.fromTextArea(document.getElementById('code-area'), {
				mode: "text/javascript",
				lineNumbers: true,
			});
			editor.setSize(null, 600)
			editor.setValue(response)
			editor.save()
			editor.on("change", function() {
				editor.save()
			})

			//Show file name input
			$("#filename").show();
		},
	});
}

function create_configfile(iscomplete, page, action){
	
	//Get JSON text from textarea
	var textToWrite = document.getElementById("code-area").value;
	//If period is custom, get custom value, else "none"
	var period = document.getElementById("period").value;
	var customtime = "none";
	if(period == 'custom'){
		customtime = document.getElementById("custom").value
	}
	// preserving line breaks
	var textToWrite = textToWrite.replace(/\n/g, "\r\n");
	// Check config file integrity
	$.ajax({
		url         : "scripts/config_validation.py",
		method      : 'POST',
		datatype	: 'json',
		data        : {
			jsontext : textToWrite,
			period : period,
			from : "editor"
		},
		beforeSend: function(){
		// Show loader image container
			$("#loader").show();
			window.document.body.scrollTop = 0;
			window.document.documentElement.scrollTop = 0;
		},
		success: function(response){
			$("#loader").hide();
			isvalid = response['isvalid']
			if(isvalid == false){
				msg = response['msg']
				alert(msg);
			}
			else{
				save_configfile(textToWrite, iscomplete, page, customtime, period, action)
			}
		}
	})
}

function save_configfile(textToWrite, iscomplete, page, customtime, period, action){
	// filename to save as
	var fileNameToSaveAs = document.getElementById("infile").value
	var file_arr = fileNameToSaveAs.split(".")
	var user = document.getElementById("session-user").innerHTML
	if(file_arr!=""){
		if(file_arr[1]!="json"){fileNameToSaveAs = fileNameToSaveAs+".json"}
		//save file in users/config
		$.ajax({
			//url         : phpfile,
			url         : "config_handler.php",
			method      : 'POST',
			datatype	: 'json',
			data        : {
				file : fileNameToSaveAs,
				jsontext : textToWrite,
				period : period,
				user : user,
				iscomplete : iscomplete,
				page : page,
				cust_val : customtime,
				action : action,
			},
			success     : function(response){
				console.log(response)
				jsontext = JSON.parse(response)
				var msg = "Configuration File successfully "
				if(page=="new"){
					msg = msg +"created!\n";
				}
				else{
					msg = msg +"updated!\n";
				}
       
				if(jsontext['status']=="success"){
					if(action == "run"){
                      	msg = msg + "Report generation is scheduled or running. You will receive an email when a report is completed.\n";
						run_report(jsontext['file'], period, user, jsontext['isrunning'])
					}
					else{
						msg = msg + "You can list it in \"Configuration Files\" page.\n";
					}
					alert(msg);
				}else if(jsontext['status']=="warning"){
					msg = msg +"Warning: "+jsontext['msg']
					if(action == "run"){
                      	msg = msg + "\nReport generation is scheduled or running. You will receive an email when a report is completed.\n";					                      
						//run report generation
						run_report(jsontext['file'], period, user, jsontext['isrunning'])
					}
					else{
						msg = msg + "You can list it in \"Configuration Files\" page.\n";
					}                  
					alert(msg);
				}
				else{
					alert("Impossible to create configuration file!\n"+jsontext['msg']);
				}
				document.getElementById("infile").value = jsontext['file'];
 				if(action=="run"){
					//window.location.href='list-config.php'; 
				}
				else{
					window.location.href='edit-config.php?conf='+jsontext['file']+'&p='+period+'&w=';
				}
			},
		});
		event.preventDefault();
	}
	else
	{
		alert("Impossible to create configuration file!\nConfiguration file name not defined.");
	}
}
		

function run_report(configfile, period, user, isrunning){
	$.ajax({
		url         : "scripts/run_report.py",
		method      : 'POST',
		datatype	: 'json',
		data        : {
			config : configfile,
			period : period,
			user : user,
			isrunning : isrunning,
			iodaurl : window.location.host
		},
		success:	function(response){
			msg = "OK"
		},
		error: function(response){
        	msg = "ERROR! Impossible to start report generation.\nImpossible to connect to local DB.\n\nPlease, contact AIDA admin";
        }
      	
	});
	event.preventDefault();
}		

function run_from_db(configfile, period, user, opmode, isrunning){
	var op_error = 0
	//check operating mode
	var curr_opmode = document.getElementById("opmode").innerHTML
	if(opmode != curr_opmode){
		alert("Error! Impossible to use config file in current Operating Mode ("+curr_opmode+"). Configuration file created for "+opmode+" Operating Mode")
      	op_error = 1
    }    
	//add function update isrunning
	if(op_error==0){	
      $.ajax({
        url         : "functions.php",
        method      : 'POST',
        datatype	: 'json',
        data        : {
          file : configfile,
          action: "update_isrunning"
        },
        success:	function(response){
          if(response == "true"){
            $.ajax({
              url         : "functions.php",
              method      : 'POST',
              datatype	: 'json',
              data        : {
                username : user,
                operation : "Launched report generation from existing configuration file",
                infile : "NA",
                out : '{"period" : "'+period.charAt(0).toUpperCase() + period.slice(1)+'", "configuration file" : "'+configfile+'"}',
                conf : "",
                action: "update_history"
              }
            })
            run_report(configfile, period, user, isrunning)
            alert("Report generation is scheduled or running. You will receive an email when a report is completed. ")
          }
        },
        error: function(response){
          alert("Error! Something has gone wrong while updating configuration data. Please contact AIDA admin.")
        }
      })
        .done(function() {
        window.location.reload(); //CHIUDERE FINESTRA????
      });		  
      event.preventDefault();
    }
}

$(document).ready(function() {		
	$('#submit_btn_upload').on('click', function(event){
		
		var user = document.getElementById("session-user").innerHTML
		var period = document.getElementById("period").value
		var t_custom = document.getElementById("custom").value
		//upload file
		const url = 'upload.php'
		const form = document.querySelector('form')
		const files = document.querySelector('[type=file]').files
		var formData = new FormData()
		for (let i = 0; i < files.length; i++) {
			let file = files[i]
			console.log(file)
			formData.append('files[]', file)
		}
		formData.append('username', user)
		formData.append('period', period)
		formData.append('t_custom', t_custom)
		$.ajax({
			url         : 'upload.php',
			data        : formData ? formData : form.serialize(),
			cache       : false,
			contentType : false,
			processData : false,
			type        : 'POST',
			datatype	: 'json',
			success     : function(response){
				var text = "{"+response.split("{")[1]
				jsonres = JSON.parse(text)
				filename = jsonres['filename']
				idhist = jsonres['histid']
				if(jsonres['status'] != "failed"){
					//Check file integrity
					$.ajax({
						url         : "scripts/config_validation.py",
						method      : 'POST',
						datatype	: 'json',
						data        : {
							filename : "../users/config/"+filename,
							period : period,
							from : "upload"
						},
						beforeSend: function(){
						// Show loader image container
							$("#loader").show();
							window.document.body.scrollTop = 0;
							window.document.documentElement.scrollTop = 0;
						},
						success     : function(response){
							$("#loader").hide();
							isvalid = response['isvalid']
							if(isvalid == false){
								msg = response['msg']
								remove_upload(filename, idhist)
								alert(msg);
							}
							else{
								if(jsonres['status']=="success"){
									//run report generation
									run_report(jsonres['filename'], period, user, jsonres['isrunning'])
									alert("Upload completed.\nReport generation is scheduled or running. You will receive an email when a report is completed. ");
								}else if(jsonres['status']=="warning"){
									//run report generation
									run_report(jsonres['filename'], period, user, jsonres['isrunning'])
									alert("Upload Complete!" + "\n"+jsonres['msg']+"\nReport generation is scheduled or running. You will receive an email when a report is completed. ");
								}
							}
						}
					})
					.done(function() {
						window.location.reload();; //CHIUDERE FINESTRA???
					});
				}
				else{
					alert("Impossible to upload file!\n"+jsonres['msg']);
				}
			}
				
		})
		event.preventDefault();
	})
});	


function resume_report(id, t0, cf, user, period){
	alert("Report generation is scheduled or running. You will receive an email when a report is completed.")
   	$.ajax({
		method : 'POST',
		url : 'scripts/cs_interface.py',
		data : {
			runid: id,
          	configfile : cf,
           	username : user,
          	period : period,
          	start_time : t0,
           	action : "resume_report",
          	iodaurl : window.location.host
		},
		datatype    : 'json'
	});
}  

function stop_report(id, pid, cf, act){
	var user = document.getElementById("session-user").innerHTML
    if(act == "kill"){
		msg = "Are you sure to stop Report generation "+id+"? \nThis operation can not be canceled."
    }
  	else if(act == "pause"){
		msg = "Are you sure to pause Report generation "+id+"?"
    }
  	else{
		msg = "Are you sure to completely remove Report generation "+id+"? \nThis operation can not be canceled."
	}
	    
    var r = confirm(msg)
	if (r == true) {
      	$("#loader").show();
      	$.ajax({
			method : 'POST',
			url : 'scripts/kill_report.py',
			data : {
				runid: id,
				pid : pid,
              	configfile : cf,
            	user : user,
              	action : act
			},
			datatype    : 'json',
			success     : function(response){
           		error = response['error']
              	if (error == 1) {
                	alert("Impossible to stop report "+id+". \n\nERROR : "+response['msg']+"\n\nPlease, contact AIDA admin");
                }
              	else if (error == 2){
                  	alert("Report generation "+id+" stopped. \n\nWARNINGS :\n"+response['msg']+"\n\nPlease, contact AIDA admin");
                }
				else{
                  if (act == "kill"){
                    alert("Report generation "+id+" stopped. No more related reports will be produced.");
                  }
                  else if(act == "pause"){
                    alert("Report generation "+id+" paused. No more related reports will be produced until resume.");
                  }
                  else{
                    alert("Report generation "+id+" completely removed. All temporary data have been deleted.");
                  }
                }
			},
          	error : function(response){console.log("ERROR"); console.log(response)},
          	complete : function(){$("#loader").hide();}
		});
	}
}