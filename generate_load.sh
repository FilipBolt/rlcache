#!/bin/sh


# find ycsb path
# it might be different version
YCSB_PATH=ycsb/ycsb-0.17.0
# run workload

# path to bin
YCSB_BIN_PATH=$YCSB_PATH/bin/ycsb.sh

# path to workloads
YCSB_WORKLOAD_PATH=$1

echo "YCSB_PATH: $YCSB_PATH"
echo "YCSB_BIN_PATH: $YCSB_BIN_PATH"
echo "YCSB_WORKLOAD_PATH: $YCSB_WORKLOAD_PATH"

# generate load

$YCSB_BIN_PATH load basic -P $YCSB_WORKLOAD_PATH 
$YCSB_BIN_PATH run basic -P $YCSB_WORKLOAD_PATH > workload.log

python load_generator.py workload.log
