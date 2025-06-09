<?php   

	$homeurl = 'index.php';                               
	$homepage = "";
	$path = $_SERVER['REQUEST_URI'];
	$current_array = explode("/", $path);
	$currentpage = end($current_array);
	//only for landing page
	if($currentpage == $homepage or $currentpage == $homeurl) {?>
		<footer class = "page-footer">
			<div class = "col-md-2"></div>
			<div class = "col-md-2">
				<h3>Useful Links</h3>
				<ul>
					<li><a href="https://rubinobservatory.org/" target="_blank">Rubin-LSST Official</a></li>
					<li><a href="https://www.lsst.org/scientists/in-kind-program" target="_blank">Rubin-LSST In-Kind Program</a></li>
					<li><a href="https://rubinobservatory.org/for-scientists/resources/community-forum" target="_blank">Rubin Community Forum</a></li>
					<li><a href="https://www.inaf.it/" target="_blank">INAF</a></li>
				</ul>
			</div>
			<div class = "col-md-4 logodiv">
				<h3>AIDA is a Rubin-LSST project for monitoring, analysis & visualization for commissioning phase</h3>
				<div class="logos">
					<img src="assets/images/INAF_logo.png" height="100" alt="">
					<!--<img src="assets/images/esa_logo.png" height="100" alt="">
					<img src="assets/images/asi_logo.png" height="100" alt="">-->
                    <img src="assets/images/vera.png" height="100" alt="">
                    <img src="assets/images/lsstback2.png" height="100" alt="">
				</div>
			</div>
			<div class = "col-md-2">
				<h3>Credits & Contacts</h3>
				<p>For infos and technical support:</p>
				<ul>
					<li><a href="mailto://giuseppe.riccio@inaf.it">G. Riccio - giuseppe.riccio@inaf.it</a></li>
					<li><a href="mailto://massimo.brescia@inaf.it">M. Brescia - massimo.brescia@inaf.it</a></li>
					<li><a href="mailto://stefano.cavuoti@gmail.com">S. Cavuoti - stefano.cavuoti@gmail.com</a></li>
				</ul>
			</div>
			<div class = "col-md-2"></div>

		</footer>
		
	<?php } ?> 

	
