function toggle(id){

	$("#"+id).toggle();
	//$("#"+id).hide();
}
// PLOTS RESTYLE
function reset_custom_plot(){
	reset_general()
	reset_traces()
	reset_axes()
	reset_legend()
/* 	$("#collapse2One").attr("aria-expanded","false");
	$("#collapse2Two").attr("aria-expanded","false");
	$("#collapse2Three").attr("aria-expanded","false");
	$("#collapse2Four").attr("aria-expanded","false"); */
	
}	

function reset_traces(){
//TRACES - COLOR AND NAME RESET ON FORM GENERATION
 	var plot = document.getElementById('plot_type').value;

	//different settings for bar plot
	var pborderval, postext
	if(plot=="histogram"){	
		pborderval = '2'
		postext = 'none'
	}
	else{
		pborderval = '0'
		postext = 'middle center'
	}		
	
	//DISPLAY
	document.getElementById("tr-p").checked = true;
	document.getElementById("tr-l").checked = true;
	document.getElementById("tr-t").checked = false;
	//section linked to display
	$("#cp-tr-markers").show()
	$("#cp-tr-lines").show()
	$("#cp-tr-text").show()
	
	//POINTS
	//Opacity
	$('#slider-p-opac').val('100')
	$('#p-opac').val('100')
	//Size
	$('#p-size').val('6')	
	//Border width
	$('#p-border-width').val(pborderval)

	//LINES
	//Width
	$('#l-width').val('2')
	//Opacity
	$('#slider-l-opac').val('100')
	$('#l-opac').val('100')	

	//Type
	$('#tr_line_type').val('solid')	
	//Shape
	$('#tr_line_shape').val('linear')	
	//Connect gasp
	$('#tr-connectgaps').prop("checked", false);
	//Fill to
	$('#tr_fill').val('none')	
	
	//TEXT
	//Text position
	$('#tr_pos_text').val(postext)			
	//Text
	$('#tr_shown_text').val('')
	//Typeface
	$('#tr_tf').val('')	
	//Font size
	$('#tr_size').val('12')	
	//Font color
	$('#img-color-trtext').val('#000000')
	$('#color-trtext').val('#000000')
	$("#img-color-trtext").css("background-color",'#000000')	
}

function reset_axes(){
	//console.log("VADIO")
	document.getElementById("alla").checked = true;
	document.getElementById("xa").checked = false;
	document.getElementById("ya").checked = false;
	$("#lbl_axx").removeClass("active")
	$("#lbl_axy").removeClass("active")
	$("#lbl_axall").removeClass("active")
	$("#lbl_axall").addClass("active")	

	$("#grspace_div").hide()			
	$("#range_div").hide()			
	$("#axis-title-text").hide();
	$("#ticks-position").hide();
	$("#ticks-angle").hide();

	//init_axis_form()
	
	// ALL
		// Titles
		$("#tf_axis").val("Open Sans")
		$("#font-axis-title").val("12")
		$("#tcolor-axis").val("#000000")
		$("#img-tcolor-axis").css("background-color",'#000000')
		
		// Axis line
		document.getElementById("axiss").checked = false
		document.getElementById("axish").checked = true
		$("#axis_show_line").hide()
		$("#axis-thick").val("1")
		$("#color-axis").val("#444444")
		$("#img-color-axis").css("background-color",'#444444')
	
		// Grid lines
		document.getElementById("gridh").checked = false
		document.getElementById("grids").checked = true
		$("#grid_show_line").show()
		$("#grid-thick").val("1")		
		$("#color-grid").val("#EBF0F8")
		$("#img-color-grid").css("background-color",'#EBF0F8')

		// Zero line
		document.getElementById("zeroh").checked = false
		document.getElementById("zeros").checked = true	
		$("#zero_line_show").show()		
		$("#zerol-thick").val("1")
		$("#color-zerol").val("#000000")
		$("#img-color-zerol").css("background-color",'#000000')
		
		//Thick labels
		document.getElementById("tickh").checked = false
		document.getElementById("ticks").checked = true			
		$("#ticklabels_show").show()		
		$("#tf_ticks").val("Open Sans")
		$("#font-axis-ticks").val("12")
		$("#color-ticks").val("#000000")
		$("#img-color-ticks").css("background-color",'#000000')		

	
	//	X/Y				(DA VEDERE DOPO ALL)
		// text					""
		// Range
			// Type				Date per trend, verificare per gli altri plot
			// Range			Auto
			// MIN/MAX non necessario?
		//Grid spacing			Auto
			//Step size			""
		//Tick labels
			//position				Bottom
			//Angle					-45 per X, "" per Y
		

}

function reset_general(){
//GENERAL SETTINGS
	//BACKGROUND
	//Plot Background
	$('#img-color-bg').val('#ffffff')
	$('#color-bg').val('#ffffff')
	$("#img-color-bg").css("background-color",'#ffffff')
	//Margin Color
	$('#img-color-margins').val('#ffffff')
	$('#color-margins').val('#ffffff')
	$("#img-color-margins").css("background-color",'#ffffff')	
	
	//TEXT	
	//Typeface
	$('#tf_general').val('')
	//Font Size
	$('#all_fsize').val('12')	
	//Font Color
	$('#img-color-all').val('#000000')
	$('#color-all').val('#000000')
	$("#img-color-all").css("background-color",'#000000')	
	
	//TITLE
	//Text
	$('#title_textarea').val('')
	//Typeface
	$('#tf_title').val('')
	//Font Size
	$('#title_fsize').val('18')	
	//Font Color
	$('#img-color-title').val('#000000')
	$('#color-title').val('#000000')
	$("#img-color-title").css("background-color",'#000000')	
	//Horizontal position
	$('#listenSlider2').val('50')
	$('#hslider').val('50')	
	
	//hide sub-panels
	$("#cp-gen-bg").hide()
	$("#cp-gen-text").hide()
	$("#cp-gen-title").hide()
}

function reset_legend(){
//LEGEND
	//SHOW/HIDE
	//$("input[type='radio'][name='legend_sel']").val("show")
	$("#leg_show").show();
	$("#lbl_lgshow").removeClass("active")
	$("#lbl_lghide").removeClass("active")
	$("#lbl_lgshow").addClass("active")
	
	//TITLE
	//Text
	$('#legend_textarea').val('')
	//Typeface
	$('#tf_lg_title').val('')
	//Font Size
	$('#font-legend-title').val('12')	
	//Font Color
	$('#img-tcolor-legend').val('#000000')
	$('#tcolor-legend').val('#000000')
	$("#img-tcolor-legend").css("background-color",'#000000')	

	//TEXT
	//Typeface
	$('#tf_lg_text').val('')
	//Font Size
	$('#font-legend-text').val('12')	
	//Font Color
	$('#img-color-legend').val('#000000')
	$('#color-legend').val('#000000')
	$("#img-color-legend").css("background-color",'#000000')	
	
	//BOX
	//Border Width
	$('#border-legend-width').val('0')		
	//Border Color
	$('#img-bcolor-legend').val('#000000')
	$('#bcolor-legend').val('#000000')
	$("#img-bcolor-legend").css("background-color",'#000000')	
	//Background Color
	$('#img-bgcolor-legend').val('#E2E2E2')
	$('#bgcolor-legend').val('#E2E2E2')
	$("#img-bgcolor-legend").css("background-color",'#E2E2E2')	
	
	//hide sub-panels
	$("#cp-leg-title").hide()
	$("#cp-leg-text").hide()
	$("#cp-leg-box").hide()	
}

function show_custom_plot(){
  var dom = document.getElementById('chartContainer');

	var curr_layout = dom.layout	
//	console.log(curr_layout)  
  document.getElementById("plot_image").classList.add('col-xs-10');

  document.getElementById("plot_image").classList.remove('col-xs-12');
  document.getElementById("plot_settings").classList.add('col-xs-2');
  document.getElementById("plot_settings").style.display = 'block';
  var w = document.getElementById('chartContainer').offsetWidth;  
  Plotly.relayout(dom, {width:w});
  var el = $('.modebar-btn[data-title="Customize Plot"]').toggle();

  //build traces menu
	var ntraces = dom.data.length
	var seltrace = document.getElementById('tracelist');
	seltrace.innerHTML=""
	$("#trace_set").hide();
	var firstop = document.createElement("option");
	firstop.innerHTML = "Select a trace";
	firstop.setAttribute("value","");
	firstop.setAttribute("disabled","disabled");
	firstop.setAttribute("selected","selected");
	seltrace.appendChild(firstop)	
	for(var i = 0;i<ntraces;i++){
		if(dom.data[i]['x'].length>0){
			var curropt = document.createElement("option");
			curropt.innerHTML = "Trace "+(i+1);
			curropt.setAttribute("value",i);
			seltrace.appendChild(curropt)
		}
	}
	

	
}

function hide_custom_plot(){
  document.getElementById("plot_settings").classList.remove('col-xs-2');
  document.getElementById("plot_settings").style.display = 'none';  

  var dom = document.getElementById('chartContainer');
  document.getElementById("plot_image").classList.add('col-xs-12');  
  document.getElementById("plot_image").classList.remove('col-xs-10');

  var w = dom.offsetWidth;  

  if(dom.innerHTML!=""){Plotly.relayout(dom, {width:w})};
  var el = $('.modebar-btn[data-title="Customize Plot"]').show();  

}
	
  $("input[type='radio'][name='range_sel']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	//var axis = which_axis()
	var axis = $("input[type='radio'][name='axis_sel']:checked").val()
	var scale = $("#rangetype").val()

		if($(this).val()=="auto"){
			$('#range_lim').hide()
			if(curr_layout[axis+"axis"]==null){
				curr_layout[axis+"axis"]={}
			}			
			curr_layout[axis+"axis"]['autorange'] = true
			//curr_layout[axis+"axis"]['range'] = null
			Plotly.update(dom, {}, curr_layout);
		}
		else{
			
			$('#range_lim').show()
			var minval = curr_layout[axis+"axis"]['range'][0]
			var maxval = curr_layout[axis+"axis"]['range'][1]
			var mindiv = document.getElementById("minrangelim")
			var maxdiv = document.getElementById("maxrangelim")		
			//reset div
			mindiv.innerHTML=""
			maxdiv.innerHTML=""			
			if(scale!="date"){
				var node = document.createElement("input");
				node.setAttribute("type", "number");
				node.id = "minrangeinput";
				node.setAttribute("value", minval);
				node.setAttribute("class", "cp-ranlim");	
				//node.setAttribute("name", id);
				mindiv.appendChild(node)

				var node = document.createElement("input");
				node.setAttribute("type", "number");
				node.id = "maxrangeinput";
				//node.setAttribute("name", id);
				node.setAttribute("value", maxval);
				node.setAttribute("class", "cp-ranlim");				
				maxdiv.appendChild(node)

				$("#minrangeinput").on("change", function () {
					Plotly.relayout(dom, axis+'axis.range', [$("#minrangeinput").val(), $("#maxrangeinput").val()])
				});
				$("#maxrangeinput").on("change", function () {
					Plotly.relayout(dom, axis+'axis.range', [$("#minrangeinput").val(), $("#maxrangeinput").val()])
				});

				
				
			}
			else{

				var node = document.createElement("input");
				node.setAttribute("type", "text");
				node.id = "minrangeinput";
				node.setAttribute("class", "cp-dates");				
				node.setAttribute("value", minval);
				mindiv.appendChild(node)
				$('#minrangeinput').datetimepicker({
					useCurrent: false,
					date : minval,
					timeZone : "UTC",
					format: 'YYYY-MM-DD HH:mm:ss',
					//maxDate: "now"

				});				
			  
			  
				var node = document.createElement("input");
				node.setAttribute("type", "text");
				node.id = "maxrangeinput";
				node.setAttribute("class", "cp-dates");
				node.setAttribute("value", maxval);
				//node.setAttribute("name", id);
				maxdiv.appendChild(node)
				$('#maxrangeinput').datetimepicker({
					useCurrent: false, //Important! See issue #1075 - This comment is for useCurrent:"day" maybe OLD
					date : maxval,
					timeZone : "UTC",
					format: 'YYYY-MM-DD HH:mm:ss',
				});
				$("#minrangeinput").on("dp.change", function (e) {
					if( e.date ){

						$('#maxrangeinput').data("DateTimePicker").minDate(e.date);			
						//curr_layout[axis+"axis"]['autorange'] = false
						Plotly.relayout(dom, axis+'axis.range', [$("#minrangeinput").val(), $("#maxrangeinput").val()])

					}
				});
				$("#maxrangeinput").on("dp.change", function (e) {
					if( e.date ){
						Plotly.relayout(dom, axis+'axis.range', [$("#minrangeinput").val(), $("#maxrangeinput").val()])
					}
				});				
			}
		}
	
	
	 //Plotly.update(dom, {}, curr_layout);

	
  });	
	
	
	
	
  $("input[type='radio'][name='axis_sel']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout	
    if($(this).val()!="all")
    {
	  $("#range_div").show()
	  $("#grspace_div").show()
      $("#axis-title-text").show();
      $("#ticks-position").show();
	  var angle = curr_layout[$(this).val()+"axis"]["tickangle"]
	  if(angle!=null){
		  $("#tick-angle").val(angle)
	  }else{
		  $("#tick-angle").val("0")
	  }
	  $("#ticks-angle").show();
    }
    else
    {
		$("#grspace_div").hide()			
		$("#range_div").hide()			
		$("#axis-title-text").hide();
		$("#ticks-position").hide();
		$("#ticks-angle").hide();
		//get layout values
		//console.log(dom.layout)
    }
	init_axis_form($(this).val())	
  });

function init_axis_form(axis="all"){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	var defaults = false
	if(axis == "all"){
		//all axes
		console.log(curr_layout)
		//controlla valori di entrambi gli assi, se sono diversi, metti vuoto
		//titles check
		var xdata = curr_layout['xaxis']
		var ydata = curr_layout['yaxis']
		
		if(xdata["title"]["font"]["family"]==ydata["title"]["font"]["family"]){
			$("#tf_axis").val(ydata["title"]["font"]["family"])
		}	
		else{
			
			$("#tf_axis").val("")					
		}		
		if(xdata["title"]["font"]["size"]==ydata["title"]["font"]["size"]){
			$("#font-axis-title").val(ydata["title"]["font"]["size"])
		}
		else{
			$("#font-axis-title").val("")
		}

		if(xdata["title"]["font"]["color"]==ydata["title"]["font"]["color"]){
			$("#tcolor-axis").val(ydata["title"]["font"]["color"])
			$("#img-tcolor-axis").css("background-color", ydata["title"]["font"]["color"])
		}
		else{
			$("#tcolor-axis").val("")
			$("#img-tcolor-axis").css("background-color", "#ffffff")
		}		
		//lines
		//axis line
/* 		var showline_x = xdata["showline"]
		var showline_y = ydata["showline"]
		if(showline_x == null && showline_y == null){
			$("#axiss").checked = true
			$("#axish").checked = false
		}
		else{
			if(showline_x == showline_y){
				if(showline_x == true){
					$("#axiss").checked = true
					$("#axish").checked = false					
				}
				else{
					$("#axiss").checked = false
					$("#axish").checked = true					
				}
			}
			else{
				$("#axiss").checked = false
				$("#axish").checked = false				
			}
		} */

				//axis thickness
				//axis color
			//grid lines
				//grid thickness
				//grid color
			//zero line
				//line thickness
				//line color				
		//tick labels
			//show/hide
			//typeface
			//font size
			//font color
		
	}
	else{
		console.log(curr_layout)
		//single axis
		var a = axis+"axis"
		const axis_data = curr_layout[a]
		//Titles defaults
		title_defaults(axis_data)
		
		//Range defaults
		range_defaults(axis_data, axis)
		//Lines defaults
		lines_defaults(axis_data, axis)
	
		//Tick Labels defaults
		ticks_defaults(axis_data, axis)		
	
	}
	
	
}

function range_dates_jq(axis_data, axis, minval, maxval){
	var dom = document.getElementById('chartContainer');
	var atype = axis_data["type"]

	if(atype=="date"){
		$('#minrangeinput').datetimepicker({
			useCurrent: false,
			date : minval,
			timeZone : "UTC",
			format: 'YYYY-MM-DD HH:mm:ss',
			//maxDate: "now"

		});		
		
		$('#maxrangeinput').datetimepicker({
			useCurrent: false, //Important! See issue #1075 - This comment is for useCurrent:"day" maybe OLD
			date : maxval,
			timeZone : "UTC",
			format: 'YYYY-MM-DD HH:mm:ss',
		});	
		
		$("#minrangeinput").on("dp.change", function (e) {
			if( e.date ){

				$('#maxrangeinput').data("DateTimePicker").minDate(e.date);			
				//curr_layout[axis+"axis"]['autorange'] = false
				Plotly.relayout(dom, axis+'axis.range', [$("#minrangeinput").val(), $("#maxrangeinput").val()])

			}
		});
		$("#maxrangeinput").on("dp.change", function (e) {
			if( e.date ){
				Plotly.relayout(dom, axis+'axis.range', [$("#minrangeinput").val(), $("#maxrangeinput").val()])
			}
		});
	}
	else{
		$("#minrangeinput").on("change", function () {
			Plotly.relayout(dom, axis+'axis.range', [$("#minrangeinput").val(), $("#maxrangeinput").val()])
		});
		$("#maxrangeinput").on("change", function () {
			Plotly.relayout(dom, axis+'axis.range', [$("#minrangeinput").val(), $("#maxrangeinput").val()])
		});
	}
	
	
}	


function range_defaults(axis_data, axis){
	//axis type
	var atype = axis_data["type"]

 	if(atype!=null){
		$("#rangetype").val(atype)
	}else{
		$("#rangetype").val("linear")
	}		
	//range auto/custom
	if("autorange" in axis_data){
		if(axis_data["autorange"]){
			document.getElementById('autor').checked=true
			document.getElementById('customr').checked=false
			$("#range_lim").hide()			
		}
		else{
			document.getElementById('autor').checked=false
			document.getElementById('customr').checked=true
			$("#range_lim").show()				
		}
	}
	else{
		document.getElementById('autor').checked=true
		document.getElementById('customr').checked=false
		$("#range_lim").hide()			
	}
	//min-max
	var minval = axis_data["range"][0]
	var maxval = axis_data["range"][1]
	var mindiv = document.getElementById("minrangelim")
	var maxdiv = document.getElementById("maxrangelim")		
	//reset div
	mindiv.innerHTML=""
	maxdiv.innerHTML=""
	//min div
	var node = document.createElement("input");
	node.id = "minrangeinput";
	if(atype!="date"){
		var inputtype = "number"
		var inputcls = "cp-ranlim"
	}
	else{
		var inputtype = "text"
		var inputcls = "cp-dates"		
	}
	node.setAttribute("type", inputtype);
	node.setAttribute("value", minval);
	node.setAttribute("class", inputcls);
	mindiv.appendChild(node)
	//max div
	node = document.createElement("input");
	node.id = "maxrangeinput";
	node.setAttribute("type", inputtype);
	node.setAttribute("value", maxval);
	node.setAttribute("class", inputcls);
	maxdiv.appendChild(node)
	range_dates_jq(axis_data, axis, minval, maxval)		

}

function ticks_defaults(axis_data, axis){
	//tick labels show/hide
	if("showticklabels" in axis_data){
		if(axis_data["showticklabels"]){
			document.getElementById('ticks').checked=true
			document.getElementById('tickh').checked=false
			$("#ticklabels_show").show()
		}
		else{
			document.getElementById('ticks').checked=false
			document.getElementById('tickh').checked=true
			$("#ticklabels_show").hide()
		}			
	}
	else{
		document.getElementById('ticks').checked=true
		document.getElementById('tickh').checked=false
		$("#ticklabels_show").show()			
	}	
	//position
	$('input:radio[name=tickpos_show]').each(function () {
		$(this).prop("checked", false);
	});
	if(axis == "x"){
		$("#tickps_txt").html(" Top")
		$("#tickph_txt").html(" Bottom")
		$("#tickps").val("top")		
		$("#tickph").val("bottom")		
		var def = "bottom"
	}
	else{
		$("#tickps_txt").html(" Left")
		$("#tickph_txt").html(" Right")	
		$("#tickph").val("right")		
		$("#tickps").val("left")
		var def = "left"		
	}
	    
  	if("side" in axis_data){
		def = axis_data["side"]	
	}
	$("input[name=tickpos_show][value=" + def + "]").prop('checked', true);

 	if("tickfont" in axis_data){
		//typeface
		if("family" in axis_data["tickfont"]){
			$('#tf_ticks').val(axis_data["tickfont"]["family"])
		}
		else{
			$('#tf_ticks').val("")
		}
		//font size		
		if("size" in axis_data["tickfont"]){
			$('#font-axis-ticks').val(axis_data["tickfont"]["size"])
		}
		else{
			$('#font-axis-ticks').val("12")
			
		}
		//font color		
		if("color" in axis_data["tickfont"]){
			$('#color-ticks').val(axis_data["tickfont"]["color"])
			$('#img-color-ticks').css("background-color", axis_data["tickfont"]["color"])
			
		}
		else{
			$('#color-ticks').val("#000000")
			$('#img-color-ticks').css("background-color", "#000000")					
			}
	}
	else{
		$('#tf_ticks').val("")		
		$('#font-axis-ticks').val("12")
		$('#color-ticks').val("#000000")
		$('#img-color-ticks').css("background-color", "#000000")		
	}
			
	//angle	
	if("tickangle" in axis_data){
		$('#tick-angle').val(axis_data["tickangle"])
	}
	else{
		$('#tick-angle').val("")	
	}	

}

function lines_defaults(axis_data, axis){
	var dom = document.getElementById('chartContainer');
	//axis line show/hide
	if("showline" in axis_data){
		if(axis_data["showline"]){
			document.getElementById('axiss').checked=true
			document.getElementById('axish').checked=false
			$("#axis_show_line").show()
		}
		else{
			document.getElementById('axiss').checked=false
			document.getElementById('axish').checked=true
			$("#axis_show_line").hide()
		}			
	}
	else{
		document.getElementById('axiss').checked=false
		document.getElementById('axish').checked=true
		$("#axis_show_line").hide()			
	}
	// axis thickness
	if("linewidth" in axis_data){
		$('#axis-thick').val(axis_data["linewidth"])
	}
	else{
		$('#axis-thick').val("1")	
	}
	//	axis color		
	if("linecolor" in axis_data){
		$('#color-axis').val(axis_data["linecolor"])
		$('#img-color-axis').css("background-color", axis_data["linecolor"])		
	}
	else{
		$('#color-axis').val("#000000")
		$('#img-color-axis').css("background-color", "#000000")		
	}
	//grid lines show/hide
	if("showgrid" in axis_data){
		if(axis_data["showgrid"]){
			document.getElementById('grids').checked=true
			document.getElementById('gridh').checked=false
			$("#grid_show_line").show()
		}
		else{
			document.getElementById('grids').checked=false
			document.getElementById('gridh').checked=true
			$("#grid_show_line").hide()
		}			
	}
	else{
		document.getElementById('grids').checked=true
		document.getElementById('gridh').checked=false
		$("#grid_show_line").show()			
	}		
	// grid thickness
	if("gridwidth" in axis_data){
		$('#grid-thick').val(axis_data["gridwidth"])
	}
	else{
		$('#grid-thick').val("1")	
	}
	//grid color
	if("gridcolor" in axis_data){
		$('#color-grid').val(axis_data["gridcolor"])
		$('#img-color-grid').css("background-color", axis_data["gridcolor"])		
	}
	else{
		$('#color-grid').val("#EBF0F8")
		$('#img-color-grid').css("background-color", "#EBF0F8")		
	}
	//grid spacing auto/custom
	if("tickmode" in axis_data){
		if(axis_data["tickmode"]=="auto"){
			document.getElementById('autog').checked=true
			document.getElementById('customg').checked=false
			$("#grid_sp").hide()
		}
		else{
			document.getElementById('autog').checked=false
			document.getElementById('customg').checked=true
			//step size and step offset
			var fmt = ""
			var gsizediv = document.getElementById("stepsize")
			gsizediv.innerHTML=""
			var node = document.createElement("input");
			node.setAttribute("type", "number");
			node.id = "gridsizeinput";			
			if(axis_data["type"]=="date"){
				fmt = "date"
				$("#stepoff_div").hide()
				node.setAttribute("class", "cp-dates");				
				node.setAttribute("style", "width:80px !important");
				node.setAttribute("step", "0.1");
				var ms = 3600000
			}
			else{
				node.setAttribute("step", "any");				
				node.setAttribute("class", "cp-grid-size");
				var ms = 1
				
				var goffdiv = document.getElementById("stepoff")
				goffdiv.innerHTML=""	
				//create input element
				var nodeoff = document.createElement("input");
				nodeoff.setAttribute("type", "number");
				nodeoff.id = "gridoffinput";
				nodeoff.setAttribute("class", "cp-grid-offset");	
				nodeoff.setAttribute("step", "any");
				goffdiv.appendChild(nodeoff)
				if("tick0" in axis_data){
					$('#gridoffinput').val(axis_data["tick0"])
				}
				else{
					$('#gridoffinput').val("")	
				}					
				$("#stepoff_div").show()				
				
			}
			
			gsizediv.appendChild(node)
			if(fmt=="date"){
				node = document.createElement("span");
				node.innerHTML = "hours"
				gsizediv.appendChild(node)			
			}
			if("dtick" in axis_data){

				$('#gridsizeinput').val(axis_data["dtick"]/ms)
			}
			else{

				$('#gridsizeinput').val("")	
			}			
			grid_spacing_jq(dom, axis, fmt)			
			$("#grid_sp").show()			
		}			
	}
	else{
		document.getElementById('autog').checked=true
		document.getElementById('customg').checked=false
		$("#grid_sp").hide()			
	}	

	//zero line show/hide
	if("zeroline" in axis_data){
		if(axis_data["zeroline"]){
			document.getElementById('zeros').checked=true
			document.getElementById('zeroh').checked=false
			$("#zero_line_show").show()
		}
		else{
			document.getElementById('zeros').checked=false
			document.getElementById('zeroh').checked=true
			$("#zero_line_show").hide()
		}			
	}
	else{
		document.getElementById('zeros').checked=true
		document.getElementById('zeroh').checked=false
		$("#zero_line_show").show()			
	}		
	//line thickness
	if("zerolinewidth" in axis_data){
		$('#zerol-thick').val(axis_data["zerolinewidth"])
	}
	else{
		$('#zerol-thick').val("1")	
	}
	//line color
	if("zerolinecolor" in axis_data){
		$('#color-zerol').val(axis_data["zerolinecolor"])
		$('#img-color-zerol').css("background-color", axis_data["zerolinecolor"])		
	}
	else{
		$('#color-zerol').val("#000000")
		$('#img-color-zerol').css("background-color", "#000000")		
	}	
}

function title_defaults(axis_data){
	if("title" in axis_data){
		//title text
		if("text" in axis_data["title"]){
			$('#axis-title-text').find('textarea').val(axis_data["title"]["text"])
		}
		else{
			$('#axis-title-text').find('textarea').val("")
		}
		
		//title font
		if("font" in axis_data["title"]){
			if("family" in axis_data["title"]["font"]){
				$('#tf_axis').val(axis_data["title"]["font"]["family"])
			}
			else{
				$('#tf_axis').val("")
			}
			if("size" in axis_data["title"]["font"]){
				$('#font-axis-title').val(axis_data["title"]["font"]["size"])
			}
			else{
				$('#font-axis-title').val("12")
				
			}
			if("color" in axis_data["title"]["font"]){
				$('#tcolor-axis').val(axis_data["title"]["font"]["color"])
				$('#img-tcolor-axis').css("background-color", axis_data["title"]["font"]["color"])
				
			}
			else{
				$('#tcolor-axis').val("#000000")
				$('#img-tcolor-axis').css("background-color", "#000000")					
			}
		}
		else{
			$('#tf_axis').val(axis_data["title"][""])
			$('#tf_axis').val("")
			$('#font-axis-title').val("12")
			$('#tcolor-axis').val("#000000")
			$('#img-tcolor-axis').css("background-color", "#000000")				
		}		
	}else{
		//defaults
		$('#axis-title-text').find('textarea').val("")
		$('#tf_axis').val("")
		$('#font-axis-title').val("12")
		$('#tcolor-axis').val("#000000")
		$('#img-tcolor-axis').css("background-color", "#000000")			
	}	
	
}


  $("input[type='radio'][name='legend_sel']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	
    if($(this).val()=="show")
    {
      $("#leg_show").show();
		curr_layout['showlegend'] = true
		var layout = curr_layout  
	  //var layout = {showlegend: true};
    }
    else
    {
      $("#leg_show").hide();
	  curr_layout['showlegend'] = false
	  var layout = curr_layout 	  
	 // var layout = {showlegend: false};
    }
	
  Plotly.update(dom, {}, layout);	
	
  });  

  $("input[type='radio'][name='grid_show']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	var axis = which_axis()
	
	for(var i=0;i<axis.length;i++){
			
		if($(this).val()=="show")
			{
			  $("#grid_show_line").show();
			  toshow = true
			}
			else
			{
			  $("#grid_show_line").hide();
			  toshow = false
			}
			
			if(curr_layout[axis[i]+"axis"]==null){
				curr_layout[axis[i]+"axis"]={}
			}		
			curr_layout[axis[i]+"axis"]['showgrid'] = toshow
	}
	
	  Plotly.update(dom, {}, curr_layout);

	
  });

  $("input[type='radio'][name='tickl_show']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	var axis = which_axis()
	
	for(var i=0;i<axis.length;i++){
			
		if($(this).val()=="show")
			{
			  $("#ticklabels_show").show();
			  toshow = true
			}
			else
			{
			  $("#ticklabels_show").hide();
			  toshow = false
			}
			
			if(curr_layout[axis[i]+"axis"]==null){
				curr_layout[axis[i]+"axis"]={}
			}		
			curr_layout[axis[i]+"axis"]['showticklabels'] = toshow
	}
	
	  Plotly.update(dom, {}, curr_layout);

	
  });

  $("input[type='radio'][name='axis_show']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	var axis = which_axis()
	
	for(var i=0;i<axis.length;i++){
			
		if($(this).val()=="show")
			{
			  $("#axis_show_line").show();
			  toshow = true
			}
			else
			{
			  $("#axis_show_line").hide();
			  toshow = false
			}
			
			if(curr_layout[axis[i]+"axis"]==null){
				curr_layout[axis[i]+"axis"]={}
			}		
			curr_layout[axis[i]+"axis"]['showline'] = toshow

	}
	
	  Plotly.update(dom, {}, curr_layout);
  });

  $("input[type='radio'][name='zerol_show']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	var axis = which_axis()
	
	for(var i=0;i<axis.length;i++){
			
		if($(this).val()=="show")
			{
			  $("#zero_line_show").show();
			  toshow = true
			}
			else
			{
			  $("#zero_line_show").hide();
			  toshow = false
			}
			
			if(curr_layout[axis[i]+"axis"]==null){
				curr_layout[axis[i]+"axis"]={}
			}		
			curr_layout[axis[i]+"axis"]['zeroline'] = toshow

	}
	
	  Plotly.update(dom, {}, curr_layout);
  });

  $("input[type='radio'][name='tickpos_show']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout

	var axis = which_axis()
	for(var i=0;i<axis.length;i++){	
		if(curr_layout[axis[i]+"axis"]==null){
			curr_layout[axis[i]+"axis"]={}
		}
		curr_layout[axis[i]+"axis"]['side'] = $(this).val()

	}
	Plotly.update(dom, {}, curr_layout);		
  }); 



function grid_spacing_jq(dom, axis, fmt=""){
	if(fmt=="date"){
		$("#gridsizeinput").on("change", function () {
			var val_h = $("#gridsizeinput").val()
			var val_ms = val_h*3600000
			var update = {}
			update[axis+'axis'] = {
					'tickmode' : 'linear',
					'tick0' : 0,
					'dtick' : val_ms
				}


			Plotly.relayout(dom, update)
		});		
	}
	else{
		$("#gridoffinput").on("change", function () {
			var update = {}
			update[axis+'axis'] = {
					'tickmode' : 'linear',
					'tick0' : $("#gridoffinput").val(),
					'dtick' : $("#gridsizeinput").val()
				}


			Plotly.relayout(dom, update)
		});

		$("#gridsizeinput").on("change", function () {
			if($("#gridoffinput").val()!=null){
				var tick0 = $("#gridoffinput").val()
			}
			else{
				var tick0 = curr_layout[axis+"axis"]['tick0']
				if(tick0 == null){tick0 = 0}
			}
			var update = {}
			update[axis+'axis'] = {
					'tickmode' : 'linear',
					'tick0' : tick0,
					'dtick' : $("#gridsizeinput").val()
				}


			Plotly.relayout(dom, update)
		});		
		
	}
	
}


  //grid spacing layout update
  $("input[type='radio'][name='grid_spacing']").change(function(){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	var axis = $("input[type='radio'][name='axis_sel']:checked").val()

			
	if($(this).val()=="auto")
		//creazione input e set valori di default
		{
		  $('#grid_sp').hide()
			//autoset grid spacing e grid step
 			if(curr_layout[axis+"axis"]==null){
				curr_layout[axis+"axis"]={}
			}			

/*			//curr_layout[axis+"axis"]['range'] = null*/
			Plotly.relayout(dom, axis+'axis.tickmode', "auto")
//			Plotly.update(dom, {}, curr_layout); 		  
		  //toshow = true
		}
		else
		{
			$('#grid_sp').show()

			var tickmode = curr_layout[axis+"axis"]['tickmode']
			var gsizediv = document.getElementById("stepsize")
			gsizediv.innerHTML=""
			//var gsizeval = curr_layout[axis+"axis"]['dtick']
			if($("#rangetype").val() == "date"){
				$("#stepoff_div").hide()
				//create input element
				var node = document.createElement("input");
				node.setAttribute("type", "number");
				node.id = "gridsizeinput";
				node.setAttribute("class", "cp-dates");				
				node.setAttribute("style", "width:80px !important");
				node.setAttribute("step", "0.1");				
				node.setAttribute("value", "");
				gsizediv.appendChild(node)
				
				node = document.createElement("span");
				node.innerHTML = "hours"
				gsizediv.appendChild(node)				
				grid_spacing_jq(dom, axis, "date")
				
			}else{
				var goffdiv = document.getElementById("stepoff")
				goffdiv.innerHTML=""
				//var goffval = curr_layout[axis+"axis"]['tick0']				
				//create input element
				var node = document.createElement("input");
				node.setAttribute("type", "number");
				node.id = "gridoffinput";
				node.setAttribute("value", "");
				node.setAttribute("class", "cp-grid-offset");	
				node.setAttribute("step", "any");
				goffdiv.appendChild(node)	

				var node = document.createElement("input");
				node.setAttribute("type", "number");
				node.id = "gridsizeinput";
				node.setAttribute("value", "");
				node.setAttribute("step", "any");				
				node.setAttribute("class", "cp-grid-size");				
				gsizediv.appendChild(node)
				grid_spacing_jq(dom, axis)
				
				$("#stepoff_div").show()
			}
		}
  });

function set_font(s, section, tag, object=""){

//  console.log(s)
  var dom = document.getElementById('chartContainer');  
  switch(section){
      //TAB GENERAL SETTINGS  
    case "all":
      var curr_layout = dom.layout
      //title
      if(curr_layout['title'] != null){
        if(curr_layout['title']['font'] != null){
          curr_layout['title']['font'][tag] = s
        }
        else{
          curr_layout['title']['font'] = {}
          curr_layout['title']['font'][tag] = s          
        }
      }
      else{
        curr_layout['title']={}
        curr_layout['title']['font']={}
        curr_layout['title']['font'][tag] = s        
      }

      //xaxis           
      var curr_x = curr_layout['xaxis']
      if(curr_x['title'] != null){
        if(curr_x['title']['font'] != null){
          curr_x['title']['font'][tag] = s
        }
        else{
          curr_x['title']['font'] = {}
          curr_x['title']['font'][tag] = s 
        }
      }
      else{
        curr_x['title']={}
        curr_x['title']['font']={}
        curr_x['title']['font'][tag] = s         
      }
      if(curr_x['tickfont'] != null){
        curr_x['tickfont'][tag] = s
      }
      else{
        curr_x['tickfont'] = {}
        curr_x['tickfont'][tag] = s        
      }      
      curr_layout['xaxis'] = curr_x

      //yaxis       
      var curr_y = curr_layout['yaxis']
      if(curr_y['title'] != null){
        if(curr_y['title']['font'] != null){
          curr_y['title']['font'][tag] = s
        }
        else{
          curr_y['title']['font'] = {}
          curr_y['title']['font'][tag] = s 
        }
      }
      else{
        curr_y['title']={}
        curr_y['title']['font']={}
        curr_y['title']['font'][tag] = s         
      }
      if(curr_y['tickfont'] != null){
        curr_y['tickfont'][tag] = s
      }
      else{
        curr_y['tickfont'] = {}
        curr_y['tickfont'][tag] = s        
      }      
      curr_layout['yaxis'] = curr_y      

      //legend
      if(curr_layout['legend'] == null){
		var curr_leg = {}
      }
      else{
        var curr_leg = curr_layout['legend']
      }      

      if(curr_leg['title'] != null){
        if(curr_leg['title']['font'] != null){
          curr_leg['title']['font'][tag] = s
        }          
        else{
          curr_leg['title']['font'] = {}
          curr_leg['title']['font'][tag] = s 
        }
      }
      else{
        curr_leg['title'] = {}
        curr_leg['title']['font']={}
        curr_leg['title']['font'][tag] = s         
      }        

      if(curr_leg['font'] != null){
        curr_leg['font'][tag] = s
      }
      else{
        curr_leg['font'] = {}
        curr_leg['font'][tag] = s         
      }

      curr_layout['legend'] = curr_leg   
      var layout = curr_layout

	  //update all related form fields
	  switch(tag){
		case "family":
			$("#tf_title").val(s)
			$("#tf_axis").val(s)
			$("#tf_ticks").val(s)
			$("#tf_lg_title").val(s)
			$("#tf_lg_text").val(s)
			break;
		case "size":
			$("#title_fsize").val(s)
			$("#font-axis-title").val(s)
			$("#font-axis-ticks").val(s)
			$("#font-legend-text").val(s)
			$("#font-legend-title").val(s)
			break;
		case "color":
			$("#color-title").val(s)
			$("#tcolor-axis").val(s)
			$("#color-ticks").val(s)
			$("#tcolor-legend").val(s)
			$("#color-legend").val(s)			
			
			$("#img-color-title").css("background-color",s)
			$("#img-tcolor-axis").css("background-color",s)
			$("#img-color-ticks").css("background-color",s)
			$("#img-tcolor-legend").css("background-color",s)
			$("#img-color-legend").css("background-color",s)
			break;			
	  }

	  
      break;
      //TITLE IN GENERAL SETTINGS      
    case "title": 

      var curr_layout = dom.layout
      //title
      if(curr_layout['title'] != null){
        if(curr_layout['title']['font'] != null){
          curr_layout['title']['font'][tag] = s
        }
        else{
          curr_layout['title']['font'] = {}
          curr_layout['title']['font'][tag] = s          
        }
      }
      else{
        curr_layout['title']={}
        curr_layout['title']['font']={}
        curr_layout['title']['font'][tag] = s        
      }      

      var layout=curr_layout

      break;      

      //TAB AXES      
    case "axis":
      var chkval = $("input[type='radio'][name='axis_sel']:checked").val()
      var curr_layout = dom.layout

      switch(chkval){
        case "all":
          var curr_x = curr_layout['xaxis']
          var curr_y = curr_layout['yaxis'] 

          if(object=="titles"){         
            //xaxis           

            if(curr_x['title'] != null){
              if(curr_x['title']['font'] != null){
                curr_x['title']['font'][tag] = s
              }
              else{
                curr_x['title']['font'] = {}
                curr_x['title']['font'][tag] = s 
              }
            }
            else{
              curr_x['title']={}
              curr_x['title']['font']={}
              curr_x['title']['font'][tag] = s         
            }


            //yaxis       

            if(curr_y['title'] != null){
              if(curr_y['title']['font'] != null){
                curr_y['title']['font'][tag] = s
              }
              else{
                curr_y['title']['font'] = {}
                curr_y['title']['font'][tag] = s 
              }
            }
            else{
              curr_y['title']={}
              curr_y['title']['font']={}
              curr_y['title']['font'][tag] = s         
            }

          }          
          else if(object=="ticks"){
            //xticks
            if(curr_x['tickfont'] != null){
              curr_x['tickfont'][tag] = s
            }
            else{
              curr_x['tickfont'] = {}
              curr_x['tickfont'][tag] = s        
            }      
            //yticks
            if(curr_y['tickfont'] != null){
              curr_y['tickfont'][tag] = s
            }
            else{
              curr_y['tickfont'] = {}
              curr_y['tickfont'][tag] = s        
            }             
          }
          curr_layout['xaxis'] = curr_x
          curr_layout['yaxis'] = curr_y           

          break;
        case "x":
          var curr_x = curr_layout['xaxis']
          if(object=="titles"){
            if(curr_x['title'] != null){
              if(curr_x['title']['font'] != null){
                curr_x['title']['font'][tag] = s
              }
              else{
                curr_x['title']['font'] = {}
                curr_x['title']['font'][tag] = s 
              }
            }
            else{
              curr_x['title']={}
              curr_x['title']['font']={}
              curr_x['title']['font'][tag] = s         
            }

          }
          else if(object=="ticks"){
            if(curr_x['tickfont'] != null){
              curr_x['tickfont'][tag] = s
            }
            else{
              curr_x['tickfont'] = {}
              curr_x['tickfont'][tag] = s        
            }
          }
          curr_layout['xaxis'] = curr_x          
          break;
        case "y":
          var curr_y = curr_layout['yaxis']
          if(object=="titles"){
            if(curr_y['title'] != null){
              if(curr_y['title']['font'] != null){
                curr_y['title']['font'][tag] = s
              }
              else{
                curr_y['title']['font'] = {}
                curr_y['title']['font'][tag] = s 
              }
            }
            else{
              curr_y['title']={}
              curr_y['title']['font']={}
              curr_y['title']['font'][tag] = s         
            }

          }
          else if(object=="ticks"){
            if(curr_y['tickfont'] != null){
              curr_y['tickfont'][tag] = s
            }
            else{
              curr_y['tickfont'] = {}
              curr_y['tickfont'][tag] = s        
            }
          }
          curr_layout['yaxis'] = curr_y
          break;          
      }
      var layout=curr_layout      
      break;      


    case "legend":
      var curr_layout = dom.layout
      if(curr_layout['legend'] == null){
		var curr_leg = {}
      }
      else{
        var curr_leg = curr_layout['legend']
      }
      
      if(object=="title"){
        if(curr_leg['title'] != null){
          if(curr_leg['title']['font'] != null){
            curr_leg['title']['font'][tag] = s
          }          
          else{
            console.log("TITLE FONT NULL")
            //curr_leg['title'] = {"text" : "CIAO"}              
            curr_leg['title'] = {}              
            curr_leg['title']['font'] = {}
            curr_leg['title']['font'][tag] = s 
          }
        }
        else{
          curr_leg['title'] = {}
          curr_leg['title']['font']={}
          curr_leg['title']['font'][tag] = s
        }        
      }     
      else if(object=="text"){            
        if(curr_leg['font'] != null){
          curr_leg['font'][tag] = s
        }
        else{
          curr_leg['font'] = {}
          curr_leg['font'][tag] = s         
        }
      }

      curr_layout['legend'] = curr_leg     
      var layout=curr_layout       
      break;
  }      
  Plotly.update(dom, {}, layout);
}





/* QUESTA VA BENE PER LINE

function set_border(s,elem,tag){
	var dom = document.getElementById('chartContainer');	
	const traceid = document.getElementById('tracelist').value	
	var fulltrace = dom.data[traceid]
	console.log(fulltrace)
	var settings = fulltrace[elem]
	if(settings != null){
		if(elem == "marker"){
			if(settings["line"] == null){
				settings["line"] = {}
			}
		}
	}
	else{
		settings = {}
		settings["line"] = {}	
	}
	settings["line"][tag] = s
	settings["line"]["color"] = "#FF0000"	

	Plotly.restyle(dom, settings, traceid);	
} */

function apply_color(object, newcolor, tochange, dataelem = null){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	switch(object){
		case "bg":
			{
				curr_layout['plot_bgcolor'] = newcolor
				Plotly.update(dom, {}, curr_layout);
				break;
			}
		case "margins":
			{
				curr_layout['paper_bgcolor'] = newcolor
				Plotly.update(dom, {}, curr_layout);
				break;
			}
		case "grid":
			{
				var axis = which_axis()
				for(var i=0;i<axis.length;i++){
					if(curr_layout[axis[i]+"axis"]==null){
						curr_layout[axis[i]+"axis"]={}
					}
					curr_layout[axis[i]+"axis"]['gridcolor'] = newcolor
				}

				Plotly.update(dom, {}, curr_layout);				
				break;
			}
		case "bordercolor":
			{
				curr_layout['legend']['bordercolor'] = newcolor
				Plotly.update(dom, {}, curr_layout);
				break;
			}
		case "lg-bg":
			{
				curr_layout['legend']['bgcolor'] = newcolor
				Plotly.update(dom, {}, curr_layout);
				break;
			}
		case "axisline":
			{
				var axis = which_axis()
				for(var i=0;i<axis.length;i++){
					if(curr_layout[axis[i]+"axis"]==null){
						curr_layout[axis[i]+"axis"]={}
					}
					curr_layout[axis[i]+"axis"]['linecolor'] = newcolor
				}				

				Plotly.update(dom, {}, curr_layout);
				break;
			}
		case "zerol":
			{
				var axis = which_axis()
				for(var i=0;i<axis.length;i++){
					if(curr_layout[axis[i]+"axis"]==null){
						curr_layout[axis[i]+"axis"]={}
					}
					curr_layout[axis[i]+"axis"]['zerolinecolor'] = newcolor
				}				

				Plotly.update(dom, {}, curr_layout);
				break;
			}
		case "ticks":
			{
				var axis = which_axis()
				for(var i=0;i<axis.length;i++){
					if(curr_layout[axis[i]+"axis"]==null){
						curr_layout[axis[i]+"axis"]={}
					}
					if(curr_layout[axis[i]+"axis"]['tickfont']==null){
						curr_layout[axis[i]+"axis"]['tickfont']={}
					}					
					curr_layout[axis[i]+"axis"]['tickfont']['color'] = newcolor
				}				

				Plotly.update(dom, {}, curr_layout);
				break;
			}		
		case "tr-markers":{
			
			var fulltrace = dom.data[dataelem]
			var lineset = fulltrace["line"]
			if(lineset != null){
				var linecolor = lineset["color"]
				if(linecolor == null){
					var d3colors = Plotly.d3.scale.category10().domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);;
					var def_color = d3colors(dataelem)						
				}
				else{
					var def_color = linecolor
				}
			}
		
			
			var update = {
				'marker.color': newcolor,
				'line.color' : def_color
			}
			Plotly.restyle(dom, update, dataelem);

			break;
		}
		case "tr-markers-border":{
			var fulltrace = dom.data[dataelem]
			console.log(fulltrace)
			var lineset = fulltrace["line"]
			if(lineset != null){
				var linecolor = lineset["color"]
				if(linecolor == null){
					var d3colors = Plotly.d3.scale.category10().domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);;
					var def_color = d3colors(dataelem)						
				}
				else{
					var def_color = linecolor
				}
			}
			var settings
			var marker = fulltrace["marker"]
			if(marker == null){
				settings = {"line" : {}}
			}
			else{
				if(marker["line"]){
					marker["line"] = {}
				}
				settings = marker
			}
			settings["line"].color = newcolor
			
			
			var update = {
				'marker' : settings
			}
			Plotly.restyle(dom, update, dataelem);			
			break;
			
		}
		case "tr-lines":{
			var fulltrace = dom.data[dataelem]
 			var lineset = fulltrace["line"]
			if(lineset != null){
				lineset.color = newcolor
				settings = lineset
			}
			else{
				settings={"color" : newcolor}
			}
		
			
			var update = {
				'line': settings
			}
			Plotly.restyle(dom, update, dataelem);

			break;
		}
		case "tr-text":{
			var fulltrace = dom.data[dataelem]
 			var fontset = fulltrace["textfont"]
			if(fontset != null){
				fontset.color = newcolor
				settings = fontset
			}
			else{
				settings={"color" : newcolor}
			}
			var update = {
				'textfont': settings
			}
			Plotly.restyle(dom, update, dataelem);			
			break;
		}
		
		default:
			{
				set_font(newcolor, tochange, 'color',object)
			}
	
	}	
	
}

$(document).ready(function(){
	document.querySelectorAll('.color-pick').forEach(item => {
		item.addEventListener("input", function(event) {
		  change_color(item,event);
		});

	})
	
})

function change_color(item,event){

	//console.log(dom, curr_layout)
	
	//what to change (all,legend, thicks, bg, margins, grid...)
	var object = item.getAttribute("data-change")
	var dataelem = item.getAttribute("data-elem")
	var id = item.id
	var idsplt = id.split("-")
	var tochange = idsplt[2]
	var newcolor = event.target.value
	$("#"+idsplt[1]+"-"+tochange).val(newcolor);
	item.setAttribute("style","background-color : "+newcolor)
	apply_color(object, newcolor, tochange,dataelem)	

}

function change_color_from_text(item){
	var object = item.getAttribute("data-change")
	var dataelem = item.getAttribute("data-elem")	
	var newcolor = item.value
	var id = item.id
	var idarr = id.split("-")
	var idsplt = idarr[1]
	$("#img-"+idarr[0]+"-"+idsplt).css("background-color",newcolor)
	apply_color(object, newcolor, idsplt,dataelem)	
}





// Update the current slider value (each time you drag the slider handle)
document.getElementById("hslider").oninput = function() {
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	
	document.getElementById("listenSlider2").value = this.value;
	curr_layout['title']['x'] = this.value/100
	Plotly.update(dom, {}, curr_layout);	
}

document.getElementById("listenSlider2").oninput = function() {
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout
	
	document.getElementById("hslider").value = this.value;
	if(curr_layout['title']==null){
		curr_layout['title'] = {}
	}
	curr_layout['title']['x'] = this.value/100
	Plotly.update(dom, {}, curr_layout);	
}

// Update points opacity slider
/* document.getElementById("slider-p-opac").oninput = function() {
	var dom = document.getElementById('chartContainer');
	const traceid = document.getElementById('tracelist').value
	document.getElementById("p-opac").value = this.value;	
	var update = {
		opacity: this.value/100
	};	
} */




function set_text(val, elem){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout

	switch(elem){
		case "title":{
			if(curr_layout['title']==null){
				curr_layout['title'] = {}
			}
			curr_layout['title']['text'] = val
			Plotly.update(dom, {}, curr_layout);
			break;
		}
		case "legend":{
			if(curr_layout['legend']==null){
				curr_layout['legend'] = {}
				curr_layout['legend']['title'] = {}
			}
			else{
				if(curr_layout['legend']['title']==null){curr_layout['legend']['title'] = {}}
				
			}
			
			curr_layout['legend']['title']['text'] = val
			Plotly.update(dom, {}, curr_layout);
			break;
		}
		case "axes":{
			var chkval = $("input[type='radio'][name='axis_sel']:checked").val()

			if(curr_layout[chkval+"axis"]==null){
				curr_layout[chkval+"axis"]={}
			}
			if(curr_layout[chkval+"axis"]['title']==null){
				curr_layout[chkval+"axis"]['title']={}
			}
			curr_layout[chkval+"axis"]['title']['text'] = val

			Plotly.update(dom, {}, curr_layout);

			break;
		}
		default :{
			dom.data[elem]["name"] = val
			Plotly.update(dom, {}, curr_layout);			
			break;
		}
		
	}
	
}


function set_thickness(val, item){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout	
	switch(item){
		case "legend":{
			var legend = curr_layout['legend']
			if(legend == null){
				curr_layout['legend'] = {}
			}
			curr_layout['legend']['borderwidth'] = val
			break;
		}
		case "grid":{
			var axis = which_axis()
			for(var i=0;i<axis.length;i++){
				if(curr_layout[axis[i]+"axis"]==null){
					curr_layout[axis[i]+"axis"]={}
				}
				curr_layout[axis[i]+"axis"]['gridwidth'] = val
			}
			break;
		}		
		case "axis":{
			var axis = which_axis()
/* 			var chkval = $("input[type='radio'][name='axis_sel']:checked").val()
		
			if(chkval=="all"){
				var axis = ["x","y"]
			}
			else{
				var axis = [chkval]
			} */
			for(var i=0;i<axis.length;i++){
				if(curr_layout[axis[i]+"axis"]==null){
					curr_layout[axis[i]+"axis"]={}
				}
				curr_layout[axis[i]+"axis"]['linewidth'] = val
			}
			break;
		}
		case "zerol":{
			var axis = which_axis()
/* 			var chkval = $("input[type='radio'][name='axis_sel']:checked").val()
		
			if(chkval=="all"){
				var axis = ["x","y"]
			}
			else{
				var axis = [chkval]
			} */
			for(var i=0;i<axis.length;i++){
				if(curr_layout[axis[i]+"axis"]==null){
					curr_layout[axis[i]+"axis"]={}
				}
				curr_layout[axis[i]+"axis"]['zerolinewidth'] = val
			}
			break;
		}			
		
		
	}

	Plotly.update(dom, {}, curr_layout);	
}

function set_angle(val){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout	
	var axis = which_axis()

	for(var i=0;i<axis.length;i++){
		if(curr_layout[axis[i]+"axis"]==null){
			curr_layout[axis[i]+"axis"]={}
		}
		curr_layout[axis[i]+"axis"]['tickangle'] = val
	}	
	Plotly.update(dom, {}, curr_layout);	
}

function set_rangetype(val){
	var dom = document.getElementById('chartContainer');
	var curr_layout = dom.layout	
	var axis = which_axis()

	for(var i=0;i<axis.length;i++){
		if(curr_layout[axis[i]+"axis"]==null){
			curr_layout[axis[i]+"axis"]={}
		}
		curr_layout[axis[i]+"axis"]['type'] = val
		curr_layout[axis[i]+"axis"]['autorange'] = true
		//delete curr_layout[axis[i]+"axis"]['range']
		document.getElementById('autor').checked=true
		document.getElementById('customr').checked=false
		$("#range_lim").hide()

	}	
			console.log(curr_layout)
	Plotly.update(dom, {}, curr_layout);	
}


function which_axis(){
	var chkval = $("input[type='radio'][name='axis_sel']:checked").val()

	if(chkval=="all"){
		var axis = ["x","y"]
	}
	else{
		var axis = [chkval]
	}	
	return axis
}


//COMMON FUNCTIONS


//GENERAL FUNCTIONS





//TRACE FUNCTIONS
function fill_area(val){
	var dom = document.getElementById('chartContainer');	
	const traceid = document.getElementById('tracelist').value	
	var fulltrace = dom.data[traceid]
		console.log(fulltrace)
	var update = {
		'fill' : val
		
	}
	Plotly.restyle(dom, update, traceid);	
}


function set_size(s, elem){
	var dom = document.getElementById('chartContainer');	
	const traceid = document.getElementById('tracelist').value
	var fulltrace = dom.data[traceid]
	var settings = fulltrace[elem]
	if(settings == null){
		settings = {}
	}

	switch(elem){
		case "marker":{
//			var tag = "size"
			settings.size = s
			break;
		}
		case "line":{
//			var tag = "width"
			settings.width = s
			break;
		}		
	}
	
	var update = {}
	update[elem] = settings
	Plotly.restyle(dom, update, traceid);

}


function set_border(s,elem,tag){
	var dom = document.getElementById('chartContainer');	
	const traceid = document.getElementById('tracelist').value	
	var fulltrace = dom.data[traceid]
	var settings = fulltrace[elem]
	if(settings != null){
		if(elem == "marker"){
			if(settings["line"] == null){
				settings["line"] = {}
			}
		}
	}
	else{
		settings = {}
		settings["line"] = {}	
	}
	settings["line"][tag] = s
	//settings["line"]["color"] = "#FF0000"	

	var update = {}
	if(elem == "marker"){
		update["marker"] = settings
	}
	else{
		update = settings
	}

	Plotly.restyle(dom, update, traceid);	
}

function set_opacity(elem,what){
	var dom = document.getElementById('chartContainer');
	const traceid = document.getElementById('tracelist').value
	var fulltrace = dom.data[traceid]
//	console.log(fulltrace)

	var val = elem.value
	var val2mod,valdiv,settings,update,def_color
	var id = elem.id

	if(!id.includes("slider")){
		val2mod = "slider-"+id
	}
	else{
		val2mod = id.replace("slider-","")
	}

	switch(what){
		case "points" : {
			valdiv = document.getElementById(val2mod)

			settings = fulltrace["marker"]
			if(settings == null){
				settings = {}
			}
			settings.opacity=val/100
			update = {
				"marker" : settings
			}
			break;
		}
		case "lines" : {
			valdiv = document.getElementById(val2mod)
			settings = fulltrace["line"]
			var d3colors = Plotly.d3.scale.category10().domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
			if(settings == null){
				settings = {}
				def_color = d3colors(traceid)
			}
			else{
				def_color = settings["color"]
				if(def_color==null){
					def_color = d3colors(traceid)
				}
				
				if(def_color.includes("rgba")){
					def_color = def_color.replace("rgba(","").replace(")","")
					console.log(def_color,"RGB")
					var def_arr = def_color.split(",")
					new_color = 'rgba('+def_arr[0]+','+def_arr[1]+','+def_arr[2]+','+val/100+')'
				}
				else{
					//convert to rgb
					var def_arr = hexToRgb(def_color)
					new_color = 'rgba('+def_arr.r+','+def_arr.g+','+def_arr.b+','+val/100+')'
					
				}

			}

			settings["color"] = new_color
			console.log(new_color)
			//lines has not "opacity". Change full trace opacity and reset marker opacity with rgba
 			var markerset = fulltrace["marker"]
			if(markerset == null){
				var mark_color = d3colors(traceid)
				markerset = {}
			}
			else{
				var mark_color = markerset["color"]
				if(mark_color == null){
					var mark_color = d3colors(traceid)
				}				
			}
			if(mark_color.includes("rgba")){
				mark_color = mark_color.replace("rgba(","").replace(")","")
				var def_arr = mark_color.split(",")
				var new_mcolor = 'rgba('+def_arr[0]+','+def_arr[1]+','+def_arr[2]+',1)'
			}
			else{
				//convert to rgb
				var def_arr = hexToRgb(mark_color)
				var new_mcolor = 'rgba('+def_arr.r+','+def_arr.g+','+def_arr.b+',1)'
			}
			markerset["color"] = new_mcolor

 			var update = {
				"line" : settings,
				"marker" : markerset
			};	
			break;
		}

	}
	valdiv.value = val
	//console.log(update)
	Plotly.restyle(dom, update, traceid);	 

}

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

function rgbToHex(r, g, b) {
  return "#" + (1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1);
}

function set_color(id, color, traceid = null){
	$("#"+id).val(color)
	$("#img-"+id).val(color)
	$("#img-"+id).attr("style","background-color : "+color)
	// set ids of trace divs	
	if(traceid!=null){
		$("#"+id).attr("data-elem",traceid)
		$("#img-"+id).attr("data-elem",traceid)		
	}
}

function set_trace_defaults(traceid, main_key, item, id, dval, multiplier=1, add_id=null){
	var dom = document.getElementById('chartContainer');
	var def_marker = dom.data[traceid][main_key]
	if(def_marker!=null){
		var stored = def_marker[item]
		if(stored!=null){
			if(!isNaN(stored)){
				dval = stored*multiplier
			}
			else{
				if(stored=="spline"){stored="linear"}	//missing default spline for scattergl
				dval = stored
			}
		}
	}
	$("#"+id).val(dval)
	if(add_id!=null){
		$("#"+add_id+"-"+id).val(dval)	
	}
	
}

function set_markerline_defaults(traceid, item, id, dval){
	var dom = document.getElementById('chartContainer');
	var fulltrace = dom.data[traceid]
	if("marker" in fulltrace){
		if("line" in fulltrace["marker"]){
			if(item in fulltrace["marker"]["line"]){
				dval = fulltrace["marker"]["line"][item]
			}
		}
	}
	$("#"+id).val(dval)
}

function build_trace_form(traceid){
	var dom = document.getElementById('chartContainer');
	var fulltrace = dom.data[traceid]
	//current name
	var currname = fulltrace["name"]

	//fill form with default or existing values
	//Name
	var trname = document.getElementById('tr-input-name');
	trname.setAttribute("oninput", "set_text(this.value, '"+traceid+"')");
	trname.value = currname
	
	// show/hide "display" box for trend and scatter
	$('#cp-tr-display').hide()
	var dis = set_display_box(dom.data[traceid], "tr")	
	if(dis){
		$('#cp-tr-display').show()
		$('#cp-tr-text').hide()		
	}
	else{
		$('#cp-tr-display').hide()
		$('#cp-tr-text').show()
	}


	//FALLISCE CON HISTOGRAM PERCHE' NON C'E' MODE
	//Display default settings

	document.getElementById("tr-p").checked = false;
	document.getElementById("tr-l").checked = false;
	document.getElementById("tr-t").checked = false;
	$("#cp-tr-markers").hide()	
	$("#cp-tr-lines").hide()	
	$("#cp-tr-text").hide()	
	var trmode = fulltrace["mode"]
	if(trmode != null){
		trmode = trmode.split("+")
		for(var i=0;i<trmode.length;i++){
			var curr_mode = trmode[i]
			var div, section
			switch(curr_mode){
				case "markers":
					{
						div = "tr-p"
						section = "cp-tr-markers"
						break;
					}
				case "lines":
					{
						div = "tr-l"
						section = "cp-tr-lines"
						break;
					}
				case "text":
					{
						div = "tr-t"
						section = "cp-tr-text"
						break;
					}				
			}
			document.getElementById(div).checked = true;	
			$("#"+section).show()	
		}
	}else{
		//histogram case
		$("#cp-tr-markers").show()
		$("#cp-tr-text").show()
		
	}
	
	//POINTS SECTION
	//Color
	var d3colors = Plotly.d3.scale.category10().domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
	// set ids of trace divs
/* 	$("#color-markers").attr("data-elem",traceid)
	$("#img-color-markers").attr("data-elem",traceid) */
	//set default color
	console.log(dom.data)
	var def_marker = fulltrace["marker"]
	var def_color
	if(def_marker!=null){
		if(def_marker["color"]!=null){
			def_color = def_marker["color"]
		}
		else{
			def_color = d3colors(traceid)
		}
	}
	else{
		//more than 10 colors will restart from first
		def_color = d3colors(traceid)
	}
	if(def_color.includes("rgba")){
		var rgb_arr = def_color.split(",")
		r = parseInt(rgb_arr[0].replace("rgba(",""))
		g = parseInt(rgb_arr[1])
		b = parseInt(rgb_arr[2])
		def_color = rgbToHex(r,g,b)
	}
/* 	$("#color-markers").val(def_color)
	$("#img-color-markers").val(def_color)
	$("#img-color-markers").attr("style","background-color : "+def_color) */
	set_color("color-markers",def_color, traceid)

	//Opacity
	set_trace_defaults(traceid, "marker", "opacity", "p-opac", 100, multiplier=100, add_id="slider")

	//Size
	set_trace_defaults(traceid, "marker", "size", "p-size", 6)

	//Border width
	var plot = fulltrace.type
	//different settings for bar plot
	var pborderval, postext
	if(plot=="histogram"){	
		pborderval = '2'
		postext = 'none'
	}
	else{
		pborderval = '0'
		postext = 'middle center'
	}
	set_markerline_defaults(traceid, "width", "p-border-width", pborderval)
	
	//Border color
	// set ids of borders trace divs
/* 	$("#color-markersb").attr("data-elem",traceid)
	$("#img-color-markersb").attr("data-elem",traceid) */
	var line_color = d3colors(traceid)
	if(def_marker!=null){
		var lineset = def_marker["line"]
		if(lineset != null){
			if(lineset["color"] != null){
				line_color = lineset["color"]
			}
		}
	}	
	set_color("color-markersb",line_color, traceid)
/* 	$("#color-markersb").val(line_color)
	$("#img-color-markersb").val(line_color)
	$("#img-color-markersb").attr("style","background-color : "+line_color)	 */

	//LINES SECTION
	//Width
	set_trace_defaults(traceid, "line", "width", "l-width", 2)
	//Opacity
	var def_line = fulltrace["line"]
	var def_lineopac = 1
	if(def_line != null){
		if("color" in def_line){
			var curr_color = def_line["color"]
			var cc_arr = curr_color.split(",")
			console.log(cc_arr.length)
			if(cc_arr.length == 4){
				def_lineopac = cc_arr[3].replace(")","")
			}
		}
	}
	$("#l-opac").val(def_lineopac*100)
	$("#slider-l-opac").val(def_lineopac*100)
	
	//Color
	//set ids for line color form
	set_color("color-lines",def_color, traceid)
/* 	$("#color-lines").val(def_color)
	$("#img-color-lines").val(def_color)
	$("#img-color-lines").attr("style","background-color : "+def_color)	 
	$("#color-lines").attr("data-elem",traceid)
	$("#img-color-lines").attr("data-elem",traceid)*/

	//Type
	set_trace_defaults(traceid, "line", "dash", "tr_line_type", "solid")
	
	//Shape
	set_trace_defaults(traceid, "line", "shape", "tr_line_shape", "linear")	
	
	//Connect gaps
	var gaps = fulltrace["connectgaps"]
	var def_gaps = false
	if(gaps!=null){
		def_gaps = gaps
	}
	$('#tr-connectgaps').prop("checked", def_gaps);
	//Fill to
	var fill = fulltrace["fill"]
	var def_fill = "none"
	if(fill!=null){
		def_fill = fill
	}	
	$('#tr_fill').val(def_fill)
	//TEXT SECTION
	set_trtext_defaults(traceid)

	//set ids for text color form
	$("#color-trtext").attr("data-elem",traceid)
	$("#img-color-trtext").attr("data-elem",traceid)	





/* 	//build symbol select box
	var symsel = document.getElementById('tr-marker_sym')
	//get list of symbols
	var isOpen = s => s.includes('-open')
	var isDot = s => s.includes('-dot')
	var isOpenDot = s => isOpen(s) && isDot(s)
	var isBase = s => !isOpen(s) && !isDot(s)	
	var symbolList = Plotly.PlotSchema.get()
	  .traces
	  .scatter
	  .attributes
	  .marker
	  .symbol
	  .values
	  .filter(s => typeof s === 'string')

	var symbols = symbolList.filter(isBase)
	for(var i=0; i<symbols.length;i++){
		var currsym = symbols[i]
		if(isNaN(currsym)){
			//build options
			//option da tradurre in svg. TODO in future???
			
		}
	}
	console.log(symbols) */
	$("#trace_set").show()	
}

function set_trtext_defaults(traceid){
	var dom = document.getElementById('chartContainer');
	var trace = dom.data[traceid]
	var trmode = dom.data[traceid]["mode"]
	if(trmode!=null){
		var bas_col = "#000000"
	}
	else{
		var bas_col = "#ffffff"
	}
	//Text position
	var textpos = trace["textposition"]
	if(textpos != null){
		$("#tr_pos_text").val(textpos)
	}
	else{
		$("#tr_pos_text").val("middle center")
	}
	//Text
	var txt = trace["text"]
	var val = ""
	if(txt != null){
		var xtxt = trace["x"]
		if(xtxt == txt){val = "x"}

		var ytxt = trace["y"]
		if(ytxt == txt){val = "y"}		
	
	}
	$("#tr_shown_text").val(val)
	
	//Textstyle
	var textstyle = trace["textfont"]
	if(textstyle != null){
		//Typeface
		var typeface = textstyle["family"]
		if(typeface != null){
			$("#tr_tf").val(typeface)
		}
		else{
			$("#tr_tf").val("")
		}
		//Font size
		var fontsize = textstyle["size"]
		if(fontsize != null){
			$("#tr_size").val(fontsize)
		}
		else{
			$("#tr_size").val("12")
		}		
		//Font color
		var fontcolor = textstyle["color"]
		if(fontcolor != null){
			$("#color-trtext").val(fontcolor)
			$("#img-color-trtext").css("background-color", fontcolor);
		}
		else{
			$("#color-trtext").val(bas_col)
			$("#img-color-trtext").css("background-color", bas_col);
		}		
	}
	else{
		$("#tr_tf").val("")		
		$("#tr_size").val("12")		
		$("#color-trtext").val(bas_col)
		$("#img-color-trtext").css("background-color", bas_col);
	}
}


function set_display_box(tracedata, prefix){
	var tr_type = tracedata.type
	var res, inputchk
	$("#cp-"+prefix+"-lines").hide()	
	$("#cp-"+prefix+"-markers").hide()	
	switch(tr_type){
		case "bar":
			{
				$("#cp-"+prefix+"-markers").show()
				res = false
				break;
			}		
		case "scattergl":
			{
				var tr_mode = tracedata.mode
				if(tr_mode.includes("lines")){
					inputchk = document.getElementById(prefix+'-l');
					inputchk.setAttribute("checked", "checked");
					$("#cp-"+prefix+"-lines").show()
				}
				else{
					$("#cp-"+prefix+"-lines").hide()	
				}
				if(tr_mode.includes("markers")){
					inputchk = document.getElementById(prefix+'-p');
					inputchk.setAttribute("checked", "checked");
					$("#cp-"+prefix+"-markers").show()					
				}
				else{
					$("#cp-"+prefix+"-markers").hide()	
				}
				res = true
				break;				
			}
		default:
			{
				res = false
				break;				
			}
	}

	return res
	
}

function set_linetype(val, key){
	var dom = document.getElementById('chartContainer');
	var traceid = document.getElementById('tracelist').value	
	var trace = dom.data[traceid]
	var lineset = trace["line"]
	var settings
	if(lineset!=null){
		lineset[key] = val
		settings = lineset
	}
	else{
		settings = {key : val}
	}
	var update = {
		"line" : settings
	}
	Plotly.restyle(dom, update,traceid);	
}

function connectgaps(el){
	var dom = document.getElementById('chartContainer');
	var traceid = document.getElementById('tracelist').value	

	var c = el.checked
	
	var update = {
		"connectgaps" : c
	}

	Plotly.restyle(dom, update,traceid);	

}

function display_text(val, other){
	var dom = document.getElementById('chartContainer');
	var traceid = document.getElementById('tracelist').value
	var trace = dom.data[traceid]	
	var pos, text2display
	console.log(val, other,trace[val])
	if(other == "text"){
		pos = document.getElementById('tr_pos_text').value
		if(val=="" || val==null){
			text2display = trace.customdata.map(String)
		}
		else{
			text2display = trace[val]
		}
	}
	else{
		if(val=="" || val==null){
			text2display = trace.customdata.map(String)
		}
/* 		if(trace.type=="bar"){
			text2display = trace.customdata.map(String)
		} */
		else{
			text2display = trace[document.getElementById('tr_shown_text').value]
		}
		pos = val
	}

	//var text2display = trace[val]
	var update = {
		"text" : [text2display],
		"textposition" : pos
	}
	console.log(update)
	Plotly.restyle(dom, update,traceid);	
	console.log(trace)
}

function display_plot_elem(what, id){
	var outmode
	var dom = document.getElementById('chartContainer');
	var traceid = document.getElementById('tracelist').value
	var chk = document.getElementById(id).checked
	var trace = dom.data[traceid]
	var mode_arr = trace.mode.split("+")
	if(chk){
		if(!mode_arr.includes(what)){
			mode_arr.push(what)
			$("#cp-tr-"+what).show()
		}
		else{
			$("#cp-tr-"+what).hide()
		}
		
	}
	else{
		if(mode_arr.includes(what)){
			const index = mode_arr.indexOf(what);
			mode_arr.splice(index, 1)
			$("#cp-tr-"+what).hide()
		}
		else{
			$("#cp-tr-"+what).show()
		}		
	}
	//remove none from mode
	if(mode_arr.includes("none")){
		const index = mode_arr.indexOf("none");
		mode_arr.splice(index, 1)
	}	
	
	
	outmode = mode_arr.join("+")
	if(outmode==''){outmode = "none"}
	var update = {
		mode : outmode
	}
	Plotly.restyle(dom, update,traceid);

}

function set_trace_font(){
	var dom = document.getElementById('chartContainer');
	var traceid = document.getElementById('tracelist').value
	var trace = dom.data[traceid]	
	
	var font = document.getElementById('tr_tf').value
	var font_settings = trace["textfont"]
	var update = {}
	//FONT
	if(font!="" && font!=null){
		if(font_settings!=null){
			font_settings["family"] = font
		}
		else{
			font_settings = {"family" : font}
		}
	}
	
	//SIZE
	var size = document.getElementById('tr_size').value
	if(size!="" && size!=null){
		if(font_settings!=null){
			font_settings["size"] = size
		}
		else{
			font_settings = {"size" : size}
		}
	}	

	
	var update = {
		"textfont" : font_settings
	}
	Plotly.restyle(dom, update,traceid);
}

//AXES FUNCTIONS

//LEGEND FUNCTIONS




