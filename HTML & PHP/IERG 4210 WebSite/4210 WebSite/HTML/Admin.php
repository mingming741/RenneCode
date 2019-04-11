<?php
include_once('db.php');
session_start();
error_reporting(E_ALL & ~E_NOTICE);
session_regenerate_id();

function loggedin()
{
    //Session run
	if (!empty($_SESSION['t4210'])){
        $db = ierg4210_DB();
        $result = $db->prepare("SELECT * FROM User WHERE Email = (?)");
        $result->execute(array($_SESSION['t4210']['email']));
        $array = $result->fetch();
        if($array['Type'] == 0){
            return $_SESSION['t4210']['email'];
        }
        else{
            return false;
        }
    }
		
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
				if ($key == $token['key'] && $array['Type'] == 0) {
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
		<title> Book Store Admin Panel</title>  
	</head>
    
    <body id = mainPage>
		<div id = wrapper  class="panel panel-default">           
            <div id = welcome>
                <h1> Admin Panel </h1>
			</div>
            
            <div id = navGuide>
				<div id = navGuideLeft>
					<a href= "MainPage.php"> <button type "button" class = "btn btn-primary"> Home page </button> </a>
				</div>
			</div>
            
            <div id = navCategory>                         
                <button type "button" class = "btn btn-info"><a href="?opid=1"> New Category</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=2"> Edit Category</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=3"> Delete Category</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=4"> New Book</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=5"> Edit Book</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=6"> Delete Book</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=7"> View Order</a></button>
			</div>
                
            <div id = inputForm>
            <?php
                error_reporting(E_ALL & ~E_NOTICE);
                include_once('db.php');
                $db = ierg4210_DB();    
                parse_str($_SERVER['QUERY_STRING']);  
                if($opid == 1){
                    echo 
                    '<label> Category Insert </label>
                        <form id = "catInsert" method= "POST" action="admin-process.php?action=cat_insert">
                        <label> New Category: </label>
                        <input id= "Category" type="text" name= "Category" required="true" pattern="^[\w\- ]+$" />  
                        <input type= "submit" value="Submit" />
                    </form>';              
                }
                else if($opid == 2){
                    echo 
                    '<label> Category Update </label>
                        <form id = "catEdit" method= "POST" action="admin-process.php?action=cat_edit">
                        <label> Old Category: </label>
                        <select name = "cID" id = "OldCategory">';
                        $q = 'SELECT ID, Category FROM [Book Category]';
                        $result = $db->prepare($q); 
                        $result->execute();            
                        $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                        for ($i = 0; $i < count($array); $i++){
                           echo "<option value =" .$array[$i]['ID']. ">" .$array[$i]['Category']. "</option>";                                        
                        }              
                    echo'</select>
                        <label> New Category: </label>
                        <input id= "Category" type="text" name= "Category" required="true" pattern="^[\w\- ]+$" />  
                        <input type= "submit" value="Submit" />
                    </form>';  
                }
                else if($opid == 3){
                    echo 
                    '<label> Category Delete </label>
                        <form id = "catDelete" method= "POST" action="admin-process.php?action=cat_delete">
                        <label> Old Category: </label>
                        <select name = "cID" id = "OldCategory">';
                        $q = 'SELECT ID, Category FROM [Book Category]';
                        $result = $db->prepare($q); 
                        $result->execute();            
                        $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                        for ($i = 0; $i < count($array); $i++){
                           echo "<option value =" .$array[$i]['ID']. ">" .$array[$i]['Category']. "</option>";                                        
                        }              
                    echo'</select>
                        <input type= "submit" value="Submit" />
                    </form>';  
                }
                else if($opid == 4){
                    echo 
                    '<label> Book Insert </label>
                        <form id = "bookInsert" method= "POST" action="admin-process.php?action=prod_insert" enctype="multipart/form-data">
                        <label> Category: </label>
                        <select name = "cID" id = "Category">';
                        $q = 'SELECT ID, Category FROM [Book Category]';
                        $result = $db->prepare($q); 
                        $result->execute();            
                        $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                        for ($i = 0; $i < count($array); $i++){
                           echo "<option value =" .$array[$i]['ID']. ">" .$array[$i]['Category']. "</option>";                                        
                        }              
                    echo'</select>
                        <label> Book Name: </label>
                        <input id = "Name" type="text" name= "Name" required = "true" pattern="^[\w\- ]+$" />                   
                        <label> Price </label>
			            <input id= "Price" type="number" name="Price" required="true" pattern="^[\d\.]+$" /> <br/>
                        <label> Description </label>
			            <textarea id = "Description" name= "Description" pattern="^[\w\-,\. ]$"></textarea> <br/>
                        <label> Image </label>
			            <input type = "file" name= "file" required= "true" accept="image/jpeg image/png image/gif" />
                        <input type= "submit" value="Submit" />
                    </form>'; 
                }
                else if($opid == 5){
                    echo 
                    '<label> Book Update </label>
                        <form id = "bookUpdate" method= "POST" action="admin-process.php?action=prod_edit" enctype="multipart/form-data">
                        <label> Book Name: </label>
                        <select name = "pID" id = "BookID">';
                        $q = 'SELECT ID, Name FROM [Book]';
                        $result = $db->prepare($q); 
                        $result->execute();            
                        $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                        for ($i = 0; $i < count($array); $i++){
                           echo "<option value =" .$array[$i]['ID']. ">" .$array[$i]['Name']. "</option>";                                        
                        }              
                    echo'</select> <br/>
                        <label> New Book Name: </label>
                        <input id = "Name" type="text" name= "Name" required = "true" pattern="^[\w\- ]+$" />     
                        <label> New Category: </label>
                        <select name = "cID" id = "Category">';
                        $q = 'SELECT ID, Category FROM [Book Category]';
                        $result = $db->prepare($q); 
                        $result->execute();            
                        $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                        for ($i = 0; $i < count($array); $i++){
                           echo "<option value =" .$array[$i]['ID']. ">" .$array[$i]['Category']. "</option>";                                        
                        }              
                    echo'</select>
                        <label> Price </label>
			            <input id= "Price" type="number" name="Price" required="true" pattern="^[\d\.]+$" /> <br/>
                        <label> Description </label>
			            <textarea id = "Description" name= "Description" pattern="^[\w\-,\. ]$"></textarea> <br/>
                        <label> Image </label>
			            <input type = "file" name= "file" required= "true" accept="image/jpeg image/png image/gif" />
                        <input type= "submit" value="Submit" />
                    </form>'; 
                }
                else if($opid == 6){
                    echo 
                    '<label> Book Delete </label>
                        <form id = "bookDelete" method= "POST" action="admin-process.php?action=prod_delete">
                        <label> Book Name: </label>
                        <select name = "pID" id = "BookID">';
                        $q = 'SELECT ID, Name FROM [Book]';
                        $result = $db->prepare($q); 
                        $result->execute();            
                        $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                        for ($i = 0; $i < count($array); $i++){
                           echo "<option value =" .$array[$i]['ID']. ">" .$array[$i]['Name']. "</option>";                                        
                        }              
                    echo
                        '<input type= "submit" value="Submit" />
                    </form>'; 
                }  
                else if($opid == 7){
                    echo 
                    '<table>
                      <tr>
                        <th>Order ID</th>
                        <th>User Account </th>
                        <th>Digest</th>
                        <th>Salt</th>
                        <th>Transaction ID</th>
                      </tr>';
                    $q = 'SELECT ID, CreateTime, UserName, TransactionID, Status FROM [Order]';
                    $result = $db->prepare($q); 
                    $result->execute();            
                    $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                    for ($i = count($array) - 1; $i >= 0 ; $i--){
                       echo "<tr> <td>" .$array[$i]['ID']. "</td> <td>" .$array[$i]['CreateTime']. "</td> <td> " .$array[$i]['UserName']. " </td> <td> " .$array[$i]['Status']. " </td> <td> " .$array[$i]['TransactionID']. " </td>  </tr>";                                        
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

























