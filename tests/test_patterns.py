# tests/test_patterns.py
import time
from unittest.mock import MagicMock, call

import pytest

from stress.patterns import spawn_pattern


@pytest.fixture
def mock_sleep(monkeypatch):
    """Mock time.sleep and return the mock object."""
    mock = MagicMock()
    monkeypatch.setattr(time, "sleep", mock)
    return mock


def create_mock_workflow(num_agents):
    """Helper to create a mock workflow with a specific number of agents."""
    workflow = MagicMock()
    workflow.nodes = {
        f"agent-{i}": MagicMock(runnable=MagicMock()) for i in range(num_agents)
    }
    # The spawn_pattern function iterates over workflow.nodes.items()
    # to build the agents_list.
    return workflow


def test_spawn_pattern_all_at_once(mock_sleep):
    """Test the 'all_at_once' spawn pattern."""
    mock_workflow = create_mock_workflow(10)
    config = {
        "pattern": {"type": "all_at_once"},
        "num_agents": 10,
    }

    spawn_pattern(mock_workflow, config)

    # Assert all agent entrypoints were called once
    for agent_node in mock_workflow.nodes.values():
        agent_node.runnable.invoke.assert_called_once_with({})

    mock_sleep.assert_not_called()


def test_spawn_pattern_bursts(mock_sleep):
    """Test the 'bursts' spawn pattern."""
    mock_workflow = create_mock_workflow(10)
    config = {
        "pattern": {
            "type": "bursts",
            "params": {"agents_per_burst": 3, "burst_interval": 1},
        },
        "num_agents": 10,
    }

    spawn_pattern(mock_workflow, config)

    # With handoff, only the first agent of each burst is invoked directly
    burst_indices = [0, 3, 6, 9]
    for i, agent_node in enumerate(mock_workflow.nodes.values()):
        if i in burst_indices:
            agent_node.runnable.invoke.assert_called_once_with({})
        else:
            agent_node.runnable.invoke.assert_not_called()

    # Assert time.sleep was called correctly
    # 10 agents, 3 per burst -> 4 bursts -> 4 sleeps
    assert mock_sleep.call_count == 4
    mock_sleep.assert_has_calls([call(1), call(1), call(1), call(1)])


def test_spawn_pattern_linear(mock_sleep):
    """Test the 'linear' spawn pattern."""
    mock_workflow = create_mock_workflow(5)
    config = {
        "pattern": {"type": "linear"},
        "num_agents": 5,
    }

    spawn_pattern(mock_workflow, config)

    # With handoff, only the first agent is invoked directly
    mock_workflow.nodes["agent-0"].runnable.invoke.assert_called_once_with({})
    for i in range(1, 5):
        mock_workflow.nodes[f"agent-{i}"].runnable.invoke.assert_not_called()

    # No sleep in the new linear pattern
    mock_sleep.assert_not_called()


def test_spawn_pattern_unknown(mock_sleep):
    """Test that an unknown pattern defaults to 'all_at_once'."""
    mock_workflow = create_mock_workflow(5)
    config = {
        "pattern": {"type": "unknown_pattern"},
        "num_agents": 5,
    }

    spawn_pattern(mock_workflow, config)

    # Assert all agents were called
    for agent_node in mock_workflow.nodes.values():
        agent_node.runnable.invoke.assert_called_once_with({})

    mock_sleep.assert_not_called()
