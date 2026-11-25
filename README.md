# Weather Forecast & Alert Application

A modular, industry-oriented Python application that fetches real-time and forecast weather data (via **OpenWeatherMap API** or **offline Virtual Simulation**), analyzes weather patterns with **Pandas**, evaluates multi-factor risk alerts (**Rain/Storm, Extreme Heat, High Wind, High Humidity, AQI**), visualizes forecasts with **Matplotlib**, serves JSON results via **FastAPI**, and provides an interactive **Streamlit** dashboard.

---

## Problem Statement
Individuals and operations teams often check raw weather numbers without clear, actionable risk thresholds. Unexpected rain, heatwaves, high winds, or poor air quality cause shipment delays, crop damage, energy spikes, and unsafe outdoor events. This project automates weather monitoring, threshold evaluation, alerting, visualization, and reporting in one clean pipeline.

## Industry Relevance
- **Logistics & Supply Chain**: Reroute deliveries ahead of storms or high winds.
- **Agriculture**: Plan irrigation, spraying, and harvest protection before heavy rain or heatwaves.
- **Travel & Aviation**: Anticipate visibility, wind, and storm disruptions.
- **Event Planning & Public Safety**: Trigger early warnings for extreme heat, lightning, or hazardous AQI.
- **Role Alignment**: Demonstrates skills for **Python Developer, API Integration, Data Analyst, Data Engineering, and Backend/App Developer** roles.

---

## Features
- **Dual Data Modes**:
  - **Live API Mode**: Fetches current weather, 5-day/3-hour forecast, and Air Pollution (AQI) from OpenWeatherMap.
  - **Virtual Simulation Mode**: Runs completely offline using `data/sample_weather.json` (plus deterministic virtual generation for any custom city).
- **Automated Risk Alert Engine**: Evaluates Rain/Storm, High Temperature, High Wind, High Humidity, and AQI against configurable `.env` thresholds with severity levels (`LOW`, `MODERATE`, `HIGH`, `CRITICAL`).
- **Data Processing & Reporting**: Converts JSON payloads into Pandas DataFrames, exports forecast CSVs to `outputs/`, and generates Markdown summary reports in `reports/`.
- **Data Visualization**: Generates 2-panel Matplotlib forecast & threshold charts saved to `images/`.
- **REST API (FastAPI)**: Exposes `/weather/{city}`, `/cities`, and `/alerts/evaluate` with automatic Swagger docs at `/docs`.
- **Interactive Dashboard (Streamlit)**: Visualizes KPIs, color-coded alert banners, city map, charts, and downloadable reports.

---

## Tech Stack
- **Language**: Python 3.10+
- **HTTP & API Integration**: `requests`, OpenWeatherMap REST API
- **Data Analysis & Visualization**: `pandas`, `matplotlib`
- **Backend API**: `fastapi`, `uvicorn`
- **Dashboard (Optional)**: `streamlit`
- **Configuration**: `python-dotenv`, `.env`

---

## Folder Structure
```text
Weather-Forecast-Alert-Application/
│
├── data/                   # Sample multi-city weather JSON for offline simulation
│   └── sample_weather.json
├── src/                    # Modular source code
│   ├── __init__.py
│   ├── config.py           # Environment variables, paths & alert thresholds
│   ├── weather_fetcher.py  # OpenWeatherMap API client + simulation loader
│   ├── data_processor.py   # JSON parsing & Pandas forecast summarization
│   ├── alert_engine.py     # Multi-rule risk evaluation engine
│   ├── visualizer.py       # Matplotlib forecast & risk chart generator
│   ├── report_generator.py # CSV & Markdown report exporter
│   ├── api.py              # FastAPI REST endpoints
│   └── dashboard.py        # Optional Streamlit dashboard
├── outputs/                # Generated CSV forecast files
├── images/                 # Generated Matplotlib PNG charts & screenshots
├── reports/                # Generated Markdown weather & alert reports
├── docs/                   # Architecture diagrams & project documentation
│   └── architecture.md
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Safe environment template (no secrets)
├── .gitignore              # Protects .env and virtual environments
└── README.md               # Project documentation
```

---

## Setup & API Configuration

### 1. Clone & Create Virtual Environment
```bash
git clone https://github.com/<your-username>/Weather-Forecast-Alert-Application.git
cd Weather-Forecast-Alert-Application

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure `.env` Safely
Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```
Edit `.env` and add your free OpenWeatherMap API key (from [openweathermap.org/api](https://openweathermap.org/api)) if you want to run live API mode. **Never commit `.env` to GitHub.**

---

## How to Run

### A. Run CLI in Virtual Simulation Mode (No API Key Needed)
```bash
python main.py --city Mumbai --mode simulation
```

### B. Run CLI in Live API Mode
```bash
python main.py --city London --mode api
```

### C. Run Interactive Mode
```bash
python main.py
```

### D. Start the FastAPI Server
```bash
uvicorn src.api:app --reload
```
Open Swagger API docs at: `http://127.0.0.1:8000/docs`

### E. Start the Streamlit Dashboard (Optional)
```bash
streamlit run src/dashboard.py
```

---

## Sample Output
```text
====================================================================
  WEATHER FORECAST & ALERT REPORT: MUMBAI (IN)
====================================================================
Source        : sample_dataset
Condition     : Heavy Intensity Rain
Temperature   : 31.2 °C (Feels like 37.8 °C)
Humidity      : 89 %
Wind Speed    : 11.4 m/s (41.0 km/h)
Air Quality   : 2 / 5 (Fair)

--- Risk Alert Evaluation ---
Overall Risk Level : CRITICAL (3 active alert(s))
  1. [CRITICAL] RAIN / STORM ALERT
     Details : Severe rain/storm risk detected (condition: Rain, peak rain probability: 90%).
     Advice  : Delay outdoor events, secure logistics cargo, and avoid flood-prone routes.
  2. [HIGH] HIGH WIND ALERT
     Details : Strong winds expected: 12.5 m/s (45.0 km/h) >= 10.0 m/s.
  3. [MODERATE] HIGH HUMIDITY ALERT
     Details : High humidity level: 93% >= 80% threshold.
====================================================================
```

---

## Screenshots & Visuals
- Forecast & Threshold Chart: `images/mumbai_forecast_chart.png`
- Forecast CSV Export: `outputs/mumbai_forecast.csv`
- Detailed Markdown Report: `reports/mumbai_weather_report.md`

---

## Learning Outcomes
- Consuming external REST APIs securely with `requests`, HTTP error handling, and `.env` secret management.
- Transforming nested JSON payloads into clean Pandas DataFrames for statistical summarization.
- Designing a configurable rule-based alert engine with severity prioritization.
- Building automated data pipelines that export CSVs, Markdown reports, and Matplotlib charts.
- Serving analytics via FastAPI and interactive Streamlit dashboards.
