<?php

declare(strict_types=1);

/**
 * Project: Eurostat Student Analysis Tool
 * Description: Dynamic data fetcher for Tertiary Education (educ_uoe_enrt03).
 */

// ---------------------------------------------------------
//  1: Configuration (Dictionaries)
// ---------------------------------------------------------
class EurostatConfig
{
    public static function getFieldsOfEducation(): array
    {
        return [
            'TOTAL' => '--- Total: All Fields of Education ---',
            'F00'   => '00: Generic programmes and qualifications',
            'F01'   => '01: Education',
            'F02'   => '02: Arts and humanities',
            'F03'   => '03: Social sciences, journalism and information',
            'F04'   => '04: Business, administration and law',
            'F05'   => '05: Natural sciences, mathematics and statistics',
            'F06'   => '06: Information and Communication Technologies (ICTs)',
            'F07'   => '07: Engineering, manufacturing and construction',
            'F08'   => '08: Agriculture, forestry, fisheries and veterinary',
            'F09'   => '09: Health and welfare',
            'F10'   => '10: Services',
            'UNK'   => 'Unknown field of education'
        ];
    }

    // Comprehensive List of Countries (EU + EFTA + Candidates)
    public static function getCountries(): array
    {
        return [
            // EU 27
            'AT' => 'Austria', 'BE' => 'Belgium', 'BG' => 'Bulgaria', 'HR' => 'Croatia',
            'CY' => 'Cyprus', 'CZ' => 'Czechia', 'DK' => 'Denmark', 'EE' => 'Estonia',
            'FI' => 'Finland', 'FR' => 'France', 'DE' => 'Germany', 'GR' => 'Greece',
            'HU' => 'Hungary', 'IE' => 'Ireland', 'IT' => 'Italy', 'LV' => 'Latvia',
            'LT' => 'Lithuania', 'LU' => 'Luxembourg', 'MT' => 'Malta', 'NL' => 'Netherlands',
            'PL' => 'Poland', 'PT' => 'Portugal', 'RO' => 'Romania', 'SK' => 'Slovakia',
            'SI' => 'Slovenia', 'ES' => 'Spain', 'SE' => 'Sweden',
            // EFTA
            'IS' => 'Iceland', 'NO' => 'Norway', 'LI' => 'Liechtenstein', 'CH' => 'Switzerland',
            // Candidates/Others
            'UK' => 'United Kingdom', 'TR' => 'Turkey', 'RS' => 'Serbia', 'MK' => 'North Macedonia'
        ];
    }

    public static function getYears(): array
    {
        $years = [];
        $currentYear = (int)date('Y');
        for ($i = $currentYear - 1; $i >= 2013; $i--) {
            $years[] = (string)$i;
        }
        return $years;
    }
}

// ---------------------------------------------------------
//  2: Data Acquisition
// ---------------------------------------------------------
class EurostatFetcher
{
    private string $baseUrl = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/";//base part of url
    private string $datasetCode = 'educ_uoe_enrt03';// code for students table

    public function fetchData(string $year, string $fieldCode, array $countries): array
    {
        // Parameter Construction
        $params = [
            'format'   => 'JSON',    // Format Json
            'lang'     => 'en',      // En language
            'sex'      => 'T',       // Total sex( can be changed to F or M
            'unit'     => 'NR',      // Number
            'isced11'  => 'ED5-8',   // Type Tertiary Education (Universities)
            'iscedf13' => $fieldCode,
            'time'     => $year
        ];

        $queryString = http_build_query($params); //makes sting look like format=JSON&lang=en&sex=T...

        // Add countries
        if (empty($countries)) {
            throw new Exception("Please select at least one country.");
        }
        foreach ($countries as $geo) {//&geo=LT&geo=DE&geo=FR, because standard function http_build_query do not work with same keys (geo) so it was done manually
            $queryString .= "&geo=" . urlencode($geo);
        }

        $url = $this->baseUrl . $this->datasetCode . "?" . $queryString;// creating final url

        // Fetch
        $response = @file_get_contents($url); //get request

        if ($response === false) {//error handling
            throw new Exception("Error connecting to Eurostat. Data might be missing for this specific Year/Field combination.");
        }

        return json_decode($response, true);// decode json to php array for easy processing
    }
}

// ---------------------------------------------------------
//  3: Processing
// ---------------------------------------------------------
class DataProcessor
{
    public function process(array $rawData): array
    {
        $result = [];

        if (!isset($rawData['value']) || !isset($rawData['dimension']['geo'])) {
            return [];// if no data return nothing
        }

        $geoIndices = $rawData['dimension']['geo']['category']['index'] ?? [];
        $geoLabels  = $rawData['dimension']['geo']['category']['label'] ?? [];
        $values     = $rawData['value'];

        foreach ($geoIndices as $code => $index) {//run through all countries returned by api
            $valKey = (string)$index; //json index ( 0 or 1 (string))
            $count = isset($values[$valKey]) ? $values[$valKey] : 0;

            $result[] = [
                'code' => $code,
                'name' => $geoLabels[$code] ?? $code,
                'count' => $count
            ];
        }

        // sort high to low
        usort($result, fn($a, $b) => $b['count'] <=> $a['count']);

        return $result;
    }
}

// ---------------------------------------------------------
// CONTROLLER
// ---------------------------------------------------------
$configFields    = EurostatConfig::getFieldsOfEducation();
$configCountries = EurostatConfig::getCountries();
$configYears     = EurostatConfig::getYears();

// Defaults
$selYear      = $_GET['year'] ?? '2021';//?? if null then default value
$selField     = $_GET['field'] ?? 'TOTAL'; // Default to Total
$selCountries = $_GET['countries'] ?? ['LT', 'DE', 'FR', 'PL', 'ES'];

$tableData = null;
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    try {
        $fetcher = new EurostatFetcher();
        $rawData = $fetcher->fetchData($selYear, $selField, $selCountries);
        $processor = new DataProcessor();
        $tableData = $processor->process($rawData);
    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tertiary Education Analyzer</title>
    <style>
        :root { --primary: #004494; --bg: #f0f2f5; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg); margin: 0; padding: 20px; color: #333; }
        .container { max-width: 950px; margin: 0 auto; }

        h1 { text-align: center; color: var(--primary); margin-bottom: 5px; }
        p.subtitle { text-align: center; color: #666; margin-bottom: 30px; }

        /* Card Style */
        .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }

        /* Form Grid */
        .form-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; }

        label { font-weight: 600; display: block; margin-bottom: 5px; color: #444; }
        select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 1rem; }

        /* Countries Checkboxes */
        .country-wrapper { grid-column: 1 / -1; border-top: 1px solid #eee; padding-top: 15px; margin-top: 10px; }
        .country-controls { margin-bottom: 10px; }
        .btn-mini { background: #e2e6ea; border: none; padding: 5px 12px; cursor: pointer; font-size: 0.85rem; border-radius: 15px; margin-right: 5px; transition: 0.2s; }
        .btn-mini:hover { background: #dbe0e5; }

        .checkbox-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 8px;
            max-height: 250px;
            overflow-y: auto;
            border: 1px solid #eee;
            padding: 10px;
            background: #fafafa;
        }
        .cb-item { font-size: 0.9rem; display: flex; align-items: center; gap: 8px; cursor: pointer; }

        /* Submit Button */
        .btn-submit { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; font-size: 1.1rem; font-weight: bold; border-radius: 5px; cursor: pointer; margin-top: 20px; transition: background 0.3s; }
        .btn-submit:hover { background: #003366; }

        /* Results Table */
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { background: var(--primary); color: white; padding: 12px; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #ddd; }
        tr:hover { background-color: #f1f1f1; }
        .count-col { font-weight: bold; color: var(--primary); }

        .error-msg { background: #ffebee; color: #c62828; padding: 15px; border-radius: 5px; border: 1px solid #ffcdd2; }
    </style>
    <script>
        function setAll(checked) {
            const cbs = document.querySelectorAll('input[name="countries[]"]');
            cbs.forEach(cb => cb.checked = checked);
        }
    </script>
</head>
<body>

<div class="container">
    <h1>🇪🇺 European Education Data</h1>
    <p class="subtitle">Tertiary Education Enrollment (Universities & Colleges)</p>

    <!-- FORM SECTION -->
    <div class="card">
        <form method="GET">
            <div class="form-grid">
                <!-- YEAR -->
                <div>
                    <label>1. Select Year</label>
                    <select name="year">
                        <?php foreach($configYears as $yr): ?>
                            <option value="<?= $yr ?>" <?= $selYear == $yr ? 'selected' : '' ?>><?= $yr ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <!-- FIELD OF STUDY -->
                <div>
                    <label>2. Field of Education</label>
                    <select name="field">
                        <?php foreach($configFields as $code => $name): ?>
                            <option value="<?= $code ?>" <?= $selField == $code ? 'selected' : '' ?>>
                                <?= $name ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <!-- COUNTRIES -->
                <div class="country-wrapper">
                    <label>3. Compare Countries</label>
                    <div class="country-controls">
                        <button type="button" class="btn-mini" onclick="setAll(true)">Select All</button>
                        <button type="button" class="btn-mini" onclick="setAll(false)">Deselect All</button>
                    </div>
                    <div class="checkbox-grid">
                        <?php foreach($configCountries as $code => $name): ?>
                            <label class="cb-item">
                                <input type="checkbox" name="countries[]" value="<?= $code ?>"
                                    <?= in_array($code, $selCountries) ? 'checked' : '' ?>>
                                <?= $name ?>
                            </label>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>

            <button type="submit" class="btn-submit">Show Statistics</button>
        </form>
    </div>

    <!-- RESULTS SECTION -->
    <div class="card">
        <?php if($error): ?>
            <div class="error-msg"><strong>Error:</strong> <?= htmlspecialchars($error) ?></div>
        <?php elseif($tableData !== null): ?>
            <h3>Results: <?= $configFields[$selField] ?> (<?= $selYear ?>)</h3>

            <?php if(empty($tableData)): ?>
                <p>No data available for this selection.</p>
            <?php else: ?>
                <table>
                    <thead>
                    <tr>
                        <th width="10%">Rank</th>
                        <th width="15%">Code</th>
                        <th width="50%">Country</th>
                        <th width="25%">Students</th>
                    </tr>
                    </thead>
                    <tbody>
                    <?php $rank = 1; foreach($tableData as $row): ?>
                        <tr>
                            <td><?= $rank++ ?></td>
                            <td><?= $row['code'] ?></td>
                            <td><?= htmlspecialchars($row['name']) ?></td>
                            <td class="count-col"><?= number_format($row['count']) ?></td>
                        </tr>
                    <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>
        <?php else: ?>
            <p>Select parameters above to generate the report.</p>
        <?php endif; ?>
    </div>
</div>

</body>
</html>