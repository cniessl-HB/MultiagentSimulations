"""
base_log_entry.py - Common log class

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

class base_log_entry:
    """Base log for an interaction.""" 
    
    def __init__(self, 
                 initiator_id: str, 
                 other_id: str, 
                 step: int, 
                 action_msg: str) -> None:
        self.initiator_id: str = initiator_id
        self.other_id: str = other_id
        self.step: int = step
        self.action_msg: str = action_msg
    
    def __str__(self) -> str:
        """Get output of log entry."""
        log_str = f"{self.initiator_id} -> {self.other_id} "
        log_str = log_str + f"@ {self.step}: "
        return log_str + self.action_msg
