/**
 * Triggers refresh of execution history for specific user or global context.
 *
 * @param {string} name Username identifier or "global".
 * @param {string} classname Target DOM container suffix/class.
 */
function update_history(name, classname){
	//refresh history on dashboard
	$("#wait_"+classname).show();
	if(name == "global"){
		get_history('global', classname);
	}
	else
	{
		var n = document.getElementById('session-user').innerHTML
		get_history(n, classname);
	}
	setTimeout(() => { $("#wait_"+classname).hide(); }, 2500);
}

/**
 * Triggers UI treeview component refresh on the dashboard.
 *
 * @param {string} name Target user or path name.
 * @param {string} classname Selector class/ID for target DOM container.
 * @param {string} ext File extension filter.
 * @param {string} olink Link target template URL.
 */
function update_tree(name, classname, ext, olink){
	//refresh trees on dashboard
	var s2 = classname.substr(1);
	$("#wait_"+s2).show();

	if(name.length == 0){
		var n = document.getElementById('session-user').innerHTML
		get_tree(n, classname, ext, olink, 1)
	}
	else
	{
		get_tree(name, classname, ext, olink, 1)
	}
	
	setTimeout(() => { $("#wait_"+s2).hide(); }, 2500);
}

/**
 * Fetches user or global history markup via POST request from backend script.
 *
 * @param {string} name Username or scope identifier.
 * @param {string} classname Target DOM container element ID.
 */
function get_history(name, classname){
	//Get history on dashboard
	var divid = document.getElementById(classname);
	$.ajax({
		type: "POST",
		url: "scripts/get_history.py",
		data: {
			'user' : name,
		},
		dataType: "html",
		cache: false,
		async:'asynchronous',
		success: function(returndata){
				if(returndata.length <= 11){
					divid.innerHTML = "No history data available"
				}
				else{
					divid.innerHTML = returndata
				}
			},
		error : function(e){
				
				divid.innerHTML = "Unable to load history tree. Please retry."
                console.log(e)
		}
	});
};

/**
 * Asynchronously retrieves file directory listings and populates or refreshes jsTree instances.
 *
 * @param {string} name Main directory name.
 * @param {string} classname Selector for tree target element.
 * @param {string} ext File extension filter.
 * @param {string} openlink Node action link URL.
 * @param {number} [refresh=0] Flag indicating whether to update existing tree data (1) or create new (0).
 */
function get_tree(name, classname, ext, openlink, refresh = 0){
	//Get trees on dashboard
	$.ajax({
        type: "POST",
        url: "scripts/get_listfile.py",
        data: {
			'maindir' : name,
			'ext' : ext,
			'link': openlink
		},
  
		dataType: "html",
        cache: false,
		async:'asynchronous',
		success: function(returndata){				
				var jdata = JSON.parse(returndata)
                if(jdata["error"] == 1){
                    divid = document.getElementById(classname.replace("#",""));
                    divid.innerHTML = "Unable to load directory tree. Please retry or contact AIDA admin."                  
                }
          		else
                {
					if(refresh == 0){
                          var t = $(classname).jstree({
                            'core' : {
                                'themes' : {
                                    'responsive': false
                                }, 
                                'check_callback' : true,
                                'data' : jdata
                                }
                          });
                  	}
                 	else
                  	{
                      	$(classname).jstree(true).settings.core.data = jdata;
                     	 $(classname).jstree(true).refresh();
                 	}
                }
			},
		error : function(){
          		$(classname).html("Unable to load directory tree. Please retry.")          
		}
	});
};

/**
 * Instantiates a jsTree widget on target element using structured JSON data.
 *
 * @param {string} name Scope identifier.
 * @param {string} classname Selector for tree DOM element.
 * @param {string} jsondata JSON formatted tree hierarchy string.
 * @returns {Object} Initialized jsTree instance.
 */
function create_tree(name, classname, jsondata){
	//render tree from backend data
	var jdata = JSON.parse(jsondata)
	var t = $(classname).jstree({
		'core' : {
			'themes' : {
				'responsive': false
			}, 
			'check_callback' : true,
			'data' : jdata
		},
	});

	return t
}
