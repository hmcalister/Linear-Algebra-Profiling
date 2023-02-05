#!/bin/bash

batchsize_list=(2048 4096 8192 16384 32768)

echo "trials,multiplications,batchsize,time"
for ((RAND_GENS=0;RAND_GENS<$1;RAND_GENS++))
do
    BATCHSIZE=${batchsize_list[$RANDOM % ${#batchsize_list[@]}]}
    TRIALS=$[RANDOM%100000+$BATCHSIZE]
    MULTIPLICATIONS=$[RANDOM%100000+1]
    >&2 echo -ne "$RAND_GENS => $TRIALS,$MULTIPLICATIONS,$BATCHSIZE                        \r"
    TIME_BEFORE=$(date +%s%N)
    python main.py --trials=$TRIALS --multiplications=$MULTIPLICATIONS --batchsize=$BATCHSIZE
    TIME_AFTER=$(date +%s%N)
    echo "$TRIALS,$MULTIPLICATIONS,$BATCHSIZE,$((TIME_AFTER-TIME_BEFORE))"
done
