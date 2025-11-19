🚀 NASA NEO (Near Earth Objects) Data Analysis

This project analyzes real asteroid data from NASA’s Near Earth Object (NEO) open API.
It demonstrates how to fetch, process, visualize, and interpret open scientific data using Python and modular programming.

🌍 Open Data Source

NASA Near Earth Object Web Service
🔗 API: https://api.nasa.gov/neo/rest/v1/feed

The dataset contains information about asteroids that pass near Earth, including:

Estimated diameter

Relative velocity

Miss distance from Earth

Whether the asteroid is potentially hazardous

Orbiting body

Close-approach date

This is publicly accessible open data provided by NASA.

🧠 Project Features

✔ Fetch asteroid data for any date range
✔ Process raw JSON into a clean pandas DataFrame
✔ Export structured data to CSV (asteroid_data.csv)
✔ Analyze:

Top 10 largest asteroids

Closest asteroid to Earth

✔ Generate visualizations:

📊 diameter_distribution.png — Asteroid size distribution

🥧 hazardous_pie.png — Hazardous vs non-hazardous

🔵 velocity_vs_diameter.png — Velocity vs diameter comparison

✔ Fully modular, PEP8-compliant Python code
✔ Command-line date selection using --start and --end

📁 Project Structure
project/
│
├── main.py                       # Main program controller
├── data_fetcher.py               # Handles NASA API data requests
├── data_processor.py             # Processes and analyzes asteroid data
├── visualization.py              # Creates charts and saves PNG files
│
├── asteroid_data.csv             # Generated dataset output
├── diameter_distribution.png      # Chart output
├── hazardous_pie.png              # Chart output
├── velocity_vs_diameter.png       # Chart output
│
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation

⚙️ How to Run
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run the project with date range
python main.py --start 2024-01-01 --end 2024-01-03

🔑 NASA API Key

The project uses NASA’s default DEMO_KEY, which works but may be rate-limited.
Get your own API key here:

https://api.nasa.gov/

Then update in main.py:

api_key = "YOUR_API_KEY"

📊 Generated Visualizations

The program automatically generates:

File	Description
diameter_distribution.png	Histogram of asteroid diameters
hazardous_pie.png	Hazardous vs non-hazardous ratio
velocity_vs_diameter.png	Scatter plot of asteroid speed vs size

All charts are saved locally and also displayed.

📝 Example Output
Fetching data from NASA...
Processing data...

Number of asteroids: 54
Hazardous asteroids: 4

Top 10 Largest Asteroids:
   ...

Closest Asteroid to Earth:
   ...

Charts generated and saved as PNG files.

🧪 Technologies Used

Python 3

Requests

Pandas

Matplotlib

JSON parsing

Command-line argument parsing

Modular programming (OOP principles)

PEP8 style compliance

🎓 Academic Compliance

This project fully meets the requirements for:

Open data utilization

Data filtering, transformation, visualization, and analysis

Clean modular Python code

Proper documentation

Public GitHub repository submission

📄 License

This project is released under the MIT License.
