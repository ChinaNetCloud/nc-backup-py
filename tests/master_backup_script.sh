#!/bin/bash
###########################################
# Master Backup script
#
# Description: handle custom backup script
# Contact: vincent.viallet@gmail.com
# Version: 0.5b
###########################################
# Changes:
#   2009-02-07 VV       initial creation
#   2009-06-05 DL       Add Remote backup
#   2009-06-05 DL       Add config file
#   2009-06-15 VV       Corrections + reorganisation
#   2009-06-20 VV       Add checks + options + menu
#   2009-06-29 VV       Add version + test + misc + fifo files
#   2009-07-01 VV       Add logger
#       2009-08-24      VV      Remove compression of the final archive (done already by sub-scripts)
#       2010-01-21      VV      Use configuration file -- simple source
#                                       add SSH + S3 backup
#                                       enable / disable encryption
#   2010-06-28 DL       FIFO also for transfer file
#   2010-11-17 DL       Add split function for S3 backup, due to 4G limitation
#   2010-11-25 DL       Fix bug for cleaning up function for split S3 backup
#                       remove error log for /dev/cdrom ,when run lvm commander
#                       fix bug for md5sum when remote MD5 is empty
#   2012-06-20 AS       Compatible with CentOS6 + gnupg2
#   2012-06-21 AS       AliYun OSS support
#   2013-11-06 AS       Added a timestamp in the log
#   2014-08-07 BZ       Added LOCK_FILE to prevent more than one backup process running ; Change folder of pid file 
#   2015-07-30 CL       Added qiniu resoucre storage funcation 
#   2015-12-30 DX       Added local storage method for the customer who don't want remote backups
#                       Also changed default value of the variable STORAGE_METHOD to "local" if it's not defined in the conf file
#   2016-01-13 DX       Added Microsoft Azure storage
###########################################

# TODO
# add option to (re)configure the script:
#  - parse script folder
#  - list available backup scripts + display description + version
#  - save md5 of script files and store them in config file (ensure script integrity)
# this will allow:
#  - adding custom backup script to the list of jobs
#  - independent backup scripts for easier debugging
################################################
# Master script API for sub-scripts
#
# INPUT:
#  - $1 -- root destination backup folder
#  - $2 -- prefix
#  - $3 -- config file
#
# OUTPUT:
#  - 1 backup archive tar.gz -- Naming Format: PREFIX_XXXXX.tar.gz
#  - STDOUT -- to be appened to mail notice
#  - STDERR -- to be appened to error log for mail notice
################################################

# logger command for syslog
logger "Master Backup Script - started..."

version_num="0.5d"

#BINARIES
DATE="/bin/date"
SENDMAIL="/usr/sbin/sendmail"
SSH="/usr/bin/ssh"
SCP="/usr/bin/scp"
MD5="/usr/bin/md5sum"
GPG="/usr/bin/gpg"
S3CMD="/usr/bin/s3cmd"
GPGAGENT="/usr/bin/gpg-agent"
ALICMD="/usr/bin/alicmd"
QINIUCMD="/usr/bin/qiniucmd"
AZURECMD="/usr/bin/azure"
WGET="/usr/bin/wget"

#
## default work environement
## to be used ONLY when no config file is provided
set_default_work_env() {
  ###########################################
  # Define working environment
  HOSTNAME=`hostname`
  HOME_MASTER=
  BACKUP_FOLDER=

  ###########################################
  # ENCRYPT configuration section
  # define whether the encryption need to be turned ON
  ENABLE_ENCRYPT="YES"
  # Define Encrypt Key File and owner+permission
  KEY_FILE="$HOME_MASTER/key_file"
  KEY_PERMS='-r--------' #400
  KEY_OWNER=
  KEY_GROUP=

  ###########################################
  # Mail report
  MAIL_REPORT_ADDRESS=ncbackup_report@chinanetcloud.com

  ###########################################
  # Remote storage (SSH - S3)
  STORAGE_METHOD=SSH
  #
  # via SSH
  BACKUP_ID_RSA=
  BACKUP_SERVER=
  SSH_PORT=
  BACKUP_DIR=
  SSH_USER=
  #
  # via Amazon S3
  S3_BUCKET=
  S3_FOLDER=$HOSTNAME
  S3_CONFIG=
}

#
## use the work environment to build the other required
## variables that depend on the work env.
set_work_env() {
  ###########################################
  # Define working environment
  SCRIPT_FOLDER="$HOME_MASTER/scripts-enabled"
  PID_FOLDER="$HOME_MASTER/pid_$(date '+%Y%m%d_%H%M')"
  DATE_FORMATED=`$DATE "+%y%m%d_%H%M%S"`
  PREFIX_BACKUP="$DATE_FORMATED"_"$HOSTNAME"

  ###########################################
  # Define Log
  MASTER_OUTPUT_LOG="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_MASTER_SCRIPT.log
  MASTER_ERROR_LOG="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_MASTER_SCRIPT.error

  ###########################################
  # ENCRYPT configuration section
  # Define Encrypt Key File and owner+permission
  KEY_FILE="$HOME_MASTER/key_file"

  ###########################################
  # Define Check MD5 FILE
  MD5_CHECK_FILE=local_md5_"$DATE_FORMATED"

  ###########################################
  # Define Archive
  FULL_BACKUP_FILE="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_full.tar
  FULL_BACKUP_FILE_GPG="$FULL_BACKUP_FILE".gpg

  ###########################################
  # Define Mail
  MAIL_REPORT_FILE="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_mail_report.txt
}

#
## NOT IN USE -- TO REMOVE IF PROVEN USELESS

# use_config() {
#   # get value from config file
#   if [ -f "$CONF_FILE" ]
#   then
#     # Select Variable from config file
#     for i  in `grep = $CONF_FILE | grep -v ^#`
#     do
#     # Declare Variable from config file
#      declare ${i%\=*}=${i#*=}
#     done
#   fi
# }


###########################################
# environment check
#
# TODO
#  generic function to check for variable / folder
###########################################
#
## Check BINARIES
check_binary(){
  binary="$1"
  if [ ! -x $binary ]; then
        echo "$binary - is not executable -- review the configuration" >&2
        exit 2
  fi
}

#
## Check FOLDER
check_folder(){
  folder="$1"
  # Get the Value of Variable whose name is a Variable
  # e.g: AA=aaa; BB=AA; echo ${!BB} will display 'aaa'
  if [ -z "${!folder}" ]
  then
    echo "$folder: missing value - correct the script" >&2
    exit 2
  else
    # check if the folder exists
    if [ ! -d "${!folder}" ]; then
          # if not creates it
          mkdir -p "${!folder}"
          # if creation fails
      if [ $? -ne 0 ]; then
            echo "permission issue - have not write permission for $folder" >&2
            exit 2
          fi
        fi
  fi
}

#
## Check that the working environment is properly set
check_work_env () {
  check_binary $DATE
  check_binary $SENDMAIL
  check_binary $MD5

  check_folder HOME_MASTER
  check_folder SCRIPT_FOLDER
  check_folder PID_FOLDER
  check_folder BACKUP_FOLDER
}

#
## Prepare backup environment - clean old temp files, etc.
prepare_work_env () {
  # we insert the values from the config file specified
  if [ -f "$CONF_FILE" -a -r "$CONF_FILE" ]; then
    source "$CONF_FILE"
  elif [ -s "$CONF_FILE" -o ! -r "$CONF_FILE" -o ! -f "$CONF_FILE" -o -z "$CONF_FILE" ]; then
    echo "$CONF_FILE is invalid - check permissions / content / path" >&2
    exit 2
  else
    # no config file -- use default config
    set_default_work_env
  fi

  # create PATHS for work env
  set_work_env

  # Check work environment - check PATH + Binaries
  check_work_env

  # Remove any existing PID file
  #rm -f "$PID_FOLDER/*.pid"
  # Mick - 20140711
  rm -f $PID_FOLDER/*.pid

  # Define whether encryption need to be turned on (Default - enable)
  if [ "$ENABLE_ENCRYPT" == "NO" -o "$ENABLE_ENCRYPT" == "No" -o "$ENABLE_ENCRYPT" == "no"  ]; then
    echo "Encryption of the archive is DISABLED !"
    ENABLE_ENCRYPT="NO"
    FULL_BACKUP_ARCHIVE="$FULL_BACKUP_FILE"
  else
    ENABLE_ENCRYPT="YES"
    FULL_BACKUP_ARCHIVE="$FULL_BACKUP_FILE_GPG"
    check_binary $GPG
  fi

  # Define storage Method (Default - LOCAL)
  if [ "$STORAGE_METHOD" == "S3" ]; then
    echo "Selected storage method : Amazon S3"
    STORAGE_METHOD="S3"
    check_binary $S3CMD
  elif [ "$STORAGE_METHOD" == "OSS" ]; then
    echo "Selected storage method : AliYun OSS"
    STORAGE_METHOD="OSS"
    check_binary $ALICMD
  elif [ "$STORAGE_METHOD" == "QINIU" ]; then
    echo "Selected storage method : QiNiu Storage"
    STORAGE_METHOD="QINIU"
    check_binary $QINIUCMD
  elif [ "$STORAGE_METHOD" == "AZURE" ]; then
    echo "Selected storage method : AZURE Storage"
    STORAGE_METHOD="AZURE"
    check_binary $AZURECMD
  elif [ "$STORAGE_METHOD" == "SSH" ]; then
    echo "Selected storage method : SSH"
    STORAGE_METHOD="SSH"
    check_binary $SSH
    check_binary $SCP
  else
    echo "Selected storage method : LOCAL"
    STORAGE_METHOD="LOCAL"
  fi
}

##########################################
# find scripts
# WARNING the security check of the scripts is not in use yet
##########################################
#
## NOT IN USE YET
## list scripts selected to run from the config file
list_selected_scripts () {
  list_scripts=""
  cd "$SCRIPT_FOLDER"
  for script in `ls`
  do
    if [ $(is_script_selected "$script") -eq 1 ]; then
      list_scripts="$list_scripts $SCRIPT_FOLDER/$script"
    fi
  done
}

#
## NOT IN USE YET
## Check if the script is selected in the config file
## Check for the script integrity - to avoid external modification
is_script_selected () {
  script="$1"
  # should be present in the configuration file, with the good md5sum
  script_md5= $(grep "$script" "$CONF_FILE" | cut -f2 -d'=')
  if [ $(md5sum "$script") == "$script_md5" ]; then
    # success
    exit 1
  fi
  exit 2
}

#
## NOT IN USE YET
## Write in the config file
## list available scripts
## prompt for including the script in the job list
## add md5 in the config file
set_selected_scripts () {
  echo selected_script
}

#
## List available scripts in SCRIPT_FOLDER
get_list_jobs () {
  list_scripts=""
  # -A do not list . and ..
  # 20141028 -A removed by Shaun Smith, to avoid .svn directory (all . dirs)
  for script in `ls "$SCRIPT_FOLDER"`
  do
    if [ -z "$list_scripts" ]; then
      list_scripts="$SCRIPT_FOLDER/$script"
    else
      list_scripts="$list_scripts $SCRIPT_FOLDER/$script"
    fi
  done

  #
  ## check if there is actually scripts to be ran
  if [ -z "$list_scripts" ]; then
    echo "No scripts available" >&2
    exit 2
  fi

  #
  ## return the script list
  echo "$list_scripts"

}

##########################################
# validate script file
##########################################
#
## validate if the script is runnable
validate_script () {
  job="$1"

  #
  ## Check if the script file exist
  if [ ! -f "$job" ]; then
    echo "$job does not exist - correct the script" >&2
    exit 2

  #
  ## Check if the script file is executable
  elif [ ! -x "$job" ]; then
    echo "$job is not executable - check permissions" >&2
    exit 2
  fi
}


#########################################
# run backup scripts
#########################################
# $1: script full path
run_script_bg () {
  job="$1"

  SCRIPT_OUTPUT_LOG="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_"`basename $job`".log
  SCRIPT_ERROR_LOG="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_"`basename $job`".error

  #
  ## execute script in background
  ##  - store STDOUT to .log
  ##  - store STDERR to .error
  "$job" "$BACKUP_FOLDER" "$PREFIX_BACKUP" "$CONF_FILE" > "$SCRIPT_OUTPUT_LOG" 2> "$SCRIPT_ERROR_LOG" &

  #
  ## store background script PID in the PID folder
  echo $! > "$PID_FOLDER"/`basename $job`.pid
  echo "`basename $job` backup script launched in background"
  logger "Master Backup Script - `basename $job` backup script launched in background"
}

#########################################
# wait for scripts to complete
#
# TODO
#  add a timeout to avoid the master script to run
#  forever if a sub script is stuck
#########################################
wait_job_bg () {
  #
  ## list PID files of currently running scripts
  for pids in `ls "$PID_FOLDER"/*.pid`
  do
    pids=`basename $pids`

    #
    ## retrieve PID value of the current file
    pid=`cat "$PID_FOLDER"/"$pids"`

    #
    ## while the PID is still present in /proc we wait
    ## the /proc/pid folder will be removed once the background script is complete
    while [ -d /proc/$pid ]
    do
      echo "Jobs not completed yet: `$DATE "+%y%m%d_%H%M%S"`"
      sleep 10
    done

    # remove PID file when backup process stuck , to help investigate in the future
    rm -rf "$PID_FOLDER"/"$pids"

  done
}

#########################################
# ENCRYPTION SECTION
#########################################
# Manage encryption
#########################################
# Define encryption
# encrypt key file
# check for proper security

initial_pgp_key_creation () {
  echo "Creating passphrase..."
  if [ -f "$KEY_FILE" ]; then
    mv "$KEY_FILE" "$KEY_FILE".old
    echo "existing passphrase file renamed to:"
    echo "  $KEY_FILE.old"; echo
    logger "Master Backup Script - WARNING - Old PGP passphrase backup-ed"
  fi
  cat /var/log/* 2> /dev/null | md5sum | awk {'print $1'} > "$KEY_FILE"
  chmod 400 "$KEY_FILE"
  echo "Passphrase created."
  logger "Master Backup Script - WARNING - New PGP passphrase generated"
}

#
# check key file
check_key_file () {
  # should check on saved md5 of the key file in config file
  # in case of change send an email of alerts about key change
  #
  # check for permissions and security + alert

  #
  ## Check for existing key file (contains passphrase)
  if [ ! -f "$KEY_FILE" ]; then
    initial_pgp_key_creation
  fi

  #
  ## Get key file permissions: "-r-------- root root" (or differently chosen)
  key_file_perms=$(ls -la "$KEY_FILE" | awk {'print $1" "$3" "$4'})
  if [ x"$key_file_perms" != x"$KEY_PERMS $KEY_OWNER $KEY_GROUP" ]; then
    echo "Security breach ! ensure proper passphrase security !" >&2
    exit 2
  fi

  ## Check if the size of $KEY_FILE is correct
  LENGTH=`cat $KEY_FILE`
  if [ ${#LENGTH} -ne 32 ]; then
    echo "Key File is not correct size!" >&2
    exit 2
  fi
}

#
# encrypt file
encrypt () {
  FILE="$1"
  FILE_GPG="$2"

  #
  ## check if the parameters exist
  if [ -z "$FILE" ]; then
    echo "encrypt> missing source file" >&2
    exit 2
  fi
  if [ -z "$FILE_GPG" ]; then
    echo "encrypt> missing destination file" >&2
    exit 2
  fi

  #
  ## check for existing and secure key_file
  ## exit if not correct
  check_key_file
  if [ $? -ne 0 ]; then exit 2 ; fi

  # we don't want to store several times the archives on the disk -- size consuming
  if [ "$STORAGE_METHOD" != "S3" -a "$STORAGE_METHOD" != "OSS"  -a "$STORAGE_METHOD" != "QINIU" -a "$STORAGE_METHOD" != "AZURE" ]; then #DL#
    mkfifo "$FILE_GPG" #DL#
  fi #DL#

  # echo "Encrypting $FILE into FIFO file..."
  echo "Encrypting $FILE file..."
  # we cat both the key file and the file to be encrypted -- only the 1st line is
  # considered as the passphrase by --passphrase-fd 0
  if [ "$STORAGE_METHOD" == "S3" -o "$STORAGE_METHOD" == "OSS" -o "$STORAGE_METHOD" == "QINIU" -o "$STORAGE_METHOD" == "AZURE" ]; then #DL#
    if grep '6.' /etc/redhat-release &>/dev/null; then
        cat "$KEY_FILE" "$FILE" | $GPGAGENT --daemon gpg2 --batch --yes --no-tty --quiet -c --passphrase-fd 0 | split  -d -b 4000m - "$FILE_GPG". #DL-NEW1#
    elif grep 'AMI' /etc/issue &>/dev/null; then
        cat "$KEY_FILE" "$FILE" | $GPGAGENT --daemon gpg2 --batch --yes --no-tty --quiet -c --passphrase-fd 0 | split  -d -b 4000m - "$FILE_GPG". #DL-NEW1#
    else
        cat "$KEY_FILE" "$FILE" | gpg --no-tty --quiet -c --passphrase-fd 0 | split  -d -b 4000m - "$FILE_GPG". #DL-NEW1#
    fi
  else #DL#
    if grep '6.' /etc/redhat-release &>/dev/null; then
        cat "$KEY_FILE" "$FILE" | $GPGAGENT --daemon gpg2 --batch --yes --no-tty --quiet -c --passphrase-fd 0  | tee "$FILE_GPG" | md5sum >"$BACKUP_FOLDER"/"$MD5_CHECK_FILE" & #DL#
    elif grep 'AMI' /etc/issue &>/dev/null; then
        cat "$KEY_FILE" "$FILE" | $GPGAGENT --daemon gpg2 --batch --yes --no-tty --quiet -c --passphrase-fd 0  | tee "$FILE_GPG" | md5sum >"$BACKUP_FOLDER"/"$MD5_CHECK_FILE" & #DX#
    else
        cat "$KEY_FILE" "$FILE" | gpg --no-tty --quiet  -c --passphrase-fd 0 | tee "$FILE_GPG" | md5sum >"$BACKUP_FOLDER"/"$MD5_CHECK_FILE" & #DL#
    fi
  fi #DL#
  echo "GPG file ready."; echo
}

#########################################
# create archive
#########################################
#
## concatenate all the sub-scripts archives into 1 single archive
create_archive () {
  FILE="$1"
  if [ -z "$FILE" ]; then
    echo "Missing destination backup file" >&2
    exit 2
  fi

  # depending whether we want to encrypt or not, we either :
  #   - use FIFO file -- the transfered file will be the GPG file, not the TAR file
  #   - use real file -- the transfered file will be the TAR file
  if [ "$STORAGE_METHOD" == "S3" -o "$STORAGE_METHOD" == "OSS" -o "$STORAGE_METHOD" == "QINIU" -o "$STORAGE_METHOD" == "AZURE" ]; then #DL#
    if [ "$ENABLE_ENCRYPT" == "YES" ]; then #DL#
      # we don't want to store several times the archives on the disk -- size consuming
      mkfifo "$FILE" #DL#
    fi #DL#
  else #DL#
    mkfifo "$FILE" #DL#
  fi #DL#

  cd "$BACKUP_FOLDER"

  #
  ## retrieve files created with the specified prefix
  file_list=$(find . -name "$PREFIX_BACKUP*tar.gz")

  #
  ## create archive
  if [ "$ENABLE_ENCRYPT" == "YES" ]; then
    echo "Taring sub-scripts archives into FIFO main archive..."

    if [ "$STORAGE_METHOD" == "S3" -o "$STORAGE_METHOD" == "OSS" -o "$STORAGE_METHOD" == "QINIU" -o "$STORAGE_METHOD" == "AZURE" ]; then #DL#
      tar cf "$FILE" $file_list & #DL#
    else #DL#
      tar c -O $file_list > "$FILE" & #DL#
    fi #DL#

    echo "Taring Ready in FIFO file."; echo
  elif [ "$ENABLE_ENCRYPT" == "NO" ]; then
    echo "Taring sub-scripts archives into main archive..."

    if [ "$STORAGE_METHOD" == "S3" -o "$STORAGE_METHOD" == "OSS" -o "$STORAGE_METHOD" == "QINIU" -o "$STORAGE_METHOD" == "AZURE" ]; then #DL#
#      tar cf "$FILE" $file_list #DL#
      tar cf - $file_list | split  -d -b 4000m - "$FILE".       #DL-NEW1#
    else #DL#
      tar c -O $file_list | tee "$FILE" | md5sum > "$BACKUP_FOLDER"/"$MD5_CHECK_FILE" & #DL#
    fi #DL#

    echo "Taring Complete."; echo
  fi

}

#########################################
# Email management
#########################################
prepare_email_header () {
  STATUS=0
  # check if the size of all error file in $BACKUP_FOLDER is empty
  for error_file in `ls "$BACKUP_FOLDER"/"$PREFIX_BACKUP"*.error`
  do
    [ -s "$error_file" ] && STATUS=1
  done

  # define the Subject according to the error file size
  [ "$STATUS" -ne 0 ] && BK_STATUS="FAILED" || BK_STATUS="-- OK"

  cat > "$MAIL_REPORT_FILE" << EOF
To: $MAIL_REPORT_ADDRESS
Subject: $BK_STATUS [$HOSTNAME] backup report - $date

EOF
}

prepare_email_subcontent () {
  list_jobs="$1"
  echo "######################################################"    >> "$MAIL_REPORT_FILE"
  echo "Backup Summary:"                                           >> "$MAIL_REPORT_FILE"
  echo "######################################################"    >> "$MAIL_REPORT_FILE"
  echo "-- Logs:"                                                  >> "$MAIL_REPORT_FILE"
  cat "$MASTER_OUTPUT_LOG"                                         >> "$MAIL_REPORT_FILE"
  echo
  if [ -s "$MASTER_ERROR_LOG" ]; then
    echo "-- Errors:"                                              >> "$MAIL_REPORT_FILE"
    cat "$MASTER_ERROR_LOG"                                        >> "$MAIL_REPORT_FILE"
    echo                                                           >> "$MAIL_REPORT_FILE"
  fi
  echo "######################################################"    >> "$MAIL_REPORT_FILE"
  echo                                                             >> "$MAIL_REPORT_FILE"
  echo "Below is the list of each individual backup job:"          >> "$MAIL_REPORT_FILE"

  for job in $list_jobs
  do
    SCRIPT_OUTPUT_LOG="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_"`basename $job`".log
    SCRIPT_ERROR_LOG="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_"`basename $job`".error

    echo "******************************************************"    >> "$MAIL_REPORT_FILE"
    echo "Job: $job"                                                 >> "$MAIL_REPORT_FILE"
    echo "******************************************************"    >> "$MAIL_REPORT_FILE"
    echo "-- Logs:"                                                  >> "$MAIL_REPORT_FILE"
    cat "$SCRIPT_OUTPUT_LOG"                                                                 >> "$MAIL_REPORT_FILE"
    echo                                                             >> "$MAIL_REPORT_FILE"
    #
    ## only display errors if there is error in the file
    ## do not pollute e-mail with it
    if [ -s "$SCRIPT_ERROR_LOG" ]; then
      echo "-- Errors:"                                              >> "$MAIL_REPORT_FILE"
      cat "$SCRIPT_ERROR_LOG"                                                                        >> "$MAIL_REPORT_FILE"
      echo                                                           >> "$MAIL_REPORT_FILE"
    fi
    echo "******************************************************"    >> "$MAIL_REPORT_FILE"
    echo                                                             >> "$MAIL_REPORT_FILE"
  done
}

send_email () {
  prepare_email_header
  prepare_email_subcontent "$list_jobs"
  cat "$MAIL_REPORT_FILE" | $SENDMAIL $MAIL_REPORT_ADDRESS
}

#########################################
# sending archive for remote storage
#  FULL_BACKUP_ARCHIVE (either tar.gz or gpg file)
#########################################
send_archive_ssh() {
  # set SSH command
  EXEC_REMOTE_SSH="$SSH -i $BACKUP_ID_RSA -p $SSH_PORT $SSH_USER@$BACKUP_SERVER"

  # create remote storage location via SSH
  $EXEC_REMOTE_SSH "mkdir -p $BACKUP_DIR/$HOSTNAME"

  # send archive to the backup server via SCP
  #$SCP -rp -i $BACKUP_ID_RSA -P $SSH_PORT "$FULL_BACKUP_ARCHIVE" $SSH_USER@$BACKUP_SERVER:$BACKUP_DIR/$HOSTNAME/
  cat "$FULL_BACKUP_ARCHIVE" | $EXEC_REMOTE_SSH "cat > $BACKUP_DIR/$HOSTNAME/$(basename $FULL_BACKUP_ARCHIVE)" #DL#

  # get archive MD5
  #MD5_ENC=`$MD5 "$FULL_BACKUP_ARCHIVE" | awk '{ print $1 }'`
  MD5_ENC="$(cat $BACKUP_FOLDER/$MD5_CHECK_FILE | awk '{ print $1 }' | sed 's/\ //g')" #DL#

  if [ $? == 0 ]; then
    # get remote MD5 of the transfered file
    REM_MD5=`$EXEC_REMOTE_SSH "md5sum $BACKUP_DIR/$HOSTNAME/$(basename $FULL_BACKUP_ARCHIVE)" | awk '{ print $1 }' | sed 's/\ //g'`
    if [ x"$MD5_ENC" != x"$REM_MD5" ]; then
      echo "TRANSFER FAILED -- remote MD5 differs from local MD5" >&2
      logger "Master Backup Script - WARNING - Remote transfer failed BAD MD5"
    else
      echo "TRANSFER OK -- remote and local MD5 are equal"
    fi
    # list files on the remote server
    echo "File detail on the remote server"
    $EXEC_REMOTE_SSH "ls -la $BACKUP_DIR/$HOSTNAME/$(basename $FULL_BACKUP_ARCHIVE)"

  else
    echo "TRANSFER FAILED -- the archive has not been sent out" >&2
    logger "Master Backup Script - ERROR - Remote transfer failed"
  fi
}

send_archive_s3() {
  # send to S3
  echo "Sending file to S3 - s3://$S3_BUCKET/$S3_FOLDER/"

  for file_piece in $(ls $FULL_BACKUP_FILE.*) #DL-NEW1#
  do
    $S3CMD -c $S3_CONFIG put $file_piece s3://$S3_BUCKET/$S3_FOLDER/
    if [ $? -eq 0 ]; then
      echo "$file_piece upload done !"
    else
      echo "$file_piece upload failed !" >&2
    fi

    # we only want the basename for comparison not the full path
    BACKUP_FILE=`basename $file_piece`

    MD5_ENC=`$MD5 "$file_piece" | awk '{ print $1 }'`
    REM_MD5=`$S3CMD -c $S3_CONFIG ls --list-md5 s3://$S3_BUCKET/$S3_FOLDER/$BACKUP_FILE | awk '{ print $4 }'`

    echo "local MD5 : $MD5_ENC"
    echo "remote MD5 : $REM_MD5"

    if [ x"$MD5_ENC" != x"$REM_MD5" ]; then
      echo "$file_piece MD5 are not correct ! Transfer ERROR" >&2
    else
      echo "$file_piece MD5 are equal locally and on S3, transfer OK"
    fi
  done
}







send_archive_s3_cn() {
  # send to S3
  echo "Sending file to S3 - s3://$S3_BUCKET/$S3_FOLDER/"

  for file_piece in $(ls $FULL_BACKUP_FILE.*) #DL-NEW1#
  do
   # $S3CMD -c $S3_CONFIG put $file_piece s3://$S3_BUCKET/$S3_FOLDER/
     $S3CMD s3 cp  $file_piece s3://$S3_BUCKET/$S3_FOLDER/
    if [ $? -eq 0 ]; then
      echo "$file_piece upload done !"
    else
      echo "$file_piece upload failed !" >&2
    fi

    # we only want the basename for comparison not the full path
    BACKUP_FILE=`basename $file_piece`

   # MD5_ENC=`$MD5 "$file_piece" | awk '{ print $1 }'`
   # REM_MD5=`$S3CMD -c $S3_CONFIG ls --list-md5 s3://$S3_BUCKET/$S3_FOLDER/$BACKUP_FILE | awk '{ print $4 }'`

   # echo "local MD5 : $MD5_ENC"
   # echo "remote MD5 : $REM_MD5"

   # if [ x"$MD5_ENC" != x"$REM_MD5" ]; then
   #   echo "$file_piece MD5 are not correct ! Transfer ERROR" >&2
   # else
   #   echo "$file_piece MD5 are equal locally and on S3, transfer OK"
   # fi
  done
}




send_archive_qiniu() {
  # send to Qiniu
  echo "Sending file to Qiniu ..."

  for file_piece in $(ls $FULL_BACKUP_ARCHIVE.*) #DL-NEW1#
  do
    file_name=$(basename $file_piece)
	# upload finished, return upload status
    $QINIUCMD -u $file_piece >/tmp/${file_name}.Status
    Transfer_Status=$(cat /tmp/${file_name}.Status)

    if [ ${Transfer_Status} == 0 ]; then
      echo "Upload Succeed, $file_piece Hash are equal, Transfer OK"
    elif [ ${Transfer_Status} == 1 ]; then
      echo "Upload Succeed, $file_piece Hash are not correct! Transfer ERROR"
    elif [ ${Transfer_Status} == -1 ]; then
      echo "$file_piece is not regular file, Transfer Termination"
    else
      echo "Upload Failed, $file_piece Hash are not correct! Transfer ERROR" >&2
    fi
    /bin/rm -f /tmp/$(basename $file_piece).Status
  done
}

send_archive_azure() {
  #send to AZURE
  echo "Sending file to AZURE ..."

  # export azure env variables before upload files
  if [ -s "$AZURE_CONFIG" -a -r "$AZURE_CONFIG" ]; then
    source $AZURE_CONFIG
  else 
    echo "Missing azure config file, please check the /etc/.azure_variable file!" >&2
    exit 2
  fi

  if [ -z $AZURE_STORAGE_BUCKET ]; then
    echo "Not bucket name defined, please check the /etc/.azure_variable file!" >&2
  else
    # upload files
    for file_piece in $(ls $FULL_BACKUP_FILE.*) #DL-NEW1#
    do
      file_name=$(basename $file_piece)
          # upload finished, return upload status
      sudo $AZURECMD storage blob upload --account-name $AZURE_STORAGE_ACCOUNT --account-key $AZURE_STORAGE_ACCESS_KEY $file_piece $AZURE_STORAGE_BUCKET > /tmp/${file_name}.Status
      Transfer_Status=$(cat /tmp/${file_name}.Status| grep OK |wc -l)

      if [ ${Transfer_Status} -eq 1 ]; then
        echo "Upload Succeed, $file_piece Hash are equal, Transfer OK"
      else
        echo "Upload Failed, $file_piece Hash are not correct! Transfer ERROR" >&2
        /bin/cat /tmp/${file_name}.Status >&2
      fi
      /bin/rm -f /tmp/${file_name}.Status
    done
  fi
}


send_archive_oss() {
  # send to OSS
  echo "Sending file to AliYun OSS ..."

  for file_piece in $(ls $FULL_BACKUP_FILE.*) #DL-NEW1#
  do
    $ALICMD --upload $file_piece > /tmp/$(basename $file_piece).md5
    if [ $? -eq 0 ]; then
      echo "$file_piece upload done !"
    else
      echo "$file_piece upload failed !" >&2
    fi

    # we only want the basename for comparison not the full path
    BACKUP_FILE=`basename $file_piece`

    MD5_ENC=`$MD5 "$file_piece" | awk '{ print $1 }'`
    REM_MD5=`cat /tmp/$(basename $file_piece).md5`

    echo "local MD5 : $MD5_ENC"
    echo "remote MD5 : $REM_MD5"

    if [ x"$MD5_ENC" != x"$REM_MD5" ]; then
      echo "$file_piece MD5 are not correct ! Transfer ERROR" >&2
    else
      echo "$file_piece MD5 are equal locally and on OSS, transfer OK"
    fi
    /bin/rm -f /tmp/$(basename $file_piece).md5
  done
}
##remove Non-standard error logs from error log file
clean_log(){

  for error_file in `ls "$BACKUP_FOLDER"/"$PREFIX_BACKUP"*.error`;
  do
    sed -i '/file changed as we read it/d' $error_file;
    sed -i '/leaked on lvcreate invocation/d' $error_file;
    sed -i '/Removing leading/d' $error_file;
    sed -i '/No medium found/d' $error_file;
    sed -i '/WARNING/d' $error_file
  done

}

###### ADDED BY AMMAR 27 MAY 2014 16:42 ########################

### ------------- ADDED BY NICOLAO SCARAFFIA - 2013-09-27 -------------------


convertSizeToHumanReadable()
{
    echo $1 | awk 'function human(x) {
     s=" B   KiB MiB GiB TiB EiB PiB YiB ZiB"
     while (x>=1024 && length(s)>1)
           {x/=1024; s=substr(s,5)}
     s=substr(s,1,4)
     xf=(s==" B  ")?"%5d   ":"%8.2f"
     return sprintf( xf"%s\n", x, s)
    }
    {gsub(/^[0-9]+/, human($1)); print}'
}



#
## $1 = "pack" :   print the list of the packages with the associated size
## $1 = else :     print just their dimensions
#
## every line is terminated with ? to work easily with awk    

packageListFunc()
{
    find $BACKUP_FOLDER -type d | tail -n +2 | while read folderPath
    do
        lastPackage=$(find $folderPath | grep $PREFIX_BACKUP | grep tar.gz | tail -1)
        packageSize=`ls -l $lastPackage | sed 's/ *$//g' | awk -F" " '{print $5;}'`
        if [ $1 = "pack" ]; then
            echo "$lastPackage $(convertSizeToHumanReadable $packageSize)"
        else
            echo "$packageSize"
        fi
    done
}

# get the total size of the backup package
getPackageTotalSize()
{
    tmpFileName="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_Report_tmpFile.txt     # create a temporary file to easily sum the values
    packageListFunc size > $tmpFileName
    #
    ## sum all the sizes of the packages
    sum=0
    #sum=$(cat $tmpFileName | while read currSize
    sum=$(packageListFunc size | awk -F" " '{ for(i=0;i<NF;i++) { print $i; if(i!=NF-1) print "\n";} }' | while read currSize
    do
        sum=$[$sum+$currSize]
        echo $sum              
    done | tail -1)   # total size of the packages
   
    convertSizeToHumanReadable $sum
}

# get the list with the packages and their list
getPackageSizeList()
{
    packageListFunc pack
}

# encode special characters to avoid problems with POST
rawurlencode()
{
    local string="${1}"
    local strlen=${#string}
    local encoded=""

    for (( pos=0 ; pos<strlen ; pos++ ))
    do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            *)               printf -v o '%%%02x' "'$c"
        esac
        encoded+="${o}"
    done    

    echo "${encoded}"
}




# send the informations concerning the success or fail of the backup operations
updateBackupReporterServiceInfo()
{
        finalLogFile="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_Report_finalLog.txt
        touch $finalLogFile
        ## build the final log file to send to the backup report server
        # remove the first line with the header of the email
        cat $MAIL_REPORT_FILE | tail -n +2 > $finalLogFile
        echo "" >> $finalLogFile
        echo "#### BACKUP PACKAGES INFO ###"    >> $finalLogFile
        echo "" >> $finalLogFile
        getPackageSizeList >> $finalLogFile

       
         ## build the final error log file to send to the backup report server
        finalErrorFile="$BACKUP_FOLDER"/"$PREFIX_BACKUP"_Report_finalLog.error
    touch $finalErrorFile
    find $BACKUP_FOLDER | grep $PREFIX_BACKUP | grep ".*\.error$" | while read errorFileName
    do
            if [ -s $errorFileName ];then
            echo "" >> $finalErrorFile
            echo "" >> $finalErrorFile
            echo "### LOG FILE: $(basename $errorFileName) ###" >> $finalErrorFile
            cat $errorFileName >> $finalErrorFile
        fi
    done

        ## send data to the backup report server
        echo "Sending backup report...."
        outputPostVar="srvname=$HOSTNAME&result=$STATUS&bckmethod=ncscript&size="$(getPackageTotalSize | sed -e 's/^[ \t]*//')"&log="$(rawurlencode "Not in use")"&error="$(rawurlencode "$(cat $finalErrorFile)")    

    if [ ! -x $WGET ]; then
        echo "$WGET - is not executable -- review the configuration" >&2
    fi

    sendReportOutput=$($WGET -qO- --post-data="$outputPostVar" https://backupreporter.service.chinanetcloud.com/backup_report_service/backup_service.php | tr -d '\040\011\012\015')
        if [ "$sendReportOutput" != "SUCCESS" ]; then
                echo "send backup report failed" >&2
        fi
}

### ------------- END ADDED BY NICOLAO SCARAFFIA - 2013-09-27 -------------------



###########################################################################
# MAIN function
###########################################################################

main(){
  # Judge if lock file exists 
  if [ -e $LOCK_FILE ] ; then
	logger "Master Backup Script is running , probably stuck. Please check ! "
	echo "Master Backup Script is running , probably stuck. Please check ! " >&2
	exit 1
  fi

  # create lock file 
  touch $LOCK_FILE 
  
  ## retrieve jobs
  list_jobs=`get_list_jobs`

  #
  ## start backup
  echo "`/bin/date | awk '{print $4}'` Starting backup jobs"
  for job in $list_jobs
  do
    validate_script "$job"
    run_script_bg "$job"
  done
  echo "`/bin/date | awk '{print $4}'` Backup jobs running in background"; echo

  #
  ## wait for the jobs to complete
  echo "`/bin/date | awk '{print $4}'` Waiting for backup jobs to complete..."
  wait_job_bg
  echo "`/bin/date | awk '{print $4}'` Backup jobs completed."; echo

  #
  #Skip "archive", "encrypt" and  "remote-storage" functions when we are only running local backup
  if [ "$STORAGE_METHOD" != "LOCAL" ]; then 

    ## create main archive
    echo "`/bin/date | awk '{print $4}'` Preparing main archive..."
    create_archive "$FULL_BACKUP_FILE"
    if [ $? -ne 0 ]; then
      echo "Errors occured during the master archive creation, check logs" >&2
    else
      echo "`/bin/date | awk '{print $4}'` Main archive prepared."; echo
    fi

    #
    ## encrypt archive
    if [ "$ENABLE_ENCRYPT" == "YES" ]; then
      echo "`/bin/date | awk '{print $4}'` Encrypting archive for remote storage..."
      encrypt "$FULL_BACKUP_FILE" "$FULL_BACKUP_FILE_GPG"
      if [ $? -ne 0 ]; then
        echo "Errors occured during the encryption of the master archive, check logs" >&2
      else
        echo "`/bin/date | awk '{print $4}'` Archive encrypted."; echo
      fi
    fi

    # remote storage
    echo "`/bin/date | awk '{print $4}'` Sending archive remotely..."
    if [ "$STORAGE_METHOD" == "S3" ]; then
      send_archive_s3
    # send_archive_s3_cn
    elif [ "$STORAGE_METHOD" == "OSS" ]; then
      send_archive_oss
    elif [ "$STORAGE_METHOD" == "QINIU" ]; then
      send_archive_qiniu
    elif [ "$STORAGE_METHOD" == "AZURE" ]; then
      send_archive_azure
    else
      send_archive_ssh
    fi

    if [ $? -ne 0 ]; then
      echo "Errors occured during the remote transfer, check logs" >&2
    else
      echo "`/bin/date | awk '{print $4}'` Archive sent."; echo
    fi
    # cleaning extra files
    echo "`/bin/date | awk '{print $4}'` Cleaning extra files that take space on the server..."
      # remove full archive - keep individual sub-scripts archives
      rm -f "$FULL_BACKUP_ARCHIVE"*
    echo "`/bin/date | awk '{print $4}'` Cleaning completed."
  fi

  logger "Master Backup Script - INFO - operation completed - validate from log "

  # remove Non-standard error logs from error log file
  clean_log
  
  # remove lock file 
  rm -f $LOCK_FILE

 }

####################################
# Interactive funtions
####################################

# display version
print_version() {
  printf "Version: %s\n" $version_num
}

help() {
  print_version
  printf "Usage: %s: [-h] [-v] [-i] [-t | -r] [-c config_file] args" $(basename $0)

  echo
  echo "-h | --help                        -- display help (this)"
  echo "-v | --version                     -- version"
  echo "-i | --init                        -- init script ### NOT READY YET"
  echo "-t | --test                        -- test backup jobs :"
  echo "                                      display output and errors - remote storage - no mail report"
  echo "-r | --run                         -- run backup :"
  echo "                                      full backup + sub-scripts + remote storage + encrypt + email report"
  echo "-c CONFIG_FILE | --config file     -- specify config file"
  echo
}

# get options to play with and define the script behavior
get_options() {
  # -h -- display help
  # -v -- version
  # -i -- init script
  # -t -- test backup jobs - only display output and errors - no remote storage - no real backup
  # -r -- run backup
  # -c -- specify config file

  # init flags
  test_flag=0
  init_script_flag=0
  run_flag=0

  # Note that we use `"$@"' to let each command-line parameter expand to a
  # separate word. The quotes around `$@' are essential!
  # We need TEMP as the `eval set --' would nuke the return value of getopt.

  OPTIONS=`getopt --options hvitrc: \
           --long help,version,init,test,run,config: \
           -- "$@"`

  # exit if the options have not properly been gathered
  if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

  # Note the quotes around `$OPTIONS': they are essential!
  eval set -- "$OPTIONS"

  while true ; do
    case "$1" in
      -h|--help) help ; exit ;;
      -v|--version) print_version ; exit ;;
      -i|--init) init_script_flag=1 ; shift ;; # NOT IN USE YET
      -t|--test) test_flag=1 ; shift ;;
      -r|--run) run_flag=1 ; shift ;;
      -c|--config) CONF_FILE=$2 ; shift 2 ;;
      --) shift ; break ;;
      *) echo "Internal error!" ; exit 1 ;;
    esac
  done
}

# get the options entered on the command line
get_options "$@"

# Prepare backup env - source config file - check binaries / paths - clean temp files - etc.
prepare_work_env

# we run the script
if [ $test_flag -eq 1 ]; then
  main
elif [ $run_flag -eq 1 ]; then
  main > "$MASTER_OUTPUT_LOG" 2> "$MASTER_ERROR_LOG"
  echo "Finished." >> "$MASTER_OUTPUT_LOG"
  send_email
  updateBackupReporterServiceInfo
else
  help
fi
