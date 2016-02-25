#!/usr/bin/env bash

#echo -n "Enter numnber : "
#read n
#rem=$(( $n % 2 ))
#if [ $rem -eq 0 ]
#then
#  echo "$n is even number"
#else
#  echo "$n is odd number"
#fi

counter=1
#echo $rest
for KEY_VAR in "$@"
do
    REST=$(( $counter % 2 ))
    if [ $REST -eq 0 ];
        then
            echo "Even"
        else
            echo "odd"
#            AUX_VALUE=$KEY_VAR
        fi
    counter=$(( counter + 1 ))
#    echo $KEY_VAR
done


## Get the last argument
#outputfile=${ARGS[-1]}
## Drop it from the array
##unset ARGS[${#ARGS[@]}-1]
#
#echo "${ARGS[2]}"

