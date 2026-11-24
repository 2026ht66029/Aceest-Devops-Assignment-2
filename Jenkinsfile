pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    parameters {
        string(name: 'DOCKERHUB_REPOSITORY', defaultValue: 'YOUR_DOCKERHUB_USER/aceest-fitness', description: 'Docker Hub repository, without a tag')
        booleanParam(name: 'PUSH_DOCKER_IMAGES', defaultValue: false, description: 'Push all version tags after Docker login is configured')
        booleanParam(name: 'RUN_SONARQUBE', defaultValue: false, description: 'Run SonarQube Scanner when the Jenkins server is configured')
        booleanParam(name: 'DEPLOY_KUBERNETES', defaultValue: false, description: 'Apply the selected Kubernetes manifest')
    }

    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONDONTWRITEBYTECODE = '1'
        DEPLOY_STRATEGY = 'rolling'
        DEPLOY_VERSION = '3.2.4'
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage('Prepare Environment') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install --requirement requirements-dev.txt
                    mkdir -p artifacts/versions
                '''
            }
        }

        stage('Build Every Supplied Version') {
            steps {
                script {
                    def entries = [
                        [version: '1.0.0', expected_failure: false],
                        [version: '1.1.0', expected_failure: false],
                        [version: '1.1.2', expected_failure: false],
                        [version: '2.0.1', expected_failure: false],
                        [version: '2.1.2', expected_failure: false],
                        [version: '2.2.1', expected_failure: false],
                        [version: '2.2.4', expected_failure: false],
                        [version: '3.0.1', expected_failure: true],
                        [version: '3.1.2', expected_failure: false],
                        [version: '3.2.4', expected_failure: false]
                    ]
                    for (def entry : entries) {
                        stage("Build ${entry.version}") {
                            sh ".venv/bin/python ci/build_version.py ${entry.version}"
                        }
                    }
                }
            }
        }

        stage('Validate Every Version') {
            steps {
                script {
                    def entries = [
                        [version: '1.0.0', expected_failure: false],
                        [version: '1.1.0', expected_failure: false],
                        [version: '1.1.2', expected_failure: false],
                        [version: '2.0.1', expected_failure: false],
                        [version: '2.1.2', expected_failure: false],
                        [version: '2.2.1', expected_failure: false],
                        [version: '2.2.4', expected_failure: false],
                        [version: '3.0.1', expected_failure: true],
                        [version: '3.1.2', expected_failure: false],
                        [version: '3.2.4', expected_failure: false]
                    ]
                    for (def entry : entries) {
                        stage("Validate ${entry.version}") {
                            if (entry.expected_failure == true) {
                                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                                    sh ".venv/bin/python ci/test_version.py ${entry.version}"
                                }
                                echo "Expected failure recorded for ${entry.version}; later versions continue."
                            } else {
                                sh ".venv/bin/python ci/test_version.py ${entry.version}"
                            }
                        }
                    }
                }
            }
        }

        stage('Pytest Unit Tests') {
            steps {
                sh '.venv/bin/pytest --junitxml=artifacts/pytest-results.xml --cov-report=xml:coverage.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'artifacts/pytest-results.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            when {
                expression { return params.RUN_SONARQUBE }
            }
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        docker run --rm --network host \
                          -e SONAR_HOST_URL=http://127.0.0.1:9000 \
                          -e SONAR_TOKEN="$SONAR_TOKEN" \
                          -v "$PWD:/usr/src" \
                          sonarsource/sonar-scanner-cli:latest
                    '''
                    echo 'SonarQube analysis completed; quality gate is verified on the SonarQube project page.'
                }
            }
        }

        stage('Build Docker Image For Every Version') {
            steps {
                script {
                    def entries = [
                        [version: '1.0.0', expected_failure: false],
                        [version: '1.1.0', expected_failure: false],
                        [version: '1.1.2', expected_failure: false],
                        [version: '2.0.1', expected_failure: false],
                        [version: '2.1.2', expected_failure: false],
                        [version: '2.2.1', expected_failure: false],
                        [version: '2.2.4', expected_failure: false],
                        [version: '3.0.1', expected_failure: true],
                        [version: '3.1.2', expected_failure: false],
                        [version: '3.2.4', expected_failure: false]
                    ]
                    for (def entry : entries) {
                        stage("Docker ${entry.version}") {
                            sh "docker build --build-arg APP_VERSION=${entry.version} --tag ${params.DOCKERHUB_REPOSITORY}:${entry.version} ."
                        }
                    }
                }
            }
        }

        stage('Push Docker Hub Tags') {
            when {
                expression { return params.PUSH_DOCKER_IMAGES }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USER" --password-stdin
                        while read -r version; do
                            docker push "${DOCKERHUB_REPOSITORY}:${version}"
                        done < <(python3 -c 'import json; print("\n".join(x["version"] for x in json.load(open("ci/version_manifest.json"))))')
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy To Kubernetes') {
            when {
                expression { return params.DEPLOY_KUBERNETES }
            }
            steps {
                sh './scripts/deploy.sh "$DEPLOY_STRATEGY" "$DEPLOY_VERSION" "$DOCKERHUB_REPOSITORY"'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**,coverage.xml', allowEmptyArchive: true
        }
        unstable {
            echo 'The intentional version regression was recorded. Review the Validate 3.0.1 stage.'
        }
        success {
            echo 'ACEest pipeline completed; all non-intentional stages passed.'
        }
    }
}
