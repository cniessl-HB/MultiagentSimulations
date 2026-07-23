"""
test_typing.py - Common interface class for individual agents

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import pytest

from datetime import datetime

from basesimlib.base_masim_types import (
    some_log,
    some_action,
    some_action_stub,
    some_agent,
    some_sim,
)


class fake_log_entry(some_log):
    def get_step(self) -> int:
        return super().get_step()

    def get_action_time(self) -> datetime:
        return super().get_action_time()

    def __lt__(self, other) -> bool:
        return super().__lt__(other)

    def __eq__(self, other) -> bool:
        return super().__eq__(other)


class fake_action_stub(some_action_stub):
    def apply(self, simulation) -> some_log:
        return super().apply(simulation)

    def get_initiator_id(self) -> str:
        return super().get_initiator_id()

    def get_target_id(self) -> str:
        return super().get_target_id()


class fake_action(some_action):
    def create_stub(self, target_id: str) -> some_action_stub:
        return super().create_stub(target_id)


class fake_agent(some_agent):
    def get_id(self) -> str:
        return super().get_id()

    def is_active(self) -> bool:
        return super().is_active()

    def plan_action(self) -> some_action_stub:
        return super().plan_action()

    def set_active(self, active_val: bool) -> None:
        return super().set_active(active_val)

    def add_to_history(self, log_entry) -> None:
        return super().add_to_history(log_entry)

    def get_history(self) -> list[some_log]:
        return super().get_history()


class fake_sim(some_sim):
    def get_step(self) -> int:
        return super().get_step()


def test_unimpl_log_entry() -> None:

    class incomplete_log_entry(some_log):
        pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        _ = incomplete_log_entry()


def test_incomplete_log_entry_impl() -> None:
    test_log = fake_log_entry()

    with pytest.raises(NotImplementedError):
        test_log.get_step()
    with pytest.raises(NotImplementedError):
        test_log.get_action_time()
    with pytest.raises(NotImplementedError):
        test_log.__lt__(test_log)
    with pytest.raises(NotImplementedError):
        test_log.__eq__(test_log)


def test_unimpl_action_stub() -> None:
    class incomplete_action_stub(some_action_stub):
        pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        _ = incomplete_action_stub()


def test_incomplete_masim_action_stub_impl() -> None:

    test_action = fake_action_stub()

    with pytest.raises(NotImplementedError):
        test_action.apply(None)
    with pytest.raises(NotImplementedError):
        test_action.get_initiator_id()
    with pytest.raises(NotImplementedError):
        test_action.get_target_id()


def test_unimpl_action() -> None:
    class incomplete_action(some_action):
        pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        _ = incomplete_action()


def test_incomplete_masim_action_impl() -> None:
    test_action = fake_action()

    with pytest.raises(NotImplementedError):
        test_action.create_stub("")


def test_unimpl_agent() -> None:
    class incomplete_agent(some_agent):
        pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        _ = incomplete_agent()


def test_incomplete_agent_impl() -> None:
    test_agent = fake_agent()

    with pytest.raises(NotImplementedError):
        test_agent.get_id()

    with pytest.raises(NotImplementedError):
        test_agent.is_active()

    with pytest.raises(NotImplementedError):
        test_agent.plan_action()

    with pytest.raises(NotImplementedError):
        test_agent.set_active(False)

    with pytest.raises(NotImplementedError):
        test_agent.add_to_history(fake_log_entry())

    with pytest.raises(NotImplementedError):
        test_agent.get_history()


def test_unimpl_sim() -> None:
    class incomplete_sim(some_sim):
        pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        _ = incomplete_sim()


def test_incomplete_sim_impl() -> None:
    test_sim = fake_sim()
    with pytest.raises(NotImplementedError):
        test_sim.get_step()
