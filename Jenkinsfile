pipeline {
    agent none
    stages {
        stage('Setup on centos7') {
        agent { dockerfile {filename 'Dockerfile.centos7'} }
            steps {
                sh 'python --version'
                sh 'ls -l /etc/nc-backup-py'
                sh 'ls -l /var/lib/nc-backup-py'
                sh 'grep ncbackup /etc/passwd'
                sh 'sudo cat /etc/sudoers.d/ncbackup'
            }
        }
        stage('Setup on centos6') {
        agent { dockerfile {filename 'Dockerfile.centos6'} }
            steps {
                sh 'python --version'
                sh 'ls -l /etc/nc-backup-py'
                sh 'ls -l /var/lib/nc-backup-py'
                sh 'grep ncbackup /etc/passwd'
                sh 'sudo cat /etc/sudoers.d/ncbackup'
            }
        }
        stage('Setup on ubuntu14') {
        agent { dockerfile {filename 'Dockerfile.ubuntu14'} }
            steps {
                sh 'python --version'
                sh 'ls -l /etc/nc-backup-py'
                sh 'ls -l /var/lib/nc-backup-py'
                sh 'grep ncbackup /etc/passwd'
                sh 'sudo cat /etc/sudoers.d/ncbackup'
            }
        }
        stage('Setup on ubuntu16') {
        agent { dockerfile {filename 'Dockerfile.ubuntu16'} }
            steps {
                sh 'python --version'
                sh 'ls -l /etc/nc-backup-py'
                sh 'ls -l /var/lib/nc-backup-py'
                sh 'grep ncbackup /etc/passwd'
                sh 'sudo cat /etc/sudoers.d/ncbackup'
            }
        }
    }
}
