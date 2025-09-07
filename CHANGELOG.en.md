# 📋 Changelog

**[🇺🇸 English](CHANGELOG.en.md) | [🇷🇺 Русский](CHANGELOG.md)**

All notable changes to the Anomalizer project are documented in this file.

---

## [2.0.0] - 2024-01-XX

### 🆕 Added
- **Full support for all operating systems** (Windows, Linux, macOS)
- **Docker deployment** with docker-compose.yml and nginx configuration
- **Automated launch scripts** (run.bat, run.sh)
- **Extended test coverage** (23 tests vs 2 in v1.0)
- **Version management module** (version.py)
- **Documentation system** with complete installation guides
- **Support for venv, conda, Docker** deployment methods
- **Interactive information panel** in sidebar
- **Docker Compose profiles** for development and production

### 🔧 Changed
- **Complete code architecture refactoring**
  - Split app5.py into functional modules
  - Improved readability and maintainability
  - Reduced function complexity (cyclomatic complexity < 10)
- **Enhanced error handling**
  - Empty data validation
  - Proper edge case handling
  - NaN value processing
- **Optimized visualization**
  - Improved grouped data display
  - Clearer charts and labels
  - Responsive interface
- **Updated user interface**
  - Added v2.0 version display
  - Informative sidebar
  - Enhanced instructions

### 🛠️ Fixed
- **All PEP 8 linting issues**
  - Fixed trailing whitespaces
  - Resolved long lines
  - Added missing newlines
- **Import issues**
  - Removed unused imports
  - Organized imports per PEP 8
- **Type annotation issues**
  - Added type hints to all functions
  - Improved IDE compatibility

### 📝 Documentation
- **Complete README.md rewrite**
  - Added Linux, macOS, Windows instructions
  - Detailed Docker instructions
  - Troubleshooting section
  - System requirements
- **New documentation files**
  - QUICK_START.md for quick start
  - REFACTORING_SUMMARY.md with refactoring details
  - CLAUDE.md for developers
- **Improved code comments**
  - Docstrings for all functions
  - Detailed parameter descriptions

### 🧪 Testing
- **Expanded from 2 to 23 tests**
- **Added new test modules**
  - test_anomaly_processor.py for batch processing
  - Edge case tests
  - Data grouping tests
- **Improved code coverage**
  - Tests for all core functions
  - Empty data handling tests
  - NaN value processing tests

### ⚡ Performance
- **Optimized anomaly detection algorithms**
- **Improved large file handling**
- **Optimized Docker images** with .dockerignore

### 🔒 Security
- **Updated all dependencies** to latest versions
- **Improved file handling** in temporary directories
- **Added input data validation**

---

## [1.0.0] - 2024-01-XX

### ✨ First Release
- Basic anomaly detection functionality using IQR method
- Simple Streamlit interface
- Excel file upload support
- Plotly visualization
- Excel results export
- Data grouping by categories
- Time series analysis

---

## 📋 Types of Changes

- **🆕 Added** - new features
- **🔧 Changed** - changes in existing functionality
- **⚠️ Deprecated** - features that will be removed soon
- **❌ Removed** - removed features
- **🛠️ Fixed** - bug fixes
- **🔒 Security** - vulnerability fixes