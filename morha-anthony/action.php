<?php
include("./includes/database.php");

if(isset($_POST["addCSVData"])){
	$send_dType = preg_replace("/[^a-zA-Z]/", "", $_POST["send_dType"]);
	
	$sendLimit = 1000;
	$sendPage = 2;			// Overstay is max 15 / 1000 // Decision 110 / 1000
	
	if($send_dType == "addDecM" || $send_dType == "addDecF"){
		$recInserted = 0;
		$file = "./permit_req_grant/Sprendimas.csv";
		
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
		
		foreach($dataRows as $row){
			if($row["lytis"] === "V" && $row["pilietybe"] !== "Nežinoma"){
				$chkDataQu = $con->prepare("SELECT * FROM `trp_decisions_male` WHERE `id_1` = ? AND `id_2` = ? AND `gender` = ? LIMIT 1");
				$chkDataQu->execute([$row["_id"], $row["id"], $row["lytis"]]);
				
				if($chkDataQu !== false && $chkDataQu->rowCount() <= 0){
					$insDecM = $con->prepare("INSERT INTO `trp_decisions_male`(`id_1`, `id_2`, `registration_of_decision`, `decision`, `citizenship`, `age_group`, `gender`, `basis_for_decision`, `need`, `upload_date`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())");
					$insDecM->execute([$row["_id"], $row["id"], $row["sprendimo_registracija"], $row["sprendimas"], $row["pilietybe"], $row["amziaus_grupe"], $row["lytis"], $row["pagrindas"], $row["poreiksme"]]);
					if($insDecM !== false){ $recInserted++; }
				}
			}elseif($row["lytis"] === "M" && $row["pilietybe"] !== "Nežinoma"){
				$chkDataQu2 = $con->prepare("SELECT * FROM `trp_decisions_female` WHERE `id_1` = ? AND `id_2` = ? AND `gender` = ? LIMIT 1");
				$chkDataQu2->execute([$row["_id"], $row["id"], $row["lytis"]]);
				
				if($chkDataQu2 !== false && $chkDataQu2->rowCount() <= 0){
					$insDecF = $con->prepare("INSERT INTO `trp_decisions_female`(`id_1`, `id_2`, `registration_of_decision`, `decision`, `citizenship`, `age_group`, `gender`, `basis_for_decision`, `need`, `upload_date`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())");
					$insDecF->execute([$row["_id"], $row["id"], $row["sprendimo_registracija"], $row["sprendimas"], $row["pilietybe"], $row["amziaus_grupe"], $row["lytis"], $row["pagrindas"], $row["poreiksme"]]);
					if($insDecF !== false){ $recInserted++; }
				}
			}else{
				continue;
			}
		}
		
		echo "<pre>";
		echo $recInserted." records inserted successfully";
		//print_r($dataRows);
		echo "</pre>";
		
	}elseif($send_dType == "addOverM" || $send_dType == "addOverF"){
		$recInserted = 0;
		$file = "./permit_req_grant/GrazinimasIssiuntimasIpareigojimas.csv";
		
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
		
		foreach($dataRows as $row){
			if($row["lytis"] === "V" && $row["pilietybe"] !== "Nežinoma"){
				$chkDataQu = $con->prepare("SELECT * FROM `trp_overstay_male` WHERE `id_1` = ? AND `id_2` = ? AND `gender` = ? LIMIT 1");
				$chkDataQu->execute([$row["_id"], $row["id"], $row["lytis"]]);
				
				if($chkDataQu !== false && $chkDataQu->rowCount() <= 0){
					$insOverM = $con->prepare("INSERT INTO `trp_overstay_male`(`id_1`, `id_2`, `citizenship`, `registration_of_decision`, `decision`, `basis_for_decision`, `age_group`, `gender`, `departure`, `need`, `upload_date`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())");
					$insOverM->execute([$row["_id"], $row["id"], $row["pilietybe"], $row["sprendimo_registracija"], $row["sprendimas"], $row["sprendimo_pagrindas"], $row["amziaus_grupe"], $row["lytis"],  $row["nurodytas_isvykimas"],  $row["poreiksme"]]);
					if($insOverM !== false){ $recInserted++; }
				}
			}elseif($row["lytis"] === "M" && $row["pilietybe"] !== "Nežinoma"){
				$chkDataQu2 = $con->prepare("SELECT * FROM `trp_overstay_female` WHERE `id_1` = ? AND `id_2` = ? AND `gender` = ? LIMIT 1");
				$chkDataQu2->execute([$row["_id"], $row["id"], $row["lytis"]]);
				
				if($chkDataQu2 !== false && $chkDataQu2->rowCount() <= 0){
					$insOverF = $con->prepare("INSERT INTO `trp_overstay_female`(`id_1`, `id_2`, `citizenship`, `registration_of_decision`, `decision`, `basis_for_decision`, `age_group`, `gender`, `departure`, `need`, `upload_date`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())");
					$insOverF->execute([$row["_id"], $row["id"], $row["pilietybe"], $row["sprendimo_registracija"], $row["sprendimas"], $row["sprendimo_pagrindas"], $row["amziaus_grupe"], $row["lytis"],  $row["nurodytas_isvykimas"],  $row["poreiksme"]]);
					if($insOverF !== false){ $recInserted++; }
				}
			}else{
				continue;
			}
		}
		
		echo "<pre>";
		echo $recInserted." records inserted successfully";
		//print_r($dataRows);
		echo "</pre>";
	}
}
?>