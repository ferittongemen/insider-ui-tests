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
            sh 'find . -name "*.png" || true'

            script {
                def screenshotFiles = findFiles(glob: '**/screenshots/*.png')
                if (screenshotFiles.length > 0) {
                    echo "📁 Screenshot(s) found: Archiving..."
                    archiveArtifacts artifacts: '**/screenshots/*.png', fingerprint: true
                } else {
                    echo "✅ No screenshots found, skipping artifact step without marking unstable."
                }
            }
        }
    }
}