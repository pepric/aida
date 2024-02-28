(function( $ ) {

	'use strict';

	var datatableInit = function() {

      	function render_flag(data, type){
         	if (type === "exportcsv") {
               	data = data.replace('<img src="assets/images/nd.png"><span style="display:none">0</span>', "Not Defined");
               	data = data.replace('<img src="assets/images/ok.png"><span style="display:none">1</span>', "Ok");
               	data = data.replace('<img src="assets/images/warning.png"><span style="display:none">2</span>', "Warning");
               	data = data.replace('<img src="assets/images/serious.png"><span style="display:none">3</span>', "Serious");
         		return data;
         	}
   			return data;        
       }
      
		//TEMPORARY UPLOADED FILES
		var t_upl = $('#datatable-uploaded').DataTable({"language" :{"emptyTable": "No Data Available"},"columnDefs" :[ {orderable:false, targets : [2]}]});      
      
      	//TEMPORARY LOCAL DATA FILES
		var t_temp = $('#datatable-temp').DataTable({"language" :{"emptyTable": "No Data Available"},"columnDefs" :[ {orderable:false, targets : [5]}]});            
      
      
      
      	// STORED FILES TABLES (periodic/ondemand)
		var t_rep_p = $('#datatable-report-per').DataTable({"columnDefs" :[ {orderable:false, targets : [11]}]});
		var t_rep_o = $('#datatable-report-ond').DataTable({"columnDefs" :[ {orderable:false, targets : [10]}]}); 
      
      	// REPORTS TABLES (user/global)
		var t_stored_u = $('#datatable-stored-user').DataTable({"columnDefs" :[ {orderable:false, targets : [4]}]});
		var t_stored_g = $('#datatable-stored-global').DataTable({"columnDefs" :[ {orderable:false, targets : [5]}]}); 
     
      	// GENERATE REPORT FROM EXISTING TABLE
		var t_owner = $('#datatable-personal').DataTable({"columnDefs" :[ {orderable:false, targets : [7]}]});

      	// ????
		var t_glob = $('#datatable-global').DataTable();
      
		// CONFIG FILE TABLES (periodic/ondemand/uncomplete)      
		var t_per = $('#datatable-periodic').DataTable({"columnDefs" :[ {orderable:false, targets : [8]}]});
		var t_ond = $('#datatable-ondemand').DataTable({"columnDefs" :[ {orderable:false, targets : [9]}]});      
		var t_unc = $('#datatable-uncomplete').DataTable({"columnDefs" :[ {orderable:false, targets : [5]}]});
      
      	// SYSTEM INFO TABLE
		var t_sysinfo = $('#datatable-systems').DataTable({
          "dom" : "rftp",
          "language": {"emptyTable": "No Systems defined"}, 
          "bPaginate":false, 
          "columnDefs" :[ {orderable:false, targets : [2]}]
        });
      
      	//PLOTS INFO TABLE
		var t_plotinfo = $('#datatable-analysis').DataTable({
          "dom" : "rftp",
          "language": {"emptyTable": "No Analysis defined"}, 
          "bPaginate":false, 
          "columnDefs" :[ {orderable:false, targets : [2]}]
        });       
 		
		t_per
			.order( [ 1, 'desc' ])
			.draw();
		t_ond
			.order( [ 1, 'desc' ])
			.draw();
		t_owner
			.order( [ 1, 'desc' ])
			.draw();
		t_glob
			.order( [ 1, 'desc' ])
			.draw();
		t_unc
			.order( [ 1, 'desc' ])
			.draw();		
		t_sysinfo
			.order( [ 0, 'asc' ])
			.draw();
		t_plotinfo
			.order( [ 0, 'asc' ])
			.draw();      
		t_stored_u
			.order( [ 0, 'asc' ])
			.draw();
		t_stored_g
			.order( [ 0, 'asc' ])
			.draw();
		t_rep_p
			.order( [ 1, 'desc' ])
			.draw();
		t_rep_o
			.order( [ 1, 'desc' ])
			.draw();
		t_upl
			.draw();
      	t_temp
			.draw();        
	};

	$(function() {
		datatableInit();
	});
}).apply( this, [ jQuery ]);

function initParTbl(){
  		//PARAMETER INFO TABLE
	  	var t_parinfo = $('#datatable-params').DataTable( {
          	"dom" : "rftip",
          	"language": {"emptyTable": "No Parameters to show"},
			"order": [[ 0, 'asc' ]],
			"bPaginate":true,
			"bProcessing": true,
			"pageLength": 15
		});
}