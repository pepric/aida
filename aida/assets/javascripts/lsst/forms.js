function formhash(yourform, password, frompage, addmsg="") {
   // Create input that will be used as output field for cripted pwd
   var p = document.createElement("input");
   // Add element
   yourform.appendChild(p);
   p.name = "p";
   p.id = "p";
   p.type = "hidden"
   p.value = hex_sha512(password.value);
   // Pwd not sent as visible.
   password.value = "";

   //submit
   switch(frompage){
     case 'login':
       yourform.submit();
       break;
     case 'new':
		let isinstall = document.getElementById("firstinst").value
		if(isinstall==1){
			var confemail = document.getElementById("notiemail").value
			console.log(confemail)
		}
		else{
			var confemail = ""
		}
		$.ajax({
			method:"POST",
			url:"register.php",
			data:{
				name : document.getElementById("name").value,
				email : document.getElementById("email").value,
				role : document.getElementById("role").value,
				p : p.value,
				install : isinstall,
				confem : confemail,
				captcha_challenge : document.getElementById("captcha").value
			},
			beforeSend: function(){
				// Show loader image container
				$("#loader").show();
			},
			success:function(err){
				$("#loader").hide();
				switch(err){
					case "0":
						//no error
						var user = document.getElementById("name").value;
                       	var install = document.getElementById("firstinst").value
                        if(install==1){
							document.getElementById('reg-comp-ok').innerHTML='<h4>Thank you, '+user+'. Your request has been successfully sent.</h4><p>An activation email has been sent to your email address.'+addmsg+'</p>'+'<br/><p>Now you can close this page.</p>'
							$('#modal-install').modal('show');								
                        }
                      	else{
							alert('Thank you, '+user+'. Your request has been sent successfully. Your account will be activated as soon as possible.\n'+addmsg);
							window.location.href='index.php';								
                        }
						break;
					case "1":
						//already existing user
						alert('Registration failed! User already present in AIDA DB. Please, change name and/or e-mail address or contact AIDA admin.\n'+addmsg);
						var pwdconf = document.getElementById("password_confirm");
						pwdconf.value = "";
						$("#p").remove()
						break;
					case "2":
						//record not inserted in DB
						alert('Registration failed! Impossible to connect to database. Please contact AIDA admin.\n'+addmsg);
						window.location.href='index.php';
						break;
					case "3":
						//error sending emails
						alert('WARNING! Your request has been successfully submitted but it is not possible to access to the mail server. Please, directly contact AIDA admin to check your request.\n'+addmsg);
						window.location.href='index.php';
						break;
					case "4":
						//error captcha
						alert('Registration failed! Incorrect CAPTCHA\n'+addmsg);
                       	document.getElementById("captcha").value="";
						break;
					case "5":
						//created first user but failed to send email
						alert('Registration failed! Impossible to sent confirmation email. Please, check your SMTP settings and retry.\n'+addmsg);
						window.location.href='index.php';
						break;							
				}
			}
		});
       	break;
     case 'change':
		var user = document.getElementById('session-user').innerHTML
        var oldpwd = document.getElementById('oldpwd').value
        var oldp = hex_sha512(oldpwd)
		var newp = document.getElementById('p').value
		$.ajax({
			method:"POST",
			url:"functions.php",
			data:{
				username : user,
				oldpwd : oldp,
                newpwd : newp,
                action : "change_pwd"
			},
			success:function(result){
               	var json = JSON.parse(result);
				alert(json["error"])
				if(json["logout"] == 1){window.location.href = "logout.php";}
			}
		});
       	break;
    }
}

function requestnewuser(yourform, msg=""){
    if($('#signupform').validate().form()) {
		pwd = document.getElementById("password");
		formhash(yourform, pwd, 'new', msg);
    }		
}

function sendreset(){
	if($('#resetform').validate().form()) {
		var email = document.getElementById("email").value;
		$.ajax({
			method:"POST",
			url:"functions.php",
            data:{
              user : email,
              action : "reset_pwd"
            },
		   success:function(result){
               	var json = JSON.parse(result);
				alert(json["error"])
             	window.location.href = "index.php"
			}
		});    
	}		
}

function pwd_confirm(){
    if($('#updatepwd').validate().form()) {  
		var email = document.getElementById('email').value
		var newp = document.getElementById('pass1').value
        var password = hex_sha512(newp);
		$.ajax({
			method:"POST",
			url:"functions.php",
			data:{
				email : email,
            	newpwd : password,
        	 	action : "confirm_pwd_reset"
			},
	   		success:function(result){
           		var json = JSON.parse(result);
				alert(json["error"])
				window.location.href = "index.php"
			}
		});
    }
}
