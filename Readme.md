# CORD-19 Data Explorer - README

## Quick Start Guide

A complete Python data science project analyzing COVID-19 research papers from the CORD-19 dataset. Includes data analysis, visualization, and an interactive Streamlit web application.

---

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- ~2GB disk space for dataset

---

## 🚀 Installation & Setup

### 1. Clone or Create Project Directory

```bash
git clone https://github.com/GIDEON-INIOLUWA-AYANWALE/Frameworks_Assignment.git
cd Frameworks_Assignment
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pandas matplotlib seaborn streamlit numpy
```

### 4. Download Dataset

1. Go to [Kaggle CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)
2. Sign up/login to Kaggle
3. Download `metadata.csv` (can be 2GB+)
4. Place `metadata.csv` in the project root directory

---

## 📊 Running the Project

### Step 1: Run Data Analysis Script

```bash
python analysis.py
```

**This will:**
- Load metadata.csv
- Perform data exploration and cleaning
- Generate visualizations
- Create cleaned dataset (cord19_cleaned.csv)
- Save analysis chart (cord19_analysis.png)

**Expected Output:**
- Console output showing data statistics
- 4-panel visualization saved as PNG
- Cleaned CSV file for Streamlit app

### Step 2: Launch Streamlit Application

```bash
streamlit run app.py
```

**This will:**
- Start a local web server
- Open browser to http://localhost:8501
- Display interactive dashboard

**To stop:** Press `Ctrl+C` in terminal

---

## 📁 Project Structure

```
Frameworks_Assignment/
├── analysis.py              # Data analysis script
├── app.py                   # Streamlit web app
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── REPORT.md               # Detailed documentation
│
├── metadata.csv            # Dataset (download from Kaggle)
├── cord19_cleaned.csv      # Cleaned data (generated)
├── cord19_analysis.png     # Analysis charts (generated)
│
└── .gitignore             # Git ignore file
```

---

## 🎯 Features

### Analysis Script (analysis.py)

✓ **Data Loading & Exploration**
- Load large CSV files efficiently
- Display dataset dimensions and types
- Identify missing values

✓ **Data Cleaning**
- Convert date formats
- Extract year information
- Create new features
- Handle missing data

✓ **Analysis & Visualization**
- Publications over time
- Top journals analysis
- Word frequency analysis
- Source distribution

### Streamlit App (app.py)

✓ **Interactive Dashboard**
- Key metrics display
- Multi-chart layout
- Publication trends
- Journal rankings

✓ **Detailed Analysis**
- Word frequency visualization
- Statistical summaries
- Year-wise breakdown

✓ **Data Exploration**
- Browse filtered data
- Search functionality
- Download CSV export
- Custom sorting

✓ **Interactive Filters**
- Year range slider
- Journal multi-select
- Dynamic data refresh

---

## 📈 Example Usage

### In Terminal

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run analysis
python analysis.py

# Launch app
streamlit run app.py
```

### In Browser

1. Navigate to http://localhost:8501
2. Use sidebar to filter data:
   - Adjust year range
   - Select journals of interest
3. Explore three pages:
   - Dashboard with visualizations
   - Detailed analysis with statistics
   - Data sample with search

---

## 🔧 Configuration

### Memory Management

For very large datasets, modify analysis.py:

```python
# Process in chunks
chunk_size = 50000
for chunk in pd.read_csv('metadata.csv', chunksize=chunk_size):
    # Process chunk
    pass
```

### Streamlit Config

Create `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#2E86AB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"

[server]
maxUploadSize = 200
```

---

## 📊 Data Description

**metadata.csv Columns:**
- `cord_uid`: Unique identifier
- `title`: Paper title
- `authors`: Author list
- `abstract`: Paper abstract
- `publish_time`: Publication date
- `journal`: Journal name
- `source`: Publication source
- Additional metadata fields

---

## 🐛 Troubleshooting

### Issue: "No such file or directory: metadata.csv"
**Solution:** Download metadata.csv from Kaggle and place in project root

### Issue: "Module not found: pandas"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: Streamlit app not opening
**Solution:** 
- Ensure you're in the project directory
- Run: `streamlit run app.py --logger.level=debug`
- Check firewall settings

### Issue: Out of memory error
**Solution:** 
- Use a sample of the data (first 100k rows)
- Increase system RAM or use subset analysis
- Process in chunks

### Issue: Streamlit cached data not updating
**Solution:** Clear cache with `--logger.level=debug` flag or press `R` in app

---

## 📝 Assignment Checklist

- [x] Part 1: Data Loading & Exploration
- [x] Part 2: Data Cleaning & Preparation
- [x] Part 3: Analysis & Visualization
- [x] Part 4: Streamlit Application
- [x] Part 5: Documentation & Reflection
- [x] Code Comments & Documentation
- [x] GitHub Repository Setup
- [x] README Created

---

## 🎓 Learning Objectives Completed

✓ Practice loading real-world dataset
✓ Learn data cleaning techniques
✓ Create meaningful visualizations
✓ Build interactive web application
✓ Present data insights effectively
✓ Write clean, documented code
✓ Deploy with Streamlit

---

## 📚 Resources

**Documentation:**
- [Pandas Docs](https://pandas.pydata.org/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Matplotlib Guide](https://matplotlib.org/)

**Kaggle Dataset:**
- [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)

**Tutorials:**
- [Streamlit Tutorial](https://docs.streamlit.io/library/get-started)
- [Pandas Getting Started](https://pandas.pydata.org/getting_started.html)

---

## 📄 Files Included

**Source Code:**
- `analysis.py` - Main analysis script (Parts 1-3)
- `app.py` - Streamlit web application (Part 4)

**Documentation:**
- `README.md` - Quick start guide (this file)
- `REPORT.md` - Detailed project report
- `requirements.txt` - Python dependencies

**Output Files (Generated):**
- `cord19_cleaned.csv` - Cleaned dataset
- `cord19_analysis.png` - Visualization chart

---

## 🤝 Contributing

To improve this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## ✅ Verification Checklist

Run this to verify setup:

```bash
# Check Python version
python --version  # Should be 3.7+

# Check installed packages
pip list | grep -E "pandas|matplotlib|seaborn|streamlit"

# Check files exist
ls -la  # Should show analysis.py, app.py, requirements.txt

# Verify dataset
ls -la metadata.csv  # Should show file

# Test imports
python -c "import pandas, matplotlib, seaborn, streamlit; print('✓ All imports successful')"
```

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review REPORT.md for detailed documentation
3. Check Streamlit/Pandas official documentation
4. Open an issue on GitHub

---

## 📜 License

This project is part of a Python Frameworks educational assignment.

