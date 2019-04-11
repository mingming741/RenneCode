<html>
    <link href = "../CSS/MainPage.css" rel = "stylesheet" type = "text/css" />
	<head>
		<meta charset= "utf-8" />
		<title> Book Store of Showing - Login</title>  
	</head>
	<body>
        <div id = welcome>
            <h1> Login </h1>
        </div>
        <?php
            include_once('csrf.php');
            echo 
            '<form id = "Login" method= "POST" action="auth-process.php?action=login">
                <label> Email: </label>
                <input type="email" name= "Email" required="true" pattern="^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$" /> <br> <br>
                <label> Password: </label>
			    <input type="password" name="Password" required="true" pattern="^[A-Za-z_\d]\w{2,19}$" />
                <input type="hidden" name="nonce" value="'; echo csrf_getNonce('login'); echo '" />
                <input type= "submit" value="Submit" />
            </form>';         
        ?>
        <br/><button type "button" class = "btn btn-warning"> <a href="Register.php">  Register </a> </button>
        <br/>
        <br/><button type "button" class = "btn btn-warning"> <a href="FindPassword.php">  Find Password </a> </button>
	</body>
</html>