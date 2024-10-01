#!/bin/bash

today=$(date +"%Y-%m-%d")

# Make data aggregation folder

mkdir /Users/ishaanlagwankar/Desktop/code/causal-traces-repcl/data/csv/$today
touch /Users/ishaanlagwankar/Desktop/code/causal-traces-repcl/data/csv/$today/config.cfg

# Make config file

echo "[generic]" >> data/csv/$today/config.cfg
echo "data = /Users/ishaanlagwankar/Desktop/code/causal-traces-repcl/data/csv/$today/data.csv" >> data/csv/$today/config.cfg
echo "num_procs = 5" >> data/csv/$today/config.cfg
echo "xlim = 20" >> data/csv/$today/config.cfg
echo "csv = 1" >> data/csv/$today/config.cfg
echo "columns = MSG_TYPE,NODE_1,NODE_2,SEQTS,HLC,BITMAP,OFFSETS,COUNTERS,NUM_PROCS,EPSILON,INTERVAL,DELTA,ALPHA,MAX_OFFSET_SIZE,OFFSET_SIZE,COUNTER_SIZE,CLOCK_SIZE,MAX_OFFSET" >> data/csv/$today/config.cfg
echo "cwnd = 1" >> data/csv/$today/config.cfg
echo "epsilon = 1" >> data/csv/$today/config.cfg
echo "nodes = 10.1.1.1,10.1.1.2,10.1.1.3,10.1.1.4,10.1.1.5,10.1.1.6,10.1.1.7,10.1.1.8,10.1.1.9,10.1.1.10,10.1.1.11,10.1.1.12,10.1.1.13,10.1.1.14,10.1.1.15,10.1.1.16,10.1.1.17,10.1.1.18,10.1.1.19,10.1.1.20,10.1.1.21,10.1.1.22,10.1.1.23,10.1.1.24,10.1.1.25,10.1.1.26,10.1.1.27,10.1.1.28,10.1.1.29,10.1.1.30,10.1.1.31,10.1.1.32" >> data/csv/$today/config.cfg
echo "10.1.1.1 = 1" >> data/csv/$today/config.cfg
echo "10.1.1.2 = 2" >> data/csv/$today/config.cfg
echo "10.1.1.3 = 3" >> data/csv/$today/config.cfg
echo "10.1.1.4 = 4" >> data/csv/$today/config.cfg
echo "10.1.1.5 = 5" >> data/csv/$today/config.cfg
echo "10.1.1.6 = 6" >> data/csv/$today/config.cfg
echo "10.1.1.7 = 7" >> data/csv/$today/config.cfg
echo "10.1.1.8 = 8" >> data/csv/$today/config.cfg
echo "10.1.1.9 = 9" >> data/csv/$today/config.cfg
echo "10.1.1.10 = 10" >> data/csv/$today/config.cfg
echo "10.1.1.11 = 11" >> data/csv/$today/config.cfg
echo "10.1.1.12 = 12" >> data/csv/$today/config.cfg
echo "10.1.1.13 = 13" >> data/csv/$today/config.cfg
echo "10.1.1.14 = 14" >> data/csv/$today/config.cfg
echo "10.1.1.15 = 15" >> data/csv/$today/config.cfg
echo "10.1.1.16 = 16" >> data/csv/$today/config.cfg
echo "10.1.1.17 = 17" >> data/csv/$today/config.cfg
echo "10.1.1.18 = 18" >> data/csv/$today/config.cfg
echo "10.1.1.19 = 19" >> data/csv/$today/config.cfg
echo "10.1.1.20 = 20" >> data/csv/$today/config.cfg
echo "10.1.1.21 = 21" >> data/csv/$today/config.cfg
echo "10.1.1.22 = 22" >> data/csv/$today/config.cfg
echo "10.1.1.23 = 23" >> data/csv/$today/config.cfg
echo "10.1.1.24 = 24" >> data/csv/$today/config.cfg
echo "10.1.1.25 = 25" >> data/csv/$today/config.cfg
echo "10.1.1.26 = 26" >> data/csv/$today/config.cfg
echo "10.1.1.27 = 27" >> data/csv/$today/config.cfg
echo "10.1.1.28 = 28" >> data/csv/$today/config.cfg
echo "10.1.1.29 = 29" >> data/csv/$today/config.cfg
echo "10.1.1.30 = 30" >> data/csv/$today/config.cfg
echo "10.1.1.31 = 31" >> data/csv/$today/config.cfg
echo "10.1.1.32 = 32" >> data/csv/$today/config.cfg

# Function to calculate the number of bits required to store an integer
num_bits() {
    number=$1
    bits=0
    while ((number > 0)); do
        ((bits++))
        number=$((number >> 1))
    done
    echo $bits
}

n_events = 


for (( NUM_PROCS=32; NUM_PROCS<=32; NUM_PROCS+=32)); do
    for (( EPSILON=100; EPSILON<=1000; EPSILON+=50)); do
        for (( INTERVAL=10; INTERVAL<=40; INTERVAL+=10)); do
            if (( INTERVAL * EPSILON % 1000 == 0 && INTERVAL*EPSILON <= 6000 )); then
                for (( DELTA=1; DELTA<=8; DELTA*=2)); do
                    for (( ALPHA=20; ALPHA<=160; ALPHA*=2)); do
                        MAX_OFFSET_SIZE=$(num_bits $EPSILON)
                        
                        cp /Users/ishaanlagwankar/Desktop/code/ns-3-dev-git/results-2024-04-06-N.${NUM_PROCS}-E.${EPSILON}-I.${INTERVAL}-D.${DELTA}-A.${ALPHA}-M.${MAX_OFFSET_SIZE}.csv /Users/ishaanlagwankar/Desktop/code/causal-traces-repcl/data/csv/$today/data.csv
                        
                        # Remove initial fluff

                        sed -i '' '1,121d' /Users/ishaanlagwankar/Desktop/code/causal-traces-repcl/data/csv/$today/data.csv

                        # Extract first n lines


                        # Run trace generator and print into csv

                    done
                done
            fi
        done
    done
done