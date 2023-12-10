# RLCache
Reinforcement Learning Cache Manager

This project investigates using reinforcement learning in cache management by designing three separate agents for each of the cache manager tasks. Furthermore, the project investigates two advanced reinforcement learning architectures for multi-decision problems: a single multi-task agent and a multi-agent. We also introduce a framework to simplify the modelling of computer systems problems as a reinforcement learning task. The framework abstracts delayed experiences observations and reward assignment in computer systems while providing a flexible way to scale to multiple agents.




This code supplement a thesis submited on arXiv.  
```
@misc{alabed2019rlcache,
    title={RLCache: Automated Cache Management Using Reinforcement Learning},
    author={Sami Alabed},
    year={2019},
    eprint={1909.13839},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}
```


# Running workloads

First, start the server by executing the script

```
sh start_dev_env.sh
```

Then, configure and run the workloads, for example default workload A

```
sh generate_load.sh ycsb/ycsb-0.17.0/workloads/workloada
```

Modify the workload definition file to change the workload parameters. 
