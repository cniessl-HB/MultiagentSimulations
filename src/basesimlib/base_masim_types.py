"""
base_types.py - Package and basic type definitions

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from abc import ABC, abstractmethod

from datetime import datetime

class some_log(ABC):
    """Type definition for log stubs.
    
       Do not user super to access these functions."""

    @abstractmethod
    def get_step(self) -> int:
        raise NotImplementedError

    @abstractmethod    
    def get_action_time(self) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other) -> bool:
        raise NotImplementedError
    
    @abstractmethod    
    def __eq__(self, other) -> bool:
        raise NotImplementedError

class some_action_stub(ABC):
    """Type definition for action stubs.
    
       Do not user super to access these functions."""
    
    @abstractmethod
    def apply(self, simulation) -> some_log:
        raise NotImplementedError
    
    @abstractmethod
    def get_initiator_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_target_id(self) -> str:
        raise NotImplementedError

class some_action(ABC):
    
    @abstractmethod
    def create_stub(self, target_id: str) -> some_action_stub:
        raise NotImplementedError
    

class some_agent(ABC):

    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def is_active(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def set_active(self, active_val: bool) -> None:
        raise NotImplementedError

    @abstractmethod
    def plan_action(self) -> some_action_stub:
        raise NotImplementedError

    @abstractmethod
    def add_to_history(self, log_entry) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_history(self) -> list[some_log]:
        raise NotImplementedError

class some_sim(ABC):

    @abstractmethod
    def get_step(self) -> int:
        raise NotImplementedError
