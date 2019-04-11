<html>
    <link href = "../CSS/MainPage.css" rel = "stylesheet" type = "text/css" />
	<head>
		<meta charset= "utf-8" />
		<title> Book Store of Showing - Register</title>  
	</head>
	<body>
        <div id = welcome>
            <h1> Register </h1>
        </div>
        <?php
            include_once('csrf.php');
            echo 
            '<form id = "Register" method= "POST" action="auth-process.php?action=register">
                <label> Email: </label>
                <input type="email" name= "Email" required="true" pattern="^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$" /> <br> <br>
                <label> Password: </label>
			    <input type="password" name="Password" required="true" pattern="^[A-Za-z_\d]\w{2,19}$" />
                <label> Comfirm Password: </label>
			    <input type="password" name="Password_RE" required="true" pattern="^[A-Za-z_\d]\w{2,19}$" />
                <input type="hidden" name="nonce" value="'; echo csrf_getNonce('register'); echo '" />
                <input type= "submit" value="Submit" />
            </form>';         
        ?>
	</body>
</html>