<?php
define("LOG_FILE", "/var/www/ipn.log");
include_once('csrf.php');
include_once('db.php');
date_default_timezone_set("Asia/Hong_Kong");
error_reporting(E_ALL & ~E_NOTICE);
session_start();

if ($_SERVER['HTTP_REFERER'] == "")
{
    header('Location://s42.ierg4210.ie.cuhk.edu.hk/HTML/MainPage.php', true, 302);
    exit();
}

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

if (!loggedin())
{
    $data = array('ifLogin' => 0,);
    echo json_encode($data);
    exit();
}

$msg = json_decode($_POST["message"]);
$db = ierg4210_DB();
if ($msg != null) {
    $sumPrice = 0.0;
    $order = "{";
    foreach ($msg as $pid => $number) {
        $q = $db->prepare("SELECT Price FROM Book WHERE ID = $pid");
        $q->execute();
        $pro_price = $q->fetchAll(PDO::FETCH_COLUMN, 0);
        $pro_price = $pro_price[0];
        settype($pro_price, "float");
        $mc_gross = $pro_price * $number;
        round(floatval($mc_gross), 2);
        $order .= $pid . ":{" . $number . "," . $mc_gross . "},";
        $sumPrice += $mc_gross;
    }
    $order .= "}";
    $salt = mt_rand();
    round(floatval($sumPrice), 2);
    $createdtime = date("Y-m-d H:i:s");
    $message = "HKD;".$salt.";".$order.";".$sumPrice;
    error_log($createdtime. " order-message " . $message. PHP_EOL . "\r\n", 3, LOG_FILE);
    $digest = hash('md5', $message);    
    $db = ierg4210_DB();
    $q = "Insert Into [Order] (UserName, Digest, Salt, CreateTime, Status) VALUES (?,?,?,?,?)";
    $result = $db->prepare($q); 
    $result->execute(array(loggedin(), $digest, $salt,$createdtime,'Un-paid'));
    
    $lastInsertId = $db->lastInsertId();
    $data = array(
        'id' => $lastInsertId,
        'digest' => $digest,
    );
    echo json_encode($data);
    exit;
}
?>
