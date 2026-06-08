"""
base_types.py - Package and basic type definitions

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from abc import ABC, abstractmethod

from datetime import datetime

class some_action_stub:
    pass

class some_action:
    pass

class some_agent:

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def plan_action(self) -> some_action_stub:
        pass

class some_log(ABC):

    @abstractmethod
    def get_step(self) -> int:
        pass

    @abstractmethod    
    def get_action_time(self) -> datetime:
        pass

    @abstractmethod
    def __lt__(self, other) -> bool:
        pass
    
    @abstractmethod    
    def __eq__(self, other) -> bool:
        pass

class some_sim(ABC):

    @abstractmethod
    def get_step(self) -> int:
        pass
