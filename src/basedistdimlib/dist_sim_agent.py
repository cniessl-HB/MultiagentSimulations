"""
dist_sim_client.py - Distributed simulation client

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from basesimlib.base_masim_types import (
    some_action_stub,
    some_agent,
    some_log,
)

class dist_sim_agent(some_agent):
    """Base distributed agent."""

    def __init__(self, agent_id: str, host_sim_name) -> None:
        "Initialize the agent"
        self.agent_id: str = agent_id
        self.active: bool = True
        self.possible_actions: dict[str, callable] = {}
        self.next_action: str | None = None
        self.history_list: list[some_log] = []
        self.uuid: uuid.UUID = self._get_sim_uuid(host_sim_name)

    def _get_sim_uuid(self, host_sim_name) -> uuid.UUID
        raise NotImplementedError

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
