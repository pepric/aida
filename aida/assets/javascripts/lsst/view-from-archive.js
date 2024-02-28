$(document).ready(function(){
  $("#hktm_source").change(function(){
    //get current value
    var source = $("#hktm_source").val();
	var usecase = "pre-generated"
	var plot = null
	var opmode = document.getElementById("opmode").value
	loadXMLDoc("settings/forms.xml",source,usecase,plot,opmode)
	});
});

function loadXMLDoc(f,source,usecase,plot,opmode) {
	var xml_source, xml_usecase, base_form
	var htmltag, htmltxt, tbl
    $.ajax({
        type: "GET",
        url: f,
        dataType: "xml",
        error: function (e) {
            alert("An error occurred while processing XML file");
            console.log("XML reading Failed: ", e);
			location.reload();
        },
        success: function (response) {
			if(plot == "scatter"){
				var idpar = ["x","y0"]
			}
			else{
				var idpar = ["y0"]
			}			
			xml_source = $(response).find(source)
			xml_usecase = xml_source.find(usecase+"[apply='"+opmode+"']")
			if(xml_usecase.length==0){
				xml_usecase = xml_source.find(usecase+"[apply='all']")
				if(xml_usecase.length==0){
					alert("ERROR! Impossible to get form configuration for the selected Operating Mode. Please check configuration or contact AIDA team") 
					location.reload();
				}
			}
			tbl = xml_usecase.find("table")
			if(tbl.length == 0){
				tbl = usecase
			}
			else{
				tbl =$(tbl).text()
			}
			document.getElementById("tbl").value = tbl
			base_form = xml_usecase.find("items[apply='all']")
			idpar.forEach(function(elem){
				var maindiv = document.getElementById(elem+"-par-form");
				$(base_form).children().each(function(){
					htmltag = this.nodeName
					var mainelem = document.createElement(htmltag);
					$(this).children().each(function(){
						switch(this.nodeName)
						{
							case "option":
							  {
								var opttype = $(this).attr("type")
								switch(opttype){
									case "file" : {
										var jsonfile = this.innerHTML.split(",")[0]
										var idx = this.innerHTML.split(",")[1]
										//Parse forms.json
										$.ajax({
										  method:"POST",
										  url: 'functions.php',
										  data:{
											action : "build_options",
											opmode : opmode,
											usecase : usecase,
											source : source,
											idx : idx,
											filename : jsonfile
										  },
										  success :	function(resultdata){
												//build options
												var res = JSON.parse(resultdata)
												var key = Object.keys(res)[0]
												//first option
												var firstopt = document.createElement("option");
												firstopt.innerHTML = 'Select '+key;
												firstopt.setAttribute("value","");
												firstopt.setAttribute("disabled","");
												firstopt.setAttribute("selected","");
												mainelem.appendChild(firstopt)
												//all options
												for (var el in res[key]) {
													var curropt = document.createElement("option");
													curropt.innerHTML = res[key][el];
													curropt.setAttribute("value",res[key][el]);
													mainelem.appendChild(curropt)		
												}										
										  }
										});									
										break;
									}
									default:
									{
										var firstitem = this.innerHTML.split(",")[0]
										var firstopt = document.createElement("option");
										firstopt.innerHTML = firstitem;
										firstopt.setAttribute("value","");
										firstopt.setAttribute("disabled","");
										firstopt.setAttribute("selected","");
										mainelem.appendChild(firstopt)									
										var allopt = this.innerHTML.split(",")[1]
										allopt = allopt.replace("[","").replace("]","")
										allopt = allopt.split(",")
										for (var el in allopt) {
											var curropt = document.createElement("option");
											curropt.innerHTML = allopt[el];
											curropt.setAttribute("value",allopt[el]);
											mainelem.appendChild(curropt)		
										}									
									}
								}
								break;
							  }
							case "onchange":{
								var attrval = this.innerHTML
								$(mainelem).attr(this.nodeName, attrval)
								break;
							}
							case "onclick":{
								var attrval = this.innerHTML
								$(mainelem).attr(this.nodeName, attrval)
								break;
							}						
							case "style":{
								var attrval = this.innerHTML
								$(mainelem).attr(this.nodeName, attrval)
								break;
							}							  
							default:{
									var attrval = elem+"-"+this.innerHTML
									$(mainelem).attr(this.nodeName, attrval)	
									break;
							}
						}						
					})					
					mainelem.classList.add("form-control")
					$(mainelem).prop('required',true);
					maindiv.appendChild(mainelem);
				})
				document.getElementById(elem[0]+"params").style="display: block;";
			})
			//BUILD MAIN FILTER FORM ITEM (DateRange, ProductID...)
			var main_filter = xml_usecase.find("main_filter")
			if(main_filter.length>0){
				var node = document.createElement("div")
				node.classList.add("form-group")
				var bs_div = document.createElement("div")
				bs_div.classList.add("col-md-8")
				//input-group div
				var ig_div = document.createElement("div")
				ig_div.classList.add("input-daterange")
				ig_div.classList.add("input-group")
				ig_div.classList.add("date")				
				$(main_filter).children().each(function(){
					switch(this.nodeName){
						case "div_id":{
							var attrval = this.innerHTML
							$(node).attr("id",attrval)
							break;
						}
						case "label":{
							var label_el = document.createElement("label")
							label_el.classList.add("col-md-2")
							label_el.classList.add("control-label")
							label_el.innerHTML = this.innerHTML
							node.appendChild(label_el)
							break;
						}
						case "input":{
							//create html structure
							// add input
							var elem = document.createElement("input")
							$(this).children().each(function(){
								var attrval = this.innerHTML
								if(this.nodeName != "class"){
									$(elem).attr(this.nodeName,attrval)
								}
								else{
									elem.classList.add("form-control")
									elem.classList.add(attrval)
									elem.style.borderRadius = "6px";
								}
							})
							ig_div.appendChild(elem)
							break;
						}						
					}
					bs_div.appendChild(ig_div)
					node.appendChild(bs_div)
				})					
				$(node).insertBefore("#hidden-fields")
			}
			else{
				alert("ERROR! Impossible to get XML main filter configuration. Please check configuration or contact AIDA team")
				location.reload();
			}
        }
    });
}

/* function get_json(filename,idx){
	var key, values
	return [key, values]
} */