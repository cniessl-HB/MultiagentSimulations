"""
base_agent.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from basesimlib.base_masim_types import some_action, some_action_stub, some_agent, some_log

from basesimlib.base_action_stub import base_action_stub

class base_agent(some_agent):
    """Placeholder for base agent.
    
    Agents have an ID, state, and maintain a history of
    interactions.
    
    Agents have an active flag, defaulting to true. If
    it's set False, then an agent is removed during the
    cleanup phase of a simulation.
    
    """ 
    
    def __init__(self, agent_id: str) -> None:
        "Initialize the agent"
        self.agent_id: str = agent_id
        self.active: bool = True
        self.possible_actions: dict[str, some_action] = {}
        self.history_list: list[some_log] = []
    
    def get_id(self) -> str:
        return self.agent_id
    
    def is_active(self) -> bool:
        return self.active
    
    def set_active(self, active_val: bool) -> None:
        self.active = active_val
    
    def plan_action(self) -> some_action_stub:
        """Override this function with planning method."""
        return base_action_stub(self.agent_id, "")
    
    def add_to_history(self, log_entry: some_log) -> None:
        """Add to this agent's history."""
        self.history_list.append(log_entry)
    
    def get_history(self) -> list[some_log]:
        """Return the history of interactions."""
        return self.history_list
