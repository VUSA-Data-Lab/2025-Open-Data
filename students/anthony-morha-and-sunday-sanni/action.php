<?php
// Include the database connection file
include("./includes/database.php");

// Check if the form (POST) button 'addCSVData' was clicked
if(isset($_POST["addCSVData"])){
	// Get the data type from the form and remove any non-alphabet characters
	$send_dType = preg_replace("/[^a-zA-Z]/", "", $_POST["send_dType"]);
	
	$sendLimit = 1000;		// Set default values for how many records to process and which page to start from
	$sendPage = 2;			// Overstay is max 15 / 1000 // Decision 110 / 1000
	
	// ==============================
	// CASE 1: Handle decision data
	// ==============================
	if($send_dType == "addDecM" || $send_dType == "addDecF"){
		$recInserted = 0; // Count how many records were added
		$file = "./permit_req_grant/Sprendimas.csv"; // Path to the CSV file
		
		// Stop the script if the file doesn’t exist
		if(!file_exists($file)){ echo "file_not_found"; exit(); }

		// Use the given limit and page from POST, or fall back to default
		$perPage = isset($_POST["limit"]) ? (int)$_POST["limit"] : $sendLimit;
		$page    = isset($_POST["page"]) ? (int)$_POST["page"] : $sendPage;
		$offset  = ($page - 1) * $perPage; // Calculate where to start reading rows

		$dataRows = []; // Store CSV rows

		// Open the CSV file for reading
		if(($handle = fopen($file, "r")) !== FALSE){
			$headers = fgetcsv($handle); // Read column headers
			$currentRow = 0;
			
			// Loop through each row in the file
			while(($row = fgetcsv($handle)) !== FALSE){
				// Only read the rows for the current page (limit & offset)
				if($currentRow >= $offset && $currentRow < $offset + $perPage){
					$dataRows[] = array_combine($headers, $row); // Combine headers with row data
				}
				$currentRow++;
				if($currentRow >= $offset + $perPage){ break; }
			}
			fclose($handle); // Close the file
		}

		// Loop through each row of data and insert it into the database
		foreach($dataRows as $row){
			// If gender is "V" (male) and nationality is known
			if($row["lytis"] === "V" && $row["pilietybe"] !== "Nežinoma"){
				// Check if the record already exists in the male table
				$chkDataQu = $con->prepare("SELECT * FROM `trp_decisions_male` WHERE `id_1` = ? AND `id_2` = ? AND `gender` = ? LIMIT 1");
				$chkDataQu->execute([$row["_id"], $row["id"], $row["lytis"]]);
				
				// If not found, insert a new record
				if($chkDataQu !== false && $chkDataQu->rowCount() <= 0){
					$insDecM = $con->prepare("INSERT INTO `trp_decisions_male`
					(`id_1`, `id_2`, `registration_of_decision`, `decision`, `citizenship`, `age_group`, `gender`, `basis_for_decision`, `need`, `upload_date`)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())");
					$insDecM->execute([$row["_id"], $row["id"], $row["sprendimo_registracija"], $row["sprendimas"], $row["pilietybe"], $row["amziaus_grupe"], $row["lytis"], $row["pagrindas"], $row["poreiksme"]]);
					if($insDecM !== false){ $recInserted++; }
				}
			}
			// If gender is "M" (female) and nationality is known
			elseif($row["lytis"] === "M" && $row["pilietybe"] !== "Nežinoma"){
				$chkDataQu2 = $con->prepare("SELECT * FROM `trp_decisions_female` WHERE `id_1` = ? AND `id_2` = ? AND `gender` = ? LIMIT 1");
				$chkDataQu2->execute([$row["_id"], $row["id"], $row["lytis"]]);
				
				if($chkDataQu2 !== false && $chkDataQu2->rowCount() <= 0){
					$insDecF = $con->prepare("INSERT INTO `trp_decisions_female`
					(`id_1`, `id_2`, `registration_of_decision`, `decision`, `citizenship`, `age_group`, `gender`, `basis_for_decision`, `need`, `upload_date`)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())");
					$insDecF->execute([$row["_id"], $row["id"], $row["sprendimo_registracija"], $row["sprendimas"], $row["pilietybe"], $row["amziaus_grupe"], $row["lytis"], $row["pagrindas"], $row["poreiksme"]]);
					if($insDecF !== false){ $recInserted++; }
				}
			}
			// Skip rows that don't meet conditions
			else{
				continue;
			}
		}
		
		// Show how many records were inserted
		echo "<pre>";
		echo $recInserted." records inserted successfully";
		echo "</pre>";
	
	// ==============================
	// CASE 2: Handle overstay data
	// ==============================
	}elseif($send_dType == "addOverM" || $send_dType == "addOverF"){
		$recInserted = 0;
		$file = "./permit_req_grant/GrazinimasIssiuntimasIpareigojimas.csv"; // Overstay CSV file
		
		if(!file_exists($file)){ echo "file_not_found"; exit(); }
		
		$perPage = isset($_POST["limit"]) ? (int)$_POST["limit"] : $sendLimit;
		$page    = isset($_POST["page"]) ? (int)$_POST["page"] : $sendPage;
		$offset  = ($page - 1) * $perPage;
		
		$dataRows = [];
		
		if(($handle = fopen($file, "r")) !== FALSE){
			$headers = fgetcsv($handle);
			$currentRow = 0;
			
			while(($row = fgetcsv($handle)) !== FALSE){
				if($currentRow >= $offset && $currentRow < $offset + $perPage){
					$dataRows[] = array_combine($headers, $row);
				}
				$currentRow++;
				if($currentRow >= $offset + $perPage){ break; }
			}
			fclose($handle);
		}

		// Insert overstay data by gender (male/female)
		foreach($dataRows as $row){
			// Male data
			if($row["lytis"] === "V" && $row["pilietybe"] !== "Nežinoma"){
				$chkDataQu = $con->prepare("SELECT * FROM `trp_overstay_male` WHERE `id_1` = ? AND `id_2` = ? AND `gender` = ? LIMIT 1");
				$chkDataQu->execute([$row["_id"], $row["id"], $row["lytis"]]);
				
				if($chkDataQu !== false && $chkDataQu->rowCount() <= 0){
					$insOverM = $con->prepare("INSERT INTO `trp_overstay_male`
					(`id_1`, `id_2`, `citizenship`, `registration_of_decision`, `decision`, `basis_for_decision`, `age_group`, `gender`, `departure`, `need`, `upload_date`)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())");
					$insOverM->execute([$row["_id"], $row["id"], $row["pilietybe"], $row["sprendimo_registracija"], $row["sprendimas"], $row["sprendimo_pagrindas"], $row["amziaus_grupe"], $row["lytis"],  $row["nurodytas_isvykimas"],  $row["poreiksme"]]);
					if($insOverM !== false){ $recInserted++; }
				}
			}
			// Female data
			elseif($row["lytis"] === "M" && $row["pilietybe"] !== "Nežinoma"){
				$chkDataQu2 = $con->prepare("SELECT * FROM `trp_overstay_female` WHERE `id_1` = ? AND `id_2` = ? AND `gender` = ? LIMIT 1");
				$chkDataQu2->execute([$row["_id"], $row["id"], $row["lytis"]]);
				
				if($chkDataQu2 !== false && $chkDataQu2->rowCount() <= 0){
					$insOverF = $con->prepare("INSERT INTO `trp_overstay_female`
					(`id_1`, `id_2`, `citizenship`, `registration_of_decision`, `decision`, `basis_for_decision`, `age_group`, `gender`, `departure`, `need`, `upload_date`)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())");
					$insOverF->execute([$row["_id"], $row["id"], $row["pilietybe"], $row["sprendimo_registracija"], $row["sprendimas"], $row["sprendimo_pagrindas"], $row["amziaus_grupe"], $row["lytis"],  $row["nurodytas_isvykimas"],  $row["poreiksme"]]);
					if($insOverF !== false){ $recInserted++; }
				}
			}
			else{
				continue;
			}
		}
		
		echo "<pre>";
		echo $recInserted." records inserted successfully";
		echo "</pre>";
	}
}
?>