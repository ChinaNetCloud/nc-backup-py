#!/bin/bash

GIT="/usr/bin/git"
TAR="/bin/tar"
PYTHON=`which python`
CONFIG_DIR="$HOME/nc-backup-py-configs"

echo "Using python: $PYTHON"

echo
echo "Back up config dir $CONFIG_DIR"

if [ ! -d "$CONFIG_DIR" ];then
  echo "$CONFIG_DIR does not exist creating..."
  mkdir $CONFIG_DIR
fi

tar -czvf $CONFIG_DIR/nc-backup-py.`date +%Y%m%d_%H%M%S`.bkp.tar /etc/nc-backup-py

echo
echo "Git: Pulling latest commit from $(git config --get remote.origin.url)"

$GIT pull


if [ -z $BRANCH ];then
  echo "Setting default branch to master"
  BRANCH="master"
fi

echo
echo "Installing latest update on branch $BRANCH"
$PYTHON setup.py
