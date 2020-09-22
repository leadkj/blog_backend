pipeline {
    agent any

    stages {
        stage('deploy blog_api service') {
            steps {
                sh "ansible aliyun -m shell -a 'sh /opt/deploy_cmd/blog_api.sh'"
            }
        }
    }
}