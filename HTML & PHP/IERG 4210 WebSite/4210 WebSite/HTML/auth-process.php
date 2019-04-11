<?php
session_start();
error_reporting(E_ALL & ~E_NOTICE & ~E_WARNING);
include_once('db.php'); 
define("LOG_FILE", "/var/www/ipn.log");
parse_str($_SERVER['QUERY_STRING']);  

function ierg4210_login(){
    if (empty($_POST['Email']) || empty($_POST['Password']) || !preg_match('/^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$/', $_POST['Email']) || !preg_match('/^[A-Za-z_\d]{2,19}$/', $_POST['Password'])) {
        throw new Exception('Invalid Username or Password Format');
    }
    else {
        global $db;
        $db = ierg4210_DB();
        $result = $db->prepare("SELECT * FROM User WHERE Email = (?)");
        $result->execute(array($_POST['Email']));
        $array = $result->fetchAll(PDO::FETCH_ASSOC);    
        if (count($array) == 0) {
            throw new Exception('Username do not exist');
        }
        else if (count($array) == 1){
            $password = hash_hmac('sha1', $_POST['Password'], $array[0]['Salt']);           
            if($array[0]['Password'] == $password){
                session_regenerate_id();
                $exp = time() + 3600 * 24 * 1;
                $token = array('email'=>$_POST['Email'], 'expire'=>$exp, 'key'=>hash_hmac('sha1', $exp.$array[0]['Password'], $array[0]['Salt']));
                setcookie('t4210', json_encode($token), $exp, '','', false, true);
                $_SESSION['t4210'] = $token;

                if ($array[0]['Type'] == 0) {
                    header('Location: Admin.php', true, 302);
                    exit();
                }
                else if ($array[0]['Type'] == 1){
                    header('Location: MainPage.php', true, 302);
                    exit();
                }
            }
            else {
                throw new Exception('Wrong password');
            }      
        }
    }
}

function ierg4210_register(){
    if (empty($_POST['Email']) || empty($_POST['Password']) || !preg_match('/^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$/', $_POST['Email']) || !preg_match('/^[A-Za-z_\d]{2,19}$/', $_POST['Password'])) {
        throw new Exception('Invalid Username or Password Format');
    }
    if($_POST['Password'] != $_POST['Password_RE']){
        throw new Exception('Two password is not match');
    }
    else {
        global $db;
        $db = ierg4210_DB();
        $result = $db->prepare("SELECT * FROM User WHERE Email = (?)");
        $result->execute(array($_POST['Email']));
        $array = $result->fetchAll(PDO::FETCH_ASSOC);    
        if (count($array) == 1) {
            throw new Exception('Username already exist');
        }
        else if (count($array) == 0){
            $salt = rand(0, 1000);
            $password = hash_hmac('sha1', $_POST['Password'], $salt);           
            $q = $db->prepare("INSERT INTO User (Email, Password, Type, Salt, Password_Original) values(?,?,?,?,?)");
            $q->execute(array($_POST['Email'], $password, 1, $salt, $_POST['Password']));
            header('Location: Login.php', true, 302);
            exit();
        }
    }
}

function ierg4210_changepsw(){
    if (empty($_POST['Email']) || empty($_POST['Password']) || empty($_POST['Password_New']) || !preg_match('/^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$/', $_POST['Email']) || !preg_match('/^[A-Za-z_\d]{2,19}$/', $_POST['Password'])  || !preg_match('/^[A-Za-z_\d]{2,19}$/', $_POST['Password_New'])) {
        throw new Exception('Invalid Username or Password Format');
    }
    if($_POST['Password_New'] != $_POST['Password_RE']){
        throw new Exception('Two new password is not match');
    }
    else {
        global $db;
        $db = ierg4210_DB();
        $result = $db->prepare("SELECT * FROM User WHERE Email = (?)");
        $result->execute(array($_POST['Email']));
        $array = $result->fetchAll(PDO::FETCH_ASSOC);    
        if (count($array) == 0) {
            throw new Exception('Username do not exist');
        }
        else if (count($array) == 1){
            $password = hash_hmac('sha1', $_POST['Password'], $array[0]['Salt']);           
            if($array[0]['Password'] == $password){
                $salt = rand(0, 1000);
                $password = hash_hmac('sha1', $_POST['Password_New'], $salt);           
                $q = $db->prepare("Update User Set Password = (?), Salt = (?), Password_Original = (?) where Email = (?)");
                $q->execute(array($password, $salt, $_POST['Password_New'], $_POST['Email']));
                header('Location: Login.php', true, 302);
                exit();
            }
            else {
                throw new Exception('Wrong original password');
            }      
        }
    }
}

function ierg4210_sendEmail() {
    $email = $_POST['Email'];
    error_log(date("Y-m-d H:i:s"). "email: " .$email.PHP_EOL."\r\n", 3, LOG_FILE);
    if (empty($email) || !preg_match('/^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$/', $email))
    {
        throw new Exception('Wrong Email Format');
    }
    else {
        global $db;
        $db = ierg4210_DB();
        $result = $db->prepare("SELECT * FROM User WHERE Email = (?)");
        $result->execute(array($_POST['Email']));
        $array = $result->fetchAll(PDO::FETCH_ASSOC);    
        if (count($array) == 0) {
            throw new Exception('Username do not exist');
        }
        else if (count($array) == 1){ // email exists, then send an email to it
            $to = $email;
            $subject = "Reset Password";
            $message = "Hello! There is a link for you to reset your password for Book Store of Showing ";
            $token = mt_rand();
            $result = $db->prepare("SELECT * FROM Token WHERE Email = (?)");
            $result->execute(array($email));
            $array = $result->fetch();
            if (empty($array)) {
                $result = $db->prepare("INSERT INTO Token (Email,Token) VALUES (?,?)");
                $result->execute(array($email, $token));
            }
            else {
                $q = $db->prepare("UPDATE Token SET Token = (?) WHERE Email = ?");
                $q->execute(array($token,$email));
            }
            $link = "https://s42.ierg4210.ie.cuhk.edu.hk/HTML/ResetPsd.php?email=$email&token=$token";
            $message .= $link;
            $from = "zhangyuming741@gmail.com";
            $headers = "From: $from";
            mail($to,$subject,$message,$headers);
            header('Location: //s42.ierg4210.ie.cuhk.edu.hk', true, 302);
            exit();
        }
    }
}

function ierg4210_logout(){
    if (isset($_COOKIE['t4210'])) {
        unset($_COOKIE['t4210']);
        setcookie('t4210',null,-1);
        session_start();
        session_unset();
        session_destroy();
        header('Location: Login.php', true, 302);
        exit();
    }
}

header('Content-Type: application/json');
if (empty($_REQUEST['action']) || !preg_match('/^\w+$/', $_REQUEST['action'])) {
	echo json_encode(array('failed'=>'undefined'));
	exit();
}
try {
    include_once('csrf.php');
    csrf_verifyNonce($_REQUEST['action'], $_POST['nonce']);
    if (($returnVal = call_user_func('ierg4210_' . $_REQUEST['action'])) === false) {
        if ($db && $db->errorCode())
            error_log(print_r($db->errorInfo(), true));
        throw new Exception('Failed');
    }
}
catch(PDOException $e) {
    error_log($e->getMessage());
    echo 'PDO Exception Occurred:' .$e->getMessage();
}
catch(Exception $e) {
    echo 'Error Occurred:' .$e->getMessage();
}