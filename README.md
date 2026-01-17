# ✈️ DFW Flight Operations Intelligence System

Real-time flight tracking and analysis system for Dallas Fort Worth International Airport.

## 🎯 Overview

As an aviation enthusiast living near DFW, I built this to analyze flight patterns from one of the world's busiest airports. Combines my passion for aviation with data science.

## ✨ Features

- **Real-Time Data Collection** from aviation APIs
- **Domestic/International Separation** for targeted analysis
- **Interactive Web Dashboard** with Flask
- **Statistical Analysis** with Pandas
- **Data Visualizations** with Matplotlib
- **Scalable Architecture** - easy to add routes

## 🛠️ Technologies

- Python 3.12
- Flask (web framework)
- Pandas (data analysis)
- Matplotlib (visualization)
- AviationStack API

## 📊 Key Insights

- American Airlines dominates DFW (their HQ hub)
- DFW → LA is busiest domestic route
- Code-sharing creates interesting patterns
- Real-time tracking shows operational efficiency

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone repository:
```bash
git clone https://github.com/YOUR_USERNAME/dfw-flight-tracker.git
cd dfw-flight-tracker
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Get API key from [AviationStack](https://aviationstack.com)

5. Add your API key to the code

## 📖 Usage

### Collect Data
```bash
python flight_tracker.py
```

### View Analysis
```bash
python analyze.py
```

### Launch Dashboard
```bash
python app.py
```
Then visit: `http://127.0.0.1:5001`

## 📁 Structure
```
dfw-flight-tracker/
├── flight_tracker.py    # Data collection
├── analyze.py           # CLI analysis
├── app.py              # Web dashboard
├── data/               # CSV storage
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## 🎓 About

**Developer:** Hamza Sarfraz  
**School:** University of Texas at Dallas  
**Major:** Computer Science (Freshman)  
**Focus:** Data Science & Aviation Analytics

## 📝 License

MIT License - Open Source


Built with ❤️ and ✈️
