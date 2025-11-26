# Eurostat Unemployment Data Visualization

This project is a web application that visualizes the yearly average unemployment rate in Lithuania from 2015 to 2024. The data is fetched directly from the [Eurostat API](https://ec.europa.eu/eurostat/web/main/data/database) and displayed in an interactive chart.

## Live Demo

You can view the live application here: [https://splendid-crepe-c507dc.netlify.app/](https://splendid-crepe-c507dc.netlify.app/)

## Features

*   Fetches unemployment data directly from the Eurostat API in real-time.
*   Processes and calculates the yearly average unemployment rate.
*   Displays the data in an interactive line chart.
*   Responsive design that works on different screen sizes.

## Technologies Used

### Frontend

*   **React:** A JavaScript library for building user interfaces.
*   **Vite:** A fast build tool for modern web development.
*   **Recharts:** A composable charting library built on React components.
*   **JavaScript (ES6+):** The programming language used for the frontend logic.
*   **HTML5 & CSS3:** For structuring and styling the application.

### Backend (Optional)

The backend script is no longer required for the web application to function, but it is available for users who want to fetch and process the data into a `processed.json` file manually.

*   **Python:** The programming language used for the backend script.
*   **requests:** A Python library for making HTTP requests.
*   **pandas:** A powerful data analysis and manipulation library.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   **Node.js and npm:** Make sure you have Node.js and npm installed on your machine. You can download them from [here](https://nodejs.org/).

### Installation & Running the Frontend

1.  Clone the repo
    ```sh
    git clone https://github.com/your_username_/your_repository.git
    ```
2.  Navigate to the frontend directory
    ```sh
    cd your_repository/frontend
    ```
3.  Install NPM packages
    ```sh
    npm install
    ```
4.  Start the development server
    ```sh
    npm run dev
    ```
    The application will be available at `http://localhost:5173` (the port may vary).

### Running the Backend (Optional)

If you want to generate the `processed.json` file manually:

1.  Navigate to the backend directory
    ```sh
    cd your_repository/backend
    ```
2.  Install Python packages
    ```sh
    pip install -r requirements.txt
    ```
3.  Run the script
    ```sh
    python main.py
    ```
    This will generate a `processed.json` file in the root of the project.

## Data Source

The data for this project is sourced from the [Eurostat API](https://ec.europa.eu/eurostat/web/main/data/database). Specifically, it uses the `une_rt_m` dataset, which contains monthly unemployment rates.
