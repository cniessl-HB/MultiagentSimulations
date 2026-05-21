"""
base_agent.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from basesimlib.base_agent import base_agent
from basesimlib.base_simulation import base_simulation

def test_create_agent() -> None:
    new_agent = base_agent("ABC")
    assert new_agent.agent_id == "ABC"

def test_add_agent() -> None:
    first_agent = base_agent("TEST_AGENT")
    test_sim = base_simulation("TEST_SIM")
    assert len(test_sim) == 0
    test_sim.add_agent(first_agent)
    assert len(test_sim) == 1
