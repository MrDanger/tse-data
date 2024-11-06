
# TSE Data Fetcher

## Overview

This project is designed to fetch various data types from the Iranian Stock Market (TSE) and save them in CSV files. Additionally, it includes functionality for automated data storage in Google Sheets using Google API credentials. 

## Features

- **Data Fetching**: Utilizes `pytse-client` to collect Iranian stock market data.
- **Data Storage**: Exports data into CSV format and/or uploads to Google Sheets for streamlined analysis.
- **Automation Capabilities**: Scheduling and continuous data fetching with integrated error handling.
- **Configurability**: Environment-based settings allow for easy configuration adjustments, using `.env` files.
- **Customizable Scheduler**: The project includes a `scheduler.py` file to manage regular updates with minimal manual intervention.

## Requirements

The dependencies for this project are listed in `requirements.txt`:
- `pytse-client==0.16`: For interfacing with TSE data.
- `requests==2.31.0`: HTTP requests for network interactions.
- `gspread==5.10.0`: Google Sheets API client.
- `pandas==2.0.3`: Data handling and processing.
- `python-dotenv==1.0.0`: Environment variable management.
- `jdatetime~=3.8.2`: Persian calendar support.

### Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:MrDanger/tse-data.git
   cd tse-data
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets API credentials**:
   - Place the Google API JSON credentials file in the project root directory.
   - Name it `google_credentials.json`.

4. **Configure environment variables**:
   - Create a `.env` file in the project root with required API keys and paths. Example `.env` file:

     ```plaintext
     GOOGLE_SHEETS_KEY_PATH="./google_credentials.json"
     OUTPUT_DIR="./data"
     ```

## Usage

### Data Fetching

- To fetch TSE data and save it as a CSV, use `fetch_data.py`.
  ```bash
  python fetch_data.py
  ```

### Automating Data Fetch

- Use `scheduler.py` to schedule and automate data fetching tasks. This script can be set up with a cron job or other scheduling tools for periodic execution.

### Continuous Data Collection

- `run_continues.py` enables an ongoing data collection loop with error handling and retry logic. Start it by running:
  ```bash
  python run_continues.py
  ```

### Google Sheets Integration

- `main.py` includes logic for pushing the collected data to Google Sheets.
  ```bash
  python main.py
  ```

## Project Structure

- `fetch_data.py`: Core script for fetching TSE data.
- `calc_average.py`: Contains utility functions for calculating data averages.
- `main.py`: Main script for data processing and Google Sheets integration.
- `run_continues.py`: Looping mechanism for continuous data fetching.
- `scheduler.py`: Scheduler for timed data collection.
- `static.py`: Static configuration variables for project-wide settings.

## Logging and Error Handling

Error logs are saved in `logs/`, making it easier to diagnose issues with data fetching, Google Sheets integration, or other processes.

## Customization

To extend functionality:
- Modify `scheduler.py` to adjust frequency and parameters for data collection.
- Update `static.py` for configuration changes, such as output directory or additional static configurations.

## License

This project is licensed under the MIT License.
