function run_py(e) {
	var ny = parseInt($("#n_ypar").val());
	var system = document.getElementById("hktm_source").value;
	var plot = $("#plot_type").val()	
	var stats = $("#stats_enable").val();	
	var usecase = $("#usecase").val();	
	var go = true

	
	if(go==true){
/* switch(system){
	
	case "QLA":
		out = prepare_data(ny, plot);
		//out = prepare_data(ny, plot);
		break;
	case "NISP":
		//out = prepare_nisp_data(ny, plot);
		out = prepare_data(ny, plot);
		break;
	
} */

		out = prepare_data(ny, plot);

		params = out[0];
		ny = out[2];
		console.log(params)
		labels = out[1];
		var labels = out[1];
		params.labels = labels;
		pyscript = "scripts/get_data.py";
		console.log(params)
		params.isonline = 1
		params.plot_type="scatter"
		var op = "Machine Learning";
		$.ajax({
			
			type: "POST",
			url: pyscript,
			data: params ,
		dataType: "html",
			cache: false,
			async:'asynchronous',
			beforeSend: function(){
				// Show loader image container
				$("#loader").show();
				window.document.body.scrollTop = 0;
				window.document.documentElement.scrollTop = 0;
			},
			success: function(returndata){
				results = JSON.parse(returndata)
				console.log(results)
				document.getElementById("modal-labels").value = labels
				document.getElementById("modal-tstart").value = params['tstart']     
				document.getElementById("modal-tstop").value = params['tend']
				document.getElementById("modal-pid").value = params['pid']

				//operation name
				var op2hist
				//parameters
				var l2hist = labels.slice(1).join(",")
				
				var errstatus = results['errstatus']
				var warningstatus = results['warningstatus']
				var datastatus = results['datastatus']
				var infostatus = results['infostatus']
				if (errstatus == 1){
					alert(results['msg']);
					document.getElementById("plot_container").style=("display : none");
				}
				else {
					if (warningstatus == 1  ||  datastatus == 1){
						alert(results['msg']);
						if (datastatus == 1){
							document.getElementById("plot_container").style=("display : none");
							$("#loader").hide();
						}
						
					}
					if (infostatus == 1){
						alert(results['infomsg']);
						$("#loader").hide();
					}
					
					if (datastatus == 0){
						switch(plot) {
							case "ml":
								scatterplot(returndata, ny, labels);
								op = "Machine Learning";
								break;
							case "trend":
								trend(returndata, ny, labels);
								op = "Trend analysis";
								break;
							case "histogram":
								histogram(returndata, ny, labels);
								op = "Histogram";
								break;
						}
						var modebar = document.getElementsByClassName("modebar")[0]
						if(typeof modebar != 'undefined'){
							modebar.style='display:none;';
						}
						
						console.log(stats_list)
						stat_results=calculate_stats(returndata, ny, plot, stats, labels)

					
					//Store data in history
					$.ajax({
						type: "POST",
						url: "functions.php",
						data: {
							action: "update_history",
							username : document.getElementById("session-user").innerHTML,
							operation : op,
							infile :	"NA",
							out	: returndata,
							config : JSON.stringify(params)
							},
						error : function (obj, textstatus) {
							alert("Impossible to store the operation in History")
							}
						})
					}

				
				}
			
			},
			complete:function(data){
				//display tabs
				//display_results(plot, stats);
				// Hide loader image container
				$("#loader").hide();
				
			}
		});
		e.preventDefault();	
	}
};	


/* function prepare_data(ny,plot){
	
	var y0sys = $("#y0-sys").val();
	
	var params = {
				'plot_type' : plot,
				'ny' : ny,
				'source': $("#hktm_source").val(),
				'ysys0' : y0sys,
				'ypar0' : $("#y0-params").val(),
				'tstart' : $("#tstart").val(),
				'tend' : $("#tend").val(),
				'user' : document.getElementById("session-user").innerHTML,
				'usecase' : $("#usecase").val()
			}
	
	var det = $("#det-type").val().split(",");
	if(det[1]!="None"){
		var yrow = $("#y0-det-row").val()
		var ycol = $("#y0-det-col").val();
		params.det_type = det;
		params.yrow0 = yrow;
		params.ycol0 = ycol;
		params.yval0 = $("#y0-values").val();
		ydetector = collect_detectors(det[1], yrow, ycol, "#y0-quadrant")
		params.ydet0 = ydetector;
		// CREATE Y LABEL FOR PLOT
		y0label = y0sys+"."+ydetector+"."+params.ypar0+"."+params.yval0;

	}
	else{
		y0label = y0sys+"."+params.ypar0;
	}
	
	// Create x label and add detector info (if any) if scatter plot 
	if ((plot == "scatter") || (plot == "ml")){
		var xsys = $("#x-sys").val();
		params.xsys = xsys;
		params.xpar = $("#x-params").val();
 		if(det[1]!="None"){
			var xrow = $("#x-det-row").val();
			var xcol = $("#x-det-col").val();
			xdetector = collect_detectors(det[0], xrow, xcol, "#x-quadrant");
			params.xcol = xcol;
			params.xrow = xrow;
			params.xval = $("#x-values").val();
			params.xdet = xdetector;
			xlabel = xsys+"."+xdetector+"."+params.xpar+"."+params.xval;
		}
		else{
			xlabel = xsys+"."+params.xpar;
		}
	}
	else{
		xlabel = "None"
	}	

	labels = [xlabel, y0label];
	
	// COLLECT ALL Y PARAMS
	if (ny>1) {
		var additional_y_sys = []
		var additional_y_par = [];
		var additional_y_val = [];
		var additional_y_row = [];
		var additional_y_col = [];
		var additional_y_det = [];	
		
		for (i=1; i<ny; i++){
			new_y_sys = $("#y"+i+"-sys").val();
			new_y_par = $("#y"+i+"-params").val();
			additional_y_sys.push(new_y_sys);
			additional_y_par.push(new_y_par);
			//for forms with detectors
			if(det[1]!="None"){
				new_y_val = $("#y"+i+"-values").val();
				new_y_row = $("#y"+i+"-det-row").val();
				new_y_col = $("#y"+i+"-det-col").val();	
				additional_y_val.push(new_y_val);
				additional_y_row.push(new_y_row);
				additional_y_col.push(new_y_col);
				// COLLECT DETECTOR PARAMETERS AND CREATE DETECTOR STRING
				new_ydetector = collect_detectors(det[i+1], new_y_row, new_y_col, "#y"+i+"-quadrant");
				additional_y_det.push(new_ydetector);
				//update labels
				labels.push(new_y_sys+"."+new_ydetector+"."+new_y_par+"."+new_y_val);				
				
			}
			else{		
				//update labels
				labels.push(new_y_sys+"."+new_y_par);
			}
		}
		// add to data array
		params.additional_y_sys = additional_y_sys;
		params.additional_y_par = additional_y_par;
		if(det[1]!="None"){
			params.additional_y_val = additional_y_val;
			params.additional_y_row = additional_y_row;
			params.additional_y_col = additional_y_col;
			params.additional_y_det = additional_y_det;			
		}
	
	}	
	
	return [params,labels]
	
	
}

 */

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
	if (plot == "ml"){
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
	console.log(labels)
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


function prepare_qla_data(ny, plot){
	var det = $("#det-type").val().split(",");
	var yrow = $("#y0-det-row").val()
	var ycol = $("#y0-det-col").val();
	var y0sys = $("#y0-sys").val();

	// PARAMS FROM FORM
	var params = {
				'det_type' : det,
				'plot_type' : plot,
				'ny' : ny,
				'source': $("#hktm_source").val(),
				'ysys0' : y0sys,
				'yrow0' : yrow,
				'ycol0' : ycol,			
				'ypar0' : $("#y0-params").val(),
				'yval0' : $("#y0-values").val(),
				'tstart' : $("#tstart").val(),
				'tend' : $("#tend").val(),
				'user' : document.getElementById("session-user").innerHTML,
				'usecase' : $("#usecase").val()

			}

	// Store x data if scatter plot
	if ((plot == "scatter") || (plot == "ml")){
		var xrow = $("#x-det-row").val();
		var xcol = $("#x-det-col").val();
		var xsys = $("#x-sys").val();
		xdetector = collect_detectors(det[0], xrow, xcol, "#x-quadrant");
		params.xcol = xcol;
		params.xrow = xrow;
		params.xsys = xsys;
		params.xpar = $("#x-params").val();
		params.xval = $("#x-values").val();
		params.xdet = xdetector;
		xlabel = xsys+"."+xdetector+"."+params.xpar+"."+params.xval;
	}
	else{
		xlabel = "None"
	}
		
	
	
	// COLLECT DETECTOR PARAMETERS AND CREATE DETECTOR STRING
	ydetector = collect_detectors(det[1], yrow, ycol, "#y0-quadrant")
	params.ydet0 = ydetector;
	
	
	// CREATE LABELS FOR PLOT
	y0label = y0sys+"."+ydetector+"."+params.ypar0+"."+params.yval0;
	labels = [xlabel, y0label];
	

	// COLLECT ALL Y PARAMS
	if (ny>1) {
		var additional_y_sys = []
		var additional_y_par = [];
		var additional_y_val = [];
		var additional_y_row = [];
		var additional_y_col = [];
		var additional_y_det = [];
		
		for (i=1; i<ny; i++){
			new_y_sys = $("#y"+i+"-sys").val();
			new_y_par = $("#y"+i+"-params").val();
			new_y_val = $("#y"+i+"-values").val();
			new_y_row = $("#y"+i+"-det-row").val();
			new_y_col = $("#y"+i+"-det-col").val();
			
			additional_y_sys.push(new_y_sys);
			additional_y_par.push(new_y_par);
			additional_y_val.push(new_y_val);
			additional_y_row.push(new_y_row);
			additional_y_col.push(new_y_col);
			// COLLECT DETECTOR PARAMETERS AND CREATE DETECTOR STRING
			new_ydetector = collect_detectors(det[i+1], new_y_row, new_y_col, "#y"+i+"-quadrant");
			additional_y_det.push(new_ydetector);
			//update labels
			labels.push(new_y_sys+"."+new_ydetector+"."+new_y_par+"."+new_y_val);
		}
		// add to data array
		params.additional_y_sys = additional_y_sys;
		params.additional_y_par = additional_y_par;
		params.additional_y_val = additional_y_val;
		params.additional_y_row = additional_y_row;
		params.additional_y_col = additional_y_col;
		params.additional_y_det = additional_y_det;
	}
	console.log(params)
	console.log(labels)
		
	return [params,labels]

	
	
}

function prepare_nisp_data(ny, plot){
	var y0sys = $("#y0-sys").val();
	var det = $("#det-type").val().split(",");
	if(det[1]!="None"){
		var yrow = $("#y0-det-row").val()
		var ycol = $("#y0-det-col").val();
		var y0sys = $("#y0-sys").val();
	}
	else{
		var yrow = "";
		var ycol = "";
		var y0sys = "";
	}

	// PARAMS FROM FORM
	var params = {
				'plot_type' : plot,
				'ny' : ny,
				'source': $("#hktm_source").val(),
				'ysys0' : y0sys,
				'ypar0' : $("#y0-params").val(),
				'tstart' : $("#tstart").val(),
				'tend' : $("#tend").val(),
				'user' : document.getElementById("session-user").innerHTML,
				'usecase' : $("#usecase").val()
			}
	

	// Store x data if scatter plot
	if ((plot == "scatter") || (plot == "ml")){
		var xsys = $("#x-sys").val();
		params.xsys = xsys;
		params.xpar = $("#x-params").val();
		xlabel = xsys+"."+params.xpar;
	}
	else {
		xlabel = "None"
	}

	// CREATE LABELS FOR PLOT
	y0label = y0sys+"."+params.ypar0;
	labels = [xlabel, y0label];	

	// COLLECT ALL Y PARAMS
	if (ny>1) {
		var additional_y_sys = []
		var additional_y_par = [];
		
		for (i=1; i<ny; i++){
			new_y_sys = $("#y"+i+"-sys").val();
			new_y_par = $("#y"+i+"-params").val();
			
			additional_y_sys.push(new_y_sys);
			additional_y_par.push(new_y_par);
			//update labels
			labels.push(new_y_sys+"."+new_y_par);
		}
		// add to data array
		params.additional_y_sys = additional_y_sys;
		params.additional_y_par = additional_y_par;
	}	
	
	return [params,labels]	
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
	document.getElementById('chartContainer').style='height: 570px; width: 100%; display:block;';
	var plottab = document.getElementById('plot_tab')
	//plottab.style='display:block;';
	plottab.setAttribute("class", "tab-pane active")

}


function calculate_stats(pydata, ny, plot, stats, labels){
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
			// append to output json name of function, list of configuration parameters and number of parameters for each row
			stats_data [curr_name] = {
				"func" : curr_func,
				"params" : params,
				"npar" : npar
			}
		}
	}
	
	function FormDataToJSON(FormElement){    
		var formData = new FormData(FormElement);
		var ConvertedJSON= {};
		for (const [key, value]  of formData.entries())
		{
			ConvertedJSON[key] = value;
		}

		return ConvertedJSON
	}
	
	
	// input data for Python/CGI
	datain = {
			"inputdata"	    :	JSON.stringify(JSON.parse(pydata)),
			"stats_config"  :   JSON.stringify(stats_data),
			"ny"		    : 	ny,
			"plot_type"	    :	plot,
			"stats_type"    :	stats,
			"model"		    : 	document.getElementById("model").value,
			"model_param"   :   JSON.stringify(FormDataToJSON(document.getElementById('stats_form'))),
			"split"		    : 	document.getElementById("traintest").value,
			"username"      :   document.getElementById("session-user").innerHTML,			
			"seed"		    : 	document.getElementById("splitRandomState").value
			}

	$.when(
		$.ajax({
			type: "POST",
			url: "scripts/calculate_ml.py",
			data: datain, 
			dataType: "html",
			cache: false,
			async:'asynchronous',
			//success: function(data){
				//store stats results in a hidden div
				//var div = document.getElementById('stats_results');
				//div.innerHTML = data;
				//visualize stats as tables
				//render_stats(data, ny, labels, plot, stats)
				//}
			})
			.done(function(data){
				//store stats results in a hidden div
				var div = document.getElementById('stats_results');
				div.innerHTML = data;
				//visualize stats as tables
				render_stats(data, ny, labels, plot, stats)
				
				})
			.fail(function(obj, textstatus) {
							alert("Some error occurred with your model configuration")
							})
		) 
	}


function render_stats(pydata, ny, labels, plot, stats){
/* 	try { */
	    var results = JSON.parse(pydata);



	    var parent = document.getElementById("plot_stats");
	    parent.style="display : flex; flex-wrap : wrap";
	    parent.innerHTML = "";
	    ks = Object.keys(results)
	    
	    // create stats div
	    if((plot == "scatter") || (plot == "ml")){
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


	    if (results.outputfilename != "None"){
			console.log(results.outputfilename)
			console.log(results)
    //    	document.getElementById('plot_container').innerHTML += document.write("<a href=\"" + results.outputfilename + "\"><p>output file</p></a>");
            var parent2= document.getElementById('linkContainer');
		    document.getElementById('linkContainer').style='display:block;';
		    parent2.setAttribute("class", "col-md-12");
		    parent2.innerHTML="<a href=\"" + results.outputfilename + "\" style=\"font-size:20px; font-weight:bold\"><p>output file</p></a>"
	    }	
	    if (results.modelfilename != "None"){
            var parent2= document.getElementById('linkContainer');
		    parent2.innerHTML+="<a href=\"" + results.modelfilename + "\"style=\"font-size:20px; font-weight:bold\"><p>model file</p></a>"
		    }	

	    
	    
	    // y0 stats
	    y0name = labels[1]
	    y0data = results.y0_stats;
	    create_stats_table(y0data, y0name, parent, "y0_stats");
	    
	    // additional y stats
	    //console.log(results)
	    //console.log(labels)
	    if (ny>1){
		    for (i=1; i<ny; i++){
			    
				    if ((plot == "scatter") || (plot == "ml")){ 
				    var node = document.createElement("div");
				    node.setAttribute("class", "col-md-12");
				    node.setAttribute("style", "font-size:20px; font-weight:bold");
				    var num = i+1
				    node.innerHTML="DATASET "+num.toString()
				    parent.appendChild(node)
			    }
			    
			    name = labels[i+1]
			    data = results[ks[i+1]]
			    
			    if ((plot == "scatter") || (plot == "ml")){

				    xname = labels[0];
				    xdata = results[ks[i+ny]];
    //				console.log(xdata)
				    create_stats_table(xdata, xname, parent, "x_stats"+i);
			    }
			    create_stats_table(data, name, parent, "y"+i+"_stats");
			    //console.log(name)
			    //console.log(data)
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
	    
	    if(plot!="stats"){
		    $('#plot_stats').css('display', 'none');
	    }
	    var modebar = document.getElementsByClassName("modebar")[0]
	    if(typeof modebar != 'undefined'){
		    modebar.style='display:block;';
	    }
	    $("#loader").hide();
/*     }
    catch {
    	alert("Please check model configuration and input features");
    } */
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
		//console.log(data)
		// add stats to table
		var x_keys = Object.keys(data);
		var x_values = Object.values(data);
		var n_stats = x_keys.length;
		for (var i = 0; i < n_stats; i++) {
			var tr = document.createElement('tr');
			for (var j = 0; j < 2; j++) {
//			if (i == 2 && j == 1) {
//        break
//      } else {
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



function trend(pydata, ny, labels) {

	fname = get_now_string()
	n_exp = "Trend Analysis"
	display_plot(n_exp)
	var dom = document.getElementById('chartContainer');
	//console.log(pydata)
	var results = JSON.parse(pydata)

	ks = Object.keys(results)
	data = []
	for (var i=1; i<ny+1; i++){
		var curr_y = results[ks[i+1]]
		var curr_x = results.date
		
		var indices =  find_nan(curr_y);
		var final_x = reduce_array(curr_x, indices)
		var final_y = reduce_array(curr_y, indices)
		
		var trace = {
			name : labels[i],
			x: final_x,
			y: final_y,
			mode: 'lines+markers',
			type: 'scattergl',
			line: {shape: 'spline'},
		}
		//console.log(results[ks[i+2]])
		data.push(trace)
	}
	
	

	
	

	
	var layout = {
		xaxis: {
			tickangle : -45
		},
		showlegend : true,
		legend : {
			x : 0,
			y : 1,
			font: {
			family: 'sans-serif',
			size: 12,
			color: '#000'
			},
		bgcolor: '#E2E2E2',
		bordercolor: '#FFFFFF',
		borderwidth: 2
		}
		//title: "Responsive to window's size!",
		//font: {size: 18}
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
    ["zoom2d", "pan2d", "select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",  "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"]];

	//Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displayModeBar : true});
	
	
	Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtons: modeBarButtons, displayModeBar : true});
	
}




function histogram(pydata, ny, labels) {
	
	fname = get_now_string()
	n_exp = "Histogram"
	display_plot(n_exp)
	var dom = document.getElementById('chartContainer');
	var binsize = document.getElementById('binsize').value;
	var bintype = $('input[name=bintype]:checked').val();
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
				
				console.log(resultdata)
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
					legend : {
						x : 0,
						y : 1,
						font: {
						family: 'sans-serif',
						size: 12,
						color: '#000'
						},
					bgcolor: '#E2E2E2',
					bordercolor: '#FFFFFF',
					borderwidth: 2
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
				["zoom2d", "pan2d", "select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",  "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"]];

				console.log(data)
				
				Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtons: modeBarButtons, displayModeBar : true});
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		})
	
	
		
	
	
	
	
	
/* 	var results = JSON.parse(pydata)

	ks = Object.keys(results)
	
	

	
	
	for (var i=1; i<ny+1; i++){
		var curr_y = results[ks[i+1]]
		var indices =  find_nan(curr_y); */
		//var final_y = reduce_array(curr_y, indices)	
			//change from bin number to binsize if required
		/*var numy=final_y.map(Number)
		var miny=Math.min(...numy)
		var maxy=Math.max(...numy)
		var miny=Math.min(...final_y)
		var maxy=Math.max(...final_y)*/
		


		

		

	
/* 	var layout = {
		showlegend : true,
		legend : {
			x : 0,
			y : 1,
			font: {
			family: 'sans-serif',
			size: 12,
			color: '#000'
			},
		bgcolor: '#E2E2E2',
		bordercolor: '#FFFFFF',
		borderwidth: 2
		}
		//title: "Responsive to window's size!",
		//font: {size: 18}
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

				save_csv(labels, results);
				//exportPDF(n_exp, labels);
			}
		}
	], 
	["zoom2d", "pan2d", "select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",  "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"]];

	console.log(data)
	
	Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtons: modeBarButtons, displayModeBar : true}); */
}	


function scatterplot(pydata, ny, labels) {
	
	fname = get_now_string()
	n_exp = "Scatter Plot"
	display_plot(n_exp)

	var dom = document.getElementById('chartContainer');
	var results = JSON.parse(pydata)

	ks = Object.keys(results) 	
	var idx = find_nan(results.x);
	
	data = []

	for (var i=0; i<ny; i++){
		var curr_x = results.x.slice();
		var curr_y = results[ks[i+2]]

		var idy =  find_nan(curr_y);
		var indices = idy.concat(idx)
		
		//console.log(indices)
		var final_x = reduce_array(curr_x, indices)
		var final_y = reduce_array(curr_y, indices)



		var trace = {
			name : labels[i+1],
			x: final_x,
			y: final_y,
			mode: 'markers',
			type: 'scattergl',
			text: results.date
			
		}
		//console.log(results[ks[i+2]])
		data.push(trace)
	}
	
	var layout = {
		showlegend : true,
		legend : {
			x : 0,
			y : 1,
			font: {
			family: 'sans-serif',
			size: 12,
			color: '#000'
			},
		bgcolor: '#E2E2E2',
		bordercolor: '#FFFFFF',
		borderwidth: 2
		}
		//title: "Responsive to window's size!",
		//font: {size: 18}
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
	["zoom2d", "pan2d", "select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",  "toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"]];

	//Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displayModeBar : true});
	
	
	Plotly.newPlot(dom, data, layout, {responsive:true, editable:true, displaylogo: false, scrollZoom: true, modeBarButtons: modeBarButtons, displayModeBar : true});
	

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
  $('#plot_files').css('display', 'block'); 
  //$('#plot_files').css('flex-wrap', 'wrap');
  $('#plot_stats').css('display', 'none')
  $('#custom_plot').css('display', 'none');

$('#files_tbl').DataTable().columns.adjust().draw()
  $('#plot_files').css('display', 'flex'); 
  $('#plot_files').css('flex-wrap', 'wrap');	 
} 

function onclick_stats(){
  var t = document.getElementById("plot_type").value
  if(t != "stats"){
    $('#form-div').css('display', 'none');
    
/*    if(t=="upload"){
      	console.log($("#op").val())
    	if($("#op").val()!="stats"){$('#plot_stats').removeClass('active');}
    }*/
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


