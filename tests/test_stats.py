# tests/test_stats.py
import pytest
from unittest.mock import MagicMock, patch, mock_open
import time
import json
import csv
from pathlib import Path

from stress.stats import StatsMonitor

@pytest.fixture
def mock_swarm():
    """Fixture for a mock swarm object."""
    swarm = MagicMock()
    swarm.agents = [
        MagicMock(state={"done": False}),
        MagicMock(state={"done": True}),
        MagicMock(state={"done": False}),
    ]
    return swarm

@pytest.fixture
def stats_monitor(mock_swarm, tmp_path):
    """Fixture for a StatsMonitor instance."""
    # Patch time.time before creating the monitor to control start_time
    monitor = StatsMonitor(mock_swarm, interval=1, outdir=str(tmp_path))
    monitor.start_time = 1000.0  # Set a fixed start time for tests
    return monitor


def test_stats_monitor_init(stats_monitor, mock_swarm, tmp_path):
    """Test initialization of StatsMonitor."""
    assert stats_monitor.swarm == mock_swarm
    assert stats_monitor.interval == 1
    assert stats_monitor.outdir == tmp_path
    assert stats_monitor.start_time == 1000.0
    assert not stats_monitor._stop.is_set()

def test_log_event(stats_monitor):
    """Test the log_event method."""
    with patch("time.time", return_value=1005.0):
        event = {"event": "agent_start", "agent_id": "agent_1"}
        stats_monitor.log_event(event)

    assert len(stats_monitor.records) == 1
    assert stats_monitor.records[0] == {
        "event": "agent_start",
        "agent_id": "agent_1",
        "time_sec": 5.0,  # 1005.0 - 1000.0
    }

def test_run_single_iteration(stats_monitor, mock_swarm):
    """Test a single iteration of the _run loop."""
    with patch("time.time", side_effect=[1001.0, 1001.0]), \
         patch("psutil.cpu_percent", return_value=50.5) as mock_cpu, \
         patch("psutil.virtual_memory") as mock_mem, \
         patch("time.sleep"), \
         patch.object(stats_monitor._stop, "is_set", side_effect=[False, True]):

        mock_mem.return_value.percent = 75.5

        stats_monitor._run()

        assert len(stats_monitor.records) == 1
        record = stats_monitor.records[0]
        assert record == {
            "event": "stats_tick",
            "time_sec": 1.0,
            "active_agents": 2,  # 2 not done
            "total_agents": 3,
            "cpu_percent": 50.5,
            "mem_percent": 75.5,
        }
        mock_cpu.assert_called_once()
        mock_mem.assert_called_once()


def test_save(stats_monitor, tmp_path):
    """Test the _save method."""
    stats_monitor.records = [
        {"event": "stats_tick", "time_sec": 1.0, "cpu_percent": 10},
        {"event": "agent_start", "time_sec": 1.1, "agent_id": "a1"},
    ]

    with patch("time.strftime", return_value="20240101-120000"):
        stats_monitor._save()

    json_path = tmp_path / "stats_20240101-120000.json"
    csv_path = tmp_path / "stats_20240101-120000.csv"

    assert json_path.exists()
    assert csv_path.exists()

    # Verify JSON content
    with open(json_path, "r") as f:
        data = json.load(f)
    assert data == stats_monitor.records

    # Verify CSV content
    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        # Check that all keys are present in the header
        assert "event" in reader.fieldnames
        assert "time_sec" in reader.fieldnames
        assert "cpu_percent" in reader.fieldnames
        assert "agent_id" in reader.fieldnames
        # Check data
        assert rows[0] == {"event": "stats_tick", "time_sec": "1.0", "cpu_percent": "10", "agent_id": ""}
        assert rows[1] == {"event": "agent_start", "time_sec": "1.1", "cpu_percent": "", "agent_id": "a1"}
