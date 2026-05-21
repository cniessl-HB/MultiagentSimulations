"""
base_agent.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from basesimlib.base_agent import base_agent

def test_create_agent() -> None:
    new_agent = base_agent("ABC")
    assert new_agent.agent_id == "ABC"
