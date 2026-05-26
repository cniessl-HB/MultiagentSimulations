"""
base_log_entry.py - Common log class

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from datetime import datetime

from basesimlib.base_masim_types import some_log

class base_log_entry(some_log):
    """Base log for an interaction.""" 
    
    def __init__(self, 
                 initiator_id: str, 
                 other_id: str, 
                 step: int,
                 action_time: datetime,
                 action_msg: str) -> None:
        """Initialize the log entry."""
        self.initiator_id: str = initiator_id
        self.other_id: str = other_id
        self.step: int = step
        self.action_time: datetime = datetime.now()
        self.action_msg: str = action_msg
    
    def __lt__(self, other: some_log):
        """Less than comparison for sorting."""
        if self.step < other.step:
            return True
        elif self.step == other.step:
            return (self.action_time < other.action_time)
        return False
    
    def __eq__(self, other: some_log):
        """Equality comparison for sorting."""
        if self.step == other.step:
            return (self.action_time == other.action_time)
        return False
        
    def __json__(self) -> dict:
        """Dump json formatted version of this entry."""
        ret_dict: dict = {}
        ret_dict["initiator_id"] = self.initiator_id
        ret_dict["other_id"] = self.other_id
        ret_dict["step"] = self.step
        ret_dict["action_time"] = self.action_time
        ret_dict["action_msg"] = self.action_msg
        return ret_dict
    
    def __str__(self) -> str:
        """Get string output of log entry."""
        log_str = f"{self.action_time}, @ step {self.step}: "
        log_str = log_str + f"{self.initiator_id} -> {self.other_id} "
        return log_str + self.action_msg
