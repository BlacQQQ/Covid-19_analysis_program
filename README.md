# COVID-19 Statistics Analysis Tool

## Overview

Covid-19 Statistics Analysis Tool is a Python-based tool for analyzing statistics related to the COVID-19 pandemic. The tool allows users to choose variables of interest, time periods, and countries, and then generates charts, descriptive statistics, and reports for more in-depth analysis.

## Features

- **Variable Selection:** Users can choose variables from different categories such as confirmed cases, deaths, hospitalizations, tests, vaccinations, and more.

- **Time Period Analysis:** The tool allows the analysis of data for different time periods, including custom date ranges.

- **Country-specific Analysis:** Users can choose specific countries for analysis.

- **Report Generation:** The tool enables the generation of reports in JSON format, containing detailed statistics and charts.

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Run the main script: `python main.py`

## Configuration

- In the `config.json` file, you can customize tool preferences, such as country selection, variable preferences, and time periods.

## Data Source

The COVID-19 data used in this project is sourced from [GitHub User's Repository](link/do/repository).

## Requirements

- Python 3.6 and above
- Python libraries: pandas, matplotlib, dateutil, openpyxl, seaborn, jupyter, jupyterlab (installed automatically from `requirements.txt`)

## Usage Examples

```bash
python main.py
