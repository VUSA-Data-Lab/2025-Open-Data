<?php
session_start();

include("./includes/database.php");

$setNat = $setNatVal1 = $setNatVal2 = $natTxt = "";

if(isset($_GET["country"]) && !empty($_GET["country"])){
	$setNat = preg_replace("/[^A-Z]/", "", $_GET["country"]);
	$setNatVal1 = "WHERE `citizenship` LIKE '%".$setNat."%'";
	$setNatVal2 = "AND `citizenship` LIKE '%".$setNat."%'";
	$natTxt = "from ".$setNat;
}

$getData_tdm = $con->query("SELECT * FROM `trp_decisions_male` $setNatVal1");
if($getData_tdm !== false){ $tdm_count = $getData_tdm->rowCount(); }

$getData_tdf = $con->query("SELECT * FROM `trp_decisions_female` $setNatVal1");
if($getData_tdf !== false){ $tdf_count = $getData_tdf->rowCount(); }

$getData_tom = $con->query("SELECT * FROM `trp_overstay_male` $setNatVal1");
if($getData_tom !== false){ $tom_count = $getData_tom->rowCount(); }

$getData_tof = $con->query("SELECT * FROM `trp_overstay_female` $setNatVal1");
if($getData_tof !== false){ $tof_count = $getData_tof->rowCount(); }
?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<title>Migris Overstay Probability Demo</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous" />

<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>

<script src="./plotly-3.1.0.min.js"></script>
<!-- https://plotly.com/javascript/histograms/ -->
</head>
<body>
<section>
	<div class="container">
		<div class="row py-5 justify-content-center">
			<div class="col-lg-9">
				<?php if(isset($_GET["country"]) && !empty($_GET["country"]) && !empty($setNat)){ ?>
				<h1>Total Data for <?php echo $setNat; ?> (<?php echo $tdm_count + $tdf_count + $tom_count + $tof_count; ?>)</h1>
				<p><a href="./">Reset Data</a></p>
				<?php }else{ ?>
				<h1>Data from Database (<?php echo $tdm_count + $tdf_count + $tom_count + $tof_count; ?>)</h1>
				<?php } ?>
				
				<div class="mt-3 p-3 shadow-sm border rounded">
					<form action="./" method="GET">
						<div class="mb-3">
							<label class="form-label">Select Country for Specific Data*</label>
							<select class="form-select mb-3" name="country" required>
								<option value="">Select Country</option>
								<?php
									$gtNatQu = $con->query("
										SELECT DISTINCT `citizenship` 
										FROM (
											SELECT `citizenship` FROM `trp_decisions_male` WHERE `citizenship` <> 'Be pilietybės'
											UNION
											SELECT `citizenship` FROM `trp_decisions_female` WHERE `citizenship` <> 'Be pilietybės'
											UNION
											SELECT `citizenship` FROM `trp_overstay_male` WHERE `citizenship` <> 'Be pilietybės'
											UNION
											SELECT `citizenship` FROM `trp_overstay_female` WHERE `citizenship` <> 'Be pilietybės'
										) AS all_citizenships
										WHERE CHAR_LENGTH(`citizenship`) = 3
										ORDER BY `citizenship`;
									");
									
									if($gtNatQu !== false && $gtNatQu->rowCount() >= 1){
										while($row_gtNatQu = $gtNatQu->fetch(PDO::FETCH_ASSOC)){
											$ctzn = $row_gtNatQu["citizenship"];
											echo "<option value='$ctzn'>$ctzn</option>";
										}
									}
								?>
							</select>
						</div>
						
						<input type="submit" class="btn btn-primary" name="send_request" value="Get Data" />
					</form>
				</div>
				
				<hr />
				<p class="mb-1">Total TRP Decisions Data Male <?php echo $natTxt; ?>: <?php echo $tdm_count; ?></p>
				<p class="mb-1">Total TRP Decisions Data Female <?php echo $natTxt; ?>: <?php echo $tdf_count; ?></p>
				
				<?php
					$maleRes1 = $con->query("SELECT YEAR(`registration_of_decision`) AS year, COUNT(*) AS total FROM `trp_decisions_male` $setNatVal1 GROUP BY year;");
					$femaleRes1 = $con->query("SELECT YEAR(`registration_of_decision`) AS year, COUNT(*) AS total FROM `trp_decisions_female` $setNatVal1 GROUP BY year;");
					
					$combData1 = [];
					
					// Store male results
					while($maleRow1 = $maleRes1->fetch(PDO::FETCH_ASSOC)){
						$year = $maleRow1['year'];
						$combData1[$year]['year'] = $year;
						$combData1[$year]['male'] = (int)$maleRow1['total'];
						// Ensure female is set to 0 if missing
						if(!isset($combData1[$year]['female'])){
							$combData1[$year]['female'] = 0;
						}
					}
					
					// Store female results
					while($femaleRow1 = $femaleRes1->fetch(PDO::FETCH_ASSOC)){
						$year = $femaleRow1['year'];
						$combData1[$year]['year'] = $year;
						$combData1[$year]['female'] = (int)$femaleRow1['total'];
						// Ensure male is set to 0 if missing
						if(!isset($combData1[$year]['male'])){
							$combData1[$year]['male'] = 0;
						}
					}
					
					$combData1 = array_values($combData1);
					
					$vValyr1 = array_column($combData1, 'year');
					$yVal1male = array_column($combData1, 'male');
					$yVal1fem = array_column($combData1, 'female');
				?>
				
				<div class="pt-3">
					<div id="barChart1"></div>
					
					<script>
						let xVal  = <?php echo json_encode($vValyr1); ?>;
						let yVal1 = <?php echo json_encode($yVal1male); ?>;
						let yVal2 = <?php echo json_encode($yVal1fem); ?>;
						
						let trace1 = {x:xVal, y:yVal1, name:"Male", type:"bar"};
						let trace2 = {x:xVal, y:yVal2, name:"Female", type:"bar"};
						
						let data = [trace1, trace2];
						let layout = {barmode:"group"};
						Plotly.newPlot("barChart1", data, layout);
					</script>
				</div>
				
				<?php
					$maleProb = round(100* ($tom_count / $tdm_count), 2);
					$femaleProb = round(100* ($tof_count / $tdf_count), 2);
					
					if($maleProb >= 101){ $maleProb = 100; }
					if($femaleProb >= 101){ $femaleProb = 100; }
				?>
				
				<hr />
				<p class="mb-1">Total Overstay Data Male <?php echo $natTxt; ?>: <?php echo $tom_count; ?></p>
				<?php if(isset($_GET["country"]) && !empty($_GET["country"]) && !empty($setNat)){ ?>
				<p>The probability that a <b>Male <?php echo $natTxt; ?></b> will overstay their visa is: <b><?php echo $maleProb."%"; ?></b></p>
				<hr />
				<?php } ?>
				
				<p class="mb-1">Total Overstay Data Female <?php echo $natTxt; ?>: <?php echo $tof_count; ?></p>
				<?php if(isset($_GET["country"]) && !empty($_GET["country"]) && !empty($setNat)){ ?>
				<p>The probability that a <b>Female <?php echo $natTxt; ?></b> will overstay their visa is: <b><?php echo $femaleProb."%"; ?></b></p>
				<?php } ?>
				
				<?php
					$maleRes2 = $con->query("SELECT YEAR(`registration_of_decision`) AS year, COUNT(*) AS total FROM `trp_overstay_male` $setNatVal1 GROUP BY year;");
					$femaleRes2 = $con->query("SELECT YEAR(`registration_of_decision`) AS year, COUNT(*) AS total FROM `trp_overstay_female` $setNatVal1 GROUP BY year;");
					
					$combData2 = [];
					
					// Store male results
					while($maleRow2 = $maleRes2->fetch(PDO::FETCH_ASSOC)){
						$year = $maleRow2['year'];
						$combData2[$year]['year'] = $year;
						$combData2[$year]['male'] = (int)$maleRow2['total'];
						// Ensure female is set to 0 if missing
						if(!isset($combData2[$year]['female'])){
							$combData2[$year]['female'] = 0;
						}
					}
					
					// Store female results
					while($femaleRow2 = $femaleRes2->fetch(PDO::FETCH_ASSOC)){
						$year = $femaleRow2['year'];
						$combData2[$year]['year'] = $year;
						$combData2[$year]['female'] = (int)$femaleRow2['total'];
						// Ensure male is set to 0 if missing
						if(!isset($combData2[$year]['male'])){
							$combData2[$year]['male'] = 0;
						}
					}
					
					$combData2 = array_values($combData2);
					
					$vValyr2 = array_column($combData2, 'year');
					$yVal2male = array_column($combData2, 'male');
					$yVal2fem = array_column($combData2, 'female');
				?>
				
				<div class="pt-3">
					<div id="barChart2"></div>
					
					<script>
						let x2Val  = <?php echo json_encode($vValyr2); ?>;
						let y2Val1 = <?php echo json_encode($yVal2male); ?>;
						let y2Val2 = <?php echo json_encode($yVal2fem); ?>;
						
						let data2 = [{x:x2Val, y:y2Val1, name:"Male", type:"bar"}, {x:x2Val, y:y2Val2, name:"Female", type:"bar"}];
						let layout2 = {barmode:"group"};
						Plotly.newPlot("barChart2", data2, layout2);
					</script>
				</div>
				
				<hr />
				<div class="d-flex justify-content-between">
					<a href="#" class="btn btn-primary addCSVData" dType="addDecM">Add Decision Male and Female</a>
					<a href="#" class="btn btn-primary addCSVData" dType="addOverM">Add Overstay Male and Female</a>
				</div>
				
				<div class="loadingClass"></div>
			</div>
		</div>
	</div>
</section>

<script>
$(document).ready(function(){
	$("body").on("click",".addCSVData",function(ev){
		ev.preventDefault();
		
		let dType = $(this).attr("dType");
		
		$(".loadingClass").html("<hr /><div class='progress' role='progressbar' aria-label='load' aria-valuenow='100' aria-valuemin='0' aria-valuemax='100' style='height:30px'><div class='progress-bar progress-bar-striped progress-bar-animated' style='width:100%'>Loading...</div></div>");
		
		$.ajax({
			type:	"POST",
			url:	"./action.php",
			data:	{addCSVData:1, send_dType:dType},
			success:function(new_entry){
				$(".loadingClass").html(new_entry);
			}
		});
	});
});
</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
</body>
</html>