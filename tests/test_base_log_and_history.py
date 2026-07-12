"""
test_base_log_and_history.py - Unit tests for logging and history comparison

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import json
import pytest

from basesimlib.base_agent import base_agent
from basesimlib.base_log_entry import base_log_entry


def test_history_invalid_comparison() -> None:
    """Assert exceptions with invalid comparisons."""
    sim_name = "TEST_SIM"
    agent_name = "TEST_AGENT"
    fake_log_entry = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    "Actual Log")   
    assert fake_log_entry != sim_name


def test_history_same_step_ordering() -> None:
    """Validate timestamp and step ordering of logged events.
    
    Log events sharing the same step and time in the simulation
    are considered simultaneous and equal."""
    sim_name = "TEST_SIM"
    agent_name = "TEST_AGENT"
    
    fake_log_entry_first = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    "Earliest Log")
    fake_log_entry_second = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    "Earliest Log")
    same_is_equal = (fake_log_entry_first == fake_log_entry_first)
    two_in_order_not_equal = (fake_log_entry_first != fake_log_entry_second)
    assert same_is_equal
    assert two_in_order_not_equal


def test_history_diff_step_ordering() -> None:
    """Validate timestamp and step ordering of logged events.
    
    Log events are ordered by step, then time, in the simulation.
    If an event happens at a later step, but earlier time, this
    is still considered a later event.
    """
    sim_name = "TEST_SIM"
    agent_name = "TEST_AGENT"
    
    fake_log_entry_first = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    "Earliest Log")
    fake_log_entry_second = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    "Next Log")
    
    fake_log_entry_first.step = 1
    first_comes_first = (fake_log_entry_first < fake_log_entry_second)
    second_comes_first = (fake_log_entry_first > fake_log_entry_second)
    diff_steps_not_eq = (fake_log_entry_first == fake_log_entry_second)
    assert first_comes_first is False
    assert second_comes_first
    assert diff_steps_not_eq is False


def test_history_ordering_sync() -> None:
    """Validate timestamp and step ordering of logged events.
    
    Sync is used to reassign timing to events if they need to
    be set to the same time."""
    sim_name = "TEST_SIM"
    agent_name = "TEST_AGENT"    
    fake_log_entry_first = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    "Earliest Log")
    fake_log_entry_second = base_log_entry(sim_name, 
                                    agent_name,
                                    0,
                                    "Earliest Log")
    first_comes_first = (fake_log_entry_first < fake_log_entry_second)
    assert first_comes_first is True
    fake_log_entry_first.synchronize_to_event(fake_log_entry_second)
    first_comes_first = (fake_log_entry_first < fake_log_entry_second)
    assert first_comes_first is False
    assert fake_log_entry_first == fake_log_entry_second


def test_history_str_output() -> None:
    """Validate the str decorator produces its expected output."""
    agent_name1 = "TEST_AGENT_A"
    agent_name2 = "TEST_AGENT_B"
    log_message = "A log message would be here."
    fake_log_entry = base_log_entry(agent_name1, 
                                   agent_name2,
                                   0,
                                   log_message)
    log_out_str = str(fake_log_entry)
    assert agent_name1 in log_out_str
    assert agent_name2 in log_out_str
    assert "0" in log_out_str


def test_history_json_dump() -> None:
    """Validate the json decorator produces valid json output."""
    fake_log_entry = base_log_entry("", "", 0, "")
    fake_log_entry_dump = fake_log_entry.__json__()
    assert json.loads(fake_log_entry_dump)
