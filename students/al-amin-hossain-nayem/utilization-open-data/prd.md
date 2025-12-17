# PRD: World Bank Population & Education Data Comparison (Bangladesh vs Lithuania)

## 1. Overview

A simple data-processing project where **Python** fetches and processes World Bank open data (Population + Education indicators) for **Bangladesh** and **Lithuania**, generates a single `processed.json` file, and a **React frontend** visualizes the results using charts and a search bar.

No backend server is used. Python runs once to generate the processed file. React fetches the static JSON.

---

## 2. Project Goals

1. Fetch World Bank open data for Bangladesh (BGD) and Lithuania (LTU).
2. Extract relevant indicators for population and education.
3. Process, filter, clean, and merge the data in Python.
4. Export the final dataset to `processed.json`.
5. Build a React UI that:

   * Loads the processed data.
   * Displays charts (Recharts).
   * Provides a search bar to filter by district/city.
   * Shows comparison results for both countries.

---

## 3. Data Source

**World Bank Open Data API**
Base URL: [https://api.worldbank.org/v2/](https://api.worldbank.org/v2/)

**Countries Used:**

* Bangladesh → `BGD`
* Lithuania → `LTU`

**Indicators (Examples):**

* Population total: `SP.POP.TOTL`
* School enrollment primary: `SE.PRM.ENRR`
* Literacy rate: `SE.ADT.LITR.ZS`

The exact indicators can be expanded or reduced as needed.

---

## 4. System Architecture (Option B)

### 4.1 Components

1. **Python Data Processor (Required)**

   * Fetches data from World Bank API.
   * Normalizes population and education indicators.
   * Merges BD + LT into a single structure.
   * Saves final output to `processed.json`.

2. **React Frontend (Visualization Layer)**

   * Loads `processed.json` from `/public/processed.json` or GitHub raw link.
   * Uses Recharts to display:

     * Country comparison charts
     * District/city level search results (if available in data)
   * Search bar filters data by district/city name.

3. **Static Output File**

   * `processed.json`: combined, cleaned dataset used by the UI.

---

## 5. Python Program Requirements

### 5.1 File Structure

```
python/
  main.py
  fetcher.py
  processor.py
  utils.py
  output/
    processed.json
```

### 5.2 Python Responsibilities

* Fetch BD & LT indicators.
* Clean missing values.
* Format years as sorted integer keys.
* Combine into a final format:

```
{
  "population": {
    "bangladesh": [...],
    "lithuania": [...]
  },
  "education": {
    "bangladesh": [...],
    "lithuania": [...]
  }
}
```

* (Optional) Add extra computed fields (growth %, difference, etc.)
* Export JSON to `output/processed.json`.

---

## 6. React Frontend Requirements

### 6.1 Tech Stack

* React (Vite) ude this command (npm create vite@latest)  create leatest vite project
* Recharts
* Tailwind (optional)

### 6.2 File Structure

```
react-app/
  public/
    processed.json
  src/
    components/
      CountryChart.jsx
      SearchBar.jsx
      DistrictComparison.jsx
    pages/
      Home.jsx
    utils/
      dataLoader.js
```

### 6.3 UI Features

1. **Home Page**

   * Displays population + education comparison charts for BD vs LT.
   * Uses Recharts (BarChart / LineChart).

2. **Search Bar**

   * Input: district/city name.
   * Filters matching entries from processed JSON.
   * Displays comparison chart for both countries.

3. **Charts**

   * Year-based trend for population.
   * Education indicator comparison.

---

## 7. User Workflow

1. Open website → initial charts show BD vs LT full data.
2. User types "Dhaka" or "Vilnius" → UI filters JSON.
3. React renders charts for that district in both countries.
4. If district not found → show "No data available".

---

## 8. Data Format for Search

The `processed.json` will contain a field for districts if data exists:

```
{
  "districts": {
    "bangladesh": [ { "name": "Dhaka", ... } ],
    "lithuania": [ { "name": "Vilnius", ... } ]
  }
}
```

If district-level data is not available from World Bank, a simplified internal list will be used.

---

## 9. Acceptance Criteria

* Python script runs without errors and generates `processed.json`.
* React successfully fetches the JSON.
* Charts render correctly.
* Search bar works and updates the UI.
* Clean, minimal architecture without unnecessary complexity.

---

## 10. Deliverables

1. `processed.json` (Python output)
2. Python processing code
3. React visualization app
