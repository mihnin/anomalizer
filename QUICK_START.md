# 🚀 Quick Start - Anomalizer v2.0

**[🇺🇸 English](QUICK_START.md) | [🇷🇺 Русский](QUICK_START.ru.md)**

## Fastest Way to Launch the Application

### 🐳 Docker (recommended)
```bash
# Clone repository
git clone https://github.com/yourusername/anomalizer.git
cd anomalizer

# Launch with one command
docker-compose up

# Open in browser: http://localhost:8505
```

### 🐍 Python venv
```bash
# Windows
git clone https://github.com/yourusername/anomalizer.git
cd anomalizer
run.bat venv

# Linux/macOS  
git clone https://github.com/yourusername/anomalizer.git
cd anomalizer
./run.sh venv

# Open in browser: http://localhost:8501
```

---

## 📋 Supported Launch Commands

| Command | Windows | Linux/macOS | Description |
|---------|---------|-------------|-------------|
| **venv** | `run.bat venv` | `./run.sh venv` | Python virtual environment |
| **conda** | `run.bat conda` | `./run.sh conda` | Anaconda/Miniconda |
| **docker** | `run.bat docker` | `./run.sh docker` | Docker container |
| **docker-prod** | `run.bat docker-prod` | `./run.sh docker-prod` | Docker + nginx |

---

## 🎯 First Use

1. **Upload test data** from `files_datasets/` folder
2. **Open application** at the address shown in console
3. **Drag and drop Excel file** into upload area
4. **Select columns** for analysis
5. **Click "Detect Anomalies"**
6. **Explore results** on interactive charts

---

## 🔧 Troubleshooting

### Port Issues
```bash
# If port is busy, use another one
streamlit run app5.py --server.port 8502
docker run -p 8507:8505 anomalizer:2.0
```

### Docker Issues
```bash
# Check Docker
docker --version
docker-compose --version

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Python Issues
```bash
# Check Python
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📊 Test Data

Available in `files_datasets/` folder:
- **dataset1.xlsx** - sensor data (2900+ records)
- **dataset2.xlsx** - categorical data

---

## 🆘 Get Help

- 📖 **Full documentation**: [README.md](README.md)
- 🐛 **Report bug**: [GitHub Issues](https://github.com/yourusername/anomalizer/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/anomalizer/discussions)

---

*Anomalizer v2.0 - Smart anomaly detection for your data* 📊