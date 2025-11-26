<?php
// Initialize variables for database connection and URL
$db_host = $db_user = $db_password = $db_name = $wiscoy_url = "";

// Get the current server name (e.g., localhost or a live domain)
$scriptServerName = $_SERVER["SERVER_NAME"];

// Check if the code is running on localhost (development environment)
if($scriptServerName == "localhost"){
	// Set database details for local testing
	$db_host = "localhost";
	$db_user = "root";
	$db_password = "";
	$db_name = "migris";
	
	// Set the local project URL
	$wiscoy_url = "http://localhost/soft-proc-class/";
}else{
	// Set database details for the live (production) server
	$db_host = "localhost";
	$db_user = "";
	$db_password = "";
	$db_name = "";
	$wiscoy_url = "";
}

// Try to connect to the database using PDO (PHP Data Objects)
try{
	$con = new PDO("mysql:host=$db_host;dbname=$db_name", $db_user, $db_password);
	
	// Enable error reporting for the database connection
	$con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}
catch(PDOException $e){
	// Display an error message if the connection fails
	echo "Database Connection failed: ".$e->getMessage();
}

?>