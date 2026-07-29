"""
base_agent.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import pytest

from basesimlib.base_agent import base_agent
from basesimlib.base_log_entry import base_log_entry
from basesimlib.base_action_stub import base_action_stub
from basesimlib.base_exceptions import (
    AgentNotFoundError,
    DeactivateInactiveAgentError,
    DuplicateAgentError,
    AgentAssignedNoneError,
)
from basesimlib.base_simulation import base_simulation


def test_create_agent() -> None:
    """Testes the agent name is passed properly to a created agent."""
    new_agent = base_agent("ABC")
    assert new_agent.agent_id == "ABC"


def test_sim_add_agent() -> None:
    """Tests that an agent can be added properly to a sim."""
    first_agent = base_agent("TEST_AGENT")
    test_sim = base_simulation("TEST_SIM")
    assert len(test_sim) == 0
    test_sim.add_agent(first_agent)
    assert len(test_sim) == 1


def test_sim_add_agent_same_name() -> None:
    """Tests that trying to add an agent with the same name.

    This should raise the DuplicateAgentError."""
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    with pytest.raises(DuplicateAgentError):
        test_sim.add_agent(second_agent)


def test_sim_add_agent_diff_name() -> None:
    """Tests that adding an agent with a different name in a sim.

    This checks the number of agents in the sim is 2 after 2 additions."""

    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    assert len(test_sim) == 2


def test_sim_deactivate_agent() -> None:
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


def test_sim_deactivate_non_existant_agent() -> None:
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    with pytest.raises(AgentNotFoundError):
        test_sim.deactivate_agent("TEST_AGENT3")


def test_sim_deactivate_already_deactivated_agent() -> None:
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    test_sim.deactivate_agent("TEST_AGENT2")
    with pytest.raises(DeactivateInactiveAgentError):
        test_sim.deactivate_agent("TEST_AGENT2")


def test_sim_catch_none_assigned() -> None:
    first_agent = base_agent("TEST_AGENT")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.active_agents["TEST_AGENT"] = None
    with pytest.raises(AgentAssignedNoneError):
        test_sim.deactivate_agent("TEST_AGENT")


def test_sim_cleanup_inactive_agents() -> None:
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    first_agent.set_active(False)
    second_agent.set_active(False)
    test_sim.cleanup()
    assert len(test_sim.active_agents) == 0


def test_sim_advance_step() -> None:
    first_agent = base_agent("TEST_AGENT")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    test_sim.advance_step()
    assert test_sim.sim_step == 1


def test_agent_interaction_gen_history() -> None:
    """Validate agent interactions generate history stubs."""
    first_agent = base_agent("TEST_AGENT1")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    hist1 = first_agent.get_history()
    hist2 = second_agent.get_history()
    assert len(hist1) == 1
    assert len(hist1) == len(hist2)
    action_to_apply: base_action_stub = base_action_stub("TEST_AGENT1", "TEST_AGENT2")
    test_sim.apply_action(action_to_apply)
    hist1 = first_agent.get_history()
    hist2 = second_agent.get_history()
    assert len(hist1) == 2
    assert len(hist1) == len(hist2)
    assert hist1[1].initiator_id == "TEST_AGENT1"
    assert hist1[1].initiator_id == hist2[1].initiator_id
    assert hist1[1].other_id == "TEST_AGENT2"
    assert hist2[1].other_id == hist2[1].other_id
    assert hist1[1].step == hist2[1].step


def test_sim_get_history_agents_added() -> None:
    """Validate sim history stubs are created when agents are added.

    This checks that two history stubs are created, and
    the records are in order.

    """
    number_to_add: int = 100
    sim_name = "TEST_SIM"
    test_sim = base_simulation(sim_name)
    for ii in range(0, number_to_add):
        agent_name = f"TEST_AGENT_{ii:02d}"
        new_agent = base_agent(agent_name)
        test_sim.add_agent(new_agent)
    history_list = test_sim.dump_sim_history_list()
    assert len(history_list) == number_to_add
    assert all(
        history_list[ii] < history_list[ii + 1]
        for ii in range(0, len(history_list) - 1)
    )


def test_sim_get_history_active_agents() -> None:
    """Validate active agent history stubs are fetched.

    This checks that the creation history entry for each agent
    is present and the records are in otder.
    """
    number_to_add: int = 100
    sim_name = "TEST_SIM"
    test_sim = base_simulation(sim_name)
    for ii in range(0, number_to_add):
        agent_name = f"TEST_AGENT_{ii:02d}"
        new_agent = base_agent(agent_name)
        test_sim.add_agent(new_agent)
    history_list = test_sim.dump_sim_active_agent_history_list()
    assert len(history_list) == number_to_add
    assert all(
        history_list[ii] < history_list[ii + 1]
        for ii in range(0, len(history_list) - 1)
    )


def test_sim_get_history_inactive_agents() -> None:
    """Validate fetching history from inactive agents.

    This checks that the creation history entry for each
    deactivated agent is present and the records are in otder.
    """
    number_to_add: int = 100
    sim_name = "TEST_SIM"
    test_sim = base_simulation(sim_name)
    for ii in range(0, number_to_add):
        agent_name = f"TEST_AGENT_{ii:02d}"
        new_agent = base_agent(agent_name)
        test_sim.add_agent(new_agent)
        test_sim.deactivate_agent(agent_name)
    history_list = test_sim.dump_sim_active_agent_history_list()
    assert len(history_list) == 0
    history_list = test_sim.dump_sim_inactive_agent_history_list()
    assert len(history_list) == number_to_add
    assert all(
        history_list[ii] < history_list[ii + 1]
        for ii in range(0, len(history_list) - 1)
    )


def test_sim_filter_duplicate_history_singleton() -> None:
    """Validate early exit if only one item in history list."""
    test_sim = base_simulation("TEST_SIM")
    test_event = base_log_entry("TEST_SIM", "", 0, "")
    test_sim.sim_act_history.append(test_event)
    history_dump = test_sim.dump_full_history_list()
    assert len(history_dump) == 1


def test_sim_filter_duplicate_history() -> None:
    """Validate no duplicates in generated history list."""
    first_agent = base_agent("TEST_AGENT1")
    second_agent = base_agent("TEST_AGENT2")
    test_sim = base_simulation("TEST_SIM")
    test_sim.add_agent(first_agent)
    test_sim.add_agent(second_agent)
    history_dump = test_sim.dump_full_history_list()
    dup_check_dict = {}
    for elem in history_dump:
        elem_key = elem.get_uuid()
        if elem_key in dup_check_dict:
            raise Exception
        dup_check_dict[elem_key] = elem
    assert len(history_dump) == 2
