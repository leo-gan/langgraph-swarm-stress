# tests/test_patterns.py
import pytest
from unittest.mock import MagicMock, call
from stress.patterns import spawn_pattern
import time

@pytest.fixture
def mock_sleep(monkeypatch):
    """Mock time.sleep and return the mock object."""
    mock = MagicMock()
    monkeypatch.setattr(time, "sleep", mock)
    return mock

def create_mock_workflow(num_agents):
    """Helper to create a mock workflow with a specific number of agents."""
    workflow = MagicMock()
    workflow.agents_list = [
        {"id": f"agent_{i}", "entrypoint": MagicMock()} for i in range(num_agents)
    ]
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
    for agent in mock_workflow.agents_list:
        agent["entrypoint"].assert_called_once_with({})

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

    # Assert all agent entrypoints were called
    for agent in mock_workflow.agents_list:
        agent["entrypoint"].assert_called_once_with({})

    # Assert time.sleep was called correctly
    # 10 agents, 3 per burst -> 4 bursts -> 4 sleeps
    assert mock_sleep.call_count == 4
    mock_sleep.assert_has_calls([call(1), call(1), call(1), call(1)])


def test_spawn_pattern_linear(mock_sleep):
    """Test the 'linear' spawn pattern."""
    mock_workflow = create_mock_workflow(5)
    config = {
        "pattern": {
            "type": "linear",
            "params": {"start_time_sec": 0, "stop_time_sec": 10},
        },
        "num_agents": 5,
    }

    spawn_pattern(mock_workflow, config)

    # Assert all agent entrypoints were called
    for agent in mock_workflow.agents_list:
        agent["entrypoint"].assert_called_once_with({})

    # 5 agents over 10s = 2s interval
    assert mock_sleep.call_count == 5
    mock_sleep.assert_has_calls([call(2.0), call(2.0), call(2.0), call(2.0), call(2.0)])

def test_spawn_pattern_unknown(mock_sleep):
    """Test that an unknown pattern defaults to 'all_at_once'."""
    mock_workflow = create_mock_workflow(5)
    config = {
        "pattern": {"type": "unknown_pattern"},
        "num_agents": 5,
    }

    spawn_pattern(mock_workflow, config)

    # Assert all agents were called
    for agent in mock_workflow.agents_list:
        agent["entrypoint"].assert_called_once_with({})

    mock_sleep.assert_not_called()
