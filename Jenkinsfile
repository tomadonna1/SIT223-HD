pipeline {
      agent {
            docker{
                image 'tomadonna/jenkins-cnn'
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
                echo "Check individual functions and interaction between model component"
                echo "E.g. Check model loading, inference logic, other functions"
                echo "Tool: pytest"
                sh '/opt/venv/bin/python test_model.py'
            }
        }
        stage('Code Analysis') {
            steps {
                echo "Check for code smells and style violations"
                echo "E.g. check for PEP8 compliance, unused imports, complexity"
                echo "Tool: pylint, flake8, black"
            }
        }
        stage('Security Scan') {
            steps {
                echo "Check for potential Python dependency vulnerabilities"
                echo "E.g. scan for insecure packages"
                echo "Tool: safety, bandit, pip-audit"
            }
        }
        stage('Deploy to Staging') {
            steps {
                echo "Deploy trained model and client script to a staging environment like Docker or EC2"
                echo "E.g. Simulate model serving in a test environment"
                echo "Tool: Docker, scp, Ansible"
                // sleep 10
            }
        }
        stage('Integration Tests on Staging'){
            steps {
                echo "Validate dependencies in the staging container and the inference works correctly."
                echo "E.g. Send input to check for correct predictions"
                echo "Tool: Custom test scripts for pytest, Postman, REST API"
            }
        }
        stage('Deploy to Production'){
            steps {
                echo "Move working version from staging to production"
                echo "Tool: Docker, AWS CLI, FastAPI"
            }
            post {
                success{ echo "Post success "
                        mail to: "tomdeptrai1@gmail.com",
                            subject: "Build Status Email",
                            body: "Build was successful!"
                        }
                failure { echo "Post failed" } 
            }
        }
    }
}