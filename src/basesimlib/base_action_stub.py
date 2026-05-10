"""
base_action_stub.py - Common action stub class

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from base_masim_types import some_action_stub, some_log, some_sim

class base_action_stub(some_action_stub):
    """Base log for an interaction.""" 
    
    def __init__(self, 
                 initiator_id: str, 
                 target: str) -> None:
        """Initialize the action."""
        self.initiator_id: str = initiator_id
        self.target: str = target
    
    # TODO: Create basic sim type, log type signature
    def apply(self, simulation : some_sim) -> some_log:
        """Apply the action in a given simulation. Generate a log output."""
        raise NotImplementedError
        
