# AI Data Quality Scoring System

This is a Streamlit app for analyzing and cleaning CSV data files.

## Features

- Upload CSV files
- Analyze data for missing values, duplicates, and outliers
- Calculate initial data quality score
- Automatically clean data (fill missing values, remove duplicates, remove outliers)
- Calculate final data quality score
- Download cleaned data

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the App

In the terminal, run:
```
streamlit run app.py
```

The browser will open automatically. Upload a CSV file to get started.

## Project Structure

- `app.py`: Main Streamlit application
- `data_cleaning.py`: Data analysis and cleaning functions
- `utils.py`: Utility functions (currently empty)
- `requirements.txt`: Python dependencies