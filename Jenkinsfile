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
                echo "Creating Docker network for staging environment"
                sh 'docker network create digit-net || true'

                echo "Cleaning up old staging container (if any)"
                sh 'docker rm -f digit-api-staging || true'

                echo "Building the FastAPI Docker image"
                sh 'docker build -t digit-api:staging -f Dockerfile.app .'

                echo "Running the container on custom network digit-net"
                sh 'docker run -d --name digit-api-staging --network digit-net digit-api:staging'

                echo "Verifying container is attached to digit-net"
                sh 'docker inspect digit-api-staging --format "{{json .NetworkSettings.Networks}}"'

                echo "Waiting for FastAPI app to be ready"
                sh '''
                    for i in {1..30}; do
                    docker exec digit-api-staging curl -s http://localhost:8000/health && break
                    sleep 1
                    done
                '''
            }
        }
        stage('Integration Tests on Staging'){
            steps {
                echo "🧪 Creating test-client container on digit-net"
                sh '''
                    docker rm -f test-client || true
                    docker run -dit --name test-client --network digit-net -v $PWD:/app -w /app python:3.10 bash
                '''

                echo "Installing test dependencies inside test-client"
                sh 'docker exec test-client pip install requests'

                echo "Running test_api.py from test-client"
                sh 'docker exec test-client python test_api.py'

                echo "Cleaning up test-client"
                sh 'docker rm -f test-client'
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