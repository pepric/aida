$(document).on('change', '.check', function () {
  var el = $(this)[0];
  more_stats_params(el)
});

$('#checkThemAll').on('change', function () {
  if ($(this).prop('checked')) {
    $('.check').each(function () {
      $(this).prop('checked', true).trigger('change');
    });
  } else {
    $('.check').each(function () {
      $(this).prop('checked', false).trigger('change');
    });
  }
});

$(document).ready(function () {
  $('#tend').prop('disabled', true);
  $('#tstart').datetimepicker({
    useCurrent: "day",
    timeZone : "UTC",
    format: 'YYYY-MM-DD HH:mm:ss',
    //maxDate: "now"
  });
  $('#tend').datetimepicker({
    useCurrent: false, //Important! See issue #1075 - This comment is for useCurrent:"day" maybe OLD
    timeZone : "UTC",
    format: 'YYYY-MM-DD HH:mm:ss',
  });
  $("#tstart").on("dp.change", function (e) {
    $('#tend').prop('disabled', false);
    if( e.date ){
      $('#tend').data("DateTimePicker").minDate(e.date);
      //$('#tend').data("DateTimePicker").maxDate("now");
      $('#tend').data("DateTimePicker").date(e.date);                
    }

  });
  $('#dateiconend').on("click", function (){$("#tend").focus()})
  $('#dateiconstart').on("click", function (){$("#tstart").focus()})
});

$(document).ready(function(){
  $("#hktm_source").change(function(){
    //init hidden det type
    $("#det-type").val("None");
    var plot = $("#plot_type").val();
    var usecase = $("#usecase").val();
    var source = $("#hktm_source").val();
    var stats = $("#stats_enable").val();
    $("#params").remove();
    $("#yparams").remove();
    if($("#bins").length > 0){
      $("#bins").remove();
    }          
    document.getElementById('daterange').style='display:block;';
    $.ajax({
      method:"POST",
      url: 'forms.php',
      data:{
        p : plot,
        o : usecase,
        s : source
      },
      success :	function(resultdata){
        $( resultdata ).insertBefore( "#daterange" );
        if($("#bins").length > 0){
          $("#bins").show();
          set_bins();
        }
        $("#n_ypar").val(1)
        if(source=="VIS" && (usecase=="science")){
          if(plot=="scatter"){
            var xcoord=document.getElementById('x-sys')
            xcoord.value="ALL"
            set_params(xcoord)                                
          }
          var coord=document.getElementById('y0-sys')
          coord.value="ALL"
          set_params(coord)
        }                     				
      }
    });          	
  });
});

function set_bins(){
	
  $("input[type='radio'][name=bintype]").change(function(){
    var valuebox = document.getElementById("binsize");
    if($(this).val()=="binsize")
    {
      valuebox.setAttribute("placeholder", "Set bin size...");				
      valuebox.setAttribute("min", "0.000000000000001");
      $('label[for=binsize]').remove();
      $('#bins').removeClass('has-error');                  
    }
    else
    {
      valuebox.setAttribute("placeholder", "Set number of bins...");
      valuebox.setAttribute("min", "2");
      $('label[for=binsize]').remove();
      $('#bins').removeClass('has-error');                      
    }
  });
};

$('#change_op').on("click", function(){
  $("#loader").show();
  var new_op = $('select[name=opmode] option').filter(':selected').val()
  // ajax url to fetch required filters
  var url   =   'functions.php';
  // call subcategory ajax here 
  $.ajax({
    method:"POST",
    url:url,
    data:{
      action : "update_opmode",
      new : new_op,
	  user : document.getElementById("session-user").innerHTML
    },
    success:function(data){
      var res = JSON.parse(data)["error"];
	  var msg
	  switch(res){
		  case true:
		  {
			msg="Operating Mode successfully updated."
			break;
		  }
		  case false:
		  {
			msg="ERROR! Impossible to update settings. Please, retry later or contact AIDA Admin."
			break;			
		  }
		  case "None":
		  {
			msg="INFO: Operating mode unchanged. Nothing to do."  
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
}); 


$('#export-btn').on("click", function(){
  $("#loader").show();
  var out_hist
  var conf_hist = "NA"
  //get all check settings
  var exp_users = document.getElementById("exp_users").checked ? 1:0  
  var exp_reports = document.getElementById("exp_reports").checked ? 1:0  
  var exp_repconf = document.getElementById("exp_repconf").checked ? 1:0      
  var exp_stored = document.getElementById("exp_stored").checked ? 1:0  
  var exp_sys = document.getElementById("exp_sys").checked ? 1:0      
  var exp_history = document.getElementById("exp_history").checked ? 1:0  
  var exp_smtp = document.getElementById("exp_smtp").checked ? 1:0  

  var list_req = []
  if(exp_users){list_req.push("Users data")}
  if(exp_reports){list_req.push("Reports")}
  if(exp_repconf){list_req.push("Reports configuration files")}
  if(exp_stored){list_req.push("Stored experiments")}
  if(exp_sys){list_req.push("Systems configuration")}
  if(exp_history){list_req.push("History")}
  if(exp_smtp){list_req.push("SMTP settings")}  
  out_hist = {"Requested" : list_req.join(", ")}  
  //check if at least on item is checked  
  if(exp_users || exp_reports || exp_repconf || exp_stored || exp_sys || exp_history || exp_smtp){  
    // call subcategory ajax here 
    $.ajax({
      method:"POST",
      url:"scripts/backup.py",
      data:{
        action : "export",
        users : exp_users,
        reports : exp_reports,
        repconf : exp_repconf,
        stored : exp_stored,
        systems : exp_sys,
        hist : exp_history,
        smtp : exp_smtp,
        username : document.getElementById("session-user").innerHTML
      },
      success:function(data){
		var path = window.location.href.replace("dashboard.php", "").replace("#","")
        switch(data["error"])
        {
          case 0:
            {
              //start download and remove remote tar
			  downloadPDF(path+"tmp/"+data["file"], data["file"], 0, 'application/gzip');
              break;
            }
          case 1:
            {
              alert("ERROR! Impossible to create backup file. Please, retry later or contact AIDA Admin.")              
              break;
            }      
          case 2:
            {
              alert("WARNING! Backup file has been generated but the following items have been not exported: \n" + data["msg"] +"This could cause an incomplete data import.\n It is suggested to retry later or contact AIDA Admin.")
			  conf_hist = {"Failed" : data["msg"].replace(/\n/g,", ")}
			  console.log(conf_hist)
              //start download and remove tar
			  downloadPDF(path+"tmp/"+data["file"], data["file"], 0, 'application/gzip');             
              break;			
            }
        }         
		//update history
		$.ajax({
			type: "POST",
			url: "functions.php",
			data: {
				action: "update_history",
				username : document.getElementById("session-user").innerHTML,
				operation : "Data exported",
				infile :	"NA",
				out	: JSON.stringify(out_hist),
				config : JSON.stringify(conf_hist)
				},
			error : function (obj, textstatus) {
				alert("Impossible to store the operation in History")
			}
		})        
		$("#loader").hide();                  
      }
    });      
  }
  else{
  	alert("Nothing to backup. Please, select at least one item to backup.")
  }
}); 

$('#import-btn').on("click", function(){
  $("#loader").show();

  //get all check settings
  var imp_users = document.getElementById("imp_users").checked ? 1:0  
  var imp_reports = document.getElementById("imp_reports").checked ? 1:0  
  var imp_repconf = document.getElementById("imp_repconf").checked ? 1:0      
  var imp_stored = document.getElementById("imp_stored").checked ? 1:0  
  var imp_sys = document.getElementById("imp_sys").checked ? 1:0      
  var imp_history = document.getElementById("imp_history").checked ? 1:0  
  var imp_smtp = document.getElementById("imp_smtp").checked ? 1:0
  var imp_file = document.getElementById("upfile-preview").innerHTML

  //check if at least on item is checked  
  if(imp_users || imp_reports || imp_repconf || imp_stored || imp_sys || imp_history || imp_smtp){  
	var toform = []
    // call subcategory ajax here 
    $.ajax({
      method:"POST",
      url:"scripts/backup.py",
      data:{
        action : "import",
        users : imp_users,
        reports : imp_reports,
        repconf : imp_repconf,
        stored : imp_stored,
        systems : imp_sys,
        hist : imp_history,
        smtp : imp_smtp,
        username : document.getElementById("session-user").innerHTML,
		file : imp_file
      },
      success:function(data){
        //var res = JSON.parse(data)["error"];
		//var path = window.location.href.replace("dashboard.php", "")
				console.log(data["error"])
        switch(data["error"])

        {
          case 0:
            {
				var msg = "Application has been successfully updated.\n\n"
				if(imp_smtp==0){
					msg += "INFO : No SMTP server settings imported. You will have to set it in the following steps.\n\n"
					//$("#impsmtp").val(1)
					toform.push("smtpconf_form")					
				}					
 
				if(imp_users==0){
					msg += "INFO : No Users data imported. You will have to set the first Admistrator in the following steps.\n\n"
					//$("#impusers").val(1)
					toform.push("1streg_form")
				}
				alert(msg)

				if(toform.length > 0){
					$("#nextform").val(toform);
					$("#import_bkp").hide();
					showtab(toform,0);
					$("#loader").hide();					
				}
				else{
					$.ajax({
						url: 'scripts/backup.py',
						method:"POST",
						data: {
							action:"clean"
						},
						success: function (response) {
							document.getElementById('inst-compl').innerHTML='<p style="min-height: 40px;"></p><p class="inst-compl">May the plots be with you...<p>'
							$("#loader").hide();
							$('#modal-complete').modal('show');
						},
						error: function () {
							alert("ERROR! Something has gone wrong. Impossible to finalize installation.\nPlease, retry or contact AIDA staff.")
							window.location.href = "index.php";
						}
					});
				}
				break;
            }
          case 1:
            {
				var msg = "ERROR! Impossible to import data from backup file. Please, retry later or contact AIDA Admin."
				alert(msg)
				break;
            }      
          case 2:
            {
				var msg = "WARNING! Data import has been completed but the following items have been not imported: \n" + data["msg"]+"\n"
				let smtpfail = data["msg"].includes("SMTP settings");
				if(smtpfail || imp_smtp==0){
					msg += "INFO : No SMTP server settings imported. You will have to set it in the following steps.\n\n"
					toform.push("smtpconf_form")					
				}				
				let userfail = data["msg"].includes("Users Data");
				if(userfail || imp_users==0){
					msg += "INFO : No Users data imported. You will have to set the first Admistrator in the following steps.\n\n"
					toform.push("1streg_form")					
				}						
				alert(msg)

				if(toform.length > 0){
					$("#nextform").val(toform);
					$("#import_bkp").hide();
					showtab(toform,0);
					$("#loader").hide();					
				}
				else{
					$.ajax({
						url: 'scripts/backup.py',
						method:"POST",
						data: {
							action:"clean"
						},
						success: function (response) {
							alert("INSTALLATION COMPLETE!\n\nMay the plots be with you...");
							window.location.href = "index.php";
						},
						error: function () {
							alert("ERROR! Something has gone wrong. Impossible to finalize installation.\nPlease, retry or contact AIDA staff.")
							window.location.href = "index.php";
						}
					});					
				}				
				break;			
            }
        }
      }
    });
  }
  else{
  	alert("Nothing to import. Please, select at least one item to import.")
 	
  }
});



 