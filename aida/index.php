<?php
/**
 * Application Entry Point and Router.
 *
 * Checks if the system setup is finalized (presence of `users/ready.log`).
 * Redirects to the wizard installation flow (`install.php`) if not configured,
 * otherwise loads the application landing page (`landing.php`).
 *
 * @package    AIDA
 * @subpackage Core
 * @author     Giuseppe Riccio
 * @version    1.1.0
 */
 ?>
<!doctype html>
<html class="fixed">

<?php
//redirect on installation if not yet done
if (!file_exists("users/ready.log")) {	
    include("install.php");
} else {
    include("landing.php");
}
?>

