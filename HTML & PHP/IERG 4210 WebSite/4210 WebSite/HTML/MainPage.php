<?php
error_reporting(E_ALL & ~E_NOTICE);
include_once('db.php');
include_once('csrf.php');
session_start();
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
    <script type="text/javascript" src="../JS/myLib.js"></script>
    <script type="text/javascript" src="../JS/MainPage.js"></script>
	<link href = "../CSS/Download Source/bootstrap/css/bootstrap.css" rel = "stylesheet" type = "text/css" />
	<link href = "../CSS/Download Source/bootstrap/css/bootstrap.min.css" rel = "stylesheet" type = "text/css" />
    <link href = "../CSS/Class/Main%20Page%20Style.css" rel = "stylesheet" type = "text/css" />
	<link href = "../CSS/MainPage.css" rel = "stylesheet" type = "text/css" />
	<head>
		<meta charset= "utf-8" />
		<title> Book Store of Showing </title>  
	</head>
    
    <?php
        $db = ierg4210_DB();    
        parse_str($_SERVER['QUERY_STRING']);  
    ?>

	<body id = mainPage>
		<div id = wrapper  class="panel panel-default">
			<div id = welcome>
                <h1> Welcome to book store! </h1>
                <?php
                    echo '<h5> Welcome, '.$_SESSION['t4210']['email'].'</h5>';
                ?>
			</div>

			<div id = navGuide>
				<div id = navGuideLeft>
                    <button type "button" class = "btn btn-warning"> <a href="MainPage.php"> Home page </a> </button>
                    <button type "button" class = "btn btn-warning"> <a href="Admin.php"> Admin </a> </button>
                    <button type "button" class = "btn btn-warning"> <a href="PurchasedRecord.php"> Purchased Record </a> </button>
				</div>
				<div id = navGuideRight>
					<form method= "POST" action="auth-process.php?action=logout">
                        <button type "button" class = "btn btn-warning" onclick = this.form.submit()> Logout </button>
                        <input type= "hidden" name = "nonce" value= " <?php echo csrf_getNonce('logout'); ?>" />
                    </form>
					<button type "button" class = "btn btn-warning"> <a href="ChangePassword.php"> Change Password </a> </button>
					<button type "button" class = "btn btn-warning"> <a href="Register.php">  Register </a> </button>
				</div>
			</div>

			<div id = navCategory>
                <?php
                    $q = 'SELECT ID, Category FROM [Book Category]';
                    $result = $db->prepare($q); 
                    $result->execute();
                    $Category = $result->fetchAll(PDO::FETCH_ASSOC);                                
                    for ($i = 0; $i < count($Category); $i++){   
                        echo '<button type "button" class = "btn btn-info"><a href="?catid=' .$Category[$i]['ID']. '">'. $Category[$i]['Category']. '</a></button>';
                    }
                ?>
			</div>
			
			<div id = navIndex>
				<ul>
					<li> <a href="MainPage.php"> Home Page </a> </li>
                    <?php
                    if($catid != null && $pid == null){
                        echo '<li> > </li>';
                        for ($i = 0; $i < count($Category); $i++){  
                            if($Category[$i]['ID'] == $catid){
                                echo '<li> <a href="?catid=' .$catid. '">' .$Category[$i]["Category"]. '</a></li>'; 
                            }                         
                        }
                    }
                    else if($catid != null && $pid != null){ 
                        $q = 'SELECT ID, Category, Name FROM [Book]';
                        $result = $db->prepare($q); 
                        $result->execute();            
                        $Book = $result->fetchAll(PDO::FETCH_ASSOC); 
                        
                        echo '<li> > </li>';
                        for ($i = 0; $i < count($Category); $i++){  
                            if($Category[$i]['ID'] == $catid){
                                echo '<li> <a href="?catid=' .$catid. '">' .$Category[$i]["Category"]. '</a></li>'; 
                            }                         
                        }
                        echo '<li> > </li>';
                        for ($i = 0; $i < count($Book); $i++){  
                            if($Book[$i]['ID'] == $pid){
                                echo '<li>' .$Book[$i]["Name"]. '</li>';  
                            }                         
                        } 
                    }
                    ?>
				</ul>
			</div>

			<nav id = shoppingList>
				<span> Shopping List </span>
				<div id = "shoppingCart">	

				</div>
			</nav>
            
            <?php         
            if ($catid == null){// && $pid == null){
                $q = 'SELECT ID, Category, Name, Price, Picture FROM [Book]';
                $result = $db->prepare($q); 
                $result->execute();            
                $Book = $result->fetchAll(PDO::FETCH_ASSOC); 
                
				echo '<div id = displayWrapper>
						<div id = displayWrapper_ItemsList>
                            <ul>';            
                for ($i = 0; $i < count($Book); $i++){   
                    echo '<li> <a href="?catid=' .$Book[$i]['Category']. '&pid=' .$Book[$i]['ID']. '">';
                    echo '<img class = productImag src = "' .$Book[$i]['Picture']. '"/>';
                    echo '<h2 class = productDisc >' .$Book[$i]['Name'].  '</h2>';
                    echo '<h2 class = productPrice> $' .$Book[$i]['Price']. '</h2>';
                    echo '<button type "button" onclick="addToCart(\''.$Book[$i]['ID'].'\')" class= "btn btn-danger btn-sm"> Add to Chart </button>';       
                    echo "</a></li>";
                }                          
                echo'       </ul>
                         </div>
                     </div>';
			}
            else if($catid != null && $pid == null){
                $q = 'SELECT ID, Category, Name, Price, Picture FROM [Book] Where Category = ?';
                $result = $db->prepare($q); 
                $result->execute(array($catid));            
                $Book = $result->fetchAll(PDO::FETCH_ASSOC); 
                
                echo '<div id = displayWrapper>
						<div id = displayWrapper_ItemsList>
                            <ul>';            
                for ($i = 0; $i < count($Book); $i++){   
                    echo '<li> <a href="?catid=' .$catid. '&pid=' .$Book[$i]['ID']. '">';
                    echo '<img class = productImag src = "' .$Book[$i]['Picture']. '"/>';
                    echo '<h2 class = productDisc >' .$Book[$i]['Name'].  '</h2>';
                    echo '<h2 class = productPrice> $' .$Book[$i]['Price']. '</h2>';
                    echo '<button type "button" onclick="addToCart(\''.$Book[$i]['ID'].'\')" class= "btn btn-danger btn-sm"> Add to Chart </button>';               
                    echo "</a></li>";
                }                          
                echo'       </ul>
                         </div>
                     </div>';
            }
            else if($catid != null && $pid != null){
                $q = 'SELECT ID, Category, Name, Price, Picture, Description FROM [Book] Where ID = ?';
                $result = $db->prepare($q); 
                $result->execute(array($pid));            
                $BookItem = $result->fetchAll(PDO::FETCH_ASSOC);    

                echo '<div id = displayWrapper>
						<div id = displayWrapper_Item>';          
                    echo '<div>';             
                        echo '<img id = displayWrapper_ItemPic_Img src = "' .$BookItem[0]['Picture']. '"/>'; 
                    echo "</div>";
                
                    echo '<div>';
                        echo '<h2 class = productDisc>' .$BookItem[0]['Name']. '</h2>'; 
                        echo '<h2 class = productPrice> $' .$BookItem[0]['Price']. '</h2>';
                        echo '<button type "button" onclick="addToCart(\''.$BookItem[0]['ID'].'\')" class= "btn btn-danger btn-sm"> Add to Chart </button>'; 
                        echo '<h2 class = productDisc> Description: </h2>';
                        echo '<h2 class = productDisc>' .$BookItem[0]['Description']. '</h2>';
                    echo '</div>';  
                
                echo'    </div>
                     </div>';           
            }
            ?>    

			<div id = footer>
				<hr>
				<h2> Write by Showing </h2>
				<h2> Mail: 419955347@qq.com </h2>
			</div>
            
            <!-- Load Facebook SDK for JavaScript -->
            <div id="fb-root"></div>
            <script>(function(d, s, id) {
                var js, fjs = d.getElementsByTagName(s)[0];
                if (d.getElementById(id)) return;
                js = d.createElement(s); js.id = id;
                js.src = "//connect.facebook.net/zh_CN/sdk.js#xfbml=1&version=v2.8";
                fjs.parentNode.insertBefore(js, fjs);
            }(document, 'script', 'facebook-jssdk'));</script>

            <div id="share" class="fb-share-button" data-href="https://s42.ierg4210.ie.cuhk.edu.hk/" data-layout="button_count" data-size="small" data-mobile-iframe="false"><a class="fb-xfbml-parse-ignore" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fs42.ierg4210.ie.cuhk.edu.hk%2F&amp;src=sdkpreparse">分享</a></div>
            <br/>
            <div id="like" class="fb-like" data-href="https://s42.ierg4210.ie.cuhk.edu.hk/" data-layout="standard" data-action="like" data-size="small" data-show-faces="true" data-share="false"></div>
		</div>  
	</body>
</html>