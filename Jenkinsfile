pipeline {
    agent any
    stages {
        stage('Prepare build environment') {
            steps {
                //bat 'pip install -r requirements.txt'
                bat 'pip install -e .'
            }
        }

        stage('Run unittests') {
            steps {
                bat 'python --version'
                bat 'pytest --version'
                bat 'pip install pytest'

                bat 'pytest --version'

                bat 'python -m pytest .\\unittests -v --junit-xml .\\unittests\\report.xml --cov=. --cov-report=html'
                junit '/**/*.xml'
            }
        }

        stage('Creer un tag git pour l application') {
            when {
                branch 'main'
            }
            steps {
                script {
                    bat 'echo "creating tag only in main branch"'
                    bat '.\\tag_version.bat'
                }
            }
        }

        stage('Creer une image docker') {
            steps {
                bat 'docker build -t revendeur_api -f ./deployment/Dockerfile .'
            }
        }

        stage('Pousser dans DockerHub') {
            steps {
                bat 'docker login -u boudjemaa -p dckr_pat_wHmvT6yCJa3xqn71GTHVr-nzers'
                bat 'docker tag revendeur_api boudjemaa/revendeur_api:latest'
                bat 'docker push boudjemaa/revendeur_api:latest'
            }
        }

    }
                post {
        success {
            office365ConnectorSend webhookUrl: 'https://ifagparis.webhook.office.com/webhookb2/4c2906f3-cff5-4826-8a2b-52ba2bae874d@b6e77e52-65f6-4dec-b7d9-8e45f36a536f/IncomingWebhook/8091df69c50c4271a62b0be991c079d8/872e452d-5988-4b28-949b-4ebf222982a6',
            message: 'Job Name : ' + "${env.JOB_NAME}" + ' | Build Number : ' + "${env.BUILD_NUMBER}",// + '/ lance par : ' + "${env.COMMIT_AUTHOR}" + '/ commit : ' + "${env.COMMIT_ID}" + '/ lien commit : ' + "${env.BUILD_URL/commit/${env.COMMIT_ID}}",
            status: 'Success',
            color: '#33cc33'
        }
        failure {
            office365ConnectorSend webhookUrl: 'https://ifagparis.webhook.office.com/webhookb2/4c2906f3-cff5-4826-8a2b-52ba2bae874d@b6e77e52-65f6-4dec-b7d9-8e45f36a536f/IncomingWebhook/8091df69c50c4271a62b0be991c079d8/872e452d-5988-4b28-949b-4ebf222982a6',
            message: 'Job Name : ' + "${env.JOB_NAME}" + ' | Build Number : ' + "${env.BUILD_NUMBER}",// + '/ lance par : ' + "${env.COMMIT_AUTHOR}" + '/ commit : ' + "${env.COMMIT_ID}" + '/ lien commit : ' + "${env.BUILD_URL/commit/${env.COMMIT_ID}}",
            status: 'Failure',
            color: '#ff3300'
        }
    }
}
