<?php
include_once('csrf.php');
define("LOG_FILE", "/var/www/ipn.log");
error_reporting(E_ALL & ~E_NOTICE & ~E_WARNING);
include_once('db.php');
global $db;
$db = ierg4210_DB();

function ierg4210_reset() {
    if ($_SERVER["REQUEST_METHOD"] != "POST") {
        header('Location:login.php', true, 302);
        exit;
    }
    $email = $_POST['email'];
    $token = $_POST['token'];
    $new_pw = $_POST['new_pw'];
    $r_new_pw = $_POST['r_new_pw'];

    if (empty($email) || empty($new_pw) || empty($r_new_pw) || !preg_match('/^[\w_]+@[\w]+(\.[\w]+){0,2}(\.[\w]{2,6})$/', $email) || !preg_match('/^[A-Za-z_\d]{2,19}$/', $new_pw) || !preg_match('/^[A-Za-z_\d]{2,19}$/', $r_new_pw)) {
        throw new Exception('Invalid Username or Password Format');
    }
    else if ($new_pw != $r_new_pw) {
        throw new Exception('Two new password is not match');
    }
    else {
        global $db;
        $db = ierg4210_DB();
        $result = $db->prepare("SELECT * FROM Token WHERE Email = ?");
        $result->execute(array($email));
        $array = $result->fetch();
        if (count($array) == 0) {
            throw new Exception('Username do not exist');
        }
        else {
            $saved_token = $array['Token'];
            if ($saved_token == $token) {
                $changeToken = mt_rand();
                $q = $db->prepare("UPDATE Token SET Token = (?) WHERE Email = ?");
                $q->execute(array($changeToken, $email));
                $new_salt = mt_rand();
                $sh_new_pwd = hash_hmac('sha1', $new_pw, $new_salt);
                $q = $db->prepare("UPDATE [User] SET Password = (?), Salt = (?) WHERE Email = (?)");
                $q->execute(array($sh_new_pwd, $new_salt, $email));
                echo "<script>alert(\"Reset password successfully!\")</script>";
                echo "<script>window.location.href = \"https://s42.ierg4210.ie.cuhk.edu.hk/\"</script>";
                exit;
            }
            else
            {
                echo "<script>alert(\"You can only reset password once via this link! We'll return home page!\")</script>";
                echo "<script>window.location.href = \"https://s42.ierg4210.ie.cuhk.edu.hk\"</script>";
            }
        }
    }
}
header("Content-type: text/html; charset=utf-8");
if (!empty($_REQUEST['action']) && !empty($_REQUEST['email']) && !empty($_REQUEST['token'])) {
    if (!preg_match('/^\w+$/', $_REQUEST['action']))
    include_once('csrf.php');
    csrf_verifyNonce($_REQUEST['action'], $_POST['nonce']);
}
if (($returnVal = call_user_func('ierg4210_' . $_REQUEST['action'])) === false) {
    if ($db && $db->errorCode()) {
        error_log(date("Y-m-d H:i:s"). "Failed" . PHP_EOL, 3, LOG_FILE);
    }
}
?>

<html>
    <link href = "../CSS/MainPage.css" rel = "stylesheet" type = "text/css" />
    <head>
        <meta charset="utf-8" />
        <title>Reset Password</title>
    </head>
    <body>
        <div id = welcome>
            <h1> Reset Password </h1>
        </div>
        <form method="POST" action="?action=<?php echo ($action = 'reset');?>">
            <label for="new_pw">New Password:</label>
            <input type="password" name="new_pw" required="true" pattern="^[A-Za-z_\d]\w{2,19}$" />
            <p></p>
            <label for="r_new_pw">Repeat New Password:</label>
            <input type="password" name="r_new_pw" required="true" pattern="^[A-Za-z_\d]\w{2,19}$" />

            <input type="hidden" name="email" value="<?php parse_str($_SERVER['QUERY_STRING']); echo $email?>" />
            <input type="hidden" name="token" value="<?php parse_str($_SERVER['QUERY_STRING']); echo $token?>" />
            <input type="hidden" name="nonce" value="<?php echo csrf_getNonce($action); ?>" />
            <input type="submit" value="confirm" />
        </form>

    </body>
</html>
