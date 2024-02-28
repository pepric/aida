$(document).ready(function(){
		//get tree of files in "Navigation" panel
		var name = document.getElementById("session-user").innerHTML;
		files_tree("image", "#treeImg", ["fits", "png"], 1)  
});	

$(document).ready(function(){
	var file = document.getElementById("img_file").value;
  		
	if(file!="None"){
		setTimeout(function(){
  			JS9.Load(file, {}, {display : "JS9"})
		}, 3000);      
		
      	$('#flag_img').show()
       	var isflagged = document.getElementById("isflagged").value;
       	if(isflagged==1){
			$('#flag_img').hide()
			//show comments about flagging
            $('#flag_notes').show()
		}
	}
});	

$(document).ready(function(){
	//Init flagging comments when changing flag status
	$("input[type='radio'][name=optflag]").change(function(){
		$('#input-descr').val('');
		if($(this).val()!="nd")
			{
				$("#description").show();
				$("#alert-email").show();
			}
		else
			{
				$("#description").hide();
              	$("#email-to").val('')
				$("#alert-email").hide();
			}
	});
});

$(document).ready(function() {
	$(document).on('click', '#store-img-btn', function () {
		//Store flag for the image
	  if($('#modal-form').validate().form()) {
		  //get public/private archive  
		  var store = document.getElementById("mode")
		  var save = store.options[store.selectedIndex].value  
		  //get flag
		  var expstatus = $('input[name=optflag]:checked').val();
		  //get description
		  var descr = document.getElementById('input-descr').value;  
		  //get alert email
		  var email = document.getElementById('email-to').value;
		  //filename
		  //var filename = $('input[name="id"]').val().split("[")[0]
		  var filename_arr = JS9.GetImage()['file0'].split("/")
		  var filename = filename_arr[filename_arr.length-1]		  
		  //console.log(filename)
		  //get usr
		  var user = document.getElementById('session-user').innerHTML;
		  //get source
		  var source = document.getElementById('hktm_source').value;
		  //get content of hidden filename input area
		  var fullname = document.getElementById("img_file").value
          
          exportImg(filename, save, expstatus, descr, email, user, source)
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

function exportImg(filename, save, expstatus, descr, email, user, source){
	//store flagged image
	$("#loader").show();
	var download = document.getElementById("downloadpdf").checked   

	//store images
  	var divs = ["JS9", "js9_3dPlot", "js9_XProj", "js9_YProj", "js9_Histogram", "js9_EncEnergy", "js9_RadialProj", "js9_RegionStats"]
	for (let i = 0; i < divs.length; i++) {
 		exportAndSaveCanvas(divs[i])
	}     

	pyscript = "scripts/pdfcreator.py";
	$.ajax({
        type: "POST",
        url: pyscript,
        data: {
          	"plot" : "image",
			"filename" : filename,
			"source" : source,
			"user"	: user,
			"notes"	: descr,
			"status" : expstatus,
			"save" : save,
			"email" : email,
          	"images" : divs,
          	"fullname" : JS9.GetImage()['file0']
		} ,
		dataType: "html",
        cache: false,
		async:'asynchronous',

		success: function(returndata){
			res = JSON.parse(returndata)
			error = res['error']
			if(error == 0 || error == 2){ // 0: no error, 2: experiment stored but email not sent
			
				if(error==0){
					alert("Image has been successfully stored into the AIDA archive.")
				}
				else {
					alert("Image has been successfully stored into the AIDA archive but it is impossible to send an email to: "+email+".")
				}
            	//document.getElementById('flag_img').style.display = "none"		//hide flag button
              
				// Download pdf             
				if(download==true){
					filepath = res['pdffile']
					fileurl = document.location.origin+"/"+filepath
					filesplit = filepath.split("/")
					var pdffilename = filesplit[filesplit.length-1]
					downloadPDF(fileurl, pdffilename, save);

				}           
              
              	/*update history*/
              	out_hist = {
                	"filename" : filename,
                  	"source" : source,
                  	"flag" : expstatus,
                  	"archive" : save.charAt(0).toUpperCase() + save.slice(1)
               }
				$.ajax({
					type: "POST",
					url: "functions.php",
					data: {
						action: "update_history",
						username : user,
						operation : "Image Flagged",
						infile :	filename,
						out	: JSON.stringify(out_hist),
						config : "NA"
						},
					error : function (obj, textstatus) {
						alert("Impossible to store the operation in History")
					}
				})             
				//refresh Navigation tree
				files_tree("image", "#treeImg", ["fits", "png"], 1,1)
				//show Flag Info panel
				render_flag_table(filename, "all")				
				render_flag_table(filename, user)				
	            $('#flag_notes').show()
              
			}
			else {
				alert("Impossible to store image into the AIDA archive. Please retry later or contact AIDA admin.")
			}
		},
		complete:function(data){
			// Hide loader image container
			$("#loader").hide();
		}
    });
}


function open_panel(){
		//New image explorer panel
		window.open("image-explorer.php");
    }

function flag_image(){
	//open flag modal on click
	if(JS9.GetImage()!=null){
		var filename_arr = JS9.GetImage()['file0'].split("/")
		var filename = filename_arr[filename_arr.length-1]
	}
	else{
		filename=null
	}
	//try to get source
	var fullname = document.getElementById("img_file").value
	if(fullname != "None"){
      	var source = fullname.split("/")[fullname.split("/").length - 2].toUpperCase()
		var selsrc = document.getElementById("hktm_source")
        selsrc.value = source;
    }
	if(filename != null && filename != ""){
		document.getElementById("nd").checked = true;
        $("#description").hide();
		$('#input-descr').val('');      
        $("#email-to").val('')
        $("#alert-email").hide();

        //create temporary <a> to click and open modal div
        var element = document.createElement('a');

        element.setAttribute('data-target', "#store_img")
        element.setAttribute('role', "button")
        element.setAttribute('data-toggle', "modal")
        element.style.display = 'block';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
  	else{
    	alert("No image to flag")
    }
}

function files_tree(name, classname, ext, openlink, refresh = 0){
	//Init Navigation tree
	$.ajax({
        type: "POST",
        url: "scripts/get_listfile.py",
        data: {
			'maindir' : name,
			'ext' : ext,
			'link': openlink,
          	'user' : document.getElementById("session-user").innerHTML,
          	'startimg' : document.getElementById("img_file").value
		},
		dataType: "html",
        cache: false,
		async:'asynchronous',
		success: function(returndata){
				var jdata = JSON.parse(returndata)
				//console.log(jdata)
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
			},
		error : function(){
          		$(classname).html("Unable to load directory tree. Please retry.")
		}

			
	});
};

function exportAndSaveCanvas(el)  {
	//export image
  	html2canvas($("#"+el)[0]).then((canvas) => { 
        var imgData = canvas.toDataURL('image/jpeg');
		var filename_arr = JS9.GetImage()['file0'].split("/")
		var filename = filename_arr[filename_arr.length-1]		
        var url = 'functions.php';
        $.ajax({ 
          type: "POST", 
          url: url,
          dataType: 'text',
          data: {
            action : "export_img",
            base64data : imgData,
            fname : el,
            user : document.getElementById("session-user").innerHTML,
            //imname : dirimg
			imname : filename
          }
        })
    }); //End html2canvas
} // End exportAndSaveCanvas()


 //init flags table 
$( document ).ready(function() {
	var isf = document.getElementById('isflagged').value
	var filename = document.getElementById('img_file').value
	//init public flagged table
	render_flag_table(filename)
	//init private flagged table
	var user = document.getElementById("session-user").innerHTML
	render_flag_table(filename, user)
});


function render_flag_table(filename, user = "all"){
	//render Flags Info panel
	onlyname_arr = filename.split("/")
	title = onlyname_arr[onlyname_arr.length - 1]
	$("#flags_info_title").html("<b>Filename: "+title+"</b>")	
	if(user=="all"){
		var cols = [
			{ mData: 'Flag' } ,
			{ mData: 'User' },
			{ mData: 'Notes' }
		]  
		var tbl = "#datatable-notes-public"
		var target = 2
	}
	else{
		var cols = [
			{ mData: 'Flag' } ,
			{ mData: 'Notes' }
		]
		var tbl = "#datatable-notes-private"
		var target = 1
	}

	var activetable = $(tbl).DataTable( {
		"ajax": {
			"type": "POST",
          	"url": "scripts/cs_interface.py",
			"data": {
				"action" : "flagged_images",
				"filename" : filename,
				"user" : user
			}
		},
		destroy: true,
      	autoWidth : false,
		"searching": false,
		"bPaginate": false,
		"bInfo": false,
      	"columns": cols,
      	"columnDefs" :[ {orderable:false, targets : target}]
	});	
}

function data2cat(catalog, ext=".cat"){

    switch(ext){
		case "csv":
			var cattab = catalog.replace(/,/g, '\t')
			var dashes = []
			var splitted_data =cattab.split("\n")
			var header = splitted_data[0].split("\t")


			for(var i=0; i<header.length; i++){
				var v = header[i]
				const l = v.length
				dashes.push("-".repeat(l))
			}	
			dashes = dashes.join("\t")	

			splitted_data.splice(1, 0, dashes);
			var newcat = splitted_data.join("\n")
			
			break;
		default:
			var splitted_data = catalog.split("\n")
			var newcat=[]
			for(var i=0; i<splitted_data.length; i++){
				var el = splitted_data[i]
				if(el[0] == "#" && splitted_data[i+1][0] != "#"){
					//this is the header
					newcat = build_record(el, newcat, true)
				}
				else if(el[0] == "#" && splitted_data[i+1][0] == "#"){}
				else {newcat = build_record(el, newcat)}
			}
			newcat = newcat.join("\n")
			break;
	}
	
	return newcat
}

function build_record(el, newcat, header = false){
	el = el.split(" ")
	var newel = []
    var dashes = []
	for(var j=0;j<el.length;j++){
		var v = el[j] 
		if(v != "" && v!="#"){
			newel.push(v)
			if(header){
				const l = v.length
				dashes.push("-".repeat(l))					
			}
			
		}
	}
	newel = newel.join("\t")
	newcat.push(newel)
    if(header){
        dashes = dashes.join("\t")
        newcat.push(dashes)	
	}
	
	return newcat
}