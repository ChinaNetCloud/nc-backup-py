pipeline {
    stages {
        stage('Setup on centos7') {
        agent { dockerfile {filename 'Dockerfile.centos7'} }
            steps {
                sh 'python --version'
                sh 'ls -l /etc/nc-backup-py'
                sh 'ls -l /var/lib/nc-backup-py'
                sh 'grep ncbackup /etc/passwd'
                sh 'cat /etc/sudoers.d/ncbackup'
            }
        }
        stage('Setup on centos6') {
        agent { dockerfile {filename 'Dockerfile.centos6'} }
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
