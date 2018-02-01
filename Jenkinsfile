pipeline {
    agent { dockerfile true }
    stages {
        stage('Setup') {
            steps {
                sh 'python --version'
                sh 'll /etc/nc-backup-py'
                sh 'll /var/lib/nc-backup-py'
                sh 'grep ncbackup /etc/passwd'
                sh 'cat /etc/sudoers.d/ncbackup'
            }
        }
    }
}
