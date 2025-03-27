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
                sh '. $VENV_DIR/bin/activate && PYTHONPATH=. pytest --alluredir=allure-results --capture=tee-sys'
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
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
        }
    }
}