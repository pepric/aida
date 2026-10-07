<?php
/**
 * Running Reports Table View Component.
 *
 * Renders the HTML table structure and queries running report tasks for the current user or administrator.
 *
 * @package    AIDA
 * @subpackage Views\Components
 * @author     Giuseppe Riccio
 * @version    1.1.0
 */
?>
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
											
											