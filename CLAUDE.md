# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Anomalizer is a Streamlit-based web application for time series analysis and anomaly detection using the Interquartile Range (IQR) method. It allows users to upload Excel files, configure analysis parameters, and visualize anomalies in their data.

## Common Development Commands

### Running the Application
```sh
streamlit run app5.py
```

### Running Tests
```sh
python -m pytest
```

### Linting Code
```sh
# Basic syntax errors and critical issues
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Full linting with complexity checks
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

### Installing Dependencies
```sh
# Using pip
pip install -r requirements.txt

# Using conda (recommended approach from README)
conda create --name anomalizer-env python=3.8
conda activate anomalizer-env
pip install -r requirements.txt
```

### Running a Single Test
```sh
python -m pytest tests/test_anomaly_detection.py::<TestClassName>::<test_method_name>
```

## High-Level Architecture

The application follows a modular architecture with clear separation of concerns:

### Core Modules
- **app5.py**: Main Streamlit application entry point. Handles UI rendering, file uploads, and orchestrates the analysis workflow
- **anomaly_detection.py**: Core business logic for anomaly detection using IQR method. Contains `detect_anomalies()` and `calculate_stats()` functions
- **anomaly_processor.py**: Batch processing functionality for analyzing all numeric columns in a dataset. Creates Excel reports with highlighted anomalies
- **ui_elements.py**: UI configuration and common interface elements (page config, titles, instructions, documentation)

### Data Flow
1. User uploads Excel file through Streamlit interface (app5.py)
2. Data is loaded and columns are categorized (date, numeric, categorical)
3. User selects analysis parameters (columns, grouping, thresholds)
4. IQR statistics are calculated (anomaly_detection.py)
5. Anomalies are detected based on configured thresholds
6. Results are visualized using Plotly charts and can be downloaded as Excel

### Key Design Decisions
- **IQR Method**: Uses statistical approach with Q1 - 1.5*IQR and Q3 + 1.5*IQR as default thresholds
- **Grouping Support**: Can analyze data by categorical groups independently
- **Excel Format**: Input/output in Excel format for business user accessibility
- **Interactive Visualization**: Plotly for dynamic, interactive charts

### Testing Strategy
Tests are located in `tests/test_anomaly_detection.py`. The project uses pytest with CI/CD integration via GitHub Actions that runs tests on Python 3.9, 3.10, and 3.11.

### Docker Deployment
The project includes Docker configuration with automated builds pushed to Docker Hub on successful main branch commits.