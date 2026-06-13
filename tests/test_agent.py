"""
base_agent.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import pytest

from datetime import datetime

from basesimlib.base_agent import base_agent
from basesimlib.base_masim_types import some_log, some_action_stub
from basesimlib.base_log_entry import base_log_entry
from basesimlib.base_exceptions import AgentNotFoundError, DeactivateInactiveAgentError, DuplicateAgentError
from basesimlib.base_simulation import base_simulation

def test_incomplete_masim_log_impl() -> None:
    class incomplete_log_entry(some_log):
        pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        test_log = incomplete_log_entry()
    
    class fake_log_entry(some_log):
        
        def get_step(self) -> int:
            return super().get_step()
        
        def get_action_time(self) -> datetime:
            return super().get_action_time()
        
        def __lt__(self, other) -> bool:
            return super().__lt__(other)
    
        def __eq__(self, other) -> bool:
            return super().__eq__(other)
    
    test_log2 = fake_log_entry()
    
    with pytest.raises(NotImplementedError):
        test_log2.get_step()
    with pytest.raises(NotImplementedError):
        test_log2.get_action_time()
    with pytest.raises(NotImplementedError):
        test_log2.__lt__(test_log2)
    with pytest.raises(NotImplementedError):
        test_log2.__eq__(test_log2)

def test_incomplete_masim_action_impl() -> None:
    class incomplete_action_stub(some_action_stub):
        pass
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        test_log = incomplete_action_stub()

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


def test_deactivate_agent() -> None:
    """Tests that deactivating an agent moves it to the inactive group."""
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    test_sim.deactivate_agent("TEST_AGENT")
    assert len(test_sim) == 2
    assert len(test_sim.inactive_agents) == 1
    assert len(test_sim.active_agents) == 1


def test_deactivate_non_existant_agent() -> None:
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    with pytest.raises(AgentNotFoundError):
        test_sim.deactivate_agent("TEST_AGENT3")

def test_deactivate_already_deactivated_agent() -> None:
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    test_sim.deactivate_agent("TEST_AGENT2")
    with pytest.raises(DeactivateInactiveAgentError):
        test_sim.deactivate_agent("TEST_AGENT2")

def test_advance_sim_step() -> None:
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    test_sim.advance_step()
    assert test_sim.sim_step == 1


def test_catch_invalid_history_comparison() -> None:
    sim_name = "TEST_SIM"
    agent_name = "TEST_AGENT"
    fake_log_entry = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    f"Actual Log")   
    assert fake_log_entry != sim_name

def test_history_ordering() -> None:
    """Validate timestamp and step ordering of logged events."""
    sim_name = "TEST_SIM"
    agent_name = "TEST_AGENT"
    
    fake_log_entry_first = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    f"Earliest Log")
    fake_log_entry_second = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    f"Earliest Log")
    same_is_equal = (fake_log_entry_first == fake_log_entry_first)
    two_in_order_not_equal = (fake_log_entry_first != fake_log_entry_second)
    assert same_is_equal
    assert two_in_order_not_equal
    
    fake_log_entry_first.step = 1
    first_comes_first = (fake_log_entry_first < fake_log_entry_second)
    second_comes_first = (fake_log_entry_first > fake_log_entry_second)
    diff_steps_not_eq = (fake_log_entry_first == fake_log_entry_second)
    assert first_comes_first is False
    assert second_comes_first
    assert diff_steps_not_eq is False


def test_get_sim_history() -> None:
    """Validate sim history stubs are created when added.
    
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


def test_get_agents_histories() -> None:
    """Validate active agent history stubs are created when added.
    
    This checks that a fake history entry for each agent is present
    and the records are in otder.
    """
    number_to_add: int = 100
    sim_name = "TEST_SIM"
    test_sim = base_simulation(sim_name)
    for ii in range(0, number_to_add):
        agent_name = f"TEST_AGENT_{ii:02d}"
        new_agent = base_agent(agent_name)
        fake_log_entry = base_log_entry(sim_name, 
                                        agent_name,
                                        test_sim.sim_step,
                                        f"Added to {sim_name}")
        new_agent.add_to_history(fake_log_entry)
        test_sim.add_agent(new_agent)
    history_list = test_sim.dump_sim_active_agent_history_list()
    assert len(history_list) == number_to_add
    assert all(history_list[ii] < history_list[ii + 1] for ii in range(0, len(history_list) - 1))

        
