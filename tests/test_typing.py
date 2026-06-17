"""
base_agent.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import pytest

from datetime import datetime

from basesimlib.base_agent import base_agent
from basesimlib.base_masim_types import some_log, some_action, some_action_stub
from basesimlib.base_log_entry import base_log_entry
from basesimlib.base_exceptions import AgentNotFoundError, DeactivateInactiveAgentError, DuplicateAgentError
from basesimlib.base_simulation import base_simulation

def test_incomplete_masim_log_impl() -> None:
    class incomplete_log_entry(some_log):
        pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        test_log = incomplete_log_entry()
    
    class fake_log_entry(some_log):
        
        def get_step(self) -> int:
            return super().get_step()
        
        def get_action_time(self) -> datetime:
            return super().get_action_time()
        
        def __lt__(self, other) -> bool:
            return super().__lt__(other)
    
        def __eq__(self, other) -> bool:
            return super().__eq__(other)
    
    test_log2 = fake_log_entry()
    
    with pytest.raises(NotImplementedError):
        test_log2.get_step()
    with pytest.raises(NotImplementedError):
        test_log2.get_action_time()
    with pytest.raises(NotImplementedError):
        test_log2.__lt__(test_log2)
    with pytest.raises(NotImplementedError):
        test_log2.__eq__(test_log2)

def test_incomplete_masim_action_stub_impl() -> None:
    
    class incomplete_action_stub(some_action_stub):
        pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        test_action = incomplete_action_stub()

    class fake_action_stub(some_action_stub):
        
        def apply(self, simulation) -> some_log:
            return super().apply(simulation)
    
        def get_initiator_id(self) -> str:
            return super().get_initiator_id()

        def get_target_id(self) -> str:
            return super().get_target_id()

    test_action2 = fake_action_stub()
    
    with pytest.raises(NotImplementedError):
        test_action2.apply(None)
    with pytest.raises(NotImplementedError):
        test_action2.get_initiator_id()
    with pytest.raises(NotImplementedError):
        test_action2.get_target_id()

def test_incomplete_masim_action_impl() -> None:

    class incomplete_action(some_action):
        pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        test_action = incomplete_action()

