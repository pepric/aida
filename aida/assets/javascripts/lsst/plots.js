function run_plot_offline(e){
	var ny = parseInt($("#n_ypar").val());
	var system = document.getElementById("hktm_source").value;
	var plot = $("#plot_type").val()

	var username = document.getElementById("session-user").innerHTML    
	var stats = $("#stats_enable").val();
  	var stats_list = get_stats_list()
	//prepare_data
	out = prepare_data(ny, plot);
	params = out[0];
	ny = out[2]
	params.isonline = 0
	params.plot_type = plot
	params.stats = stats
	params.stats_list = JSON.stringify(stats_list)
	params.url = window.location.host
	labels = out[1];
	params.labels = labels
  
	if(plot == "histogram"){    
		var binsize = document.getElementById('binsize').value;
		var bintype = $('input[name=bintype]:checked').val();
      	params.binsize = binsize
      	params.bintype = bintype
    }  
  
	pyscript = "scripts/get_data.py"; 
  	// perform offline analysis
	$.ajax({
		type: "POST",
		url: pyscript,
		data: params ,
		dataType: "html",
		cache: false,
		async:'asynchronous'
	});
	e.preventDefault();
}

function run_py(e) {
	var ny = parseInt($("#n_ypar").val());
	var system = document.getElementById("hktm_source").value;
	var plot = $("#plot_type").val()	
	var stats = $("#stats_enable").val();
	var usecase = $("#usecase").val();
	
	out = prepare_data(ny, plot);

	params = out[0];
	ny = out[2];
	params.isonline = 1
	var labels = out[1];
	params.labels = labels;
	pyscript = "scripts/get_data.py";

	$.ajax({
		type: "POST",
		url: pyscript,
		data: params ,
		dataType: "html",
		cache: false,
		async:'asynchronous',
		success: function(returndata){
			var results = JSON.parse(returndata)
			console.log(plot)
			console.log(results)
			document.getElementById("modal-labels").value = labels
			document.getElementById("modal-tstart").value = params['tstart']     
			document.getElementById("modal-tstop").value = params['tend']
			document.getElementById("modal-pid").value = params['pid']
			//operation name
			var op2hist
			//parameters
			var l2hist = labels.slice(1).join(",")
		
			if(plot != "pre-generated"){
				var pres = render_plot(results, plot, ny, labels, usecase)
				var op = pres[0]
				var hasdata = pres[1]
				op2hist = op
				//console.log(hasdata)
				if(results['errstatus'] == 0){
					if(results['datastatus'] == 0 && hasdata > 0){
						stat_results=calculate_stats(results, ny, plot, stats, labels)
						render_files_tbl(results, ny, labels, plot)
						$('#plot_files').css('display', 'none');
					}
					
					/*update history*/
					out_hist = {
						"source" : params['source'],
						"dates range" : "["+params['tstart']+", "+params['tend']+"]"
					}

					var checked_label = $('input[name="bintype"]:radio:checked').next().text()
					var st2hist
					if(stats=="global"){
						st2hist = "Mean,Standard_Deviation,Median,Min,Max,RMS,Variance,Kurtosis,Skewness,MAD,NMAD"
					}
					else{
						st2hist = document.getElementById('stats_list').value.slice(0, -1)
					}
					config_hist = {
						"usecase" : usecase.toUpperCase(),
						"parameters" : l2hist
					}
					if(labels[0] != "None"){
						config_hist.X = labels[0]
					}
					if(checked_label != ""){
						config_hist[checked_label] = document.getElementById('binsize').value
					}						
					config_hist.stats = st2hist
				}
				if(plot == "histogram"){
					results.bins=[document.getElementById('binsize').value, $('input[name=bintype]:checked').val()]
				}                
				document.getElementById("plotdata").innerHTML = JSON.stringify(results)              
			}
			else{
				var operation = params["ytbl0"]
				var pres = render_pregenerated(results, operation, labels[1])
				var op = pres[0]
				var hasdata = pres[1]
				op2hist = "Pre-generated " + op
				if(results['errstatus'] == 0){
					/*update history*/
					out_hist = {
						"source" : params['source'],
						"product ID" : params['pid']
					}
					config_hist = {
						"parameters" : l2hist
					}
				}
				document.getElementById("plotdata").innerHTML = JSON.stringify(results)
				document.getElementById("op").innerHTML = op
			}
			//update history
			if(results['errstatus'] == 0){
				$.ajax({
					type: "POST",
					url: "functions.php",
					data: {
						action: "update_history",
						username : document.getElementById("session-user").innerHTML,
						operation : op2hist,
						infile :	"NA",
						out	: JSON.stringify(out_hist),
						config : JSON.stringify(config_hist)
						},
					error : function (obj, textstatus) {
						alert("Impossible to store the operation in History")
					}
				})                    
			}
		},
		complete:function(data){
			// Hide loader image container
			$("#loader").hide();
		}
	});
	e.preventDefault();	
};	

function run_upload_py(e){
  	$("#loader").show();
  	//number of y parameters
	var ny = parseInt($("#n_ypar").val());
  	//plot type
	var plot = $("#op").val()
    //kind of stats
	var stats = $("#stats_enable").val();
  	//user
	var user = document.getElementById("session-user").innerHTML
    //file format
    var fmt = document.getElementById("fmt_field").value
    if(fmt==""){
		fmt = document.getElementById("filefmt").value
    }
	//filename
	var filename = document.getElementById("upfile-preview").innerHTML    
    //get cols names
    labels = []
    //x
    if($("#params").length > 0){
    	labels = [document.getElementById("x-params").value]
    }
  	else{
    	labels = ["None"]
    }
    //y
	for (var i=0; i<ny; i++){
		var curr = document.getElementById("y"+i+"-params").value
        labels.push(curr)
    }
	//get header check  
    var csv_checked = $('input[name="csvheader"]')
   	if(csv_checked.prop('checked') == true){
       	var header = 1
    }
  	else{
       	var header = 0       
    }
	var op = "Statistical Analysis"  
	$.ajax({
		type: "POST",
		url: "scripts/uploaded_data.py",
		data: {
			filename : filename,
          	fmt	:	fmt,
          	user : user,
          	cols : labels,
          	plot : plot,
          	header : header,
          	action : "get_data"
        },
		dataType: "html",
		cache: false,

		success: function(returndata){
			var results = JSON.parse(returndata)
			if(plot != "stats"){

          		var pres = render_plot(results, plot, ny, labels)
                op = pres[0]
                var hasdata = pres[1]                
              	$('#plot_tab').addClass('active')
              	//$('#plot_tab').css('display','block')
              	$('#plot_stats').removeClass('active')
              	$('#tab-stats1').removeClass('active')
            }
          	else{
            	$("#plot_tab").removeClass('active');
              	$('#tab1').css('display', 'none')
              	document.getElementById('stats_tab').setAttribute('onclick','')
              	$('#tab_stats1').addClass('active')
              	console.log(results)
              	var hasdata = 0              
              	for(var yid=0; yid<ny; yid++){
                    arr = results['y'+yid]
                  	for(var idx=0; idx<arr.length; idx++){
                        if(arr[idx] != "-999"){
                            hasdata = 1
                            break;
                        }
                    }
					if(hasdata > 0){break;}
                }
            }
          	if(hasdata > 0){
				stat_results=calculate_stats(results, ny, plot, stats, labels, store=0)
				render_files_tbl(results, ny, labels, plot)
            }
          	else
            {
              	alert("No data to plot! Data are NULL or STRINGS.");
            	$('#plot_container').css('display', 'none');
            }
            $('#plot_files').css('display', 'none');            
            
          	//additional data to store plot
            if(plot == "histogram"){
              results.bins=[document.getElementById('binsize').value, $('input[name=bintype]:checked').val()]
            }                
            document.getElementById("plotdata").innerHTML = JSON.stringify(results)
          	$('#download-btn').css('display','none')
	        /*update history*/
 	        out_hist = {
				"filename" : filename
            }
			//parameters
			var l2hist = labels.slice(1).join(",")	
			var checked_label = $('input[name="bintype"]:radio:checked').next().text()
			var st2hist
			if(stats=="global"){
				st2hist = "Mean,Standard_Deviation,Median,Min,Max,RMS,Variance,Kurtosis,Skewness,MAD,NMAD"
			}
			else{
				st2hist = document.getElementById('stats_list').value.slice(0, -1)
			}
			config_hist = {
				"parameters" : l2hist
			}
			if(labels[0] != "None"){
				config_hist.X = labels[0]
			}
			if(checked_label != ""){
				config_hist[checked_label] = document.getElementById('binsize').value
			}						
			config_hist.stats = st2hist			
			$.ajax({
				type: "POST",
				url: "functions.php",
				data: {
					action: "update_history",
					username : document.getElementById("session-user").innerHTML,
					operation : op + " on local data",
					infile :	"NA",
					out	: JSON.stringify(out_hist),
					config : JSON.stringify(config_hist)
				},
				error : function (obj, textstatus) {
					alert("Impossible to store the operation in History")
				}
			})
        },
		complete:function(data){
			// Hide loader image container
			hide_pdf();
			hide_csv();        
			$("#loader").hide();
		}
    });
	e.preventDefault();	  
}

function set_special_param(divname){
    var div = document.getElementById(divname)
    var val = "None"
    if(div != null){
        val = div.value
        if(val == ""){val = "None"}
    }    
    return val
}

function set_coeffs(coeff){
	var first_coeff
	var coeff_arr = []
	var isnumeric = !isNaN(coeff) && !isNaN(parseInt(coeff))
	if(isnumeric){
		split_coeff = false
	}
	else{
		split_coeff = true
	}
	//create list of coeff
	if(split_coeff){
		var comma_coeff = coeff.split(",")
		comma_coeff.forEach(function(item){
			var split_item = item.split("-")
			if(split_item.length==2){
				for (var i = parseInt(split_item[0]); i <= parseInt(split_item[1]); i++) {
					if(!coeff_arr.includes(i)){
						coeff_arr.push(i);
					}
				}
			}
			else{
				if(!coeff_arr.includes(parseInt(item))){				
					coeff_arr.push(parseInt(item))
				}
			}
		})
		first_coeff = coeff_arr[0]
	}
	else{
		first_coeff = coeff
	}	
	return [first_coeff, coeff_arr.slice(1)]
}

function set_1st_coeff(c){
	first_coeff = "None"
	if(!isNaN(c)){
		first_coeff = c
	}	
	return first_coeff
}

function prepare_data(ny,plot){
	var source_settings ={
		"NISP" : {"nrows" : 4, "ncols" : 4},
		"NIR" : {"nrows" : 4, "ncols" : 4},
		"SIR" : {"nrows" : 4, "ncols" : 4},
		"VIS" : {"nrows" : 6, "ncols" : 6}
	}
	var adu_flag, alt_tbl_div,  coeff_arr
	var first_coeff = "None"
	var y0sys = $("#y0-sys").val();

	//extra parameters  
  	var extra={}
    $.each($('input', '#y0_extra_filters'),function(){
        extra[$(this).attr('id')] = $(this).val();
    });
    $.each($('input', '#x_extra_filters'),function(){
        extra[$(this).attr('id')] = $(this).val();
    });
    $.each($('textarea', '#y0_extra_filters'),function(){
        extra[$(this).attr('id')] = $(this).val();
    });
    $.each($('textarea', '#x_extra_filters'),function(){
        extra[$(this).attr('id')] = $(this).val();
    });  
	// parameter type (current/statistics/voltage etc), if present
	alt_tbl = set_alt_tbl("y0")
  
	//checked box ADU/CALIBRATED, if present 
	adu_flag = set_adu("y0")
	var source = $("#hktm_source").val()
    var usecase = $("#usecase").val()
	var params = {
		'plot_type' : plot,
		'source': $("#hktm_source").val(),
		'ysys0' : y0sys,
		'ypar0' : $("#y0-params").val(),
		'tstart' : $("#tstart").val(),
		'tend' : $("#tend").val(),
		'user' : document.getElementById("session-user").innerHTML,
		'usecase' : $("#usecase").val(),
		'yic0' : $("#y0-ic").val(),
		'ytbl0' : alt_tbl,
		'yadu0' : adu_flag,
		'pid' : $("#pid").val(),
	}
	params.yval0 = $("#y0-values").val();
	console.log(params)

	var toduplicate = {}
	var det = $("#det-type").val().split(",");
	var ydetector = null
	var det_type_arr = "None"
	params.yrow0 = "None";
	params.ycol0 = "None";
	var dupli_row = false
	var dupli_col = false	
	if(det[1]!="None" && det[1]!=null){
		var yrow = $("#y0-det-row").val()
		var ycol = $("#y0-det-col").val();
		if(yrow != null){
			det_type_arr = det; 
			if(yrow == "all"){
				yrow = 1
				dupli_row = true
			}
			params.yrow0 = yrow;
			
			if(ycol == "all"){
				ycol = 1
				dupli_col = true
			}
			params.ycol0 = ycol;
			ydetector = collect_detectors(det[1], yrow, ycol, "#y0-quadrant")
			params.ydet0 = ydetector;
		}
	}
	if(dupli_row || dupli_col){
		toduplicate.y0 = [dupli_row,dupli_col]
	}
    var order = set_special_param("y0-order")
    var coeff = set_special_param("y0-coeff")
    var group = "None"
    if(source == "SIR"){
		group = set_group(plot,0)
    }
    params.yorder0 = order	
	var coeff2dupli = {}
	coeff_res = set_coeffs(coeff)
	first_coeff = set_1st_coeff(coeff_res[0])
	coeff_arr = coeff_res[1]
	if(!coeff_arr==[]){
		coeff2dupli.y0 = coeff_arr
	}
	params.ycoeff0 = first_coeff
	y0label = build_label("y0",y0sys, params.ypar0, adu_flag, source, usecase, params.yic0, params.yval0, ydetector, order, first_coeff, group)
	// Create x label and add detector info (if any) if scatter plot 
	if (plot == "scatter"){
		var xsys = $("#x-sys").val();
		params.xsys = xsys;
		params.xpar = $("#x-params").val();
		params.xval = $("#x-values").val();
      
		alt_tbl = set_alt_tbl("x")
		params.xtbl = alt_tbl;  

		//checked box ADU/CALIBRATED, if present
		adu_flag = set_adu("x")
		params.xadu = adu_flag     
      
		var xdetector = null
		var xic = $("#x-ic").val();
		params.xic = xic;
		params.xcol = "None";
		params.xrow = "None";
		params.xdet = "None";		
 		if(det[0]!="None" && det[0]!=null){
			var xrow = $("#x-det-row").val();
			var xcol = $("#x-det-col").val();
			if(xrow!=null){
				xdetector = collect_detectors(det[0], xrow, xcol, "#x-quadrant");
				params.xcol = xcol;
				params.xrow = xrow;
				params.xdet = xdetector;
			}
		}
        var order = set_special_param("x-order")
        var coeff = set_special_param("x-coeff")
        var group = "None"
        if(source == "SIR"){
			group = set_group(plot,"",true)
        }       
		xlabel = build_label("x", xsys, params.xpar, adu_flag, source, usecase, params.xic, params.xval, xdetector, order,coeff,group)      
	}
	else{
		xlabel = "None"
	}	

	labels = [xlabel, y0label];

	// COLLECT ALL Y PARAMS
	var additional_y_sys = []
	var additional_y_par = [];
	var additional_y_val = [];
	var additional_y_row = [];
	var additional_y_col = [];
	var additional_y_det = [];	
	var additional_y_ic = [];	
	var additional_y_tbl = [];
	var additional_y_adu = []
	var additional_y_order = []
	var additional_y_coeff = []
	for (i=1; i<ny; i++){
		var new_y_sys = $("#y"+i+"-sys").val();
		var new_y_par = $("#y"+i+"-params").val();
		var new_y_ic = $("#y"+i+"-ic").val();
		additional_y_sys.push(new_y_sys);
		additional_y_par.push(new_y_par);
		additional_y_ic.push(new_y_ic);
		var new_y_val = $("#y"+i+"-values").val();  
		additional_y_val.push(new_y_val);
	  
		alt_tbl = set_alt_tbl("y"+i)         
		additional_y_tbl.push(alt_tbl);          

		//checked box ADU/CALIBRATED, if present
		adu_flag = set_adu("y"+i)
		additional_y_adu.push(adu_flag)
		
		var new_ydetector = "None"
		var new_y_row = "None";
		var new_y_col = "None";		
		//for forms with detectors

		dupli_row = false
		dupli_col = false
		if(det[i+1]!="None" && det[i+1]!=null){
			new_y_row = $("#y"+i+"-det-row").val();
			new_y_col = $("#y"+i+"-det-col").val();
			if(new_y_row!=null){
				if(new_y_row == "all"){
					new_y_row = 1
					dupli_row = true
				}
				if(new_y_col == "all"){
					new_y_col = 1
					dupli_col = true
				}
				new_ydetector = collect_detectors(det[i+1], new_y_row, new_y_col, "#y"+i+"-quadrant");
			}
		}
		additional_y_row.push(new_y_row);
		additional_y_col.push(new_y_col);
		additional_y_det.push(new_ydetector);				
		if(dupli_row || dupli_col){
			toduplicate["y"+i] = [dupli_row,dupli_col]
		}
		var order = set_special_param("y"+i+"-order")
		var coeff = set_special_param("y"+i+"-coeff")
		coeff_res = set_coeffs(coeff)
		first_coeff = set_1st_coeff(coeff_res[0])
		coeff_arr = coeff_res[1]
		if(!coeff_arr==[]){
			coeff2dupli["y"+i] = coeff_arr
		}            
		additional_y_order.push(order);
		additional_y_coeff.push(first_coeff);
		var group = "None"
		if(source == "SIR"){
			group = set_group(plot,i)
		}

		l = build_label("y"+i, new_y_sys, new_y_par, adu_flag, source, usecase, new_y_ic, new_y_val, new_ydetector, order, first_coeff,group)
		labels.push(l);
		// get additional filters
		 $.each($('input', '#y'+i+'_extra_filters'),function(){
			extra[$(this).attr('id')] = $(this).val();
		 });
		 $.each($('textarea', '#y'+i+'_extra_filters'),function(){
			extra[$(this).attr('id')] = $(this).val();
		 });          
	}

	//duplicate params in case of ALL det row/col
	var ndupli = Object.keys(toduplicate).length
	//var idx0 = ny-1
	for(var i=0; i<ndupli;i++){
		var det_list=[]
		var p2dup = Object.keys(toduplicate)[i]
		var dupl_row = toduplicate[p2dup][0]
		var dupl_col = toduplicate[p2dup][1]
		var maxrow,maxcol
		if(source!="QLA"){
			maxrow = source_settings[source]["nrows"]
			maxcol = source_settings[source]["ncols"]
		}
		else{
			var curr_sys = $("#"+p2dup+"-sys").val();
			var curr_sub = curr_sys.split("-")[0]
			maxrow = source_settings[curr_sub]["nrows"]
			maxcol = source_settings[curr_sub]["ncols"]				
		}
		
		if(dupl_row){
			var r_arr = []
			for(var n=1;n<maxrow+1;n++){r_arr.push(n)}
		}
		else{
			var r_arr = [parseInt($("#"+p2dup+"-det-row").val())]
		}
		if(dupl_col){
			var c_arr = []
			for(var n=1;n<maxcol+1;n++){c_arr.push(n)}
		}
		else{
			var c_arr = [parseInt($("#"+p2dup+"-det-col").val())]
		}
		r_arr.forEach(function(a1){
		  c_arr.forEach(function(a2){
			det_list.push(a1 +"-"+ a2);
		  });
		});			
		
		// get data to duplicate from form
		for(var d=0;d<det_list.length;d++){
			var curr = det_list[d].split("-")
			var idx = parseInt(p2dup.replace("y",""))+1
			var curr_dettype = det[idx]
			var curr_det = collect_detectors(curr_dettype, curr[0], curr[1], "#"+p2dup+"-quadrant");
			var curr_sys = $("#"+p2dup+"-sys").val()
			var curr_par = $("#"+p2dup+"-params").val()
			var curr_adu = set_adu(p2dup)
			var curr_ic = $("#"+p2dup+"-ic").val()
			var curr_val = $("#"+p2dup+"-values").val()
			var curr_order = set_special_param(p2dup+"-order")
			var curr_coeff = set_special_param(p2dup+"-coeff")	

			group = "None"
			if(source == "SIR"){
				group = set_group(plot,idx-1)
			}					
			//build label
			l = build_label(p2dup, curr_sys, curr_par, curr_adu, source, usecase, curr_ic, curr_val, curr_det, curr_order, curr_coeff,group)

			if(!labels.slice(1).includes(l)){
				additional_y_sys.push(curr_sys)
				additional_y_par.push(curr_par)
				additional_y_ic.push(curr_ic)
				additional_y_tbl.push(set_alt_tbl(p2dup))
				additional_y_adu.push(curr_adu)
				additional_y_val.push(curr_val);
				additional_y_order.push(curr_order);
				additional_y_coeff.push(curr_coeff);					
				additional_y_row.push(curr[0])
				additional_y_col.push(curr[1])					
				additional_y_det.push(curr_det)	

				//duplicate extra filters		{y<i>_<extra_name>:<value>}
				 $.each($('input', '#'+p2dup+'_extra_filters'),function(){
					div_id = $(this).attr('id').split('_')[1]
					extra['y'+ny+'_'+div_id] = $(this).val();
				 });
				 $.each($('textarea', '#'+p2dup+'_extra_filters'),function(){
					div_id = $(this).attr('id').split('_')[1]
					extra['y'+ny+'_'+div_id] = $(this).val();
				 });
				//duplicate det_type
				var curr_dt = det_type_arr[idx]
				det_type_arr.push(curr_dt)
				labels.push(l);
				ny = ny +1	
			}
		}
	}
		
	//duplicate params in case of list of coeff (not concurrent with det duplication)
	var cdupli = Object.keys(coeff2dupli)

	for(var i=0; i<cdupli.length;i++){
		p2dup = cdupli[i]
		var coeffs = coeff2dupli[p2dup]
		var idx = parseInt(p2dup.replace("y",""))+1
		//TODO
		var curr_sys = $("#"+p2dup+"-sys").val()
		var curr_par = $("#"+p2dup+"-params").val()
		var curr_ic = $("#"+p2dup+"-ic").val()
		var curr_val = $("#"+p2dup+"-values").val()
		var curr_order = set_special_param(p2dup+"-order")
		var curr_adu = set_adu(p2dup)
		group = "None"
		if(source == "SIR"){
			group = set_group(plot,idx-1)
			console.log(group)
		}			
		coeffs.forEach(function(c){
			//build label
			l = build_label(p2dup, curr_sys, curr_par, "False", source, usecase, curr_ic, curr_val, null, curr_order, c,group)
			if(!labels.slice(1).includes(l)){
				additional_y_sys.push(curr_sys)
				additional_y_par.push(curr_par)
				additional_y_ic.push(curr_ic)
				additional_y_tbl.push(set_alt_tbl(p2dup))
				additional_y_adu.push("False")
				additional_y_val.push(curr_val);
				additional_y_order.push(curr_order);
				additional_y_coeff.push(curr_coeff);					
				labels.push(l);
				ny++
			}			
		});
	}
	
	params.ny = ny
	params.det_type = det_type_arr
	// add to data array
	params.additional_y_sys = additional_y_sys;
	params.additional_y_par = additional_y_par;
	params.additional_y_ic = additional_y_ic;
	params.additional_y_tbl = additional_y_tbl;
	params.additional_y_adu = additional_y_adu;
	params.additional_y_val = additional_y_val;
	params.additional_y_row = additional_y_row;
	params.additional_y_col = additional_y_col;
	params.additional_y_det = additional_y_det;	
	params.additional_y_order = additional_y_order;	
	params.additional_y_coeff = additional_y_coeff;	            
	params.extra = JSON.stringify(extra)

	return [params,labels,ny]
}

function set_alt_tbl(p){
	var alt_tbl_div = document.getElementById(p+"-partype");
	if(alt_tbl_div == null){
      var alt_tbl = ""
    }
  	else{
      var alt_tbl = alt_tbl_div.value;	  
    }	
	return alt_tbl
}

function set_adu(p){
	var adu_flag
	adu_checked = $('input[name="'+p+'-adu_cal"]')         
	if(adu_checked.length > 0){
		if(adu_checked.prop('checked') == true){
			adu_flag = "True"
		}
		else{
			adu_flag = "False"        
		}
	}
	else{
		adu_flag = "None"
	 }
	return adu_flag
}


function set_group(plot, i, isX=false){
	var group = "None"
	var div = "y"+i+"-partype"
	if(isX){
		div = "x-partype"
	}
	if(plot!="pre-generated"){				
		group = set_special_param(div)
		if(group == "parameters"){
			group = "None"
		}                
	}
	return group
}

function set_labels(adu, par, source, origin){
  return $.ajax({
    url: 'scripts/cs_interface.py',
    data: {
      action: "set_labels",
      adu	: adu,
      par	: par,
      s		: source,
      o		: origin
    }
  });
}

function build_label(pvar, sys, par, adu, source, origin, ic=null, val=null, det=null, order=null, coeff=null, group=null){
  	var label = ""
    var syslabel = sys+"."
	if(source=="VIS" && origin=="science"){
    	syslabel = ""
    }    
	if(det!=null && det!="None"){
		label = syslabel+det+"."+par;
	}
	else{
		label = syslabel+par;
	}
	if(ic!=null){label = ic+"."+label}	
	if(val!=null){label = label+"."+val}
	if(order!="None"){label = label+".order"+order}
	if(coeff!="None"){label = label+".coeff"+coeff}
	if(group!="None"){label = label+"["+group.toUpperCase()+"]"}

	var aduparent = $("#"+pvar+"-adu_check").parent().css('display');
	if(aduparent != "none"){
      switch(adu) {
		  case "True":
			  var units = $("#"+pvar+"-adu_check").find("#units").html()
			  if(units != null && units != ""){
				  var utxt = units
			  }
			  else{
				  var utxt = "no units"
			  }
			  label = label+" ("+utxt+")";

			  break;
		  case "False":
			  label = label+" (ADU)";
			  break;
		  case "None":
			  break;      
      }
    }
	return label
}

function collect_detectors(det, row, col, id){
	if (det=="DET"){
			var detector = det+"_"+row+col;
	}
	else{
		var quad = $(id).val();
		var detector = det+'_'+row+'-'+col;

		if (quad !== "full"){
			detector = detector + '["'+quad+'"]';
		}
	}
	return detector
}

function display_plot(name){
	document.getElementById('plot_container').style='display:block;';
	var plotdiv = document.getElementById('tab1')
	plotdiv.setAttribute("class", "active");
	var a = plotdiv.getElementsByTagName("a")[0];
	a.innerHTML = name;
	plotdiv.style="display : inline-block";
	document.getElementById('chartContainer').style='height: 570px; /*width: 100%;*/ display:block;';
	var plottab = document.getElementById('plot_tab')
	//plottab.style='display:block;';
	plottab.setAttribute("class", "tab-pane active")
}

function get_stats_list(){
	var stats_data = {}
	// list of selected stats
	var stats_list = document.getElementById("stats_list").value;
	var list_arr = stats_list.split(",")
	// for each stat
	for (var i=0; i<list_arr.length-1; i++){
		// values from form related to the current stat
		var curr_name = list_arr[i];
		var curr_func = document.getElementById(curr_name).value;
		var divmore = document.getElementById("more-"+curr_name);
		var addmore = parseInt(divmore.getAttribute("addmore"));
		// get number of config rows if addmore = 1
 		if(addmore == 1){
			var nexp = parseInt(document.getElementById("par-hidden-"+curr_name).value);
		} 
		else {
			var nexp = 0;
		}
		// json containing general data about stat parameters
		var valdiv = divmore.value;
		// valdiv = "" implies no additional configuration => store stat name and func
 		if (valdiv==""){
			stats_data[curr_name] = curr_func
		}
		else{
			// params is a json containing all the additional configuration parameters
			var params = {}
			var jsonval = JSON.parse(valdiv);
			// names of config parameters
			var keys = Object.keys(jsonval);
			var npar = keys.length;
			// for each configuration row
			for(var k = 0; k<nexp+1; k++){
				// for each parameter of each row
				for(var j=0; j<npar; j++){
					// general name of parameter from json
					var curr_id = jsonval[keys[j]]['id'];
					// if it is the first row, related divs and params do not have the suffix _0
					var index = "";
					if(k > 0){
						index = "_"+k;
					}
					// get value from form
					var expdiv = document.getElementById("par-others-"+curr_name+"_"+k);
					var expval = $(expdiv).find('#'+curr_id+index).val();						
					// add key, value to params
					params[curr_id+index] = expval;
				}
			}
			// append to output json name of function, list of configuraion parameters and number of parameters for each row
			stats_data [curr_name] = {
				"func" : curr_func,
				"params" : params,
				"npar" : npar
			}
		}
	}

  	return stats_data
}

function calculate_stats(pydata, ny, plot, stats, labels, store=1){
	stats_data = get_stats_list() 
	// input data for Python/CGI
	datain = {
			"inputdata"	:	JSON.stringify(pydata),
			"stats_config" : JSON.stringify(stats_data),
			"ny"		: 	ny,
			"plot_type"	:	plot,
			"stats_type":	stats
			}
	$.when(
		$.ajax({
			type: "POST",
			url: "scripts/calculate_statistics.py",
			data: datain, 
			dataType: "html",
			cache: false,
			async:'asynchronous',
		})
		.done(function(data){
			//store stats results in a hidden div
			var div = document.getElementById('stats_results');
			div.innerHTML = data;
			//visualize stats as tables
			render_stats(data, ny, labels, plot, stats, store)
		})
	) 
}

function download_image(filename, source, user){
	
	var htmlpage = window.location.href.split("/").pop()
	var fileurl = window.location.href.replace(htmlpage,"")	
	if(filename.includes("/")){
		fileurl += filename.replace("../","")
		filename = filename.split("/").pop()
	}
	else{
		fileurl += "users/"+user+"/tmp/"+source.toLowerCase()+"/"+filename
	}	
	//check if file exists on AIDA
	$.ajax({
		url:fileurl,
		type:'HEAD',
		error: function()
		{
			$.ajax({
				type: "POST",
				url: 'scripts/cs_interface.py',
				data: {
				  "action": "direct_download",
				  "source"	: source,
				  "filename" : filename,
				  "origin" : "image"
				},
				success : function(results){
					res = results['result']
					switch(res){
					    case 1:
							alert("ERROR! Impossible to download requested file");
							break;
						case 2:
							alert("ERROR! Feature not available for current repository/operating mode");
							break;
						default:
							var link = document.createElement("a");
							link.target = "_blank";
							link.href = res+filename;
							document.body.appendChild(link);
							link.click();
							document.body.removeChild(link);
							delete link;							
							break;      
					}
				}
			});
		},
		success: function()
		{
			downloadURI(fileurl, filename)
		},
	});	
}

function init_result_div(maindiv){
	var parent = document.getElementById(maindiv);
	parent.style="display : flex; flex-wrap : wrap";
	parent.innerHTML = "";	
	// create outer div
	var node = document.createElement("div");
	node.setAttribute("class", "col-md-12");
	node.setAttribute("id", "files_div");
	node.setAttribute("style", "margin: 20px 0px");
	parent.appendChild(node);	
	
	return node
}

function render_img_files_tbl(results, labels, plot, user, flist, source){
	var node = init_result_div("plot_files")
	// create table
	var tbl = document.createElement("table");
	tbl.style.width = '100%';
	tbl.setAttribute('border', '1');
	tbl.setAttribute("id", "files_tbl");
	tbl.setAttribute("class", "table table-bordered table-striped mb-none");
	var thead = document.createElement('thead');
	// table title
	var cols = ["Image FITS File",""]
	var tr = document.createElement('tr');	
	cols.forEach(function(col) {
		var th = document.createElement('th');
		th.style.textAlign = "center";
		th.style.fontWeight = "bold";
		th.setAttribute("scope","col");
		th.innerHTML = col;
		tr.appendChild(th)
	});
	thead.appendChild(tr);		
	tbl.appendChild(thead);

	var tbdy = document.createElement('tbody');
 	for(var i = 0; i < flist.length; i++){
		//new row	
	    var tr = document.createElement('tr');
		var fullname = flist[i]
		const filename = fullname.split("/").pop()
		//filename col
		var td = document.createElement('td');
		td.style.textAlign = "center";	
		td.innerHTML = filename
		tr.appendChild(td)		
		//action col
		var td = document.createElement('td');
		td.style.textAlign = "center";
		var view_onclick = "to_image_explorer(\""+filename+"\", \""+source+"\", \"image_analysis\", \""+user+"\")"
		var view_a = '<img title="Impossible to open with Image Explorer. TODO" class="download-icon" style="opacity : 0.5" width="30" src="assets/images/view_img_48.png">'
		var download_click = "download_image(\""+fullname+"\", \""+source+"\", \""+user+"\")"
		var download_a = '<a href="#" onclick=\''+download_click+'\'><img src="assets/images/down_min.png" width="30" title="View image"/></a>'
		td.innerHTML = view_a+download_a
		tr.appendChild(td)  		
        //close row
        tbdy.appendChild(tr);  	
	} 
	tbl.appendChild(tbdy);	
	node.appendChild(tbl)
	$('#files_tbl').DataTable({
		"dom" : "row <'col-sm-2'l><'col-sm-4'B><'col-sm-6'f>"+"rtip",
		"language": {"emptyTable": "No files", "buttons":{"csv" : "Export to CSV"}},
		//"scrollX": true,
		"order": [[ 0, 'desc' ]],
		"bPaginate":true,
		"bProcessing": false,
		"pageLength": 25,
		"buttons" : [
					{ extend: 'csv', className: 'btn btn-primary btn-csv3', title: 'files_list', fieldBoundary: '', exportOptions: { orthogonal: "exportcsv", columns: [0]} },
		],
	});	
}


function render_files_tbl(results, ny, labels, plot){
	var kf = Object.keys(results)
	if(kf.includes("files")){
		console.log(results["files"])
		var cols = Object.keys(results["files"])
		var parent = document.getElementById("plot_files");                         
		parent.style="display : flex; flex-wrap : wrap";
		parent.innerHTML = "";
      	// create outer div
		var node = document.createElement("div");
		node.setAttribute("class", "col-md-12");
		node.setAttribute("id", "files_div");
		node.setAttribute("style", "margin: 20px 0px");
		parent.appendChild(node);
		// create table
		var tbl = document.createElement("table");
		tbl.style.width = '100%';
		tbl.setAttribute('border', '1');
      	tbl.setAttribute("id", "files_tbl");
      	tbl.setAttribute("class", "table table-bordered table-striped mb-none");
		var thead = document.createElement('thead');
		// table title
		var tr = document.createElement('tr');
		for(var i=0; i<cols.length; i++){
          	if(results["files"][cols[i]].length >0){ 
				var th = document.createElement('th');
				th.style.textAlign = "center";
				th.style.fontWeight = "bold";
    	  		th.setAttribute("scope","col");
				th.innerHTML = cols[i];
            }
          	tr.appendChild(th)
        }
		var th = document.createElement('th');
		th.style.textAlign = "center";
		th.style.fontWeight = "bold";
      	th.setAttribute("scope","col");      
		th.innerHTML = "Date";
		tr.appendChild(th)      	
      	for(var i = 0; i < labels.length; i++) {
          	if(labels[i]!="None"){
	          	var th = document.createElement('th');
				th.style.textAlign = "center";
				th.style.fontWeight = "bold";
      			th.setAttribute("scope","col");              
				th.innerHTML = labels[i];
				tr.appendChild(th)
            }
          	thead.appendChild(tr);
        }
		thead.appendChild(tr);
		tbl.appendChild(thead);      
      	var tbdy = document.createElement('tbody');      
      	//insert values
		var fnames = results["files"]
        var dates = results["date"]
     	const source = document.getElementById("hktm_source").value
    	const usecase = document.getElementById("usecase").value
    	const username = document.getElementById("session-user").innerHTML        
		for(var i = 0; i < dates.length; i++){
			const curr_d = dates[i]
            //create row
	        var tr = document.createElement('tr');
          		//create cell for each system
				for(var s = 0; s < cols.length; s++){
					const colname = cols[s]                 	 
					const flist = fnames[colname]
					if(flist.length > 0){
                        const f = flist[i]
                        var td = document.createElement('td');
                        td.style.textAlign = "center";
						if(colname != 'HKFitsFile' && colname != 'QLAFile' && colname != 'CSVFile'){
                        	td.innerHTML = "<a href='#' onclick='to_image_explorer(\""+f+"\", \""+source+"\", \""+usecase+"\", \""+username+"\")'>"+f+"</a>"
                        }
                      	else{
                          	const link = "users/"+username+"/tmp/"+source.toLowerCase()+"/"+f
                        	td.innerHTML = "<a href='"+link+"' download>"+f+"</a>"
                        }
                        tr.appendChild(td)                    
                    }
               }
          	//create cell for date
        	var td = document.createElement('td');
         	td.style.textAlign = "center";
        	td.innerHTML = curr_d
        	tr.appendChild(td)              
			//create cells for parameters
          	if(labels[0]!="None"){
	         	var td = document.createElement('td');
				td.style.textAlign = "center";
				td.innerHTML = results["x"][i];
				tr.appendChild(td)
            }           
          
          	for(var j = 0; j < ny; j++) {
         	 	var td = document.createElement('td');
				td.style.textAlign = "center";
              	val = results["y"+j][i]
              	if(val==-999){val = "-"}
				td.innerHTML = val;
				tr.appendChild(td)         
            }
          	//close row
          	tbdy.appendChild(tr);          
        }        
		tbl.appendChild(tbdy);
		node.appendChild(tbl)        
     
      	$('#files_tbl').DataTable({
          	"dom" : "row <'col-sm-2'l><'col-sm-4'B><'col-sm-6'f>"+"rtip",
          	"language": {"emptyTable": "No files", "buttons":{"csv" : "Export to CSV"}},
          	"scrollX": true,
			"order": [[ 0, 'desc' ]],
			"bPaginate":true,
			"bProcessing": false,
			"pageLength": 25,
          	"buttons" : [
              			{ extend: 'csv', className: 'btn btn-primary btn-csv3', title: 'files_list', fieldBoundary: '', exportOptions: { orthogonal: "exportcsv", columns: ':visible'} },
			],
        });
		$('#tab-files1').show()
    }
  	else{
		$('#tab-files1').hide()
    }
}

function render_img_stats(results, labels, plot, flist, store=1){
 	var parent = document.getElementById("plot_stats");
	parent.style="display : flex; flex-wrap : wrap";	
	//render title
	if(plot=="difference"){
		var node = document.createElement("div");
		node.setAttribute("class", "col-md-12");
		node.setAttribute("style", "font-size:15px; font-weight:bold; text-align:center");
		node.innerHTML= flist[0] + " &#8212; " + flist[1]
		parent.appendChild(node)		
	}
	for(var i=0; i<labels.length;i++){
		l = labels[i].trim()
		data = results[l]
		//console.log(l,data)
		create_stats_table(data, l, parent, "y"+i+"_stats");
	}

	// Show Stats panel
	document.getElementById('plot_container').style='display:block;';
	var statstab = document.getElementById('tab-stats1')
	var a = statstab.getElementsByTagName("a")[0];
	statstab.setAttribute("class", "active")
	document.getElementById('plot_stats').setAttribute("class", "tab-pane active")
 	a.innerHTML = "Image Statistics";;
	if(store==1){  
      // create download stats button
      var divb = document.createElement("div");
      divb.setAttribute("class", "col-md-12");
      divb.setAttribute("style", "margin: 20px 0px; text-align:right");
      divb.setAttribute("id", "download-btn");
      parent.appendChild(divb)

      var b = document.createElement("button");
      b.setAttribute("class", "btn btn-primary");
      b.setAttribute("id", "download_stats");
      b.setAttribute("onclick", "select_download_dir('store_pdf', 'Image Analysis', '"+labels+"')");
      b.innerHTML = "Save Statistics";
      divb.appendChild(b)
    }	

	$("#loader").hide();
}

function render_stats(pydata, ny, labels, plot, stats, store){
	var results = JSON.parse(pydata)
	var parent = document.getElementById("plot_stats");
	parent.style="display : flex; flex-wrap : wrap";
	parent.innerHTML = "";
	ks = Object.keys(results)
	
	// create stats div
	if(plot == "scatter"){
		var node = document.createElement("div");
		node.setAttribute("class", "col-md-12");
		node.setAttribute("style", "font-size:20px; font-weight:bold");
		node.innerHTML="DATASET 1"
		parent.appendChild(node)
	}
	
	// x stats if present
	if (results.x_stats != "None"){
		xname = labels[0];
		xdata = results.x_stats;
		create_stats_table(xdata, xname, parent, "x_stats");
	}
	
	// y0 stats
	y0name = labels[1]
	y0data = results.y0_stats;
	create_stats_table(y0data, y0name, parent, "y0_stats");
	
	// additional y stats
	if (ny>1){
		for (i=1; i<ny; i++){
			if(plot == "scatter"){
				var node = document.createElement("div");
				node.setAttribute("class", "col-md-12");
				node.setAttribute("style", "font-size:20px; font-weight:bold");
				var num = i+1
				node.innerHTML="DATASET "+num.toString()
				parent.appendChild(node)
			}
			
			name = labels[i+1]
			data = results[ks[i+1]]
			
			if (plot == "scatter"){
				xname = labels[0];
				xdata = results[ks[i+ny]];
				create_stats_table(xdata, xname, parent, "x_stats"+i);
			}
			create_stats_table(data, name, parent, "y"+i+"_stats");
		}
		
	}
	// Show Stats panel
	document.getElementById('plot_container').style='display:block;';
	var statstab = document.getElementById('tab-stats1')
	var a = statstab.getElementsByTagName("a")[0];
	if (plot=="stats"){
		statstab.setAttribute("class", "active")
		document.getElementById('plot_stats').setAttribute("class", "tab-pane active")
	}
	a.innerHTML = stats.charAt(0).toUpperCase() + stats.slice(1)+" Statistics";;

  
	if(store==1){  
      // create download stats button
      var divb = document.createElement("div");
      divb.setAttribute("class", "col-md-12");
      divb.setAttribute("style", "margin: 20px 0px; text-align:right");
      divb.setAttribute("id", "download-btn");
      parent.appendChild(divb)

      var b = document.createElement("button");
      b.setAttribute("class", "btn btn-primary");
      b.setAttribute("id", "download_stats");
      b.setAttribute("onclick", "select_download_dir('store_pdf', 'Statistics', '"+labels+"')");
      b.innerHTML = "Save Statistics";
      divb.appendChild(b)
    }	
	if(plot!="stats"){
		$('#plot_stats').css('display', 'none');
	}
	var modebar = document.getElementsByClassName("modebar")[0]
	if(typeof modebar != 'undefined'){
		modebar.style='display:block;';
	}
	$("#loader").hide();
}

function create_stats_table(data, name, parent, id){
	
	// create stats div
	var node = document.createElement("div");
	node.setAttribute("class", "col-md-6");
	node.setAttribute("id", id);
	node.setAttribute("style", "margin: 20px 0px");
	parent.appendChild(node);
	
	// create table
	var tbl = document.createElement("table");
	tbl.style.width = '100%';
	tbl.setAttribute('border', '1');
	var tbdy = document.createElement('tbody');
	
	// table title
	var tr = document.createElement('tr');
	var td = document.createElement('td');
	td.style.textAlign = "center";
	td.style.fontWeight = "bold";
	td.setAttribute('colSpan', '2')
	td.innerHTML = name;
	tr.appendChild(td)
	tbdy.appendChild(tr);
	// add stats to table
	var x_keys = Object.keys(data);
	var x_values = Object.values(data);
	var n_stats = x_keys.length;
	for (var i = 0; i < n_stats; i++) {
		var tr = document.createElement('tr');
		for (var j = 0; j < 2; j++) {
			var td = document.createElement('td');
			if (j==0){
				td.style.fontWeight = "bold";
				td.innerHTML = x_keys[i].replace("_", " ");
				}
			else{
				if(x_values[i]!="-"){
					td.style.textAlign = "right";
				}
				else
				{
					td.style.textAlign = "center";
				}
				td.innerHTML = x_values[i];
				}
			tr.appendChild(td)
		}
	tbdy.appendChild(tr);
	}
	tbl.appendChild(tbdy);
	node.appendChild(tbl)
}

var csv = {
	width:875,height:1e3, path:"M0,22.261v467.478h512V22.261H0z M155.826,456.348H33.391v-77.913h122.435V456.348z M155.826,345.043H33.391V267.13	h122.435V345.043z M155.826,233.739H33.391v-77.913h122.435V233.739z M322.783,456.348H189.217v-77.913h133.565V456.348z M322.783,345.043H189.217V267.13h133.565V345.043z M322.783,233.739H189.217v-77.913h133.565V233.739z M478.609,456.348H356.174 v-77.913h122.435V456.348z M478.609,345.043H356.174V267.13h122.435V345.043z M478.609,233.739H356.174v-77.913h122.435V233.739z M478.609,122.435H33.391V55.652h445.217V122.435z", transform:"scale(1.8, 1.9)"
};

var pencil = {
  width:875,
  height:1e3, 
  ascent: 20,
  descent: 0,
  path:"M94.62,2c-1.46-1.36-3.14-2.09-5.02-1.99c-1.88,0-3.56,0.73-4.92,2.2L73.59,13.72l31.07,30.03l11.19-11.72 c1.36-1.36,1.88-3.14,1.88-5.02s-0.73-3.66-2.09-4.92L94.62,2L94.62,2L94.62,2z M41.44,109.58c-4.08,1.36-8.26,2.62-12.35,3.98 c-4.08,1.36-8.16,2.72-12.35,4.08c-9.73,3.14-15.07,4.92-16.22,5.23c-1.15,0.31-0.42-4.18,1.99-13.6l7.74-29.61l0.64-0.66 l30.56,30.56L41.44,109.58L41.44,109.58L41.44,109.58z M22.2,67.25l42.99-44.82l31.07,29.92L52.75,97.8L22.2,67.25L22.2,67.25z", 
  transform:"scale(8, 8)"
}

function trend(results, ny, labels) {
	fname = get_now_string()
	n_exp = "Trend Analysis"
	display_plot(n_exp)
	var dom = document.getElementById('chartContainer');
	ks = Object.keys(results)
	var idx = find_nan(results.date);  
	data = []
  	var hasdata = 0
	for (var i=1; i<ny+1; i++){
		var curr_y = results[ks[i+1]]
		var curr_x = results.date
		var idy =  find_nan(curr_y);
		var indices = idy.concat(idx)
		var final_x = reduce_array(curr_x, indices)
		var final_y = reduce_array(curr_y, indices)
		if(final_y.length > 0){hasdata++}				
		var trace = {
			name : labels[i],
			x: final_x,
			y: final_y,
			mode: 'lines+markers',
			type: 'scattergl',
			line: {shape: 'spline'},
		}
		data.push(trace)
	}

	if(hasdata > 0){  
      var layout = {
          xaxis: {
              tickangle : -45,
			  title : {
				  font : {
						family : "Open Sans",
						size : "12",
						color: "#000000"
				  }
			  }
          },
          yaxis: {
			  title : {
				  font : {
						family : "Open Sans",
						size : "12",
						color: "#000000"
				  }
			  }
          },		  
          showlegend : true,
          legend : {

              x : 0,
              y : 1,
              font: {
                family: 'Open Sans',
                size: 12,
                color: '#000',
              },         
			  bgcolor: '#E2E2E2',
			  bordercolor: '#000000',
			  borderwidth: 0,
          }
      };

      let modeBarButtons = [ 
		  [
			  { 
				  name: 'Download Plot as Image',
				  icon: Plotly.Icons.camera,
				  click: function (gd) {
					Plotly.downloadImage(gd, {
					  width: gd._fullLayout.width,
					  height: gd._fullLayout.height,
					  filename : "trend_"+fname
					})
				  }
			  }
		  ],
		  [
			  { 
				  name: 'Save experiment as PDF',

				  icon: Plotly.Icons.disk,
				  click: function(){
					  select_download_dir("store_pdf", n_exp, labels);
					  //exportPDF(n_exp, labels);
				  }
			  }
		  ], 
		  [
			  { 
				  name: 'Save results as CSV',
				  icon: csv,
				  click: function(){

					  save_csv(labels, results);
					  //exportPDF(n_exp, labels);
				  }
			  }
		  ], 
		  ["zoom2d", "pan2d", "select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",  "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"],
		  [
			  { 
				  name: 'Customize Plot',
				  icon: pencil,
				  click: function(){

					  show_custom_plot();
				  }
			  }
		  ]     
      ];

      Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtons: modeBarButtons, displayModeBar : true});
    }
  
  	return hasdata
}


function preg_histogram(results, data, label){
	let fname = get_now_string()
    var reskeys = Object.keys(data)

	n_exp = "Pre-generated Histogram"	
	var edges = data[reskeys[0]]
	//parse edges as array
	edges = JSON.parse(edges.replaceAll(".,",".0,"));
	
	var counts = data[reskeys[1]]
	//parse counts as array
	counts = JSON.parse(counts)
 
	var m = parseFloat(data[reskeys[2]])
	var std = parseFloat(data[reskeys[3]])
	
	var dom = document.getElementById('chartContainer');	
	var data = []
	
	//create bins
	var x = []
	var intervals = []
	for(var b=0; b<(edges.length-1); b++){
 		var end = ")"
		if(b==edges.length-2){
			end = "]"
		}
		intervals.push("["+edges[b]+", "+edges[b+1]+end)
		x.push(edges[b]+(edges[b+1]-edges[b])/2)
	}	
	//opacity
	var opac = 1.0
	var trace = {
			name : label,
			x : x,
			
			hovertemplate: '<b>Counts</b>: %{y}' +
			'<br><b>Interval</b>: %{text}<br>'+
			"<extra></extra>",
			text : intervals,
			y : counts,
			type : 'bar',
			marker: {
				opacity: opac,
				line: {
				  width: 1.5
				}
			}

	}	
	data.push(trace)
	// add mean as trace
	if(m != -999.0){
		var maxval = Math.max(...counts)
		var meantrace = {
			x : [m,m],
			y : [0,maxval+50],
			hoverinfo : "skip",
			mode: 'lines',
			type: 'scatter',
			name: reskeys[2]+' : '+m,
	
			line: {
			  color: 'rgb(96, 96, 96)',
			  width: 1.5
			}
		}
		
		data.push(meantrace)
		// add std box as trace bar
		if(std != -999.0){
			//var std_x = [m-std]
			var edge0 = m-std
			var edge1 = m+std
			var stdtrace = {
				//x : std_x,
				x0 : m,
				width : 2*std,
				hovertemplate: '<b>Interval</b>: %{text}<br>',
				text : ["["+edge0+", "+edge1+"]"],				
				y : [maxval+50],
				//mode: 'lines',
				name: reskeys[3]+' : '+std,
				type : 'bar',
				marker: {
					opacity: 0.5,
					color: 'rgb(204, 204, 0)',
					line: {
					  color: 'rgb(204, 204, 0)',
					  width: 1.5
					}
				}		
			}			
			data.push(stdtrace)	
		}		
	}		

	var layout = {
	  barmode: 'overlay',
	  bargap : 0,
	  hovermode: 'closest',
	  showlegend : true,
	  xaxis: {
		  title : {
			  font : {
					family : "Open Sans",
					size : "12",
					color: "#000000"
			  }
		  }
	  },
	  yaxis: {
		  title : {
			  font : {
					family : "Open Sans",
					size : "12",
					color: "#000000"
			  }
		  }
	  },			  
	  legend : {
		x : 0,
		y : 1,
		font: {
		  family: 'Open Sans',
		  size: 12,
		  color: '#000'
		},
		bgcolor: '#E2E2E2',
		bordercolor: '#000000',
		borderwidth: 0,
	  }

	};
	let modeBarButtons = [ 
	  [
		{ 
		  name: 'Download Plot as Image',
		  icon: Plotly.Icons.camera,
		  click: function (gd) {
			Plotly.downloadImage(gd, {
			  width: gd._fullLayout.width,
			  height: gd._fullLayout.height,
			  filename : "pregenerated_histogram_"+fname
			})
		  }
		}
	  ],


	  [
		{ 
		  name: 'Save experiment as PDF',
		  icon: Plotly.Icons.disk,
		  click: function(){

			select_download_dir("store_pdf", n_exp, labels);
		  }
		}
	  ], 
	  ["zoom2d", "pan2d", "select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",  "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"],
	  [
		  { 
			  name: 'Customize Plot',
			  icon: pencil,
			  click: function(){

				  show_custom_plot();
			  }
		  }
	  ] 
	];
    Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtons: modeBarButtons, displayModeBar : true});
	
}

function histogram(results, ny, labels) {
	console.log(results)
	fname = get_now_string()
	n_exp = "Histogram"
	display_plot(n_exp)
	var bins = results['bins']  
	if(bins == null){
		var binsize = document.getElementById('binsize').value;
		var bintype = $('input[name=bintype]:checked').val();
    }
  	else{
    	var binsize = bins[0]
        var bintype = bins[1]
    }
	var pydata = JSON.stringify(results)  	
	var dom = document.getElementById('chartContainer');
	var l = labels;
	if(bintype=="binnumber"){
		iswidth = 0
	}
	else
	{
		iswidth = 1
	}	
	var data = []

	$.ajax({
		method:"POST",
		url: 'scripts/histogram.py',
		data:{
		   iswidth : iswidth,
		   y : pydata,
		   b : binsize,
		   ny : ny
		}
	})
	.done(function(resultdata){
		for (var i=0; i<ny; i++){
			var counts = resultdata['counts_'+i]
			var bins = resultdata['bins_'+i]
			var intervals = [] //bins intervals
			var x = [] //x coordinate, modified from bins to correctly align bars
			for(var b=0; b<(bins.length-1); b++){
				var end = ")"
				if(b==bins.length-2){
					end = "]"
				}
				intervals.push("["+bins[b]+", "+bins[b+1]+end)
				x.push(bins[b]+(bins[b+1]-bins[b])/2)
			}
			var opac = 1.0
			if(ny>1){opac = 0.6}
			var trace = {
				name : l[i+1],
				x : x,
				hovertemplate: '<b>Counts</b>: %{y}' +
				'<br><b>Interval</b>: %{text}<br>'+
				"<extra></extra>",
				text : intervals,
				y : counts,
				type : 'bar',
				marker: {
					opacity: opac,
					line: {
					  width: 1.5
					}
				}
			}
		data.push(trace) 
		}

		var layout = {
		  barmode: 'overlay',
		  bargap : 0,
		  hovermode: 'closest',
		  showlegend : true,
		  xaxis: {
			  title : {
				  font : {
						family : "Open Sans",
						size : "12",
						color: "#000000"
				  }
			  }
		  },
		  yaxis: {
			  title : {
				  font : {
						family : "Open Sans",
						size : "12",
						color: "#000000"
				  }
			  }
		  },			  
		  legend : {
			x : 0,
			y : 1,
			font: {
			  family: 'Open Sans',
			  size: 12,
			  color: '#000'
			},
			bgcolor: '#E2E2E2',
			bordercolor: '#000000',
			borderwidth: 0,
		  }

		};

		let modeBarButtons = [ 
		  [
			{ 
			  name: 'Download Plot as Image',
			  icon: Plotly.Icons.camera,
			  click: function (gd) {
				Plotly.downloadImage(gd, {
				  width: gd._fullLayout.width,
				  height: gd._fullLayout.height,
				  filename : "histogram_"+fname
				})
			  }
			}
		  ],
		  [
			{ 
			  name: 'Save experiment as PDF',
			  icon: Plotly.Icons.disk,
			  click: function(){

				select_download_dir("store_pdf", n_exp, labels);
			  }
			}
		  ], 
		  [
			{ 
			  name: 'Save results as CSV',
			  icon: csv,
			  click: function(){

				save_csv(labels, JSON.parse(pydata));
				//exportPDF(n_exp, labels);
			  }
			}
		  ], 
		  ["zoom2d", "pan2d", "select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",  "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"],
		  [
			  { 
				  name: 'Customize Plot',
				  icon: pencil,
				  click: function(){

					  show_custom_plot();
				  }
			  }
		  ] 
		];

		Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtons: modeBarButtons, displayModeBar : true});

		var tabstats = document.getElementById("tab-stats1")
		if(tabstats.style.display == "none"){hide_pdf()}
	})
}	

function scatterplot(results, ny, labels) {
	
	fname = get_now_string()
	n_exp = "Scatter Plot"
	display_plot(n_exp)
	var dom = document.getElementById('chartContainer');
	ks = Object.keys(results)
	var idx = find_nan(results.x);

	data = []
	var hasdata = 0
	for (var i=0; i<ny; i++){
		var curr_x = results.x.slice();
		var curr_y = results[ks[i+2]]
		var idy =  find_nan(curr_y);
		var indices = idy.concat(idx)
		var final_x = reduce_array(curr_x, indices)
		var final_y = reduce_array(curr_y, indices)
		if(final_y.length > 0){hasdata++}
		var trace = {
			name : labels[i+1],
			x: final_x,
			y: final_y,
			mode: 'markers',
			type: 'scattergl',
			text: results.date
		}
		data.push(trace)
	}
	if(hasdata > 0){	
      var layout = {
          xaxis: {
			  title : {
				  text : labels[0],
				  font : {
						family : "Open Sans",
						size : "12",
						color: "#000000"
				  }
			  }
          },
		  yaxis: {
			  title : {
				  font : {
						family : "Open Sans",
						size : "12",
						color: "#000000"
				  }
			  }
          },
          showlegend : true,
          legend : {
              x : 0,
              y : 1,
              font: {
              family: 'Open Sans',
              size: 12,
              color: '#000'
              },
          bgcolor: '#E2E2E2',
          bordercolor: '#000000',
          borderwidth: 0,

          }
      };

      let modeBarButtons = [ 
		  [
			  { 
				  name: 'Download Plot as Image',
				  icon: Plotly.Icons.camera,
				  click: function (gd) {
					Plotly.downloadImage(gd, {
					  width: gd._fullLayout.width,
					  height: gd._fullLayout.height,
					  filename : "scatter_"+fname
					})
				  }
			  }
		  ],


		  [
			  { 
				  name: 'Save experiment as PDF',
				  icon: Plotly.Icons.disk,
				  click: function(){

					  select_download_dir("store_pdf", n_exp, labels);
				  }
			  }
		  ], 
		  [
			  { 
				  name: 'Save results as CSV',
				  icon: csv,
				  click: function(){

					  save_csv(labels, results);
					  //exportPDF(n_exp, labels);
				  }
			  }
		  ], 
		  ["zoom2d", "pan2d", "select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",  "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"],
		  [
			  { 
				  name: 'Customize Plot',
				  icon: pencil,
				  click: function(){

					  show_custom_plot();
				  }
			  }
		  ] 
		];
    Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtons: modeBarButtons, displayModeBar : true});
    }
  
  	return hasdata
}

function set_advanced_stats(){
	document.getElementById("stats_enable").value="advanced";
	document.getElementById("stats").style="display : block";
	document.getElementById("global_a").style="display : inline-block";
	document.getElementById("advanced_a").style="display : none";
}

function set_global_stats(){
	document.getElementById("stats_enable").value="global"
	document.getElementById("stats").style="display : none";
	document.getElementById("advanced_a").style="display : inline-block";
	document.getElementById("global_a").style="display : none";
}

function only_unique(value, index, self) { 
    return self.indexOf(value) === index;
}

function find_nan(in1){

	var indices = [];
	var x = in1;
	var el1 = -999;
	var idx1 = x.indexOf(el1);
	while (idx1 != -1) {
		indices.push(idx1);
		idx1 = x.indexOf(el1, idx1 + 1);
	}
	var el2 = -999.0;
	var idx2 = x.indexOf(el2);
	while (idx2 != -1) {
		indices.push(idx2);
		idx2 = x.indexOf(el2, idx2 + 1);
	}

	var el3 = "-999.0";
	var idx3 = x.indexOf(el3);
	while (idx3 != -1) {
		indices.push(idx3);
		idx3 = x.indexOf(el3, idx3 + 1);
	}  
	var el4 = "-999";
	var idx4 = x.indexOf(el4);

	while (idx4 != -1) {
		indices.push(idx4);
		idx4 = x.indexOf(el4, idx4 + 1);
	}   
	return indices
}

function reduce_array(arr, indices){
	var new_arr = [...arr]
	for (var j=0; j<indices.length; j++){
			delete new_arr[indices[j]]
		}		
	new_arr = new_arr.filter(function (el) {
		return el != null;
	});
	
	return new_arr
}

function get_now_string(){
	var date = get_utc_date()
	var curr_date = new Date(date).toISOString();
	curr_date = curr_date.split(".")[0];
	var new_date = curr_date.replace(/-/g,"").replace(/:/g,"");
	
	return new_date
}

function render_plot(results, plot, ny, labels, usecase=""){
	if($('#chartContainer').is(':visible')){hide_custom_plot()}
	var errstatus = results['errstatus']
	var warningstatus = results['warningstatus']
	var datastatus = results['datastatus']
	var infostatus = results['infostatus']
	var op = "Statistical Analysis"
	var msg = ""
    
	if (errstatus == 1){
		msg += results['msg'].replace("_RETCHAR_","\n");
		document.getElementById("plot_container").style=("display : none");
      	var hasdata = 0
	}
	else {
		switch(plot) {
			case "scatter":
				op = "Scatter plot";
				break;
			case "trend":
				op = "Trend analysis";
				break;
			case "histogram":
				op = "Histogram";
				break;      
        }
		if (warningstatus == 1 || datastatus == 1){
			msg += results['msg'].replace("_RETCHAR_","\n");
			if (datastatus == 1){
				document.getElementById("plot_container").style=("display : none");
				$("#loader").hide();
			}
		}
		if (infostatus == 1){
			msg += results['infomsg'].replace("_RETCHAR_","\n");
			$("#loader").hide();
		}
		if (datastatus == 0){
			switch(plot) {
				case "scatter":
					hasdata = scatterplot(results, ny, labels);
					break;
				case "trend":
					hasdata = trend(results, ny, labels);
					break;
				case "histogram":
                	hasdata = 0
                	for(var yid=0; yid<ny; yid++){
                    	arr = results['y'+yid]
                      	for(var idx=0; idx<arr.length; idx++){
							var check
							switch (typeof(arr[idx])){
								case "number":
									check = (arr[idx] != -999)
									break;
								case "string":
									check = !arr[idx].startsWith("-999")
									break;								
							}
							if(check){
                            	hasdata = 1
                              	break;								
							}
                        }
						if(hasdata > 0){break;}
                    }
					if(hasdata > 0){
                      histogram(results, ny, labels);
                    }
					break;
                default :
                	hasdata = 1
                	break;
			}
			if(hasdata > 0){          
              var modebar = document.getElementsByClassName("modebar")[0]
              if(typeof modebar != 'undefined'){
                  modebar.style='display:none;';
              }
            }
          	else{
				msg += "No data to plot!\nData are NULL or STRINGS"
				if(plot=="scatter"){
					msg += " or NO INTERSECTION between the two sets."
				}
				else{
					msg+="."
				}
              document.getElementById("plot_container").style=("display : none");
              $("#loader").hide();
            }
        }
    }
	if (errstatus == 1 || warningstatus == 1 || datastatus == 1 || infostatus == 1 || (datastatus == 0 && hasdata==0)){
		alert(msg);
	}
	return [op, hasdata]
}

function render_pregenerated(results, plot, label){
 	if($('#chartContainer').is(':visible')){hide_custom_plot()}
	var errstatus = results['errstatus']
	var warningstatus = results['warningstatus']
	var datastatus = results['datastatus']
	var infostatus = results['infostatus']
	var op = "Pre-generated "+plot.charAt(0).toUpperCase() + plot.slice(1);
	var msg = ""
	if (errstatus == 1){
		msg += results['msg'].replace("_RETCHAR_","\n");
		document.getElementById("plot_container").style=("display : none");
      	var hasdata = 0
	}
	else {
		if (warningstatus == 1 || datastatus == 1){
			msg += results['msg'].replace("_RETCHAR_","\n");
			if (datastatus == 1){
				document.getElementById("plot_container").style=("display : none");
				$("#loader").hide();
			}
		}
		if (infostatus == 1){
			msg += results['infomsg'].replace("_RETCHAR_","\n");
			$("#loader").hide();
		}
		if (datastatus == 0){
			switch(plot) {
				case "histogram":
					op = "Histogram";
					var d = Object.keys(results)[0]
                	hasdata = 0
					if(d != "errstatus"){
						var data = results[d]
						var edges = data['edges']
                        console.log(edges)
						if(edges != "-999" && edges != "-999.0"){
							hasdata = 1
							display_plot(op)							
							preg_histogram(results, data, label)
							$("#tab-stats1").hide()
							$("#tab-files1").hide()
						}
					}
					break;
                default :
                	hasdata = 1
                	break;
			}
			if(hasdata == 0){
				msg += "No data to plot!"
				document.getElementById("plot_container").style=("display : none");
				$("#loader").hide();				
			}
        }
    }

	if (errstatus == 1 || warningstatus == 1 || datastatus == 1 || infostatus == 1 || (datastatus == 0 && hasdata==0)){
		alert(msg);
	}

	return [op, hasdata] 
}

function onclick_plot(){
	$('#form-div').css('display', 'block');
	$('#plot_stats').css('display', 'none');
	$('#plot_files').css('display', 'none');
	$('#custom_plot').css('display', 'block');
	var dom = document.getElementById('chartContainer');
	Plotly.relayout( dom, {
		'xaxis.autorange': true,
		'yaxis.autorange': true
	});  
} 
 
function onclick_files(){
  $('#form-div').css('display', 'none'); 
  $('#plot_files').css('display', 'flex'); 
  $('#plot_files').css('flex-wrap', 'wrap');
  $('#plot_stats').css('display', 'none')
  $('#custom_plot').css('display', 'none');
$('#files_tbl').DataTable().columns.adjust(); 
}  
 
function onclick_stats(){
  var t = document.getElementById("plot_type").value
  if(t != "stats"){
    $('#form-div').css('display', 'none');
  }
  else{
    $('#form-div').css('display', 'block');
    $('#plot_tab').removeClass('active');
  }
  $('#plot_stats').css('display', 'flex'); 
  $('#plot_stats').css('flex-wrap', 'wrap'); 
  $('#plot_files').css('display', 'none');
  $('#custom_plot').css('display', 'none');   
} 

$("input[type='radio'][name=optflag]").change(function(){
	$('#description').html('');
	if($(this).val()!="nd")
	{
		populate_flags();
		$("#description").show();
		$("#parflag").show();
		$("#alert-email").show();
	}
	else
	{
		$("#description").hide();
		$("#parflag").hide();
		$("#email-to").val('')
		$("#alert-email").hide();
	}
});

//Avoid action on "Enter" key press
$(document).keypress(
  function(event){
	var tag = event.target.tagName

    if (event.which == '13' && tag != "TEXTAREA") {
      event.preventDefault();
    }
});