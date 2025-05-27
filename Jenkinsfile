pipeline {
      agent {
            docker{
                image 'tomadonna/sit223hd'
                args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
            }
        }
    triggers{
	    pollSCM '*/1 * * * *' // check git repo every 1 minute to see any changes, if changes made then run the jenkins
    }
    environment{
        DIRECTORY_PATH = 'https://github.com/tomadonna1/SIT223-HD.git'
        TESTING_ENVIRONMENT = 'testing environment'
        PRODUCTION_ENVIRONMENT = 'production environment'
    }
    options {
        skipStagesAfterUnstable()
    }  
    stages {
        stage('Docker Cleanup') {
            steps {
                echo "Cleaning Docker build cache to prevent snapshot errors"
                sh '''
                    docker builder prune -f
                '''
            }
        }
        stage('Build') {
            steps {
                echo "Fetch the source code from the directory path specified by the environment variable"
                echo "Fetching from: ${env.DIRECTORY_PATH}"
                echo "Some libraries has been pre-installed in Docker."
            }
        }
        stage('Unit and Integration Tests') {
            steps {
                echo "Running unit and integration tests with pytest"
                // sh '/opt/venv/bin/python unit_integration_tests/test_model.py'
                sh '/opt/venv/bin/pytest'
            }
        }
        stage('Code Analysis') {
            steps {
                echo "Running code quality checks on lenet.py"
                sh '/opt/venv/bin/flake8 lenet.py --count --select=E9,F63,F7,F82 --show-source --statistics || true'
                sh '/opt/venv/bin/pylint lenet.py || true'
            }
        }
        stage('Security Scan') {
            steps {
                echo "Running Bandit scan on lenet.py"
                sh '/opt/venv/bin/bandit -r lenet.py || true'

                echo "Running pip-audit for dependency vulnerabilities"
                sh '/opt/venv/bin/pip-audit || true'
            }
        }
        stage('Deploy to Staging') {
            steps {
                echo "🌐 Creating Docker network for staging environment"
                sh 'docker network create digit-net || true'

                echo "🧹 Cleaning up old staging container (if any)"
                sh 'docker rm -f digit-api-staging || true'

                echo "🐳 Building the FastAPI Docker image"
                sh 'docker build -t digit-api:staging -f Dockerfile.app .'

                echo "🚀 Running the app container on digit-net with alias"
                sh '''
                    docker run -d \
                        --name digit-api-staging \
                        --network digit-net \
                        --network-alias digit-api-staging \
                        digit-api:staging
                '''

                echo "🔍 Verifying container is attached to digit-net"
                sh 'docker inspect digit-api-staging --format "{{json .NetworkSettings.Networks}}"'

                echo "⏳ Waiting for FastAPI app to be ready (via /health)"
                sh '''
                    for i in {1..10}; do
                        if docker exec digit-api-staging curl -s http://localhost:8000/health | grep -q "ok"; then
                            echo "FastAPI app is ready!"
                            break
                        fi
                        echo "Waiting for FastAPI app to start..."
                        sleep 2
                    done
                '''
            }
        }
        stage('Integration Tests on Staging'){
            steps {
                echo "Running integration tests _inside_ app container"
                sh '''
                set -e
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install requests

                echo "🛠 Extracting IP of the running container"
                docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' digit-api-staging > app_ip.txt || true
                echo "📄 Contents of app_ip.txt:"
                cat app_ip.txt

                APP_IP=$(cat app_ip.txt | tr -d '[:space:]')
                echo "✅ APP_IP=${APP_IP}"

                if [ -z "$APP_IP" ]; then
                    echo "❌ Failed to extract IP address"
                    docker inspect digit-api-staging
                    exit 1
                fi

                echo "🌍 Running test with API_HOST=http://${APP_IP}:8000"
                env API_HOST="http://${APP_IP}:8000" venv/bin/python test_api.py 
                '''
            }
        }
        stage('Deploy to Production'){
            steps {
                echo "Move working version from staging to production"
                echo "Tool: Docker, AWS CLI, FastAPI"
            }
            // post {
            //     success{ echo "Post success "
            //             mail to: "tomdeptrai1@gmail.com",
            //                 subject: "Build Status Email",
            //                 body: "Build was successful!"
            //             }
            //     failure { echo "Post failed" } 
            // }
        }
    }
}