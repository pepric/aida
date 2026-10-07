/**
 * Core IOT Utility Functions and UI Handlers.
 *
 * Provides helper functions for form resetting, dynamic dropdown population,
 * detector grid setup, statistics parameter configuration, PDF/CSV export generation,
 * user management, and installation/update workflows.
 *
 * @package    AIDA
 * @subpackage JS\Core
 * @author     Giuseppe Riccio
 * @version    1.1.0
 */

/**
 * Resets form fields, hides parameter controls, and removes dynamic detector inputs.
 */
function reset_form(){
    
    var plot = document.getElementById('plot_type').value;
    var stats = document.getElementById('stats_enable').value;
    //get number of y parameters
    var npar = document.getElementById("n_ypar").value;
    //hide parameters and values boxes and remove detectors boxes
    // x
    if(plot=="scatter"){
        document.getElementById('x-params').style="display:none";
        document.getElementById('x-values').style="display:none";
        var xrow = document.getElementById('x-det-row')
        var xq = document.getElementById('x-quadrant')
        if(xrow != null){
            document.getElementById('x-det-row').style="display:none";
            document.getElementById('x-det-col').style="display:none";
            if(xq != null){
                xq.style="display:none";
            }
        }
    }
    
    //y
    for(var i=0; i<npar; i++){
        document.getElementById('y'+i+'-params').style="display:none";
        document.getElementById('y'+i+'-values').style="display:none";
        var yrow = document.getElementById('y'+i+'-det-row')
        var yq = document.getElementById('y'+i+'-quadrant')
        if(yrow != null){
            document.getElementById('y'+i+'-det-row').style="display:none";
            document.getElementById('y'+i+'-det-col').style="display:none";
            if(yq != null){
                yq.style="display:none";
            }
        }
    }
        
    // Reset det-type content
    var element = document.getElementById("det-type");
    if (element!==null){
        element.value="None,None";
    }
    // remove additional y forms if existing
    var els = document.querySelectorAll('.additional')
    // Reset additional y
    for (var i=0; i<els.length; i++){
        els[i].remove()
    }
    // Reset n_ypar
    ny = document.getElementById("n_ypar");
    ny.value="1"
    // Hide remove button
    document.getElementById("remove").style="display: none;"
}

/**
 * Sets input element names for a system selection control.
 *
 * @param {string} system System identifier.
 * @param {string} id Target select element ID.
 */
function set_system(system, id) {
    var selectname = "hktm_"+system.toLowerCase();
    var systemname = system.toLowerCase()+"_system";
    var where = "";
    var selectList = document.getElementById(id);
    selectList.name = selectname;
}

/**
 * Populates parameter group dropdowns based on repository metadata.
 *
 * @param {HTMLElement} elem Select element triggering parameter group setup.
 */
function set_pargroup(elem){
    var par = elem.id.split("-")[0] 
    var target_sel = par+"-sys"
    $("#"+par+"-params").hide()
    remove_prev_detectors(par)
    var dp = elem.value
    var repo = JSON.parse(document.getElementById('repo_json').innerHTML)
    var pargroup=repo[dp]
    var selectgr = document.getElementById(target_sel)
    selectgr.innerHTML=""
    var firstopt = document.createElement("option");
    firstopt.innerHTML = 'Select Parameter Group';
    firstopt.setAttribute("value","");

    firstopt.setAttribute("disabled","");
    firstopt.setAttribute("selected","");
    selectgr.appendChild(firstopt)
    for (var key in pargroup) {
        var curropt = document.createElement("option");
        curropt.innerHTML = key;
        curropt.setAttribute("value",key);
        selectgr.appendChild(curropt)       
   }
  
   $("#"+target_sel).show()
   show_addmore(par)
}

/**
 * Dynamically creates detector row/column and quadrant select controls.
 *
 * @param {HTMLElement} sys System selection element.
 * @param {string} par Axis/parameter prefix ('x' or 'yN').
 * @param {string} [elbefore="sys"] DOM element ID after which detectors are inserted.
 */
function init_detectors(sys, par, elbefore="sys"){
    var value = sys.value;
    var plot = document.getElementById('plot_type').value;
    
    if (par == "x"){
        var pos = 0
    } else {
        pos = parseInt(par.substr(1))+1;
    }
    // Create new detector setting boxes
    var valsplt = value.split("-")
    var instr = valsplt[0];
  
    if(instr == 'NISP' || instr == "NIR"){
        var nrow = 4;
        var ncol = 4;
        var dettype = document.getElementById("det-type");
        var dettypearr = dettype.value.split(",");
        dettypearr[pos] = "DET";
        dettype.value = dettypearr.toString();
    }
    else {
        var nrow = 6;
        var ncol = 6;
        if(valsplt.length > 1){
            var mainsource = "QLA"
        }
        else{
            var mainsource = instr
        }
        create_quadrant(par+"-params", par+"-quadrant", mainsource);
        var dettype = document.getElementById("det-type");
        var dettypearr = dettype.value.split(",");
        dettypearr[pos] = "CCD";
        dettype.value = dettypearr.toString();
    }
    
    if (plot == "scatter"){
        idpar = "params";
    } else {
        idpar = "yparams";
    }
    set_detectors(idpar, par+"-det-row", nrow, par+"-det-col", ncol, par+"-"+elbefore);
}

/**
 * Updates UI controls and fetches parameter definitions when a system/subsystem changes.
 *
 * @param {HTMLElement} sys Select element.
 * @param {boolean} [fromdb=false] Whether parameters are retrieved from database.
 */
function set_params(sys, fromdb=false) {

    var par = sys.id.split("-")[0]
    var system = document.getElementById("hktm_source").value; //EFD
    var stats = document.getElementById('stats_enable').value;
    var usecase = document.getElementById('usecase').value; //HTKM

    // Remove previous detector setting boxes
    // quadrant
    remove_prev_detectors(par)
    
    // reset param values select box
    $("#"+par+"-values").empty();

    // reset filter select box
    // Add subsystem query
    var element = document.getElementById(par+"-partype");
    
    /*ADDED FOR LSST */
    if(fromdb==true){
        
        var url   =   'functions.php';
        $.ajax({
            method:"POST",
            url:url,
            data:{
              action : "get_parameter_group",
              syst : system,
              origin : usecase,
              subs : document.getElementById(sys.id).value
            },
            success:function(data)
            {
                element.innerHTML='<option value="" disabled selected>Select Field</option>'+data
            }
        });
    }
    else{
        
        if (element!==null){
          for(i=1; i<element.options.length;i++){
            element.options[i].value = element.options[i].innerHTML
          }
        }  
    }

    if(usecase == "science"){
        if(system == 'QLA'){
          init_detectors(sys,par);
          document.getElementById(par + '-values').style='display:inline;';        
        }
        else{
            init_detectors(document.getElementById("hktm_source"),par);
        }
    }
    var partype_div = document.getElementById(par+"-partype");
    if(partype_div == null){
        document.getElementById(par + '-params').style='display:inline;';
    }
    else{
        partype_div.value=""
        document.getElementById(par + '-params').style='display:none;';      
    }
    //show parameter type select if exists  
    var element = document.getElementById(par+"-partype");
    if (element!==null){
        element.style='display:inline;';
    }
    populate_params(sys)
    //show addmore button for y  
    show_addmore(par)

    if(document.getElementById(par+"_extra_filters_btn_show")) {
        document.getElementById(par+"_extra_filters_btn_show").style = "display: inline";
    }
    if (stats == "advanced"){
        document.getElementById('stats').style='display:inline;';
    }
}

/**
 * Removes detector selection controls (quadrant, row, column) from DOM.
 *
 * @param {string} par Axis/parameter prefix.
 */
function remove_prev_detectors(par){
    var element = document.getElementById(par+"-quadrant");
    if (element!==null){
        element.parentNode.removeChild(element);
    }
    // row
    var element = document.getElementById(par+"-det-row");
    if (element!==null){
        element.parentNode.removeChild(element);
    }
    // col
    var element = document.getElementById(par+"-det-col");
    if (element!==null){
        element.parentNode.removeChild(element);
    }
}

/**
 * Displays the "Add more..." button for multi-parameter configurations.
 *
 * @param {string} par Axis/parameter prefix.
 */
function show_addmore(par){
  //show addmore button for y
  if(par.substring(0, 1) == "y"){
    if(document.getElementById("addmore")!=null){
        document.getElementById("addmore").style = "display: inline";
    }
    var currnpar = parseInt(par.substring(1))
    var prevpar = "y"+(currnpar-1)
    }
}

/**
 * Refreshes parameter list when parameter type selection changes.
 *
 * @param {HTMLElement} sys Select element.
 */
function reset_option(sys){
    var coord = sys.id.split("-")[0]
    var partype = document.getElementById(coord + "-partype");
    var ptval = partype.options[partype.selectedIndex].value;
    if(ptval!=""){
        refresh_params(partype)   
    }
}

/**
 * Fetches subsystem parameter options from XML configuration files via AJAX.
 *
 * @param {HTMLElement} cat Target category element.
 */
function xml_refresh_params(cat){
    var filter = cat.value
    var par_id = cat.id.split("-")[0]
    var tbl = document.getElementById("tbl").value
    var source = document.getElementById("hktm_source").value.toLowerCase()
    var subsystem = document.getElementById(par_id+"-ic").value
    var main_tbl = tbl + "_" + source
    
    $.ajax({
        method:"POST",
        url:"functions.php",
        data:{
          action : "fetch_values_subsystem",
          cat_val : subsystem,
          cat_name : main_tbl,
          cat_filter : filter
        },
        success:function(data)
        {
          $("#"+par_id+"-params").html(data);
          $("#"+par_id+"-params").show()
          //$("#"+par_id+"-values").html("");       
        }
    });
}

/**
 * Reloads parameter selection controls based on category choices.
 *
 * @param {HTMLElement} cat Category selection element.
 */
function refresh_params(cat){
    var sub = cat.value;
    var par_id = cat.id.split("-")[0]
    var hidden_chk = document.getElementById(par_id+"-adu_check")
    if(hidden_chk != null){
        hidden_chk.setAttribute("style","display:none");
    }
    var repo_set = document.getElementById("repo_json")
    var usecase = document.getElementById("usecase").value
    if(repo_set!=null){
        var dp = document.getElementById(par_id+"-ic").value
        var det = JSON.parse(repo_set.innerHTML)[dp][sub]

        if(usecase == "calibration"){
            if(det=="det"){
                init_detectors(document.getElementById("hktm_source"),par_id);      
            }
            else{
                if(par_id == "x"){
                    var idx = 0
                }
                else{
                    var idx = parseInt(par_id.substring(1))+1;
                }
                var curr_type = document.getElementById("det-type").value.split(",")                
                curr_type[idx] = "None"
                document.getElementById('det-type').value = curr_type.join()
                remove_prev_detectors(par_id)
            }

        }
    }
    //populate params
    populate_params(cat,sub);
    document.getElementById(par_id+"-params").style.display="inline";  
    if(document.getElementById(par_id+"_extra_filters_btn_show")) {
        document.getElementById(par_id+"_extra_filters_btn_show").style = "display: inline";
    }
    if (document.getElementById('stats_enable').value == "advanced"){
        document.getElementById('stats').style='display:inline;';
    }
    if(usecase == "calibration"){
        var ptypediv = document.getElementById(par_id+"-partype")
        if(ptypediv != null){
            var ptype = ptypediv.value
        }
        else{
            var ptype = ""
        }
        if(document.getElementById('hktm_source').value == "SIR" &&  ptype != "parameters"){
            if(ptype != "pivot"){
                $("#"+par_id+"-order").show()
            }else{
                $("#"+par_id+"-order").hide()
                $("#"+par_id+"-order").val("")
            }
            $("#"+par_id+"-coeff").show()
        }
        else{
            $("#"+par_id+"-order").hide()
            $("#"+par_id+"-coeff").hide()
            $("#"+par_id+"-order").val("")
            $("#"+par_id+"-coeff").val("")
        }  
    }
}

/**
 * Fetches subsystem parameter list from database via AJAX.
 *
 * @param {HTMLElement} sys Target selection element.
 * @param {string} [f=""] Optional filter parameter.
 */
function populate_params(sys, f=""){
    var system = document.getElementById("hktm_source").value.toLowerCase();
    var usecase = document.getElementById('usecase').value;
    cat_id = sys.id
 
    switch(system){
        case "efd":{
            cat_val = document.getElementById(cat_id.split("-")[0]+"-sys").value
            break;      
        }
        case "nisp":{
            if(usecase == "science"){
              cat_val = "None"
            }
            else{
              cat_val = document.getElementById(cat_id.split("-")[0]+"-sys").value
            }
            break;
        }
        case "vis":{
            if(usecase == "hktm"){
              coord = cat_id.split("-")[0]
              cat_val = document.getElementById(coord+"-sys").value;
              if(cat_val=="ALL"){cat_val="None"}
            }
            else{
              cat_val = "None"          
            }
            break;
        }
        case "qla":{
            if(usecase == "science"){
              coord = cat_id.split("-")[0]
              cat_val = document.getElementById(coord+"-sys").value;
              if(cat_val=="ALL"){cat_val="None"}
            }
            else{
              cat_val = "None"          
            }
            break;      
          
        }
        case "nir":{
            cat_val = document.getElementById(cat_id.split("-")[0]+"-ic").value
            break;
        }
        case "sir":{
            cat_val = document.getElementById(cat_id.split("-")[0]+"-ic").value
            break;
        }
        default:{
            cat_val = sys.value
            break;          
        }
    }  

    cat_name = usecase+"_"+system
    par_id = cat_id.split("-")[0]
    // ajax url to fetch subcategory
    var url   =   'functions.php';
    // call subcategory ajax here 
 
    $.ajax({
        method:"POST",
        url:url,
        data:{
          action : "fetch_values_subsystem",
          cat_val : cat_val,
          cat_name : cat_name,
          cat_filter : f
        },
        success:function(data)
        {
          $("#"+par_id+"-params").html(data);
          $("#"+par_id+"-values").html("");     
        }
    });
}

/**
 * Toggles ADU calibration checkbox visibility via AJAX query.
 *
 * @param {HTMLElement} sys Select element.
 */
function show_adu_checkbox(sys){
    var y = sys.id.split("-")[0]
    var par = sys.value
    var system = document.getElementById("hktm_source").value.toLowerCase();
    var usecase = document.getElementById('usecase').value;
    $.ajax({
       method:"POST",
       url:'functions.php',
       data:{
           action : "show_adu_checkbox",
           par : par,
           system : system,
           usecase : usecase
       },
       success:function(data)
        {
            var d = "none"
            var hascalib = JSON.parse(data)["hascalib"]
            if(hascalib == "1"){
                d = "inline"
            }
            var aduchkdiv = document.getElementById(y+"-adu_check")
            if(aduchkdiv!=null){
                aduchkdiv.style.display = d
                aduchkdiv.style.marginRight = "30px"
                document.getElementById(y+"-adu_cal").checked=false
            }
        }
    });
}

/**
 * Retrieves discrete parameter values via AJAX and populates target dropdown.
 *
 * @param {HTMLElement} sys Target parameter select element.
 */
function populate_values(sys){
    var par = sys.id.split("-")[0]
    var cat_val = sys.value
    var param = document.getElementById(par+"-sys").value

    // ajax url to fetch subcategory
    var url             =   'functions.php';
    // call subcategory ajax
    $.ajax({
       method:"POST",
       url:url,
       data:{
           action : "fetch_values",
           cat_val : cat_val,
           cat_sys : param
       },

       success:function(data)
        {
            $("#"+par+"-values").html(data);
        }
    });
}

/**
 * Creates and appends detector row and column select controls.
 *
 * @param {string} idpar Parent container element ID.
 * @param {string} name_row Element name/ID for row selector.
 * @param {number} nrow Number of rows.
 * @param {string} name_col Element name/ID for column selector.
 * @param {number} ncol Number of columns.
 * @param {string} elbefore Target DOM element ID to insert controls after.
 */
function set_detectors(idpar, name_row, nrow, name_col, ncol, elbefore){
    var coord = name_row.split("-")[0]
    var myDiv = document.getElementById(idpar); 
    //Create and append select list
    var selectListRow = document.createElement("select");
    selectListRow.name = name_row;
    selectListRow.id = name_row;
    selectListRow.classList.add("form-control");
    //selectListRow.setAttribute("required", "");
    myDiv.appendChild(selectListRow);
    
    var selectListCol = document.createElement("select");
    selectListCol.name = name_col;
    selectListCol.id = name_col;
    selectListCol.classList.add("form-control");
    //selectListCol.setAttribute("required", "");
    myDiv.appendChild(selectListCol);

    //Create and append the options
    if (nrow==4){
        var detname = "Detector";
    }
    else{
        var detname = "CCD";
    }

    var firstrow = document.createElement("option");
    var firstcol = document.createElement("option");
    firstrow.innerHTML = detname + ' Row';
    firstcol.innerHTML = detname + ' Col';
    firstrow.setAttribute("value","");
    firstcol.setAttribute("value","");
    firstrow.setAttribute("disabled","");
    firstcol.setAttribute("disabled","");
    firstrow.setAttribute("selected","");
    firstcol.setAttribute("selected","");
    
    selectListRow.appendChild(firstrow);
    selectListCol.appendChild(firstcol);
    
    //"ALL" option
    if(coord !="x"){
        var allrow =  document.createElement("option");
        var allcol =  document.createElement("option");
        allrow.innerHTML = 'ALL';
        allcol.innerHTML = 'ALL';
        allrow.setAttribute("value","all");
        allcol.setAttribute("value","all");
        selectListRow.appendChild(allrow);
        selectListCol.appendChild(allcol);
    }
    
    for (var i = 1; i < nrow+1; i++) {
        var option = document.createElement("option");
        option.value = i;
        option.text = i;
        selectListRow.appendChild(option);
    }
    
    for (var i = 1; i < ncol+1; i++) {
        var option = document.createElement("option");
        option.value = i;
        option.text = i;
        selectListCol.appendChild(option);
    }
    
    $(selectListCol).insertAfter(("#"+elbefore));
    $(selectListRow).insertAfter(("#"+elbefore));
    
}

/**
 * Appends CCD quadrant selector control to DOM.
 *
 * @param {string} idpar Parent container ID.
 * @param {string} name_quad Element name/ID for quadrant selector.
 * @param {string} instr Instrument identifier.
 */
function create_quadrant(idpar, name_quad, instr){
    var par = idpar.split("-")[0]
    var ptype_div = document.getElementById(par+"-partype")
    if(ptype_div==null){
        var obj_before = document.getElementById(idpar);
    }
    else{
        var obj_before = ptype_div
    }
    //Create and append select list
    var selectQuadrant = document.createElement("select");
    selectQuadrant.classList.add("form-control");
    selectQuadrant.name = name_quad;
    selectQuadrant.id = name_quad;
    selectQuadrant.style="margin-right: 3px;"
    obj_before.parentNode.insertBefore(selectQuadrant, obj_before);
    
    var first = document.createElement("option");
    first.innerHTML = 'Select Quadrant';
    first.setAttribute("disabled", "disabled");
    first.setAttribute("readonly", "readonly");
    first.setAttribute("selected", "selected");
    selectQuadrant.appendChild(first);
    
    //CCD AS A WHOLE  
    if(instr=="QLA"){
      //update_filter(par)      
      var full = document.createElement("option");        
      full.innerHTML = 'CCD as a whole';
      full.value="full";
      selectQuadrant.appendChild(full);      
      //update filter content
      selectQuadrant.setAttribute("onchange", "update_filter('"+par+"')")
    }
  
    const qname=["E","F","G","H"]
    for (var i = 0; i < qname.length; i++) {
      var option = document.createElement("option");
      option.value = qname[i];
      option.text = qname[i];
      selectQuadrant.appendChild(option);
    }     
}

/**
 * Updates filter options according to selected CCD quadrant ('full' vs specific quadrant).
 *
 * @param {string} par Parameter prefix.
 */
function update_filter(par){
    var val = $('select[name='+par+'-quadrant] option').filter(':selected').val()
    if(val=="full"){
        var prefix = "full_"
    }
    else{
        var prefix = ""
    }

    var filters = document.getElementById(par+"-partype");

    for(i=1; i<filters.options.length;i++){
      filters.options[i].value = prefix+filters.options[i].innerHTML
    }        
    filters.value="";   
    var params = document.getElementById(par+"-params");
     
    $("#"+par+"-params").empty();
    $("#"+par+"-values").empty();  
}

/**
 * Formats selected detector, row, column, and quadrant into a single string token.
 *
 * @param {string} det Detector type string ('DET' or 'CCD').
 * @param {string} row Selected row.
 * @param {string} col Selected column.
 * @param {string} id Quadrant select element ID.
 * @returns {string} Formatted detector string token.
 */
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

/**
 * Hides target plot/results panel and activates initial tab.
 *
 * @param {string} tab_id Tab element ID.
 * @param {string} id Container element ID to remove.
 */
function hide_panel(tab_id, id){
    var ref = document.getElementById(id);
    var par = document.getElementById(tab_id).parentNode;
    alert(ref.id);
    alert(par.id);
    $(id).remove();
    par.style.display = "none";
    $('#tab1').addClass('active');
}

/**
 * Dynamically creates additional inputs for statistical function parameters.
 *
 * @param {HTMLInputElement} box Checkbox element for a statistical function.
 */
function more_stats_params(box){
    var funcname = box.name;
    var func = box.value;
    if ($(box).is(':checked')) {
        $('#stats_list').val($('#stats_list').val() + funcname + ',');
    
        var param_data= document.getElementById("more-"+funcname);
        if (document.contains(document.getElementById("par-"+funcname))) {
            document.getElementById("par-"+funcname).remove();
        }      
        var divpars = document.createElement("div");
        divpars.id = "par-"+funcname;
        var parameters = param_data.value;
        if (parameters != ""){
            var addmore = $(param_data).attr('addmore');
            var jsonpar = JSON.parse(parameters);
            ks = Object.keys(jsonpar)
            var divothers = document.createElement("div");
            divothers.setAttribute("class", "par-others col-md-12");
            divothers.id = "par-others-"+funcname+"_0"
            for (i=0; i<ks.length; i++){
                var par = ks[i];
                var type = jsonpar[par].type;
                var id = jsonpar[par].id;
                var required = jsonpar[par].required;
                if (required == "True"){required = 'required';} else {required = '';}
                
                var node = document.createElement("label");
                node.setAttribute("for", id);
                node.innerHTML = par;
                divothers.appendChild(node);
                if (type == "number"){
                    var min = jsonpar[par].min;
                    var def = jsonpar[par].default;
                    var max = jsonpar[par].max;
                    var node = document.createElement("input");
                    node.setAttribute("type", type);
                    node.id = id;
                    node.setAttribute("class", "par-input");
                    node.setAttribute("name", id);
                    node.setAttribute("min", min);
                    if (typeof max !=='undefined'){node.setAttribute("max", max);}
                    node.setAttribute("required", required);
                    node.setAttribute("value", def);
                    node.setAttribute("placeholder", def);
                    divothers.appendChild(node);
                }
                if (type == "select"){
                    var opt_arr = jsonpar[par].option;
                    var node = document.createElement("select");
                    node.id = id;
                    node.setAttribute("name", id);
                    node.setAttribute("required", required);
                    divothers.appendChild(node);
                    for (i=0; i<opt_arr.length; i++){
                        var option = document.createElement("option");
                        option.value = opt_arr[i];
                        option.text = opt_arr[i];
                        node.appendChild(option);
                    }               
                }
            }
            divpars.appendChild(divothers);
            if (addmore == 1){
                var node = document.createElement("a");
                node.id = "addmore_stats_"+funcname;
                node.setAttribute("class", "stats_button");
                node.setAttribute("onclick", "addmore_stats(this)");
                node.innerHTML = "Add more...";
                divothers.appendChild(node);
                
                var node = document.createElement("a");
                node.id = "remove_stats_"+funcname;
                node.setAttribute("class", "stats_button");
                node.setAttribute("style", "display:none");
                node.setAttribute("onclick", "remove_stats(this)");
                node.innerHTML = "Remove Last...";
                divothers.appendChild(node);
            var node = document.createElement("input");
                node.id = "par-hidden-"+funcname;
                node.setAttribute("name", "par-multi-"+funcname);
                node.setAttribute("type", "hidden");
                node.value = "0";
                divpars.appendChild(node);
            }
        }
    $(divpars).insertAfter($(param_data));
    } else {
        document.getElementById("par-"+funcname).remove();
        var stats_list = document.getElementById("stats_list");
        var old_list = stats_list.value;
        var new_list = old_list.replace(funcname+",", "");
        stats_list.value = new_list;
    }
};

/**
 * Clones and appends parameter inputs for multi-instance statistical functions.
 *
 * @param {HTMLElement} div Button element triggering addition.
 */
function addmore_stats(div){
    var parentID = $(div).parent().attr('id');
    var parentDiv = document.getElementById(parentID);
    var parentFunc0 = parentID.split("_")[0];
    var parentFunc = parentFunc0.split("-")[2];
    var hidden = document.getElementById("par-hidden-"+parentFunc)
    console.log(parentFunc) 
    document.getElementById("remove_stats_"+parentFunc).style="display: inline;"
    
    var old_val = hidden.value
    var new_val = parseInt(old_val) + 1;
    hidden.value=new_val;
    var clone = parentDiv.cloneNode(true);
    clone.setAttribute("id", "par-others-"+parentFunc+"_"+new_val);
    $(clone).children().last().remove();
    $(clone).children().last().remove();    
    
    var childDivs = clone.getElementsByTagName('label');
    for (i=0;  i< childDivs.length; i++ ){
        var childDiv = childDivs[i];
        var labelfor = childDiv.htmlFor
        var splitfor = labelfor.split("_")[0];
    childDiv.htmlFor = splitfor + "_" + new_val;
    }

    var childDivs = clone.getElementsByTagName('input');
    for (i=0;  i< childDivs.length; i++ ){
        var childDiv = childDivs[i];
        var inputID = childDiv.id
        var splitID = inputID.split("_")[0];
        childDiv.id = splitID + "_" + new_val;
        childDiv.name = splitID + "_" + new_val;
    }
    
    var childDivs = clone.getElementsByTagName('select');
    for (i=0;  i< childDivs.length; i++ ){
        var childDiv = childDivs[i];
        var inputID = childDiv.id
        var splitID = inputID.split("_")[0];
        childDiv.id = splitID + "_" + new_val;
        childDiv.name = splitID + "_" + new_val;
    }
    var last = document.getElementById("par-others-"+parentFunc+"_"+old_val);
    last.parentNode.insertBefore(clone, last.nextSibling);
    event.preventDefault()
}

/**
 * Removes the last added parameter input group for a statistical function.
 *
 * @param {HTMLElement} div Button element triggering removal.
 */
function remove_stats(div){
    var parentID = $(div).parent().attr('id');
    var parentDiv = document.getElementById(parentID)
    var parentFunc0 = parentID.split("_")[0];
    var parentFunc = parentFunc0.split("-")[2];
    var hidden = document.getElementById("par-hidden-"+parentFunc)
    var nmore = hidden.value;
    
    var todelete = document.getElementById("par-others-"+parentFunc+"_"+nmore)
    todelete.remove();
    var new_nmore = parseInt(nmore)-1;
    hidden.value = new_nmore;
    
    if (nmore == 1){
        document.getElementById("remove_stats_"+parentFunc).style="display: none;"
    }
    event.preventDefault();
}

/**
 * Returns current timestamp in UTC string format.
 *
 * @returns {string} UTC formatted date string.
 */
function get_utc_date(){
    var today = new Date();
    dateTime = today.toUTCString()
    return dateTime;
}

/**
 * Converts Plotly chart to image and requests server-side PDF report creation via Python.
 *
 * @param {string} n_exp Experiment title or type.
 * @param {Array<string>} labels Parameter label array.
 * @param {string} save Storage scope ('public' or 'private').
 * @param {boolean} download Download PDF flag.
 */
function exportPDF(n_exp, labels, save, download){
    //get experiment info
    var source = document.getElementById("hktm_source").value;
    var tstart = document.getElementById("modal-tstart").value;
    var tstop = document.getElementById("modal-tstop").value;
    var user = document.getElementById("session-user").innerHTML;
    var usecase = document.getElementById("usecase").value;
    var tbl_div = document.getElementById("tbl")
    if(tbl_div != null){
        var tbl = tbl_div.value
    }
    else{
        var tbl = usecase       
    }
    var plot_st = document.getElementById('plot_type').value

    switch(n_exp){
        case "Statistics":{
            var plot_t = "statistics"
            break;
        }
        case "Image Analysis":{
            var plot_t = "img_analysis"
            break;
        }
        case "Pre-generated Histogram":{
            var plot_t = $('#plot_type').val()
            plot_st = "histogram"
            break;          
        }
        default : {
            var plot_t = $('#plot_type').val()
            break;
        }
        
    }

    var ftbl = $('#files_tbl').DataTable();
    var heads = [];
    $('#files_tbl').find("th").each(function () {
        heads.push($(this).text().trim());
    });
    var fobj = []  
    var files_data  = ftbl.rows().data();  
    if(files_data.length > 0){
        for(var i = 0; i < files_data.length; i++){
            row = files_data[i]
            if(plot_t != "img_analysis"){
                fname = row[0].substring(0, row[0].length-4)
            }
            else{
                fname = row[0]
            }

            fname = fname.split(">")
            fname = fname[fname.length-1]

            fpar = {"Filename":fname}
            for(var j = 1; j < row.length; j++){
                fpar[heads[j]] = row[j]
            }
            fobj.push(fpar)
        }
        var fdata = JSON.stringify(fobj)   
    }
    $("#loader").show();
    //generate image to save in pdf
    var d3 = Plotly.d3;
    var img_png = d3.select('#png_img');
    var dom = document.getElementById('chartContainer');
    //var img = Plotly.toImage(dom,{format:'png', height:120,width:120})
    Plotly.toImage(dom,{format:'png', height:720,width:1200})
      .then(function(url){
        img_png.attr("src", url);
        return Plotly.toImage(dom,{format:'png',height:720,width:1200});
      })
    .then(function(){
        img = document.getElementById('png_img').src
        stats = document.getElementById('stats_results').innerHTML;
        
        //import flags and notes
        var expstatus = $('input[name=optflag]:checked').val();
        if(expstatus != "nd"){
            var gl_descr=[]
            var gl_flag = []
            for (i=0;  i< labels.length; i++ ){
                //console.log(labels[i])
                if(labels[i] != "None"){
                    var v = document.getElementById('descr-'+i).value;
                    if(v!=""){
                        var descr = document.getElementById('descr-'+i).value;
                    }
                    else{
                        var descr = "None"
                    }
                    var flag = document.getElementById('parflag-'+i).value;
                }
                else{
                    var descr = "None"
                    var flag = "None"
                }
                gl_descr[i] = descr;
                gl_flag[i] = flag;
            }
        }
        
        //get alert email
        var email = document.getElementById('email-to').value;
        pyscript = "scripts/pdfcreator.py";
        var loc = window.location.href;
        $.ajax({
            type: "POST",
            url: pyscript,
            data: {
                "img" : img,
                "source" : source,
                "tstart"    : tstart,
                "tstop" : tstop,
                "user"  : user,
                "plot"  : plot_t,
                "notes" : gl_descr,
                "flags" : gl_flag,
                "status" : expstatus,
                "labels"    : labels,
                "stats" : stats,
                "location" : loc,
                "save" : save,
                "email" : email,
                "usecase" : usecase,
                "filesdata" : fdata,
                "plotdata" : document.getElementById('plotdata').innerHTML,
                "plot_subtype" : plot_st,
                "pid" : document.getElementById("modal-pid").value,
                "tbl" : tbl
            } ,
            dataType: "html",
            cache: false,
            async:'asynchronous',
            success: function(returndata){
                res = JSON.parse(returndata)
                error = res['error']
                if(error == 0 || error == 2){ // 0: no error, 2: experiment stored but email not sent
                    if(download==true){
                        filepath = res['file']
                        fileurl = document.location.origin+filepath
                        filesplit = filepath.split("/")
                        filename = filesplit[filesplit.length-1]
                      console.log(fileurl)
                        downloadPDF(fileurl, filename, save);
                    }
                    if(error==0){
                        alert("Experiment has been successfully stored into the AIDA archive.")
                    }
                    else {
                        alert("Experiment has been successfully stored into the AIDA archive but it is impossible to send an email to: "+email+".")
                    }
                    out_hist = {"plot" : plot_t.charAt(0).toUpperCase() + plot_t.slice(1)}
                    if(tstart != "NULL"){
                        out_hist["dates range"] = "["+tstart+", "+tstop+"]"
                    }
                    out_hist.flag = expstatus
                    out_hist.archive = save.charAt(0).toUpperCase() + save.slice(1)
                    $.ajax({
                        type: "POST",
                        url: "functions.php",
                        data: {
                            action: "update_history",
                            username : user,
                            operation : "Experiment Flagged",
                            infile :    "NA",
                            out : JSON.stringify(out_hist),
                            config : "NA"
                            },
                        error : function (obj, textstatus) {
                            alert("Impossible to store the operation in History")
                        }
                    })              
                }
                else {
                    alert("Impossible to store the experiment into the AIDA archive. Please retry later or contact AIDA admin.")
                }
            },
            complete:function(data){
                // Hide loader image container
                $("#loader").hide();
            }
        });
    });
}

/**
 * Downloads a PDF file from a given URL using XMLHttpRequest and FileSaver.js.
 *
 * @param {string} dataurl Resource URL.
 * @param {string} filename Output filename.
 * @param {string} save Archive type.
 * @param {string} [type='application/pdf'] MIME type.
 */
function downloadPDF(dataurl, filename, save, type='application/pdf'){
    
    var oReq = new XMLHttpRequest();
    // Configure XMLHttpRequest
    oReq.open("GET", dataurl, true);
    // Important to use the blob response type
    oReq.responseType = "blob";
    // When the file request finishes
    // Is up to you, the configuration for error events etc.
    oReq.onload = function() {
        // Once the file is downloaded, open a new window with the PDF
        // Remember to allow the POP-UPS in your browser
        var file = new Blob([oReq.response], { 
            type: type 
        });
        // Generate file download directly in the browser !
        saveAs(file, filename);
    };
    oReq.send();
}

/**
 * Displays custom option fields based on selected mode.
 *
 * @param {string} val Selected option value.
 */
function show_opt(val){
    switch(val)
    {
        case "custom":
        {
            $("#custom-div").show();
            break;          
        }
        default:
        {
            $("#custom-div").hide();
            break;          
        }
    }
}

/**
 * Prepares modal form values and opens export modal dialog.
 *
 * @param {string} id Target modal element ID.
 * @param {string} n_exp Experiment type string.
 * @param {Array<string>} labels Parameter labels array.
 */
function select_download_dir(id, n_exp, labels){
    document.getElementById("nd").checked = true;
    $("#description").hide();
    $("#email-to").val('')
    $("#alert-email").hide();
    //add n_exp and labels to modal form
    var n = document.getElementById('n_exp')
    n.value = n_exp
    
    //create temporary <a> to click and open modal div
    var element = document.createElement('a');
    element.setAttribute('data-target', "#"+id)
    element.setAttribute('role', "button")
    element.setAttribute('data-toggle', "modal")
    element.style.display = 'block';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

/**
 * Populates parameter flag dropdowns and comment textareas inside modal form.
 */
function populate_flags(){
    var labels = document.getElementById("modal-labels").value.split(",");
    var div = document.getElementById('description')
    for (i=0;  i< labels.length; i++ ){
        if(labels[i] != "None"){
            var node = document.createElement("label");
            node.setAttribute("style","font-weight : bold");
            node.innerHTML = "Details for " + labels[i]
            div.appendChild(node);
            var node = document.createElement("div");
          
            var sel = document.createElement("select");
            sel.name = "parflag-"+i;
            sel.id = "parflag-"+i;
            sel.className += "parflag";
            var values = ["Not Defined", "Ok","Warning","Serious"];
            for (const val in values){
                var option = document.createElement("option");
                option.value = values[val];
                option.text = values[val];
                sel.appendChild(option);                
            }          
          
            var l = document.createElement('label')
            l.innerHTML = "Parameter flag"
            l.htmlFor = 'parflag';
            node.appendChild(l);
            node.appendChild(sel); 
            div.appendChild(node);
          
            var l = document.createElement("label");
            l.innerHTML = "Comments"
            div.appendChild(l);          
            var descr = document.createElement("textarea");
            descr.setAttribute("id", "descr-"+i);
            descr.setAttribute("rows", "3");
            descr.setAttribute("style", "width: 100%; display: block; margin-bottom: 20px;");
            div.appendChild(descr);
        }
    }   
}

/**
 * Deletes a stored file from repository via AJAX request.
 *
 * @param {number} id Record database ID.
 * @param {string} file Filename to delete.
 * @param {string} path Subdirectory path.
 */
function delete_file(id, file, path){
    
    res=confirm("You have chosen to delete the file "+file+". Please confirm ");
    if(res==true){
        var url =   'functions.php';
    // call subcategory ajax
        $.ajax({
           method:"POST",
           url:url,
           data:{
               action : "delete_file",
               file :file,
               path : path,
               id : id,
               user : document.getElementById("session-user").innerHTML
           },
           success:function(res)
            {
                alert(res);
                window.location.reload();
            }
        });
    }
}

/**
 * Displays extended details popover for a history log entry.
 *
 * @param {HTMLElement} div Hovered/clicked element.
 */
function show_more(div){
    id = div.id.substr(2)
    t_user = div.id.substr(0,2)
    if(t_user == "hg"){
        document.getElementById('moredata').style.bottom = "-10%";  
    } else {document.getElementById('moredata').style.bottom = "88%";}
    content = document.getElementById("more-"+id).innerHTML
    document.getElementById('moredata').innerHTML=content
    document.getElementById('moredata').style.visibility = "visible";
    document.getElementById('moredata').style.opacity = 1;
}

/**
 * Hides extended details popover for history log entries.
 */
function hide_more(){
    document.getElementById('moredata').style.visibility = "hidden";
    document.getElementById('moredata').style.opacity = 0;
}

/**
 * Validates whether a string is a valid JSON payload.
 *
 * @param {string} str Input text.
 * @returns {boolean} True if valid JSON, false otherwise.
 */
function IsValidJSONString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

/**
 * Deletes a temporary uploaded file record via AJAX.
 *
 * @param {string} fname Filename.
 * @param {number} id Record ID.
 */
function remove_upload(fname, id){
    $.ajax({
        url         : "functions.php",
        method      : 'POST',
        datatype    : 'json',
        data        : {
            action : 'delete_upload',
            file : filename,
            id : id
        }
    })
}

/**
 * Calls Python script via AJAX to generate and download CSV formatted results.
 *
 * @param {Array<string>} labels CSV header labels.
 * @param {Object} indata Data payload.
 */
function save_csv(labels, indata){
    
    var user = document.getElementById("session-user").innerHTML
    var plot = document.getElementById('plot_type').value;
    var source = document.getElementById("hktm_source").value
    tmpname = user+"_temp.csv"
    filename = plot+"_"+source+".csv"
    $.ajax({
        url: "scripts/create_csv.py",
        method      : 'POST',
        datatype    : 'json',
        data : {
            "labels" : labels,
            "indata" : JSON.stringify(indata),
            "filename" : tmpname,
            "iodaurl" : window.location.href
        },
       success:function(res)
        {
            downloadURI(res['url'], filename);
        },
        error:function(){
            alert("Error! Impossible to download file. Please, retry later or contact AIDA admin")
        }
    })
}

/**
 * Triggers a browser file download via temporary anchor element.
 *
 * @param {string} uri File URI.
 * @param {string} name Destination filename.
 */
function downloadURI(uri, name) {
  var link = document.createElement("a");
  link.download = name;
  link.href = uri;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  delete link;
}

/**
 * Updates user account state (activate, deactivate, remove) via AJAX request.
 *
 * @param {number} id User account database ID.
 * @param {string} action Action command ('active', 'deactive', 'remove').
 * @param {string} user Target username.
 * @param {string} email User email address.
 */
function manage_user(id, action, user, email){
    switch(action){
        case "active":
            msg = "Confirm to activate user: "+user+"?"
            break;
        case "deactive":
            msg = "Confirm to de-activate user: "+user+"?"
            break;
        case "remove":
            msg = "Confirm to remove user: "+user+"?\nNOTE: This operation cannot be canceled"
            break;
    }
    if(confirm(msg)){
        $.ajax({
            url: "functions.php",
            method      : 'POST',
            data : {
                "action" : "manage_user",
                "id" : id,
                "op" : action,
                "email" : email,
                "username" : user,
                "admin" : document.getElementById("session-user").innerHTML
            },
           success:function(res)
            {
                if(res==0){
                    alert("AIDA DB successfully updated!");
                    window.location.reload();
                }
                else{
                    alert("Error! Impossible to complete the requested operation.")
                }
            },
            error:function(){
                alert("Error! Something has gone wrong")
            }
        })
    }
}

/**
 * Prompts user for logout confirmation and redirects to logout script.
 */
function session_logout(){
    res=confirm("Are you sure to quit? All downloaded data will be deleted.");
    if(res==true){
        window.location.href = "logout.php";
    }
}

/**
 * Hides the "Save experiment as PDF" button if present in UI.
 */
function hide_pdf(){
    var btn = document.querySelector("[data-title='Save experiment as PDF']"); 
    if(btn!=null){btn.style.display = "none"}
}

/**
 * Hides the "Save results as CSV" button if present in UI.
 */
function hide_csv(){
    var btn = document.querySelector("[data-title='Save results as CSV']"); 
    if(btn!=null){btn.style.display = "none"}
}

/**
 * Opens a file in JS9 Image Explorer window via AJAX interface.
 *
 * @param {string} filename Base filename.
 * @param {string} source Data source identifier.
 * @param {string} origin Data origin identifier.
 * @param {string} user Owner username.
 */
function to_image_explorer(filename, source, origin, user){
    $("#loader").show();
    $.ajax({
        url: "scripts/cs_interface.py",
        method      : 'POST',
        datatype    : 'json',
        data : {
            "filename" : filename,
            "s" : source,
            "o" : origin,
            "username" : user,
            "action" : "file_to_image"
        },
       success:function(res)
        {
            var url = res["result"]
            if(url != "error"){
                var finalfile = "users/"+user+"/tmp/"+source.toLowerCase()+"/"+url
                window.open("image-explorer.php?file="+finalfile, "Image-Explorer_"+url, "width=2048,height=1024")
            }
            else{
                alert("ERROR! Impossible to download image from repository.")            
            }
            $("#loader").hide();
        },
        error:function(){
            alert("ERROR! Impossible to download image from repository.")
            $("#loader").hide();            
        }
    })
}

/**
 * Reads metadata and column headers from uploaded data files via Python backend script.
 *
 * @param {string} filename Uploaded file name.
 * @param {string} [fmt=""] File format identifier.
 * @param {number} [csv_checked=-999] CSV header state flag.
 * @param {string} [origin=""] Data origin context.
 */
function read_uploaded_file(filename, fmt="", csv_checked=-999, origin=""){
    //Read data from uploaded files
    var user = document.getElementById("session-user").innerHTML
    if(fmt==""){
        fmt = document.getElementById("filefmt").value
    }
    //get header check
    if(csv_checked==-999){
        csv_checked = $('input[name="csvheader"]')
        if(csv_checked.prop('checked') == true){
            var header = 1
        }
        else{
            var header = 0       
        }      
    }
    else{

        var header = csv_checked
    
    }
    $("#loader").show();    
    //AJAX TO GET COLUMNS
    $.ajax({
        url: "scripts/uploaded_data.py",
        method      : 'POST',
        datatype    : 'json',
        data : {
            "filename" : filename,
            "user" : user,
            "fmt" : fmt,
            "header" : header,
            "origin" : origin,
            "action" : "get_cols"
        },
        success:function(res)
        {
            var error = res['error']
            var cols = res['cols']
            switch(error)
            {
                case 0: //all ok
                {
                    $('#choice-div').hide()
                    $('#config-upload').show()
                    $('#config-table').hide()                  
                    $('#title-conf').html("Configure Analysis")
                    $('#progressbar').fadeOut().progressbar();
                    $('#uploader').hide()              
                    $('#cols').val(cols)
                    $('#okupload').show()              
                    $("#opselection").show()
                    $("#loader").hide();
                    break;
                }
                case 1: //error uploading
                {
                    reset = alert("Error! Impossible to upload the file")
                    if(reset){} else {window.location.reload()}     
                    break;                  
                }
                case 2: //no data in file
                {
                    reset = alert("Error! No data in uploaded file")
                    if(reset){} else {window.location.reload()} 
                    break;                  
                }
                case 3: //file uploaded but not stored in DB
                {
                    $('#choice-div').hide() 
                    $('#config-upload').show()
                    $('#config-table').hide()                  
                    $('#title-conf').html("Configure Analysis")                  
                    $('#progressbar').fadeOut().progressbar();
                    $('#uploader').hide()              
                    $('#cols').val(cols)
                    alert("Warning! File has been uploaded, but it is impossible to store it in the local temporary files DB.")                  
                    $('#okupload').show()              
                    $("#opselection").show()
                    $("#loader").hide();
                    break;
                }
                case 4: //file uploaded but already present in local DB
                {
                    $('#choice-div').hide()
                    $('#config-upload').show()
                    $('#config-table').hide()
                    $('#title-conf').html("Configure Analysis")                  
                    $('#progressbar').fadeOut().progressbar();
                    $('#uploader').hide()              
                    $('#cols').val(cols)
                    alert("Warning! A file with name "+filename+" already exists in local temporary files. It has been overwritten.")                  
                    $('#okupload').show()              
                    $("#opselection").show()
                    $("#loader").hide();
                    break;
                }
            }            
        },
        error:function(){
            alert("Error! Impossible to upload the file")
            $("#loader").hide(); 
        }
    })  
}

/**
 * Retrieves parameter metadata table for a system and displays inspection panel.
 *
 * @param {string} system System identifier.
 * @param {string} origin Origin identifier.
 */
function show_parameters(system, origin){
  $.ajax({
    url: "functions.php",
    method      : 'POST',
    data : {
      "action" : "render_pars",
      "system" : system,
      "origin" : origin
    },
    success:function(res)
    {
        console.log(res)
        var data = JSON.parse(res);
        $('#parinfo-title').html(system+" - "+origin.toUpperCase()+" parameters info")
        $('#parinfo-div').css("display","block")

        if(data["error"] == 0){
            $('#parinfo-tbl').html(data["table"])
            initParTbl()
        }
        else{
            $('#parinfo-tbl').html("Error retrieving parameters data. Please retry or contact AIDA admin")
        }

    }
  })  

}

/**
 * Opens report flagging modal dialog.
 *
 * @param {string} filename Target report filename.
 * @param {string} period Recurrence periodicity.
 */
function flag_report(filename, period){
    $("#fname").val(filename)
    $("#fcreator").val(document.getElementById("session-user").innerHTML)
    $("#period").val(period)

    //create temporary <a> to click and open modal div
    var element = document.createElement('a');
    element.setAttribute('data-target', "#store_report")
    element.setAttribute('role', "button")
    element.setAttribute('data-toggle', "modal")
    element.style.display = 'block';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);  
}

/**
 * Submits report flag details and sends summary PDF report via Python script.
 *
 * @param {string} filename Report filename.
 * @param {string} creator Flag creator username.
 * @param {string} expstatus Flag status ('ok', 'warning', 'serious').
 * @param {string} descr Comment text.
 * @param {string} email Notification email address.
 */
function export_report_flag(filename, creator, expstatus, descr, email){
    $("#loader").show();
    $.ajax({
        type: "POST",
        url: "scripts/pdfcreator.py",
        data: {
            "plot" : "report",
            "filename" : filename,
            "creator"   : creator,
            "notes" : descr,
            "status" : expstatus,
            "email" : email
        } ,
        dataType: "html",
        cache: false,
        async:'asynchronous',

        success: function(returndata){
            res = JSON.parse(returndata)
            error = res['error']
            if(error == 0 || error == 2){ // 0: no error, 2: experiment stored but email not sent
                if(error==0){
                    alert("Report has been successfully flagged into the AIDA archive.")
                }
                else {
                    alert("Report has been successfully flagged into the AIDA archive but it is impossible to send an email to: "+email+".")
                }
                /*update history*/
                out_hist = {
                    "filename" : filename,
                    "flag" : expstatus,
                    "period" : document.getElementById("period").value
               }
                $.ajax({
                    type: "POST",
                    url: "functions.php",
                    data: {
                        action: "update_history",
                        username : creator,
                        operation : "Report Flagged",
                        infile :    filename,
                        out : JSON.stringify(out_hist),
                        config : "See report details"
                        },
                    error : function (obj, textstatus) {
                        alert("Impossible to store the operation in History")
                    }
                })             
            }
            else {
                alert("Impossible to flag report into the AIDA archive. Please retry later or contact AIDA admin.")
            }
        },
        complete:function(data){
            // Hide loader image container
            $("#loader").hide();
            location.reload()
        }
    });
}

/**
 * Parses uploaded backup archive payload via Python backend script.
 *
 * @param {string} filename Backup archive filename.
 */
function upload_backup(filename){
    //Read data from uploaded files
    var user = document.getElementById("session-user").innerHTML
    $("#loader").show();    

    //AJAX TO GET COLUMNS
    $.ajax({
        url: "scripts/backup.py",
        method      : 'POST',
        datatype    : 'json',
        data : {
            "filename" : filename,
            "user" : user,
            "action" : "upload"
        },
        success:function(res)
        {
            var error = res['error']
            var cols = res['msg']
            switch(error)
            {
                case 0: //all ok
                {
                    $('#progressbar').fadeOut().progressbar();
                    $('#uploader').hide()              
                    $('#cols').val(cols)
                    $('#okupload').show()
                    $('#btn-div').show()
                    for(var i=0;i<cols.length;i++){
                        $("#check_"+i).css("display", cols[i]);
                    }
                    $('#import_items').show()
                    $("#loader").hide();
                    break;
                }
                case 1: //error uploading
                {
                    var msg = res['msg']
                    reset = alert(msg)
                    $('#progressbar').fadeOut().progressbar();
                    document.getElementById("file-preview").innerHTML = ""
                    $("#loader").hide();                    
                    //if(reset){} else {window.location.reload()}       
                    break;                  
                }
                case 2: //missing users data
                {
                    var goon = confirm("Missing Users data. Once import is completed, you should register the first admin.\n\n Proceed anyway?")
                    $('#progressbar').fadeOut().progressbar();
                    if(goon){
                        $('#uploader').hide()                      
                        $('#cols').val(cols)
                        $('#okupload').show()
                        $('#btn-div').show()
                        for(var i=0;i<cols.length;i++){
                            $("#check_"+i).css("display", cols[i]);
                        }
                        $('#import_items').show()                    
                    }
                    else{
                        document.getElementById("file-preview").innerHTML = ""                    
                    }
                    $("#loader").hide();                    
                    break;                  
                }                
            }            
        },
        error:function(){
            alert("Error! Impossible to upload the file")
            $('#progressbar').fadeOut().progressbar();
            document.getElementById("file-preview").innerHTML = ""          
            $("#loader").hide(); 
        }
    })
}

/**
 * Deletes uploaded temporary PDF file via AJAX.
 */
function remove_upfile(){
    $('#okupload').hide()
    document.getElementById("file-preview").innerHTML=""
    $('#uploader').show()
    $('#btn-div').hide()
    $('#import_items').hide()
    var file = document.getElementById("upfile-preview").innerHTML
    $.ajax({
        url: "functions.php",
        method      : 'POST',
        datatype    : 'json',
        data : {
            "file" : "tmp/"+file,
            "action" : "deletepdf"
        }
    })  
}

/**
 * Navigates to target tab step in wizard.
 *
 * @param {Array<string>} idlist Array of tab DOM IDs.
 * @param {number} n Step index.
 */
function showtab(idlist, n){
    if(idlist.length > 0){
        var oldtab = "import_bkp"
        var newtab = idlist[n]
        if(n>0){
            oldtab = idlist[n-1]
        }
        $('#'+newtab).show()
        $('#'+oldtab).hide()
    }
}

/**
 * Navigates back to previous wizard tab.
 *
 * @param {string} el Current step identifier.
 */
function backtab(el){
    var idstr = $("#nextform").val()
    var idlist = idstr.split(",")   
    let curridx = idlist.indexOf(el+"_form")    
    $('#'+el+"_form").hide()
    if(curridx-1 >= 0){
        $('#'+idlist[curridx-1]).show()
    }
    else{
        $('#import_bkp').show()
    }
}

/**
 * Saves SMTP configuration via Python backend script.
 *
 * @param {string} el Calling step identifier.
 */
function store_smtp(el){
    $.ajax({
        url: "scripts/backup.py",
        method      : 'POST',
        datatype    : 'json',
        data : {
            "host" : document.getElementById("conf_host").value,
            "port" : document.getElementById("conf_port").value,
            "user" : document.getElementById("conf_user").value,
            "pwd" : document.getElementById("conf_pwd").value,          
            "action" : "savesmtp"
        },
        success:function(res)
        {
            var error = res['error']
            switch(error){
                case 0:
                {
                    $("#loader").hide();                        
                    alert("SMTP data correctly stored")
                    nexttab(el)
                    break;
                }               
                case 1:
                {
                    $("#loader").hide();                        
                    alert("Error storing SMTP data. Please retry or contact AIDA support team.")
                    break;
                }
                case 2:
                {
                    $("#loader").hide();                        
                    alert("ERROR! SMTP connection check failed. Please check your settings.")
                    break;
                }               
                
            }
        },
        error:function(){
            alert("Error storing SMTP data. Please retry or contact AIDA support team.")
            $("#loader").hide(); 
        }
    })  
}

/**
 * Prompts user to confirm installation abort and restores application defaults.
 */
function abort_install(){
    var abort = confirm("Application will be restored to default setting, by deleting imported data and already set configurations.\nAre you sure?")
    if(abort){
        $("#loader").show();
        $.ajax({
            url: "scripts/backup.py",
            method      : 'POST',
            datatype    : 'json',
            data : {
                "action" : "flush"
            },
            success:function()
            {
                $("#loader").hide();                        
                alert("Application restored. You have to restart installation procedure to use AIDA.")
                window.location.href = "index.php";
        
            },
            error:function(){
                alert("Error! Impossible to restore application. You can start a brand new installation to overwrite stored settings.")
                $("#loader").hide(); 
            }
        })          
    }
}

/**
 * Validates installation step input forms.
 *
 * @param {string} el Step identifier ('smtpconf' or '1streg').
 */
function validate_install(el){
    switch(el){
        case "smtpconf":
        {
            if($('#smtpconf').validate().form()) {
                $("#loader").show();
                store_smtp(el)
            }
            break;
        }
        case "1streg":
        {
            requestnewuser($('#signupform').form)
            break;
        }       
    }
    
    // initialize the validator
    $('#smtpconf').validate({
        highlight: function(element) {
            $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
        },
        success: function(element) {
            $(element).closest('.form-group').removeClass('has-error');
        },
    }); 
}

/**
 * Navigates to next wizard tab or completes installation.
 *
 * @param {string} el Current step identifier.
 */
function nexttab(el){
    var idstr = $("#nextform").val()
    var idlist = idstr.split(",")
    let curridx = idlist.indexOf(el+"_form")
    if(curridx < (idlist.length-1)){
        showtab(idlist, curridx+1)
    }
    else{
        clean_installation()
    }   
}

/**
 * Refreshes user and global history treeviews via AJAX.
 */
function refresh_history(){
    $("#wait_history").show();  
    var role = document.getElementById("session-role").innerHTML
    update_history('','treeUserHist');
    if(role=="admin"){
        update_history('global','treeGlobalHist');
    }
    setTimeout(() => { $("#wait_history").hide(); }, 2500);
}

/**
 * Configures system selection options based on subsystem inputs.
 *
 * @param {HTMLElement} ic Subsystem input element.
 * @param {boolean} [fromdb=true] Database query flag.
 * @param {string} [next="sys"] Target select element identifier.
 */
function set_sys_options(ic, fromdb=true, next="sys"){
    var par = ic.id.split("-")[0]
    var system = document.getElementById("hktm_source").value; //EFD
    var stats = document.getElementById('stats_enable').value;
    var usecase = document.getElementById('usecase').value; //HTKM
    var element = document.getElementById(par+"-"+next);    
    

    if(fromdb==true){
        
        var url   =   'functions.php';
        $.ajax({
            method:"POST",
            url:url,
            data:{
              action : "get_parameter_group",
              syst : system,
              origin : usecase,
              subs : document.getElementById(ic.id).value
            },
            success:function(data)
            {
                element.innerHTML='<option value="" disabled selected>Select Field</option>'+data
            }
        });
        $("#"+par+"-"+next).show()
    }
    else    
    {
        alert("NOT IMPLEMENTED YET")
    }
}

/**
 * Fetches filtered parameter options based on subsystem selections.
 *
 * @param {HTMLElement} div Filter selection element.
 */
function set_par_options(div){
    var par_id = div.id.split("-")[0]
    var system = document.getElementById("hktm_source").value; //EFD
    var stats = document.getElementById('stats_enable').value;
    var usecase = document.getElementById('usecase').value; //HTKM

    var tbl = usecase+"_"+system.toLowerCase()
    var subs = document.getElementById(par_id+"-ic").value;
    var extra = div.value
    
    //console.log(tbl,subs,extra)
    const url = "functions.php"
    $.ajax({
        method:"POST",
        url:url,
        data:{
          action : "fetch_values_subsystem",
          cat_val : subs,           //y0-ic value
          cat_name : tbl,           //usecase+"_"+system
          cat_filter : extra                //extra => y0-sys value
        },
        success:function(data)
        {
          $("#"+par_id+"-params").html(data);
          $("#"+par_id+"-values").html("");     
          $("#"+par_id+"-params").show()
          show_addmore(par_id)
            if (stats == "advanced"){
                document.getElementById('stats').style='display:inline;';
            }         
        }
    }); 
    
    
}