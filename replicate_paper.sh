#!/bin/bash

# with sed set desired record count and operation count
# recordcount=10000
# operationcount=100000

CACHE_CAPACITIES=(100 1000 2500 5000)
# define list of read write ratios
READ_WRITE_RATIOS=(0 50 75 90 95 100)
DESIRED_RECORD_COUNT=10
DESIRED_OPERATION_COUNT=100

# set config capacity
CONFIG_FILES=("simple_config.json" "rl_all_strategy.json" "rl_caching_strategy.json" "rl_eviction_strategy.json"  "rl_ttl_strategy.json" "rl_multi_strategy.json")

for capacity in "${CACHE_CAPACITIES[@]}"
do
    for config in "${CONFIG_FILES[@]}"
    do 
        export FLASK_APP="rlcache.server.cache_manager_server"
        export FLASK_ENV="development"
        export PYTHONPATH=$(pwd)
        export CONFIG_FILE=$(pwd)/configs/$config

        # setup cache capacity in json file
        sed -i "s/\"capacity\": [0-9]*/\"capacity\": $capacity/g" $CONFIG_FILE

        flask run --no-reload --without-threads &

        health_check="curl -s localhost:5000"

        # wait until flask is up and curl is successful
        while ! $health_check
        do
            echo "waiting for flask to start"
            sleep 5
        done

        for ratio in "${READ_WRITE_RATIOS[@]}"
        do sed -i "s/recordcount=[0-9]*/recordcount=${DESIRED_RECORD_COUNT}/g" workload_paper_${ratio}
           sed -i "s/operationcount=[0-9]*/operationcount=${DESIRED_OPERATION_COUNT}/g" workload_paper_${ratio}
        done
        
        curl -X DELETE localhost:5000/close
        sh generate_load.sh workload_paper_100
        curl -X DELETE localhost:5000/close
        sh generate_load.sh workload_paper_95
        curl -X DELETE localhost:5000/close
        sh generate_load.sh workload_paper_90
        curl -X DELETE localhost:5000/close
        sh generate_load.sh workload_paper_75
        curl -X DELETE localhost:5000/close
        sh generate_load.sh workload_paper_50
        curl -X DELETE localhost:5000/close
        sh generate_load.sh workload_paper_0

        # exclude grep from ps aux
        flask_ps=$(ps aux | grep 'flask run' | grep -v grep | awk '{print $2}')

        while [ -n "$flask_ps" ]
        do
            kill -9 $flask_ps
            pkill flask
            echo "killing flask"
            sleep 5
            flask_ps=$(ps aux | grep 'flask run' | grep -v grep | awk '{print $2}')
        done
    done
done
