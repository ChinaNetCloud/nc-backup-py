pipeline {
    agent { dockerfile {filename 'Dockerfile.centos7'} }
    stages {
        stage('Setup') {
            steps {
                sh 'python --version'
                sh 'ls -l /etc/nc-backup-py'
                sh 'ls -l /var/lib/nc-backup-py'
                sh 'grep ncbackup /etc/passwd'
                sh 'cat /etc/sudoers.d/ncbackup'
            }
        }
    }
}
