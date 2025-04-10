# CI/CD & Test Monitoring Setup (Local Jenkins + InfluxDB + Grafana)

This document details the CI/CD pipeline and test monitoring system implemented in the project using Jenkins, GitHub Webhooks, InfluxDB, and Grafana.

---

## 🎥 Demo Videos

- [🔗 Jenkins +  Grafana + Ngrok + GitHub Webhook Trigger Demo PART 1](https://www.loom.com/share/573a7300434347f199c6f64bfc901b2e)
- [🔗 Jenkins +  Grafana + Ngrok + GitHub Webhook Trigger Demo PART 2](https://www.loom.com/share/91729b61720a4a1188a8aa0caa289771)

---

## 🧰 Tools Used

- Jenkins (locally installed) for CI/CD automation  
- Ngrok to expose local Jenkins instance to the internet  
- GitHub Webhooks to trigger Jenkins jobs  
- InfluxDB (locally installed) to store test results  
- Grafana to visualize test metrics from InfluxDB  
- Pytest for automated UI testing  

---

## 🔧 Installation & Setup Guide

### 📂 InfluxDB Installation (macOS with Homebrew)

```bash
brew update
brew install influxdb@1
```

Start InfluxDB service:

```bash
influxd
```

Create the database:

```bash
influx
CREATE DATABASE test_results;
```

---

### 📂 Grafana Installation (macOS with Homebrew)

```bash
brew install grafana
brew services start grafana
```

Access Grafana at: [http://localhost:3000](http://localhost:3000)

Default credentials:
- Username: `admin`
- Password: `admin` (will prompt to change on first login)

---

### 🔗 Connect Grafana to InfluxDB

1. Go to `Configuration > Data Sources`
2. Click **Add data source**
3. Select **InfluxDB**
4. Configure:
   - URL: `http://localhost:8086`
   - Database: `test_results`
   - HTTP Method: `GET`
5. Click **Save & Test**

---

## 🌐 Ngrok Setup

Install (if not already installed):

```bash
brew install --cask ngrok
```

Run Ngrok tunnel for Jenkins:

```bash
ngrok http 8080
```

Copy the HTTPS forwarding URL and add it to GitHub Webhooks.

---

## 🛠️ Jenkins Setup

### Jenkins Installation & Pipeline Configuration

Jenkins is installed and runs locally on `localhost:8080`.

A Pipeline job is created and configured with the following Jenkinsfile:

```groovy
pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
                sh '. $VENV_DIR/bin/activate && pip install --upgrade pip'
                sh '. $VENV_DIR/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. $VENV_DIR/bin/activate && PYTHONWARNINGS=ignore pytest --alluredir=allure-results --capture=tee-sys -p no:warnings'
            }
        }
    }

    post {
        always {
            echo "🔍 Searching for screenshots to archive..."
            script {
                def screenshotExists = sh(script: "find . -name '*.png' | grep -q .", returnStatus: true) == 0
                if (screenshotExists) {
                    echo "📸 Screenshots found, archiving..."
                    archiveArtifacts artifacts: '**/screenshots/*.png', fingerprint: true
                } else {
                    echo "✅ No screenshots found. Skipping archive."
                }
            }

            echo "🧾 Generating Allure report..."
            script {
                try {
                    allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
                } catch (Exception e) {
                    echo "❌ Allure report generation failed: ${e.message}"
                }
            }

            echo "📦 Final Result: ${currentBuild.result}"
        }
    }
}
```

---

## 🔁 GitHub Webhook Integration

Ngrok is used to tunnel Jenkins from localhost:

```bash
ngrok http 8080
```

The generated HTTPS endpoint is used in GitHub Webhook settings:

- **Payload URL**: `https://<ngrok_subdomain>.ngrok.io/github-webhook/`
- **Content type**: `application/json`
- **Events**: Push

---

## 🧪 Test Metrics & InfluxDB

### Test Result Logger (`database_controller.py`)

```python
from influxdb import InfluxDBClient

def insert_test_result_to_influxdb(test_name, status, duration, timestamp):
    try:
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('test_results')

        json_body = [
            {
                "measurement": "ui_test_results",
                "tags": {
                    "test_name": test_name,
                    "status": status,
                },
                "time": timestamp.isoformat(),
                "fields": {
                    "duration": float(duration)
                }
            }
        ]

        client.write_points(json_body)
        client.close()
        print(f"✅ InfluxDB'ye veri yazıldı: {test_name} | {status} | {duration:.2f}s")

    except Exception as e:
        print(f"❌ InfluxDB yazım hatası: {e}")
```

---

## 📈 Grafana Setup

### Grafana Configuration

- InfluxDB is added as a data source using:
  - Type: `influxdb`
  - UID: `feh34z1n6yo00b`
  - Database: `test_results`

### Custom Dashboard (Pie Chart Example)

**Query:**

```sql
SELECT count("duration") FROM "ui_test_results" WHERE $timeFilter GROUP BY "status"
```

**Panel includes color overrides:**
- `status = failed` → red  
- `status = passed` → green  

---

## ✅ CI/CD Flow Summary

1. Developer pushes code to GitHub  
2. GitHub webhook triggers Jenkins pipeline  
3. Jenkins installs dependencies, runs Pytest tests  
4. `database_controller.py` writes test metrics to InfluxDB  
5. Grafana dashboard reflects test results in real-time  

---

## 🗂️ Notes

- Jenkins, InfluxDB, and Grafana are all running locally (no Docker)  
- Ngrok must be kept active during webhook usage  
- Consider automating Ngrok startup via `systemd` or a startup script  
- All test statuses, durations, and timestamps are stored as time-series data  

---

> ✅ This setup provides full visibility into test performance and a seamless CI/CD feedback loop with no containerization overhead.