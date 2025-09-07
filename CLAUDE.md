# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Anomalizer v2.0 is a Streamlit-based web application for time series analysis and anomaly detection using the Interquartile Range (IQR) method. It allows users to upload Excel files, configure analysis parameters, and visualize anomalies with interactive charts. The v2.0 release features a complete architectural refactor with modular components, expanded testing (23 tests), and comprehensive deployment options.

## Common Development Commands

### Running the Application
```sh
# Standard local development
streamlit run app5.py

# Docker development
docker-compose up

# Docker production with nginx
docker-compose --profile production up -d
```

### Testing Commands
```sh
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_anomaly_detection.py
python -m pytest tests/test_anomaly_processor.py

# Run specific test class/method
python -m pytest tests/test_anomaly_detection.py::TestCalculateStats::test_calculate_stats_basic

# Run with coverage
pytest --cov=. --cov-report=html
```

### Code Quality Commands
```sh
# Critical linting issues only
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Full linting with complexity checks (max complexity: 10, max line length: 127)
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Lint specific files after refactoring
flake8 anomaly_detection.py anomaly_processor.py ui_elements.py app5.py --max-line-length=127
```

### Environment Setup
```sh
# Python venv (recommended)
python -m venv anomalizer-env
source anomalizer-env/bin/activate  # Linux/macOS
# or anomalizer-env\Scripts\activate  # Windows
pip install -r requirements.txt

# Conda alternative
conda create --name anomalizer-env python=3.9
conda activate anomalizer-env
pip install -r requirements.txt

# Quick start scripts
./run.sh venv          # Linux/macOS
run.bat venv           # Windows
```

## High-Level Architecture

### Version 2.0 Refactored Structure
The application was completely refactored from a monolithic structure to modular components:

#### Core Application Modules
- **app5.py**: Main Streamlit entry point, now modularized into focused functions:
  - `load_data()` - Excel file processing
  - `select_columns()` - UI for column selection
  - `create_visualization()` - Plotly chart generation
  - `process_anomalies()` - Main anomaly detection workflow
- **anomaly_detection.py**: Core IQR algorithm with enhanced error handling for empty data and edge cases
- **anomaly_processor.py**: Batch processing for analyzing all numeric columns simultaneously
- **ui_elements.py**: Reusable Streamlit UI components with version 2.0 branding
- **version.py**: Version management system with centralized metadata

#### Key Architectural Improvements (v2.0)
- **Functional Decomposition**: Large complex functions broken into single-purpose functions
- **Error Handling**: Comprehensive handling of empty DataFrames, NaN values, and edge cases
- **Type Safety**: Full type annotations added across all modules
- **Separation of Concerns**: Clear boundaries between UI, business logic, and data processing

### Data Flow Architecture
1. **File Upload** → `load_data()` processes Excel files with engine detection
2. **Column Analysis** → Automatic categorization of date/numeric/categorical columns
3. **User Configuration** → Interactive selection of analysis parameters via `select_columns()` and `select_categories()`
4. **Statistical Calculation** → `calculate_stats()` computes Q1, Q3, IQR for threshold determination
5. **Anomaly Detection** → `detect_anomalies()` applies IQR method with optional grouping
6. **Visualization** → `create_visualization()` generates interactive Plotly charts with anomaly highlighting
7. **Export** → Results downloadable as Excel with conditional formatting

### IQR Algorithm Implementation
- **Default Thresholds**: Q1 - 1.5×IQR (lower), Q3 + 1.5×IQR (upper)
- **Grouping Support**: Independent analysis per categorical group using pandas groupby
- **Edge Case Handling**: Graceful handling of single values, identical values, and empty datasets
- **Performance**: Optimized for datasets up to 100K rows with chunking recommendations for larger files

### Testing Architecture
- **test_anomaly_detection.py**: 14 comprehensive tests covering core algorithm, edge cases, and error conditions
- **test_anomaly_processor.py**: 9 tests for batch processing functionality including Excel I/O and temporary file handling
- **Test Categories**: 
  - Core functionality (basic algorithm correctness)
  - Edge cases (empty data, single values, NaN handling)
  - Grouping scenarios (categorical data analysis)
  - File processing (Excel operations, Windows file handle management)

### Deployment Architecture
- **Development**: Local Streamlit server on port 8501
- **Docker Development**: Containerized app on port 8505
- **Docker Production**: nginx reverse proxy on port 80 with WebSocket support for Streamlit
- **Multi-platform**: Native support for Windows, Linux, macOS with automated setup scripts

### Version Management
The application uses a centralized version system:
- **VERSION file**: Contains current version number
- **version.py**: Provides `__version__` and `VERSION_INFO` with feature list
- **UI Integration**: Version displayed in page title and sidebar with feature descriptions

## Key Implementation Notes

### File Handling Patterns
- Excel files processed via BytesIO to handle Streamlit uploads
- Engine auto-detection: 'openpyxl' for .xlsx, 'xlrd' for legacy .xls
- Temporary file cleanup required for Windows compatibility in tests

### Error Handling Strategy
- Empty DataFrame validation before processing
- NaN value tolerance in statistical calculations
- Graceful degradation for unsupported data types
- User-friendly error messages for common issues

### Performance Considerations
- Recommended data size limits: <100K rows for optimal performance
- Memory usage scales with dataset size and number of groups
- Docker containers allocated appropriate resources for typical workloads