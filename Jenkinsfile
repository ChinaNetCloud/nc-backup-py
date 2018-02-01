node {
    checkout scm
    /*
     * In order to communicate with the MySQL server, this Pipeline explicitly
     * maps the port (`3306`) to a known port on the host machine.
     */
    docker.image('alpine:3.7').inside('--name nc-backup-py') { c ->
        sh 'whoami'
        sh 'su - root'
        /* Add aliyun mirrors and install git */
        sh 'sed "s|dl-cdn.alpinelinux.org|mirrors.aliyun.com|g" /etc/apk/repositories -i'
        sh 'apk add git python'
        /* Clone repo */
        sh 'git clone https://github.com/ChinaNetCloud/nc-backup-py.git'
        sh 'git checkout jenkins-setup'
        /* Run pip install.*/
        sh 'cd nc-backup-py'
        sh 'pip install --upgrade .'
        /* */
        sh ''
        /* */
        sh ''
    }
}
