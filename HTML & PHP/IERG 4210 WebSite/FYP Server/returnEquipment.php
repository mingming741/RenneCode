<?php
header('Content-Type: application/json');

parse_str($_SERVER['QUERY_STRING']);  
error_reporting(E_ALL & ~E_NOTICE);
include_once('db.php');
$db = ierg4210_DB();

if($operation == "userData"){
    $q = 'SELECT did, Users.userName as userName, CategoryData.dataType as dataType, time, value 
    FROM [HealthData] 
    left join Users 
    on Users.uid = HealthData.userID
    left join CategoryData 
    on CategoryData.id = HealthData.dataTypeID
';
}
else if($operation == "equipment"){
    $q = 'SELECT eid, Users.userName as userName, weapon, cloth, weaponList, clothList, reward, todayQuota
        FROM [Equipment] 
        left join Users 
        on Users.uid = Equipment.userID
    ';
}
else if($operation == "quota"){
    $q = 'SELECT eid, Users.userName as userName, reward, todayQuota
        FROM [Equipment] 
        left join Users 
        on Users.uid = Equipment.userID
    ';
}

$result = $db->prepare($q); 
$result->execute();
$array = $result->fetchAll(PDO::FETCH_ASSOC);

print json_encode($array);

?>