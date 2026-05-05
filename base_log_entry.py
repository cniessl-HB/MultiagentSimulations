"""
Interaction_Log.py - Common log class

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

class base_log_entry:
    """Base log for an interaction.""" 
    
    def __init__(self, initiator_id, other_id, action_msg) -> None:
        self.initiator_id: str = initiator_id
        self.other_id: str = other_id
        self.action_msg: str = action_msg
    
    def __str__(self) -> str:
        start_str = f"{self.initiator_id} -> {self.other_id}: "
        return start_str + self.action_msg
