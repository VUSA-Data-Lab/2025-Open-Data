# Lithuania EV Charging Infrastructure Analysis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-orange)

## 📌 Project Overview

This project utilizes **Open Data** to analyze the growth and geographic distribution of Electric Vehicle (EV) charging stations in Lithuania.

Built with **Python**, the application follows a **Modular Object-Oriented** architecture to:

1.  **Extract** real-time XML data from the Lithuanian Road Administration.
2.  **Transform** and clean the data (handling dates, types, and missing values).
3.  **Visualize** the results using interactive maps and statistical charts.

## 📂 Data Source

- **Provider:** Via Lietuva (Lithuanian Road Administration)
- **URL:** [Energy Infrastructure Table Publication](https://ev.vialietuva.lt/publicdata/EnergyInfrastructureTablePublication)
- **Format:** XML (DATEX II Standard)
- **Content:** Real-time data on public charging points, power output, and connector types.

## 🏗 Project Structure

The project adheres to strict **PEP8** standards and uses a modular design:

```text
├── data/                   # Stores raw downloaded CSV data
├── output/                 # Generated results
│   ├── maps/               # Interactive HTML maps
│   └── plots/              # Static PNG statistical charts
├── src/                    # Source code package
│   ├── __init__.py         # Package initialization
│   ├── etl.py              # Data extraction and cleaning logic (Class: EVDataPipeline)
│   └── visualizer.py       # Visualization logic (Class: EVVisualizer)
├── main.py                 # Entry point of the application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
🚀 Installation & Usage
Prerequisites
Python 3.8 or higher
Git
Setup
Clone the repository:
code
Bash
git clone https://github.com/MuhamedSaber1990/Lithuania-EV-Charging-Infrastructure.git
cd Lithuania-EV-Charging-Infrastructure
Install dependencies:
code
Bash
pip install -r requirements.txt
Run the application:
code
Bash
python main.py
📊 Outputs
After running the program, the following files are generated in the output/ directory:
Interactive Map (output/maps/lithuania_ev_map.html):
A zoomable map of Lithuania showing all charging stations.
Red Markers: Fast Chargers (≥50 kW).
Green Markers: Standard Chargers (<50 kW).
Includes clustering for better visibility in high-density areas.
Growth Chart (output/plots/growth_chart.png):
A time-series graph showing the cumulative installation of charging stations.
Power Distribution (output/plots/power_dist.png):
A histogram displaying the frequency of different power outputs (kW).
🛠 Technologies Used
Language: Python 3
Data Processing: pandas, xml.etree
Visualization: folium (Maps), matplotlib (Charts)
Networking: requests
📝 Authors
Mohamed Saber - Student Project
```
