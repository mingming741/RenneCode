<?php
header('Content-Type: application/json');

error_reporting(E_ALL & ~E_NOTICE);
include_once('db.php');
$db = ierg4210_DB();    

$q = 'SELECT did, Users.userName as userName, CategoryData.dataType as dataType, time, value 
    FROM [HealthData] 
    left join Users 
    on Users.uid = HealthData.userID
    left join CategoryData 
    on CategoryData.id = HealthData.dataTypeID
';
$result = $db->prepare($q); 
$result->execute();            
$array = $result->fetchAll(PDO::FETCH_ASSOC);

print json_encode($array);

?>