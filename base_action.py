"""
base_action.py - Common action class

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

class base_action:
    """Base log for an interaction.""" 
    
    def __init__(self, 
                 initiator_id: str, 
                 target: str): -> None
        """Initialize the action."""
        self.initiator_id: str = initiator_id
        self.target: str = target
    
    # TODO: Create basic sim type, log type signature
    def apply_action(self, simulation : sim_type) -> log_type:
        """Apply the action in a given simulation. Generate a log output."""
        raise NotImplemented
        
