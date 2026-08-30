"""
base_log_entry.py - Common log class

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import json
import uuid
from datetime import datetime

from basesimlib.base_masim_types import some_log


class base_log_entry(some_log):
    """Base log for an interaction."""

    def __init__(
        self, initiator_id: str, other_id: str, step: int, action_msg: str
    ) -> None:
        """Initialize the log entry."""
        self.initiator_id: str = initiator_id
        self.other_id: str = other_id
        self.step: int = step
        self.action_time: datetime = datetime.now()
        self.action_msg: str = action_msg
        self.uuid = uuid.uuid4()

    def get_step(self) -> int:
        return self.step

    def get_action_time(self) -> datetime:
        return self.action_time

    def get_uuid(self) -> uuid.UUID:
        return self.uuid

    def __lt__(self, other: some_log):
        """Less than comparison for sorting."""
        if self.step < other.get_step():
            return True
        elif self.step == other.get_step():
            return self.get_action_time() < other.get_action_time()
        return False

    def __eq__(self, other: object):
        """Equality comparison for sorting."""
        if not isinstance(other, some_log):
            # Type mismatch comparison
            return False
        if self.step == other.get_step():
            return self.get_action_time() == other.get_action_time()
        return False

    def __json__(self) -> str:
        """Dump json formatted version of this entry."""
        ret_dict: dict = {}
        ret_dict["initiator_id"] = self.initiator_id
        ret_dict["other_id"] = self.other_id
        ret_dict["step"] = self.step
        ret_dict["action_time"] = self.action_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        ret_dict["action_msg"] = self.action_msg
        return json.dumps(ret_dict)

    def __str__(self) -> str:
        """Get string output of log entry."""
        log_str = f"{self.action_time}, @ step {self.step}: "
        log_str = log_str + f"{self.initiator_id} -> {self.other_id} "
        return log_str + self.action_msg

    def synchronize_to_event(self, sync_event: some_log) -> None:
        """Adjust the timestamp of the log to other event."""
        self.action_time = sync_event.get_action_time()
