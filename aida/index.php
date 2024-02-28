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

