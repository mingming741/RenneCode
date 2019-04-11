<html>
    <link href = "../CSS/MainPage.css" rel = "stylesheet" type = "text/css" />
	<head>
		<meta charset= "utf-8" />
		<title> Book Store of Showing - Change Password</title>  
	</head>
	<body>
        <div id = welcome>
            <h1> Change Password </h1>
        </div>
        <?php
            include_once('csrf.php');
            echo 
            '<form id = "ChangePassword" method= "POST" action="auth-process.php?action=changepsw">
                <label> Email: </label>
                <input type="email" name= "Email" required="true" pattern="^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$" />
                <label> Old Password: </label>
			    <input type="password" name="Password" required="true" pattern="^[A-Za-z_\d]\w{2,19}$" /> <br> <br>
                <label> New Password: </label>
			    <input type="password" name="Password_New" required="true" pattern="^[A-Za-z_\d]\w{2,19}$" />
                <label> Comfirm Password: </label>
			    <input type="password" name="Password_RE" required="true" pattern="^[A-Za-z_\d]\w{2,19}$" />
                <input type="hidden" name="nonce" value="'; echo csrf_getNonce('changepsw'); echo '" />
                <input type= "submit" value="Submit" />
            </form>';         
        ?>
	</body>
</html>
