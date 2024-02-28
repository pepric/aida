
<table class="table tab-reports table-bordered table-striped mb-none" id="datatable-running">
	<thead>
		<tr >
		<!--<th scope="col">#</th>-->
		<th scope="col">ID</th>
		<?php if($_SESSION["role"] == "admin"){?>
			<th scope="col">User</th>
		<?php }?>
		<th scope="col">Period</th>
		<th scope="col">Config File</th>
		<th scope="col">Start Run Date</th>
		<th scope="col">Progress</th>
		<?php if($_SESSION["role"] == "admin"){?>
			<th scope="col"></th>
		<?php }?>
	  </tr>
	</thead>


<?php 
	$result = get_running_reports($mysqli, $_SESSION["username"], $_SESSION["role"]); 
	render_view_running_reports($result, $_SESSION["role"]);

?>
	
</table>
											
											