#!/bin/bash

# echo "trials,multiplications,threads,batchsize,time"
for TRIALS in {10..100..10}
do
    for MULTIPLICATIONS in {10..100..10}
    do
        for THREADS in 1
        do
            for BATCHSIZE in 1 8 32 64
            do
                TIME_BEFORE=$(date +%s%N)
                python main.py --trials=$TRIALS --multiplications=$MULTIPLICATIONS --threads=$THREADS --batchsize=$BATCHSIZE
                TIME_AFTER=$(date +%s%N)
                echo "$TRIALS,$MULTIPLICATIONS,$THREADS,$BATCHSIZE,$((TIME_AFTER-TIME_BEFORE))"
            done
        done
    done
done
