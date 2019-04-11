<?php
include_once('db.php');
session_start();
error_reporting(E_ALL & ~E_NOTICE);
session_regenerate_id();

function loggedin()
{
    //Session run
	if (!empty($_SESSION['t4210']))
		return $_SESSION['t4210']['email'];
    //Session out but with cooike
	if (!empty($_COOKIE['t4210'])) {
		if ($token = json_decode(stripslashes($_COOKIE['t4210']), true)) {
			if (time() > $token['expire']) {
                return false;
            }
			$db = ierg4210_DB();
			$result = $db->prepare("SELECT * FROM User WHERE Email = (?)");
			$result->execute(array($token['email']));
			if ($array = $result->fetch()) {
				$key = hash_hmac('sha1', $token['expire'].$array['Password'], $array['Salt']);
				if ($key == $token['key'] && $array['Type'] == 1) {
					$_SESSION['t4210'] = $token;
					return $token['email'];
				}
			}
		}
	}
	return false;
}

//Without cookie
if (!loggedin()) {
    header('Location:Login.php');
    exit();
}
?>


<html>
    <meta charset="utf-8">
    <link href = "../CSS/Download Source/bootstrap/css/bootstrap.css" rel = "stylesheet" type = "text/css" />
	<link href = "../CSS/Download Source/bootstrap/css/bootstrap.min.css" rel = "stylesheet" type = "text/css" />
    <link href = "../CSS/Class/Main%20Page%20Style.css" rel = "stylesheet" type = "text/css" />
    <link href = "../CSS/Admin.css" rel = "stylesheet" type = "text/css" />
    <head>
		<meta charset= "utf-8" />
		<title> Purchased List</title>  
	</head>
    
    <body id = mainPage>
		<div id = wrapper  class="panel panel-default">           
            <div id = welcome>
                <h1> Purchased List</h1>
                <?php
                    echo '<h5> Welcome, '.$_SESSION['t4210']['email'].'</h5>';
                ?>
			</div>
            
            <div id = navGuide>
				<div id = navGuideLeft>
					<a href= "MainPage.php"> <button type "button" class = "btn btn-primary"> Home page </button> </a>
				</div>
			</div>
            
            <div id = navCategory>      
                <?php
                    include_once('db.php');
                    $db = ierg4210_DB();    
                    parse_str($_SERVER['QUERY_STRING']);
                    $q = 'SELECT ID, UserName, TransactionID FROM [Order] where UserName = (?) and TransactionID is not null order by ID desc';
                    $result = $db->prepare($q); 
                    $result->execute(array(loggedin()));            
                    $array = $result->fetchAll(PDO::FETCH_ASSOC);     
                    $num = 5;
                    if(count($array) < $num){
                        $num = count($array);
                    }
                    for ($i = 0; $i < $num; $i++){
                       echo '<button type "button" class = "btn btn-info"><a href="?tranid='.$array[$i]["TransactionID"].'"> Record- '  .($i + 1). '</a></button>';                                        
                    }           
                ?>
                
			</div>
                
            <div id = inputForm>
            <?php
                if($tranid != null){
                    $db = ierg4210_DB();    
                    parse_str($_SERVER['QUERY_STRING']);
                    $q = 'SELECT ID, ProductID, Quantity, Price FROM [PurchasedList] where TransactionID = (?)';
                    $result = $db->prepare($q); 
                    $result->execute(array($tranid));            
                    $array = $result->fetchAll(PDO::FETCH_ASSOC);  
                    echo 
                    '<h6> Transaction ID: '.$tranid.'</h6>
                    <table>
                      <tr>
                        <th>Product ID</th>
                        <th>Product Name</th>
                        <th>Total Price</th>
                        <th>Quantity</th>
                      </tr>';
                    for ($i = 0; $i < count($array); $i++){
                        $q0 = 'SELECT ID,Name FROM [Book] where ID = (?)';
                        $result0 = $db->prepare($q0); 
                        $result0->execute(array($array[$i]['ProductID']));            
                        $array0 = $result0->fetchAll(PDO::FETCH_ASSOC);  
                        
                       echo "<tr> <td>" .$array[$i]['ProductID']. "</td> <td>" .$array0[0]['Name']. "</td> <td> " .$array[$i]['Price']. " </td> <td> " .$array[$i]['Quantity']. "</td>  </tr>";                                        
                    }  
                    echo'</table>'; 
                }
            ?>
            </div>  
            
            <div id = footer>
                <hr>
                <h2> Write by Showing </h2>
                <h2> Mail: 419955347@qq.com </h2>
            </div>
        </div>
    </body>
</html>

























