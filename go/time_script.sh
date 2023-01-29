#!/bin/bash

echo "trials,multiplications,threads,time"
for TRIALS in {10..100..10}
do
    for MULTIPLICATIONS in {10..100..10}
    do
        for THREADS in 1 2 4 8 16 
        do
            TIME_BEFORE=$(date +%s%N)
            ./linalg_profiling --trials=$TRIALS --multiplications=$MULTIPLICATIONS --threads=$THREADS
            TIME_AFTER=$(date +%s%N)
            echo "$TRIALS,$MULTIPLICATIONS,$THREADS,$((TIME_AFTER-TIME_BEFORE))"
        done
    done
done

for TRIALS in {100..1000..100}
do
    for MULTIPLICATIONS in {100..1000..100}
    do
        for THREADS in 1 2 4 8 16
        do
            TIME_BEFORE=$(date +%s%N)
            ./linalg_profiling --trials=$TRIALS --multiplications=$MULTIPLICATIONS --threads=$THREADS
            TIME_AFTER=$(date +%s%N)
            echo "$TRIALS,$MULTIPLICATIONS,$THREADS,$((TIME_AFTER-TIME_BEFORE))"
        done
    done
done

for TRIALS in {1000..10000..1000}
do
    for MULTIPLICATIONS in {1000..10000..1000}
    do
        for THREADS in 1 2 4 8 16
        do
            TIME_BEFORE=$(date +%s%N)
            ./linalg_profiling --trials=$TRIALS --multiplications=$MULTIPLICATIONS --threads=$THREADS
            TIME_AFTER=$(date +%s%N)
            echo "$TRIALS,$MULTIPLICATIONS,$THREADS,$((TIME_AFTER-TIME_BEFORE))"
        done
    done
done