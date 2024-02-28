$(document).ready(function() {
	// init validation rule:sequence of integer numbers separated by return
	$.validator.addMethod("listnum", function(value, element){
      	var arr = value.split("\n")
        if(value==""){return true}
		for(var i=0; i<arr.length; i++){
          	//console.log(arr[i])
          	//console.log(arr[i].trim())
          	var res_l = arr[i].trim() && /^\d+$/.test(arr[i].trim())
			//console.log(res_l)
            if(!res_l){return false}
        }
      	return true
	}, "This field must be a sequence of integer numbers separated by return");

	// init validation rule:sequence of strings separated by return
	$.validator.addMethod("liststr", function(value, element){
        if(value==""){return true}        
        if(value.includes(",")){return false}
        return true
		}, "This field must be a sequence of strings separated by return");
		
	// init validation rule:End Date must be greater than Start Date
	$.validator.addMethod("greaterthan", function(value, element){
            return value > $('#tstart').val()
	}, "End Date must be greater than Start Date");        

	// init validation rule: single integer, comma separated integers or range of integers (int>0)
	$.validator.addMethod("numbers_n_ranges", function(value, element){
		const isNumeric = value => !isNaN(value) && value > 0 // you may also check if the value is a nonzero positive integer
		const isOrdered = (start, end) => parseInt(start) < parseInt(end)
		const isRangeValid = range => range.length == 2 && range.every(isNumeric) && isOrdered(range[0], range[1])
		const isSingleValid = single => single.length == 1 && isNumeric(single[0])
		const inputs = value.split(',').map(x => x.trim());
		for (const x of inputs) {
			if (!x) return false;
			const pages = x.split('-');
			if (!isSingleValid(pages) && !isRangeValid(pages))
				return false;
		}
		return true;
	}, "Invalid format. Only single integer >0, comma separated integers >0 or range of integers >0 (a-b) are allowed");  

	$('#submit_img_button').on('click', function(event) { 
		$("#img_op").val("")
		var ny = document.getElementById("n_ypar").value
		//dates validation
		$('#tend').rules("add", 
			{
				greaterthan : true
			});

		for(var i=0; i<ny; i++){
			// adding rules for elements
			$('#y'+i+'-sys').each(function() {
				$(this).rules("add", 
				{
					required : {
						depends : function(){
							return $(this).val()===null
						}
					}
				})
			}); 
		}
		// prevent default submit action         
		event.preventDefault();
		// test if form is valid 
		if($('#detector_form').validate().form()) {
			get_list_files()
	   }
	})

	$('#submit_button').on('click', function(event) { 
		var ny = document.getElementById("n_ypar").value
		var plot = document.getElementById("plot_type").value
		//dates validation
		if($('#tstart').length && $('#tend').length){
			$('#tend').rules("add", 
				{
					greaterthan : true
				});
		}

		if($('#pid').length){
			$('#pid').rules("add", 
				{
					required : true
				});
		}		
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
			$('#y'+i+'-ic').each(function() {
				$(this).rules("add", 
					{
						required: true,
					})
			});				
			$('#y'+i+'-sys').each(function() {
				$(this).rules("add", 
					{
						required : {
							depends : function(){
								return $(this).val()===null
							}
						}
					})
			}); 

			$('#y'+i+'-params').each(function() {
				$(this).rules("add", 
					{
						required: true
					})
			}); 
			$('#y'+i+'-partype').each(function() {
				$(this).rules("add", 
					{
						required: true
					})
			});
			$('#y'+i+'-det-col').each(function() {
				$(this).rules("add", 
					{
						required: true
					})
			}); 

			$('#y'+i+'-det-row').each(function() {
				$(this).rules("add", 
					{
						required: true
					})
			});
			
			$('#y'+i+'-quadrant').each(function() {
				$(this).rules("add", 
					{
						required: true
					})
			});				
			$('#x-det-row').each(function() {
				$(this).rules("add", 
					{
						required: true
					})
			});
			$('#x-det-col').each(function() {
				$(this).rules("add", 
					{
						required: true
					})
			});
			$('#x-quadrant').each(function() {
				$(this).rules("add", 
					{
						required: true
					})
			});				
			$('#y'+i+'_pid1').each(function() {
				$(this).rules("add", 
					{
						listnum: true
					})
			});
			$('#y'+i+'_pid2').each(function() {
				$(this).rules("add", 
					{
						listnum: true
					})
			});
			$('#y'+i+'_DataSetRelease').each(function() {
				$(this).rules("add", 
					{
						liststr: true
					})
			});

			$('#y'+i+'-coeff').each(function() {

				$(this).rules("add", 
					{
						required: true,
						numbers_n_ranges : true
					})
			});
		} 
		// prevent default submit action         
		event.preventDefault();
		// test if form is valid 
		if($('#detector_form').validate().form()) {
			var stats = $("#stats_enable").val();	
			var go = true
			if(stats=="advanced"){
				var stats_list = document.getElementById("stats_list").value;
				if(stats_list==""){
					go = confirm("No statistical operation selected! Proceed anyway?")							
				}
			}

			if(go==true){
				//Check if time interval is too large respect with current system settings
				if($("#tstart").val() != null && $("#tend").val() != null){
					$.ajax({
						method:"POST",
						url: 'scripts/cs_interface.py',
						datatype : 'json',
						data:{
							'action' : 'check_deltat',
							'source': $("#hktm_source").val(),
							'tstart' : $("#tstart").val(),
							'tend' : $("#tend").val(),
							'usecase' : $("#usecase").val(),
						},
						beforeSend: function(){
							//hide previous plot container
							$("#plot_container").hide()
							// Show loader image container
							$("#loader").show();
							window.document.body.scrollTop = 0;
							window.document.documentElement.scrollTop = 0;
						},                  
						success :	function(result){
							if(result['delta'] != null){
								if(result['delta']==0){
									run_py(event);                        
								}
								else
								{
									alert("Data range is too large to compute online. An email will be send when analysis is completed.")
									run_plot_offline(event)
									$("#loader").hide();
								}
							}
							else{alert("ERROR! Impossible to submit your request. Please, contact AIDA admin.");$("#loader").hide();}
						}
			  
					});
				}
				else{
					$("#plot_container").hide()
					// Show loader image container
					$("#loader").show();
					window.document.body.scrollTop = 0;
					window.document.documentElement.scrollTop = 0;						
					run_py(event);
				}
			}
		}
	})
	
	// initialize the validator
	$('#detector_form').validate({

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

$(document).ready(function() {

	$('#submit_config').on('click', function(event) {
	// prevent default submit action         
		event.preventDefault();

		// test if form is valid 
		if($('#config_form').validate().form()) {
			var period_box = document.getElementById("period");
			period_box.setAttribute("disabled", "disabled");
			generate_editor();
		}	
	});
	
	// initialize the validator
	$('#config_form').validate({
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
});	

$(document).ready(function() {
	$('#run_config').on('click', function(event) {
		var page = document.getElementById("page").value	
	// prevent default submit action         
		event.preventDefault();
		// test if form is valid 
		if($('#editor_form').validate().form()) {
			create_configfile(1, page, "run");
		}	
	});
	
	// initialize the validator
	$('#editor_form').validate({
	
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
});


$(document).ready(function() {

	$('#complete_config').on('click', function(event) {
		var page = document.getElementById("page").value	
	// prevent default submit action         
		event.preventDefault();

		// test if form is valid 
		if($('#editor_form').validate().form()) {
			create_configfile(1, page, "save"); //MODIFICARE CONFIG_HANDLER.PHP
		}	
	});
	
	// initialize the validator
	$('#editor_form').validate({
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
});	

$(document).ready(function() {

	$('#submit_temp').on('click', function(event) {
		var page = document.getElementById("page").value
	// prevent default submit action         
		event.preventDefault();
		// test if form is valid 
		if($('#editor_form').validate().form()) {
			create_configfile(0, page, "save");
		}	
	});
	
	// initialize the validator
	$('#editor_form').validate({
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
});	

$(document).ready(function() {
	$('#store-btn').on('click', function(event) {
		// prevent default submit action         
		event.preventDefault();
		// test if form is valid 
		if($('#modal-form').validate().form()) {
			var store = document.getElementById("mode")
			var labels = document.getElementById("modal-labels").value.split(",");                
			var save = store.options[store.selectedIndex].value
			var download = document.getElementById("downloadpdf").checked
			var nameexp = document.getElementById("n_exp").value
			//console.log(nameexp, labels, save, download,store)
			exportPDF(nameexp, labels, save, download)
		}
	});
	
	// initialize the validator
	$('#modal-form').validate({
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
});	


$(document).ready(function() {
	$('#change-pwd').on('click', function(event) {

	// prevent default submit action         
		event.preventDefault();

		// test if form is valid 
		if($('#modal-pwd').validate().form()) {
			var pwd = document.getElementById("newpwd");
			var form = document.getElementById("modal-pwd");
			formhash(form, pwd, 'change');
			$("#pwd").hide();
		}
	});
		
	// initialize the validator
	$('#modal-pwd').validate({
		rules : {
			newpwd : {
				checkpwd : true,
				minlength : 8
			},
			checkpwd : {
				equalTo : "#newpwd"
			}
		},
		messages : {
			newpwd: {
				checkpwd: "An upper case letter and a digit required",
				minlength: "At least 8 characters required"
			},
		},
	
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
	
	$.validator.addMethod("checkpwd", function(value) {
		return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) // consists of only these
		&& /[A-Z]/.test(value) // has a lowercase letter
		&& /\d/.test(value) // has a digit
	});
});

$(document).ready(function() {
	$(document).on('click', '#store-rep-btn', function () {

		if($('#modal-form').validate().form()) {
			//get filename
        	var filename = document.getElementById('fname').value;
        	//get creator
        	var creator = document.getElementById('fcreator').value;
          	//get flag
            var expstatus = $('input[name=repflag]:checked').val();
            //get description
            var descr = document.getElementById('input-descr').value;  
            //get alert email
            var email = document.getElementById('email-to').value;
            export_report_flag(filename, creator, expstatus, descr, email)
        }
    });

    $('#modal-form').validate({

      highlight: function(element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
      },
      success: function(element) {
        $(element).closest('.form-group').removeClass('has-error');
      },
    }); 
});

$(document).ready(function() {
		
	// initialize the validator
	$('#signupform').validate({
		rules : {
			password : {
				pwcheck : true,
				minlength : 8
			},
			password_confirm : {
				equalTo : "#password"
			}
		},
		messages : {
			password: {
				pwcheck: "An upper case letter and a digit required",
				minlength: "At least 8 characters required"
			},
		},
		highlight: function(element) {
			$(element).closest('.form-group').removeClass('has-success').addClass('has-error');
		},
		success: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
	});
	
	$.validator.addMethod("pwcheck", function(value) {
		return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) // consists of only these
		&& /[A-Z]/.test(value) // has a lowercase letter
		&& /\d/.test(value) // has a digit
	});
	
});