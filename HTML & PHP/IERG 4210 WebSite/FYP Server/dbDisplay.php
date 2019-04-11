<html>
    <link href = "Download Source/bootstrap/css/bootstrap.css" rel = "stylesheet" type = "text/css" />
	<link href = "Download Source/bootstrap/css/bootstrap.min.css" rel = "stylesheet" type = "text/css" />
    <link href = "MainPageStyle.css" rel = "stylesheet" type = "text/css" />
    <link href = "DataDisplay.css" rel = "stylesheet" type = "text/css" />
	<head>
		<meta charset= "utf-8" />
		<title> Fitness Game - Background data</title>  
	</head>
    
    <body id = mainPage>
		<div id = wrapper  class="panel panel-default">   
            <div id = welcome>
                <h1> User Data </h1>
            </div>
            
            <div id = navGuide>
				<div id = navGuideLeft>
					<a href= "../index.html"> <button type "button" class = "btn btn-primary"> Home page </button> </a>
				</div>
			</div>
            
            <div id = navCategory>                         
                <button type "button" class = "btn btn-info"><a href="?opid=1"> Users</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=2"> Data Type</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=3"> Health Data</a></button>
                <button type "button" class = "btn btn-info"><a href="?opid=4"> Equipment Data</a></button>
			</div>
                
            <div id = inputForm>
            <?php
                error_reporting(E_ALL & ~E_NOTICE);
                include_once('db.php');
                $db = ierg4210_DB();    
                parse_str($_SERVER['QUERY_STRING']);  
                if($opid == 1){
                    echo '<table class="table table-striped">
                      <tr>
                        <th>User ID</th>
                        <th>User Name</th>
                      </tr>';
                    $q = 'SELECT uid, userName FROM [Users]';
                    $result = $db->prepare($q); 
                    $result->execute();            
                    $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                    for ($i = 0; $i < count($array) ; $i++){
                       echo "<tr> <td>" .$array[$i]['uid'].  " </td> <td> " .$array[$i]['userName']. " </td> </tr>";
                    }
                    echo'</table>';             
                }
                else if($opid == 2){
                    echo '<table class="table table-striped">
                      <tr>
                        <th>ID</th>
                        <th>Data Type</th>
                      </tr>';
                    $q = 'SELECT id, dataType FROM [CategoryData]';
                    $result = $db->prepare($q); 
                    $result->execute();            
                    $array = $result->fetchAll(PDO::FETCH_ASSOC);                                
                    for ($i = 0; $i < count($array) ; $i++){
                       echo "<tr> <td>" .$array[$i]['id'].  " </td> <td> " .$array[$i]['dataType']. " </td> </tr>";
                    }
                    echo'</table>';     
                }
                else if($opid == 3){
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
                    echo '<table class="table table-striped">
                      <tr>
                        <th>ID</th>
                        <th>User Name</th>
                        <th>Data Type</th>
                        <th>Time</th>
                        <th>Value</th>
                      </tr>';
                            
                    for ($i = 0; $i < count($array) ; $i++){
                       echo "<tr> <td>" .$array[$i]['did'].  " </td> <td> " .$array[$i]['userName']. " </td> <td> " .$array[$i]['dataType']. " </td> <td> " .$array[$i]['time']. " </td> <td> " .$array[$i]['value']. " </td> </tr>";
                    }
                    echo'</table>';    
                }
                else if($opid == 4){
                    $q = 'SELECT Users.userName as userName, weapon, cloth, weaponList, clothList, reward, todayQuota
                        FROM [Equipment] 
                        left join Users 
                        on Users.uid = Equipment.userID
                    ';
                    $result = $db->prepare($q); 
                    $result->execute();            
                    $array = $result->fetchAll(PDO::FETCH_ASSOC);           
                    echo '<table class="table table-striped">
                      <tr>
                        <th>User Name</th>
                        <th>Weapon</th>
                        <th>Cloth</th>
                        <th>Weapon List</th>
                        <th>Cloth List</th>
                        <th>Reward</th>
                        <th>Quota</th>
                      </tr>';
                    for ($i = 0; $i < count($array) ; $i++){
                       echo '<tr> <td> <a href="?opid=6&userName=' .$array[$i]['userName']. '">' .$array[$i]['userName'].  " </a></td> <td> " .$array[$i]['weapon']. " </td> <td> " .$array[$i]['cloth']. " </td> <td> " .$array[$i]['weaponList']. " </td> <td> " .$array[$i]['clothList']. " </td> <td> " .$array[$i]['reward']. " </td> <td> " .$array[$i]['todayQuota']." </td> </tr>";
                    }
                    echo'</table>';    
                }
                else if($opid == 5){                    
                    $q = 'SELECT Users.userName as userName, ATK, DEF, Points
                        FROM [GameData] 
                        left join Users 
                        on Users.uid = GameData.userID
                    ';
                    $result = $db->prepare($q); 
                    $result->execute();            
                    $array = $result->fetchAll(PDO::FETCH_ASSOC);           
                    echo '<table class="table table-striped">
                      <tr>
                        <th>User Name</th>
                        <th>ATK</th>
                        <th>DEF</th>
                        <th>Points</th>
                      </tr>';
                            
                    for ($i = 0; $i < count($array) ; $i++){
                       echo "<tr> <td>" .$array[$i]['userName'].  " </td> <td> " .$array[$i]['ATK']. " </td> <td> " .$array[$i]['DEF']. " </td> <td> " .$array[$i]['Points']. " </td> </tr>";
                    }
                    echo'</table>';    
                }
                else if($opid == 6){                    
                    $q = 'SELECT Users.userName as userName, weapon, cloth
                        FROM [Equipment]
                        left join Users 
                        on Users.uid = Equipment.userID
                        where Users.userName = ?
                    ';
                    $result = $db->prepare($q); 
                    $result->execute(array($userName));            
                    $array = $result->fetchAll(PDO::FETCH_ASSOC);     
                    echo "Charecter of: ".$array[0]['userName'];
                    $imgSource = "pic/char";
                    $imgSource = $imgSource .  $array[0]['cloth'] .  $array[0]['weapon'] . ".jpg";
                    echo "\n";
                    echo '<div id = char><img src="' .$imgSource. '"></div>';
                    
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