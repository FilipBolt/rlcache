import os
from typing import Dict

from rlcache.strategies.caching_strategies.caching_strategy_base import CachingStrategy
from rlcache.strategies.caching_strategies.rl_caching_strategy import RLCachingStrategy
from rlcache.strategies.caching_strategies.simple_strategies import OnReadWriteCacheStrategy, OnReadOnlyCacheStrategy
from rlcache.strategies.eviction_strategies.eviction_strategy_base import EvictionStrategy
from rlcache.strategies.eviction_strategies.lru_eviction_strategy import LRUEvictionStrategy
from rlcache.strategies.ttl_selection_strategies.ttl_strategy_base import TtlStrategy
from rlcache.strategies.ttl_selection_strategies.ttl_strategy_fixed import FixedTtlStrategy


def strategies_from_config(config: Dict[str, any], results_dir: str) -> [CachingStrategy,
                                                                         EvictionStrategy,
                                                                         TtlStrategy]:
    caching_strategy = caching_strategy_from_config(config['caching_strategy_settings'], results_dir)
    eviction_strategy = eviction_strategy_from_config(config['eviction_strategy_settings'], results_dir)
    ttl_strategy = ttl_strategy_from_config(config['ttl_strategy_settings'], results_dir)

    return [caching_strategy, eviction_strategy, ttl_strategy]


def caching_strategy_from_config(config: Dict[str, any], results_dir: str) -> CachingStrategy:
    _supported_type = ['read_write', 'read_only', 'rl_driven']

    results_dir += '/caching_strategy/'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    caching_strategy_type = config['type']
    if caching_strategy_type == "read_write":
        return OnReadWriteCacheStrategy(config, results_dir)
    elif caching_strategy_type == "read_only":
        return OnReadOnlyCacheStrategy(config, results_dir)
    elif caching_strategy_type == 'rl_driven':
        return RLCachingStrategy(config, results_dir)
    else:
        raise NotImplementedError("Type passed isn't one of the supported types: {}".format(_supported_type))


def eviction_strategy_from_config(config: Dict[str, any], results_dir: str) -> EvictionStrategy:
    _supported_type = ['lru']

    results_dir += '/eviction_strategy/'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    eviction_strategy_type = config['type']
    if eviction_strategy_type == "lru":
        return LRUEvictionStrategy(config, results_dir)
    else:
        raise NotImplementedError("Type passed isn't one of the supported types: {}".format(_supported_type))


def ttl_strategy_from_config(config: Dict[str, any], results_dir: str) -> TtlStrategy:
    _supported_type = ['fixed']
    results_dir += '/ttl_strategy/'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    ttl_strategy_type = config['type']
    if ttl_strategy_type == "fixed":
        return FixedTtlStrategy(config, results_dir)
    else:
        raise NotImplementedError("Type passed isn't one of the supported types: {}".format(_supported_type))
