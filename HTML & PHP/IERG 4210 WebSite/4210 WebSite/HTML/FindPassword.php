<html>
    <link href = "../CSS/MainPage.css" rel = "stylesheet" type = "text/css" />
	<head>
		<meta charset= "utf-8" />
		<title> Find Password by Email</title>  
	</head>
	<body>
        <div id = welcome>
            <h1> Find Password by Email </h1>
        </div>
        <?php
            include_once('csrf.php');
            echo 
            '<form id = "FindPassword" method= "POST" action="auth-process.php?action=sendEmail">
                <label> Email: </label>
                <input type="email" name= "Email" required="true" pattern="^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$" /> <br> <br>
                <input type="hidden" name="nonce" value="'; echo csrf_getNonce('sendEmail'); echo '" />
                <input type= "submit" value="Submit" />
            </form>';         
        ?>
	</body>
</html>
