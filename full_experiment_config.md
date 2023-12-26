# Experiment configuration

1. Start server
2. Create workloads
3. Load workload to server
4. End loading phase
5. Execute workload against server
6. End execution phase, make sure to call close episode


# Algorithm configuration

To change algorithm configuration, edit the `start_dev_env.sh` script and 
input the appropriate configuration. 

Specifically change line:

```
export CONFIG_FILE="$(pwd)/configs/simple_config.json"
```

# Read-write ratios

To modify the workload going against the server, define a workload ycsb file
and point to it when running `generate_load.sh`. 

The workload read-write section is defined in ycsb workload file as:

```
readproportion=0.95
updateproportion=0.05
```

# Running the experiment

To run the experiment exactly as it is done in the paper, simply run

```
sh replicate_paper.sh
```
