# 🚀 NASA NEO (Near Earth Objects) Data Analysis

This project analyzes real asteroid data from NASA’s **Near Earth Object (NEO)** open API.  
It transforms raw NASA data into clean datasets, insights, and visual charts using Python.

---

## 🌍 Open Data Source

**NASA Near Earth Object Web Service**  
🔗 https://api.nasa.gov/neo/rest/v1/feed  

Provides open data about:

- Estimated diameter  
- Velocity  
- Miss distance  
- Hazard classification  
- Orbiting body  
- Close-approach date  

---

## 🧠 Project Features

- Fetch asteroid data for any date range  
- Convert NASA JSON → pandas DataFrame  
- Export processed data to **CSV**  
- Find:
  - Top 10 largest asteroids  
  - Closest asteroid to Earth  
- Generate charts:
  - `diameter_distribution.png`  
  - `hazardous_pie.png`  
  - `velocity_vs_diameter.png`  
- Modular & PEP8-compliant code  
- Command-line arguments (`--start`, `--end`)

---

## 📁 Project Structure

```text
students/
 └── Mohammed-Shameem/
      ├── Report/
      │    └── NasaDataReport.pdf
      ├── Results/
      │    ├── asteroid_data.csv
      │    ├── diameter_distribution.png
      │    ├── hazardous_pie.png
      │    └── velocity_vs_diameter.png
      ├── README.md
      ├── data_fetcher.py
      ├── data_processor.py
      ├── main.py
      ├── requirements.txt
      └── visualization.py
```
---

## ⚙️ How to Run the Project

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
2️⃣ Run the program using a date range
bash
Copy code
```
python main.py --start 2024-01-01 --end 2024-01-03
```
You can change the dates to any valid range supported by NASA.

### 🔑 NASA API Key
The project uses NASA’s default DEMO_KEY, but it can be rate-limited.

Generate your own API key here:

👉 https://api.nasa.gov/

Then update the value in main.py:

python
Copy code
api_key = "YOUR_API_KEY"
📊 Generated Visualizations
The following charts are generated automatically:

File	Description
diameter_distribution.png	Histogram of asteroid diameters
hazardous_pie.png	Hazardous vs non-hazardous asteroids
velocity_vs_diameter.png	Scatter plot comparing speed vs size

All images are saved inside the Results/ folder.

### 📝 Example Terminal Output

```
Fetching data from NASA...
Processing data...

Number of asteroids: 54
Hazardous asteroids: 4

Top 10 Largest Asteroids:
    ...

Closest Asteroid to Earth:
    ...

Charts generated and saved as PNG files.
```
### 🧪 Technologies Used
- Python 3

- Requests

- Pandas

- Matplotlib

- JSON parsing

- argparse (command-line arguments)

- Modular programming (4 Python modules)

- PEP8 style conventions

### 🎓 Academic Compliance
This project satisfies all requirements:

- ✔ Uses publicly accessible open data
- ✔ Performs data filtering, cleaning, analysis, and visualization
- ✔ Code is modular, PEP8-compliant, and maintainable
- ✔ Hosted in a public GitHub repository
- ✔ Includes a final PDF report inside /Report
- ✔ Includes visual results inside /Results

### 📄 License
This project is distributed under the MIT License.

### ✨ Author
Mohammed Shameem
Karuvara Kunnath
VUŠA – Open Data Laboratory, 2025








