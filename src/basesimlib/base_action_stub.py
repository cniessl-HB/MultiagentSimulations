"""
base_action_stub.py - Common action stub class

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from datetime import datetime

from base_masim_types import some_action_stub, some_log, some_sim

class base_action_stub(some_action_stub):
    """Base log for an interaction.""" 
    
    def __init__(self, 
                 initiator_id: str, 
                 target: str) -> None:
        """Initialize the action."""
        self.initiator_id: str = initiator_id
        self.target: str = target
    
    def do_action(self, simulation: some_sim) -> str:
        """Modify agents in the simulation and return a string descriptive of the action."""
        raise NotImplementedError
    
    def apply(self, simulation : some_sim, action_time: datetime) -> some_log:
        """Apply the action in a given simulation. Generate a log output."""
        ret_str = self.do_action(simulation)
        current_step = simulation.get_step()
        return base_log_entry(self.initiator_id, 
                              self.target, 
                              current_step,
                              action_time,
                              ret_str)
