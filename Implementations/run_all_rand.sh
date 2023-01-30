#!/bin/bash

NUM_TRIALS=$1
echo $NUM_TRIALS
shopt -s dotglob
shopt -s nullglob
directories=(*/)
for dir in "${directories[@]}"
do
    cd $dir
    echo "------------------------------------"
    echo $dir
    ./rand_script.sh $1 >> rand_data.csv
    cd ..
done