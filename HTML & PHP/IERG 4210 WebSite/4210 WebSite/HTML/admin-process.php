<?php
include_once('db.php');

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
        else if($array['Type'] == 1 && $_REQUEST['action'] == 'prod_fetchByPid'){
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
                if ($key == $token['key'] && $array['Type'] == 1 && $_REQUEST['action'] == 'prod_fetchByPid') {
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

// For MainPage.php
function ierg4210_cat_fetchall() {
	global $db;
	$db = ierg4210_DB();
	$q = $db->prepare("SELECT * FROM Book Category;");
	if ($q->execute())
		return $q->fetchAll();
}

function ierg4210_cat_insert() {
	if (!preg_match('/^[\w\-, ]+$/', $_POST['Category']))
		throw new Exception("invalid-name");
	global $db;
	$db = ierg4210_DB();
	$q = $db->prepare("INSERT INTO [Book Category] (Category) VALUES (?)");
	return $q->execute(array($_POST['Category']));
}

function ierg4210_cat_edit() {
    if (!preg_match('/^[\w\-, ]+$/', $_POST['Category']))
        throw new Exception("invalid-name");
    $catID = (int) $_POST['cID'];

    global $db;
    $db = ierg4210_DB();
    $q = $db->prepare("UPDATE [Book Category] SET Category = (?) WHERE ID = $catID");
    return $q->execute(array($_POST['Category']));
}

function ierg4210_cat_delete() {
	$cid = (int) $_POST['cID'];
	global $db;
	$db = ierg4210_DB();
	$q = $db->prepare("DELETE FROM [Book Category] WHERE ID = ?");
	return $q->execute(array($cid));
}

function ierg4210_prod_fetchByCat() {
    global $db;
    $db = ierg4210_DB();
    $catID = $_POST['cID'];
    $q = $db->prepare("SELECT * FROM Book WHERE ID = $catID");
    if ($q->execute())
       return $q->fetchAll();
}

function ierg4210_prod_fetchByPid(){
    global $db;
    $db = ierg4210_DB();
    $PID = $_GET['pID'];
    $q = $db->prepare("SELECT Name, Price FROM Book WHERE ID = $PID");
    if ($q->execute())
        return $q->fetchAll();
}

function ierg4210_prod_insert() {
    if (!preg_match('/^[\w\-, ]+$/', $_POST['Name']))
        throw new Exception("invalid-name");
    if (!preg_match('/^[0-9]*$/', $_POST['Price']))
        throw new Exception("invalid-price");
    if (!preg_match('/^[\w\-,\. ]+$/', $_POST['Description']))
        throw new Exception("invalid-description");
    global $db;
    $db = ierg4210_DB();

    $q = $db->prepare("INSERT INTO Book (Category, Name, Price, Description, Picture) VALUES (?,?,?,?,?)");
    $imageName = "../Source/Shop Item/IMG_" . $_POST['Name']. "_" . $db->lastInsertId(). ".jpg";
    $q->execute(array($_POST['cID'], $_POST['Name'],$_POST['Price'],$_POST['Description'], $imageName));
    //$lastId = $db->lastInsertId();

    if ($_FILES["file"]["error"] == 0 && ($_FILES["file"]["type"] == "image/jpeg" || $_FILES["file"]["type"] == "image/png" || $_FILES["file"]["type"] == "image/gif")
        && $_FILES["file"]["size"] < 5000000) {
        if(move_uploaded_file($_FILES["file"]["tmp_name"], $imageName)){
            echo "Upload Successful";
        }
    }
}

function ierg4210_prod_edit() {
    if (!preg_match('/^[\w\-, ]+$/', $_POST['Name']))
        throw new Exception("invalid-name");
    if (!preg_match('/^[0-9]*$/', $_POST['Price']))
        throw new Exception("invalid-price");
    if (!preg_match('/^[\w\-,\. ]+$/', $_POST['Description']))
        throw new Exception("invalid-description");
    global $db;
    $db = ierg4210_DB();
    $q = $db->prepare("UPDATE Book SET Category = (?), Name = (?), Price= (?), Description = (?), Picture = (?) WHERE ID = (?)");
    $imageName = "../Source/Shop Item/IMG_" . $_POST['Name']. "_" . $db->lastInsertId(). ".jpg";   
    $q->execute(array((int)$_POST['cID'],$_POST['Name'],$_POST['Price'],$_POST['Description'], $imageName, (int)$_POST["pID"]));

    if ($_FILES["file"]["error"] == 0 && ($_FILES["file"]["type"] == "image/jpeg" || $_FILES["file"]["type"] == "image/png" || $_FILES["file"]["type"] == "image/gif")
        && $_FILES["file"]["size"] < 5000000) {
        if(move_uploaded_file($_FILES["file"]["tmp_name"], $imageName)){
            echo "Upload Successful";
        }
    }
}

function ierg4210_prod_delete() {
    $_POST['pID'] = (int) $_POST['pID'];
    global $db;
    $db = ierg4210_DB();
    $q = $db->prepare("DELETE FROM Book WHERE ID = ?");
    return $q->execute(array($_POST['pID']));
}


header('Content-Type: application/json');
// input validation
if (empty($_REQUEST['action']) || !preg_match('/^\w+$/', $_REQUEST['action'])) {
	echo json_encode(array('failed'=>'undefined'));
	exit();
}

// The following calls the appropriate function based to the request parameter $_REQUEST['action'],
//   (e.g. When $_REQUEST['action'] is 'cat_insert', the function ierg4210_cat_insert() is called)
// the return values of the functions are then encoded in JSON format and used as output
try {
	if (($returnVal = call_user_func('ierg4210_' . $_REQUEST['action'])) === false) {
		if ($db && $db->errorCode()) 
			error_log(print_r($db->errorInfo(), true));
		echo json_encode(array('failed'=>'1'));
	}
	echo 'while(1);' . json_encode(array('success' => $returnVal));
} catch(PDOException $e) {
	error_log($e->getMessage());
	echo json_encode(array('failed'=>'error-db'));
} catch(Exception $e) {
	echo 'while(1);' . json_encode(array('failed' => $e->getMessage()));
}
?>