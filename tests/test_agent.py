"""
base_agent.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import pytest

from basesimlib.base_agent import base_agent
from basesimlib.base_exceptions import DuplicateAgentError
from basesimlib.base_simulation import base_simulation

def test_create_agent() -> None:
    """Testes the agent name is passed properly to a created agent."""
    new_agent = base_agent("ABC")
    assert new_agent.agent_id == "ABC"

def test_add_agent() -> None:
    """Tests that an agent can be added properly to a sim."""
    first_agent = base_agent("TEST_AGENT")
    test_sim = base_simulation("TEST_SIM")
    assert len(test_sim) == 0
    test_sim.add_agent(first_agent)
    assert len(test_sim) == 1

def test_add_agent_same_name() -> None:
    """Tests that trying to add an agent with the same name.
    
    This should raise the DuplicateAgentError."""
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    with pytest.raises(DuplicateAgentError):
        test_sim.add_agent(second_agent)

def test_add_agent_diff_name() -> None:
    """Tests that adding an agent with a different name in a sim.
    
    This checks the number of agents in the sim is 2 after 2 additions."""
    
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    assert len(test_sim) == 2

def test_get_sim_history() -> None:
    """Validate history stubs are created when added.
    
    This checks that two history stubs are created, and
    the records are in order.
    
    """
    number_to_add: int = 100
    test_sim = base_simulation("TEST_SIM")
    for ii in range(0, number_to_add):
        agent_name = f"TEST_AGENT_{ii:02d}"
        new_agent = base_agent(agent_name)
        test_sim.add_agent(new_agent)
    history_list = test_sim.dump_sim_history_list()
    assert len(history_list) == number_to_add
    assert all(history_list[ii] < history_list[ii + 1] for ii in range(0, len(history_list) - 1))
