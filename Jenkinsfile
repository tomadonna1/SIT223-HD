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
    stages {
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
                sh '/opt/venv/bin/pytest'
            }
        }
        stage('Code Analysis') {
            steps {
                echo "Running code quality checks on lenet.py"
                sh '/opt/venv/bin/flake8 lenet.py --count --select=E9,F63,F7,F82 --show-source --statistics || true'
                sh '/opt/venv/bin/pylint lenet.py || true'

                echo "Running code quality checks on app.py"
                sh '/opt/venv/bin/flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics || true'
                sh '/opt/venv/bin/pylint app.py || true'
            }
        }
        stage('Security Scan') {
            steps {
                echo "Running Bandit scan on lenet.py"
                sh '/opt/venv/bin/bandit -r lenet.py || true'

                echo "Running Bandit scan on app.py"
                sh '/opt/venv/bin/bandit -r app.py || true'

                echo "Running pip-audit for dependency vulnerabilities"
                sh '/opt/venv/bin/pip-audit || true'
            }
        }
        stage('Deploy to Staging') {
            steps {
                echo "Creating Docker network for staging environment"
                sh 'docker network create digit-net || true'

                echo "Cleaning up old staging container"
                sh 'docker rm -f digit-api-staging || true'

                echo "Building the FastAPI Docker image"
                sh 'docker build -t digit-api:staging -f Dockerfile.app .'

                echo "Running the app container on digit-net with alias"
                sh '''
                    docker run -d \
                        --name digit-api-staging \
                        --network digit-net \
                        --network-alias digit-api-staging \
                        digit-api:staging
                '''

                echo "Verifying container is attached to digit-net"
                sh 'docker inspect digit-api-staging --format "{{json .NetworkSettings.Networks}}"'

                echo "Waiting for FastAPI app to be ready (via /health)"
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

                echo "Verifying /predict endpoint is functional"
                sh '''
                    # You must have a sample image available inside the container
                    docker cp test_images/label_0.png digit-api-staging:/app/label_0.png

                    curl_response=$(docker exec digit-api-staging curl -s -o /dev/null -w "%{http_code}" \
                        -X POST http://localhost:8000/predict \
                        -F "file=@/app/label_0.png")

                    if [ "$curl_response" -ne 200 ]; then
                        echo "/predict endpoint failed with status code $curl_response"
                        docker logs digit-api-staging
                        exit 1
                    fi

                    echo "/predict endpoint is working"
                '''

                echo "Checking container logs in case of startup failure"
                sh '''
                    sleep 3
                    if ! docker exec digit-api-staging curl -s http://localhost:8000/health | grep -q "ok"; then
                        echo "FastAPI app did not start properly. Dumping logs:"
                        docker logs digit-api-staging
                        exit 1
                    fi
                '''
            }
        }
        stage('Release to Production') {
            steps {
                echo "Promoting app to production environment"

                echo "Cleaning up old production container (if any)"
                sh 'docker rm -f digit-api-production || true'

                echo "Tagging staging image as production"
                sh 'docker tag digit-api:staging digit-api:production'

                echo "Running production container on digit-net"
                sh '''
                    docker run -d \
                        --name digit-api-production \
                        --network digit-net \
                        --network-alias digit-api-production \
                        digit-api:production
                '''

                echo "Verifying production app is running"
                sh '''
                    for i in {1..10}; do
                        if docker exec digit-api-production curl -s http://localhost:8000/health | grep -q "ok"; then
                            echo "Production app is ready!"
                            break
                        fi
                        echo "Waiting for production app to start..."
                        sleep 2
                    done
                '''
            }
        }

        stage('Monitoring and Alerting'){
            steps {
                echo "Monitoring production /health endpoint"
                script {
                    def response = sh(script: "docker exec digit-api-production curl -s -o /dev/null -w \"%{http_code}\" http://localhost:8000/health", returnStdout: true).trim()
                    if (response != "200") {
                        echo "Production health check failed: HTTP $response"
                        mail to: 'tomdeptrai1@gmail.com',
                            subject: 'Production App Health Check Failed',
                            body: "The /health endpoint returned HTTP ${response}."
                        error("Production health check failed. Alert sent.")
                    } else {
                        echo "Production health check OK" 
                    }
                }
            }
        }
    }
}