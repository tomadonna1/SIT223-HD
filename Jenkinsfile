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
                echo "Create Docker network for app + test communication"
                sh 'docker network create digit-net || true'

                echo "Build FastAPI image"
                sh 'docker build -t digit-api:staging -f Dockerfile.app .'

                echo "Remove existing container"
                sh 'docker rm -f digit-api-staging || true'

                echo "Run container on network digit-net"
                sh 'docker run -d --name digit-api-staging --network digit-net digit-api:staging'

                echo "List running containers"
                sh 'docker ps'
            }
        }
        stage('Integration Tests on Staging'){
            steps {
                echo "Run test_api.py inside isolated Python container on digit-net"
                sh '''
                    docker run --rm \
                        --network digit-net \
                        -v $PWD:/app \
                        -w /app \
                        python:3.10 \
                        sh -c "pip install requests && python test_api.py"
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