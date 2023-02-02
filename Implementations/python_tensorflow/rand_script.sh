#!/bin/bash

batchsize_list=(512 1024 2048 4096 8192)

# echo "trials,multiplications,batchsize,time"
for ((RAND_GENS=0;RAND_GENS<$1;RAND_GENS++))
do
    TRIALS=$[RANDOM%2500+1]
    MULTIPLICATIONS=$[RANDOM%2500+1]
    BATCHSIZE=${batchsize_list[$RANDOM % ${#batchsize_list[@]}]}
    >&2 echo -ne "$RAND_GENS => $TRIALS,$MULTIPLICATIONS,$BATCHSIZE                        \r"
    TIME_BEFORE=$(date +%s%N)
    python main.py --trials=$TRIALS --multiplications=$MULTIPLICATIONS --batchsize=$BATCHSIZE
    TIME_AFTER=$(date +%s%N)
    echo "$TRIALS,$MULTIPLICATIONS,$BATCHSIZE,$((TIME_AFTER-TIME_BEFORE))"
done
