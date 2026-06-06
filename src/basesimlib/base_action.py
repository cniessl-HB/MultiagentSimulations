"""
base_action.py - Common action class that generates stubs

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from basesimlib.base_masim_types import some_action, some_action_stub, some_agent

class base_action_stub(some_action):
    """Base log for an interaction.""" 
    
    def __init__(self, 
                 initiator_agent: some_agent) -> None:
        """Setup the action stub generator."""
        self.initiator_agent = initiator_agent
    
    def create_stub(self, target_id: str) -> some_action_stub:
        """Return an action_stub based on agent and target."""
        raise NotImplementedError
