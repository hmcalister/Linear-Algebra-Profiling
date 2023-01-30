#!/bin/bash

thread_list=(1 2 4 8)

echo "trials,multiplications,threads,time"
for ((RAND_GENS=0;RAND_GENS<$1;RAND_GENS++))
do
    TRIALS=$[RANDOM%2500+1]
    MULTIPLICATIONS=$[RANDOM%2500+1]
    THREADS=${thread_list[$RANDOM % ${#thread_list[@]}]}
    >&2 echo -ne "$RAND_GENS => $TRIALS,$MULTIPLICATIONS,$THREADS                        \r"
    TIME_BEFORE=$(date +%s%N)
    ./dynamic_rust_linalg --trials=$TRIALS --multiplications=$MULTIPLICATIONS --threads=$THREADS
    TIME_AFTER=$(date +%s%N)
    echo "$TRIALS,$MULTIPLICATIONS,$THREADS,$((TIME_AFTER-TIME_BEFORE))"
done
