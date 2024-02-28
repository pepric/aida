				<div class="header-right" id="header-right">
					<span class="separator"></span>
					<?php if($check==true){?>
						<?php if($currentpage != $dash){
									$display_box = 'style="display:none"';
									}
									else{$display_box = '';}
									?>
							<div id="userbox" class="userbox" <?php echo $display_box;?>>
								<a href="#" data-toggle="dropdown">
									<div class="profile-info" >
										<span class="name" id="session-user"><?php echo $_SESSION['username'];?></span>
										<span style="display:none;" id="session-role"><?php echo $_SESSION['role'];?></span>
									</div>
					
									<i class="fa custom-caret"></i>
								</a>
					
								<div class="dropdown-menu">
									<ul class="list-unstyled">
										<li class="divider"></li>
										<li>
											<a role="button" href="#" tabindex="-1" id="change_pwd" data-toggle="modal" data-target="#pwd"><i class="fa fa-lock"></i> Change Password</a>
											<!--<a role="menuitem" tabindex="-1"data-open="sidebar-right" href="#"><i class="fa fa-history"></i> History</a>-->
											<!--<a role="menuitem" tabindex="-1" href="logout.php"><i class="fa fa-user"></i> Logout</a>-->
                                          	<a role="menuitem" tabindex="-1" onclick="session_logout()" href="#"><i class="fa fa-user"></i> Logout</a>
										</li>
									</ul>
								</div>
							</div>
						
					<?php }else{ ?>
						<div class="login-box">
                          	<div class="login-panel">
                              <form method="post" action="javascript:login();" id="login_form" name="login_form">
                                 <input type="text" class="field" id="email" name="email" placeholder = "Email"/>
                                 <input type="password" class="field" name="password" id="password" placeholder = "Password"/>
                                 <input type="button" value="Login" id="loginbtn" class="btn btn-default" onclick="formhash(this.form, this.form.password, 'login');" />

                              </form>
                          	</div>
                          	<div class="login-adds">
								<table>
                                  	<tr><td>
                                 		<!--<a href="signup.html">Signup</a>-->
                                      	<a href="signup.php">Signup</a>
                                  	</td></tr>
                                  	<tr><td>
                                 		<a href="recovery.php">Forgot password?</a>
                                  	</td></tr>                                      

								</table>
                            </div>
						</div>
					<?php } ?>
				</div>
				<!-- end: search & user box -->
<script>
	function login(){ 
		var user = document.getElementById('email').value	  	
		var pwd = document.getElementById('p').value
		$.ajax({
			   method:"POST",
			   url:"functions.php",
			   data:{
				   email : user,
				   p : pwd,
                   action : "process_login"
			   },

			   success:function(logged){
                  if(logged==1){
                  	window.location.href='dashboard.php';
                 }
                  else{
                  
 					alert('Error Logging In! Please retry');                 
                  	$("#p").remove()
                  }
			}
		});
    }
</script>