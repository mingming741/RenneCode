<?php
error_reporting(E_ALL & ~E_NOTICE);
include_once('db.php');
$db = ierg4210_DB();    

$operation = $_POST['operation'];
$userName = $_POST['userName'];
if($userName == ''){
    exit(0);
}
$q = 'Select * from Users where userName = ?';
$result = $db->prepare($q); 
$result->execute(array($userName));     
$array = $result->fetchAll(PDO::FETCH_ASSOC);
if(count($array) == 0){
    $password = '';
    $q = 'INSERT INTO Users (userName,passWord) VALUES (?,?)';
    $result = $db->prepare($q); 
    $result->execute(array($userName,$password)); 
}

// recieved from app
if($operation ==  'data'){
    $dataTypeID = $_POST['dataTypeID'];
    $time = $_POST['time'];
    $value = $_POST['value'];
    
    $q = 'Select * from HealthData where userID = (select uid from Users where userName = ?) and time = ? and dataTypeID = ?';
    $result = $db->prepare($q); 
    $result->execute(array($userName,$time,$dataTypeID));     
    $array = $result->fetchAll(PDO::FETCH_ASSOC);
    
    if(count($array) == 0){
        $q = 'INSERT INTO HealthData (userID,dataTypeID,time, value) VALUES ((select uid from Users where userName = ?),?,?,?)';
        $result = $db->prepare($q); 
        $result->execute(array($userName,$dataTypeID,$time,$value)); 
    }
    else{
        $q = "UPDATE [HealthData] SET value = (?) WHERE userID = (select uid from Users where userName = ?) and dataTypeID = ? and time = ?";
        $result = $db->prepare($q); 
        $result->execute(array($value,$userName,$dataTypeID,$time));
    }
}

if($operation == 'equipment'){
    $weapon = $_POST['weapon'];
    $cloth = $_POST['cloth'];
    $weaponList = $_POST['weaponList'];
    $clothList = $_POST['clothList'];
    
    $q = 'Select * from Equipment where userID = (select uid from Users where userName = ?)';
    $result = $db->prepare($q); 
    $result->execute(array($userName));
    $array = $result->fetchAll(PDO::FETCH_ASSOC);

    if(count($array) == 0){
        $q = 'INSERT INTO Equipment (userID,weapon,cloth,weaponList,clothList,reward,todayQuota) VALUES ((select uid from Users where userName = ?),?,?,?,?,0,1)';
        $result = $db->prepare($q); 
        $result->execute(array($userName,$weapon,$cloth,$weaponList,$clothList)); 
    }
    else{
        $q = "UPDATE [Equipment] SET weapon = (?),cloth = (?),weaponList = (?),clothList = (?) WHERE userID = (select uid from Users where userName = ?)";
        $result = $db->prepare($q); 
        $result->execute(array($weapon,$cloth,$weaponList,$clothList,$userName));
    }
}

if($operation == 'rewardAdd'){
    $reward = $_POST['reward'];
    
    $q = 'Select * from Equipment where userID = (select uid from Users where userName = ?)';
    $result = $db->prepare($q); 
    $result->execute(array($userName));
    $array = $result->fetchAll(PDO::FETCH_ASSOC);

    if(count($array) == 0){

    }
    else{
        $q = "UPDATE [Equipment] SET reward = (?), todayQuota = 0 WHERE userID = (select uid from Users where userName = ?)";
        $result = $db->prepare($q); 
        $result->execute(array($reward,$userName));
    }
}

if($operation == 'rewardSub'){
    $reward = $_POST['reward'];
    
    $q = 'Select * from Equipment where userID = (select uid from Users where userName = ?)';
    $result = $db->prepare($q); 
    $result->execute(array($userName));
    $array = $result->fetchAll(PDO::FETCH_ASSOC);

    if(count($array) == 0){

    }
    else{
        $q = "UPDATE [Equipment] SET reward = (?) WHERE userID = (select uid from Users where userName = ?)";
        $result = $db->prepare($q); 
        $result->execute(array($reward,$userName));
    }
}
?> 
