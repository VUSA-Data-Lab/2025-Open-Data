<?php
$db_host = $db_user = $db_password = $db_name = $wiscoy_url = "";
$scriptServerName = $_SERVER["SERVER_NAME"];

if($scriptServerName == "localhost"){
	$db_host = "localhost";
	$db_user = "root";
	$db_password = "";
	$db_name = "migris";
	
	$wiscoy_url = "http://localhost/soft-proc-class/";
}else{
	$db_host = "localhost";
	
	$db_user = "klaipeda-user";
	$db_password = "Password12345";
	$db_name = "klaipedaDB";
	$wiscoy_url = "https://kps.tbdev.lt/";
}

try{
	$con = new PDO("mysql:host=$db_host;dbname=$db_name", $db_user, $db_password);
	$con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}
catch(PDOException $e){
	echo "Database Connection failed: ".$e->getMessage();
}

function insSysLog($id, $type, $action, $con){
	try{
		$insLogQu = $con->prepare("INSERT INTO `system_log`(`admin_user_id`, `user_type`, `log_action`, `upload_date`) VALUES (:admin_user_id, :user_type, :log_action, NOW())");
		
		$insLogQu->bindParam(":user_type", $type, PDO::PARAM_STR);
		$insLogQu->bindParam(":log_action", $action, PDO::PARAM_STR);
		$insLogQu->bindParam(":admin_user_id", $id, PDO::PARAM_INT);
		
		$insLogQu->execute();
		
		if($insLogQu !== false){
			return "system-log-inserted";
		}else{
			return "problem-inserting-system-log";
		}
	}catch(PDOException $e){
		return "Error: ".$e->getMessage();
	}
}

?>