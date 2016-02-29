#!/bin/bash
################################################
# file backup
#
# Contact: vincent.viallet@gmail.com
# Version: 0.1
# Changes:
#   2009-03-10 	VV	Initial creation
#   2009-06-05 	DL
#   2009-06-29	VV	use sudo tar + check source folder
#   2010-01-21	VV	add config file
#   2010-05-31	JS	add include folder and file function 
#   2010-11-25	DL	don't use sudo ,when you are root 
#   2015-01-14  SS	Error on use of deprecated variable FILE_EXTRA_DATA
################################################
# Requirements from the Master script API
#
# INPUT:
#  - $1 -- root destination backup folder
#  - $2 -- archive PREFIX
#  - $3 -- backup config file
#
# OUTPUT:
#  - 1 backup archive tar.gz -- Naming Format: prefix_XXXXX.tar.gz
#  - STDOUT -- to be appened to mail notice
#  - STDERR -- to be appened to error log for mail notice
################################################
SCRIPT_PREFIX="file"

################################################
# Define folders to backup
# They ALL must be Full PATH
# for now only one archive is created, could add one archive per folder
################################################
# define TIMEOUT in minutes after which we consider the script as beeing stuck
TIMEOUT=60

##################################################
# Manage parameters
##################################################
#
## Save parameters
DESTINATION_FOLDER="$1"
PREFIX="$2"
BACKUP_CONFIG_FILE="$3"

#
## Check for valid destination folder
if [ ! -d "$DESTINATION_FOLDER" ]; then
  echo "$DESTINATION_FOLDER is not a valid folder" >&2
  exit 2
fi

#
## Check for valid FULL PATH
if [ ${DESTINATION_FOLDER:0:1} != '/' ]; then
  echo "Need FULL PATH for destination backup folder" >&2
  exit 2
fi

#
## Check parameters
if [ -z "$DESTINATION_FOLDER" ]; then
  echo "Missing destination folder" >&2
  exit 2
fi

if [ -z "$PREFIX" ]; then
  echo "Missing master backup prefix" >&2
  exit 2
fi

#
## Check for valid configuration file
if [ -f "$BACKUP_CONFIG_FILE" -a -r "$BACKUP_CONFIG_FILE" ]; then 
  source "$BACKUP_CONFIG_FILE"
else
  echo "The master backup config file is not readable" >&2
  echo "$BACKUP_CONFIG_FILE" >&2
  exit 2
fi

## Check parameters
if [ -z "$FILE_DATA_INCLUDE" ]; then
  echo "Missing data include definition" >&2
  exit 2
fi

if [ -n "$FILE_EXTRA_DATA" ]; then
  echo "Use of FILE_EXTRA_DATA is deprecated - please review and update the configuration"
  exit 2
fi


#
## File name definition
BACKUP_FOLDER="$DESTINATION_FOLDER"/"$SCRIPT_PREFIX"
BACKUP_FILE="$BACKUP_FOLDER"/"$PREFIX"_"$SCRIPT_PREFIX".tar.gz

#
## check for custom backup folder
if [ ! -d "$BACKUP_FOLDER" ]; then
  mkdir -p "$BACKUP_FOLDER"
  if [ $? -ne 0 ]; then echo "$DESTINATION_FOLDER folder is not writable, check permissions" ; exit 2 ; fi
fi

#
## Check for writable destination
if [ ! -w "$BACKUP_FOLDER" ]; then
  echo "$BACKUP_FOLDER folder is not writable, check permissions" >&2
   echo "current owner UID: $UID" >&2
   echo "current PWD: $PWD" >&2
   echo " user@host:~$ ls -la $BACKUP_FOLDER" >&2
   ls -la "$BACKUP_FOLDER" >&2
  exit 2
fi


## check if the final archive exists already
if [ -f "$BACKUP_FILE" ]; then
  echo "$BACKUP_FILE already exists - Backup job Cancelled" >&2
  exit 2
fi

#
## check for FULL PATH only in SOURCE_FOLDER
for folder in ${FILE_DATA_INCLUDE}
do
  if [ ${folder:0:1} != '/' ]; then
    echo "Need FULL PATH for source backup folders / files" >&2
    exit 2
  fi
done

#########################################
# File backup
# using relative PATH from the / folder
# ease recovery in a different folder while making
# an easy replica for restoration
# need: stripped folder name for use in tar
#########################################

#
## prepare a list of folders stripped from their leading / char
for folder in ${FILE_DATA_INCLUDE}
do
  STRIPPED_SOURCE_FOLDER="${folder:1} $STRIPPED_SOURCE_FOLDER"
done
## repare a list of folders stripped from their leading / char for EXCLUDE file
for folder in ${FILE_DATA_EXCLUDE}
do
  STRIPPED_EXCLUDE_SOURCE_FOLDER="--exclude ${folder:1} $STRIPPED_EXCLUDE_SOURCE_FOLDER"
done

#
## create final archive
echo "Backing up : $FILE_DATA_INCLUDE"
if [ $(id -u) -ne 0 ]; then
	sudo /bin/tar czCf / "$BACKUP_FILE" $STRIPPED_SOURCE_FOLDER $STRIPPED_EXCLUDE_SOURCE_FOLDER
else
	/bin/tar czCf / "$BACKUP_FILE" $STRIPPED_SOURCE_FOLDER $STRIPPED_EXCLUDE_SOURCE_FOLDER
fi
echo "Backup Done."; echo

#
## display final archive details
echo "List archive"
ls -la "$BACKUP_FOLDER"/"$PREFIX"_"$SCRIPT_PREFIX"*
echo "List Done."; echo
#testing svn update
