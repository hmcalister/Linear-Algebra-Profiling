#!/bin/bash

# echo "trials,multiplications,threads,time"
for TRIALS in {1000..10000..1000}
do
    for MULTIPLICATIONS in {1000..10000..1000}
    do
        for THREADS in 1 
        do
            TIME_BEFORE=$(date +%s%N)
            python main.py --trials=$TRIALS --multiplications=$MULTIPLICATIONS --threads=$THREADS
            TIME_AFTER=$(date +%s%N)
            echo "$TRIALS,$MULTIPLICATIONS,$THREADS,$((TIME_AFTER-TIME_BEFORE))"
        done
    done
done
