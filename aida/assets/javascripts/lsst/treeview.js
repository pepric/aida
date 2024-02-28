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
