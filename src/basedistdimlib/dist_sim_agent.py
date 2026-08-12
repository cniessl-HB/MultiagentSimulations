"""
dist_sim_client.py - Distributed simulation client

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

class dist_sim_agent(some_agent):
    """Base distributed agent."""

    def get_id(self) -> str:
        raise NotImplementedError


    def is_active(self) -> bool:
        raise NotImplementedError


    def set_active(self, active_val: bool) -> None:
        raise NotImplementedError


    def plan_action(self) -> some_action_stub:
        raise NotImplementedError


    def add_to_history(self, log_entry) -> None:
        raise NotImplementedError


    def get_history(self) -> list[some_log]:
        raise NotImplementedError
