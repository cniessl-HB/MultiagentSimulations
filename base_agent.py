"""
base_agent.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

class base_agent(some_agent):
    """Placeholder for base agent.
    
    Agents have an ID, state, and maintain a history of
    interactions.
    
    """ 
    
    def __init__(self, agent_id: str) -> None:
        "Initialize the agent"
        self.agent_id: str = agent_id
        self.agent_state: any = None
        self.possible_interacts: list = []
        self.history_list: list = []
    
    def plan_action(self) -> base_action:
        """Override this function with planning method."""
        raise NotImplemented
    
    def interact(self, other: some_agent) -> None:
        """Override this function with interaction method."""
        raise NotImplemented
    
    def audit_history(self) -> list[some_log]:
        """Return the history of interactions."""
        return self.history_list
