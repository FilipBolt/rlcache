from abc import ABC
from enum import Enum
from typing import List, Dict


class ObservationType(Enum):
    Hit = 1
    Miss = 2
    Invalidate = 3
    Expiration = 4  # Signal terminal
    Monitor = 5


class Observer(ABC):
    def observe(self, key: str, observation_type: ObservationType, info: Dict[str, any]):
        raise NotImplementedError


class ObserversOrchestrator(Observer):
    def __init__(self, observers: List[Observer]):
        self.observers = observers

    def observe(self, key: str, observation_type: ObservationType, info: Dict[str, any] = None):
        for observer in self.observers:
            observer.observe(key, observation_type, info)
