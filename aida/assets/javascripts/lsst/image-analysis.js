$(document).ready(function () {
  $('#tend').prop('disabled', true);
  $('#tstart').datetimepicker({
    useCurrent: "day",
    timeZone : "UTC",
    format: 'YYYY-MM-DD HH:mm:ss',
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
      $('#tend').data("DateTimePicker").date(e.date);                
    }

  });
  $('#dateiconend').on("click", function (){$("#tend").focus()})
  $('#dateiconstart').on("click", function (){$("#tstart").focus()})
});

$(document).ready(function(){
    $('#img_filelist').DataTable({
        data: [],
        columns: [
            { title: 'FitsFile' },
            { title: 'Data Product' },
            { title: 'Date' },
            { title: '' }
        ],
        columnDefs :[{orderable:false, targets : [3]}]
    });   
  $("#sys_source").change(function(){
    //get current value
    var source = $("#sys_source").val();
    $.ajax({
      method:"POST",
      url: 'forms.php',
      data:{
        p : "image",
        o : "image",
        s : source
      },
      success :	function(resultdata){
        $( resultdata ).insertBefore( "#daterange" );
      }
    });
    $("#daterange").show();  
  });
  
  $("#img_op").change(function(){
    //get current value
    var results = document.getElementById("img_files_container")
	var jsondata = JSON.parse(results.value)
    var table = $('#img_filelist').DataTable()
    table.destroy();	
	render_image_filelist(jsondata) 
  });  
  
 $("#img_stats_submit").click(function(){
    //check form
	var error = 0
	var msg = ""
	//check operation
	var op = document.getElementById("img_op").value
	if(op==null || op==""){
		error = 1
		msg += "Operation not selected\n"
	}
	else{
		//check difference items
		if(op == "difference"){
			var a = document.getElementById("diff_A").value
			if(a==null || a==""){
				error = 1
				msg += "Missing A item\n"
			}
			var b = document.getElementById("diff_B").value
			if(b==null || b==""){
				error = 1
				msg += "Missing B item\n"
			}
		}			
	}
	if(error == 1){
		alert("CONFIGURATION ERROR!\n"+msg)
	}
	else{
		alert("Analysis process launched. An email will be send when analysis is completed.")
		//run analysis
		if(op=="difference"){
			var listfile = [a,b]
		}
		let user = document.getElementById("session-user").innerHTML;
		let source = document.getElementById("source_exp").value;
		var data2send = {
			'files' : listfile,
			'user'	: user,
			'op'	: op,
			'source' : source,
			'iodaurl' : window.location.host
		}
		console.log(data2send)
		$.ajax({
			type: "POST",
			url: 'scripts/run_img_analysis.py',
			data: data2send,
			dataType: "json",
			cache: false,
			async:'asynchronous'
		});
	}
  }); 
});

function get_list_files(){
    var table = $('#img_filelist').DataTable()
    table.destroy();
        //set data for AJAX
    var ny = parseInt($("#n_ypar").val());                
    data2send = {
        'action' : 'get_file_list',
        'source': $("#sys_source").val(),
        'yic0' : $("#y0-sys").val(),
        'tstart' : $("#tstart").val(),
        'tend' : $("#tend").val(),
        'ny' : ny
    }
    list_dps = []
    if (ny>1) {
        var additional_y_ic = []
        for (i=1; i<ny; i++){
            var new_y_ic = $("#y"+i+"-sys").val();
            additional_y_ic.push(new_y_ic);
        }
    }
    data2send.additional_y_ic = additional_y_ic
    //get list of files
    $.ajax({
        method:"POST",
        url: 'scripts/get_images_data.py',
        datatype : 'json',
        data: data2send,
        beforeSend: function(){
            //hide previous plot container
            $("#imgdata_container").hide()
            // Show loader image container
            $("#loader").show();
            window.document.body.scrollTop = 0;
            window.document.documentElement.scrollTop = 0;
        },                  
        success :	function(results){
            const errors = results["errors"]
            if(errors['errstatus'] == 0){
				document.getElementById("img_files_container").value=JSON.stringify(results)
                render_image_filelist(results)                
                if(errors['datastatus'] == 1){alert(errors['msg'])}
            }
            else{
                alert(errors['msg'])
            }
        },
        complete:function(){
            // Hide loader image container
            $("#loader").hide();
        }
    });
}

function render_image_filelist(data){
    dataset = []
	var coltitle = ""
	var action = document.getElementById('img_op').value
	var user = document.getElementById("session-user").innerHTML;
	var source = document.getElementById("source_exp").value;
	if(source == null || source == ""){
		source = document.getElementById("sys_source").value
	}
    for (const [ key, value ] of Object.entries(data)) {
        if(key != "errors"){
			var click = "to_image_explorer('"+key+"', '"+source+"', 'image', '"+user+"')"
			var full_k = '<a href="#" onclick="'+click+'">'+key+'</a>'
			full_k = key
			switch(action){
				case "difference" :{
					var coltitle = "Select items A-B"
					var form_btn = '<select id="'+key+'" class="form-control-imgtbl" onchange="set_diff(this)" required><option value=""></option><option value="A">A</option><option value="B">B</option></select><input type="hidden" id="in_'+key+'" value=""></input>'
					break;
				}
				default : {
					var coltitle = ""
					var form_btn = ""
				}
			}
            dataset.push([full_k,value["dp"],value["date"],form_btn])
        }
    }
	document.getElementById("source_exp").value = source
    $('#imgdata_container').show()
    $('#img_filelist').DataTable({
        data: dataset,
        columns: [
            { title: 'FitsFile' },
            { title: 'Data Product' },
            { title: 'Date' },
            { title: coltitle }
        ],
        columnDefs :[{orderable:false, targets : [3]}],
		searching: false,
		info : false,
		paging : false
    });    
}

function set_diff(elem){
	var fname = elem.id
	var pos = elem.value
	var old_fname = $('#diff_'+pos).val()
	var table = $('#img_filelist').DataTable()
	var data = table.rows().data()
	let nfiles = table.rows().count()
	for(var i=0; i<nfiles;i++){
		var curr_f = data[i][0]
		if(curr_f.includes("<")){curr_f = curr_f.split(">")[1].replace("</a","")}
		if(curr_f == old_fname){
			document.getElementById(curr_f).value = ""
		}
	}
	if(pos == "A"){
		var other_pos ="B"
	}
	else{
		var other_pos ="A"
	}	
	var curr_sel = document.getElementById('diff_'+pos)
	if(curr_sel != null){
		curr_sel.value = fname
		document.getElementById('in_'+fname).value=pos
		if(curr_sel.value == document.getElementById('diff_'+other_pos).value){
			document.getElementById('diff_'+other_pos).value = ""
		}
	}
	else{
		var old_pos = document.getElementById('in_'+fname).value
		document.getElementById('diff_'+old_pos).value = ""
		document.getElementById('in_'+fname).value=""
	}
}