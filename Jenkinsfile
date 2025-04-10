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
                sh '. $VENV_DIR/bin/activate && PYTHONWARNINGS=ignore pytest --alluredir=allure-results --capture=tee-sys -p no:warnings'            }
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