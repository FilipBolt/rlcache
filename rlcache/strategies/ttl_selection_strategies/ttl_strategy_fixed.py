from typing import Dict

from rlcache.cache_constants import CacheInformation
from rlcache.observer import ObservationType
from rlcache.strategies.ttl_selection_strategies.ttl_strategy_base import TtlStrategy


class FixedTtlStrategy(TtlStrategy):
    """Fixed strategy that returns a preconfigured ttl."""

    def observe(self, key: str, observation_type: ObservationType, info: Dict[str, any]):
        pass

    def __init__(self, config: Dict[str, any], shared_stats: CacheInformation):
        super().__init__(config, shared_stats)
        self.ttl = self.config['ttl']

    def estimate_ttl(self, key) -> int:
        return self.ttl
