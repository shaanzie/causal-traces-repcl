#!/bin/bash

NUM_PROCS=32

date=(date +'%Y-%m-%d')

echo "EPSILON,INTERVAL,DELTA,ALPHA,OFFSIZE,COUSIZE,EPOCH" | tee data/$date-hvc.csv

for(( EPSILON = 1; EPSILON <= 32; EPSILON *= 2 ))
do
    for(( INTERVAL = 1; INTERVAL <= EPSILON; INTERVAL *= 2 ))
    do
        for(( DELTA = 1; DELTA <= EPSILON; DELTA *= 2 ))
        do
            for(( ALPHA = 25; ALPHA <= 100; ALPHA += 25 ))
            do
                echo -------------------------------------
                echo "Running for -n $NUM_PROCS -d $DELTA -e $EPSILON -i $INTERVAL -a $ALPHA"
                echo -------------------------------------
                timeout 120 python3 simulation.py -n $NUM_PROCS -d $DELTA -e $EPSILON -i $INTERVAL -a $ALPHA | tee -a data/$date-hvc.csv
            done
        done
    done
done