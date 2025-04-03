
# Insider Career Page UI Test Automation

## 🔧 Tech Stack
- Python
- Selenium
- PyTest
- Allure Reporting
- InfluxDB + Grafana (metrics visualization)
- Jenkins CI/CD + Webhook Trigger via Ngrok

## 📦 Folder Structure
```
project/
├── pages/
├── tests/
├── utils/
├── requirements.txt
├── README.md
├── .gitignore
├── Jenkinsfile
├── database_controller.py
```

## 🚀 Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Run Tests
```bash
pytest tests/ --html=report.html --self-contained-html
```

## 📊 Run with Allure
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 🧪 CI/CD Pipeline - Jenkins + Ngrok
- Ngrok publicly exposes your Jenkins server for GitHub webhook integration.
- A new pipeline is triggered on every push.
- Each stage: checkout, venv install, dependency install, run tests, generate Allure report.

### Jenkinsfile Sample
```
stages:
  - Checkout
  - Install dependencies (venv + pip install)
  - Run tests with Allure
  - Post: save screenshots, generate reports
```

## 📈 InfluxDB + Grafana Integration
- `database_controller.py` writes each test result to InfluxDB.
- Data: test name, pass/fail, duration, timestamp.
- Grafana queries `test_results` database and visualizes:
  - ✅ Pass Rate
  - 📉 Test Duration Trend
  - 🔁 Frequently failing test cases

## 👨‍💻 Author
Ferit Tongemen
