# API Reference

## Core Classes

### StubAgent

```python
class StubAgent:
    def __init__(self, agent_id: int, ttl: int, memory_mb: int, event_logger=None)
    def act(self, state: dict) -> dict
```

Basic agent implementation with memory allocation and lifecycle management.

**Parameters:**
- `agent_id` (int): Unique identifier
- `ttl` (int): Time-to-live in seconds
- `memory_mb` (int): Memory to allocate in MB
- `event_logger` (callable, optional): Event callback function

**Returns:**
- `dict`: State with `done` boolean

### StubAgentGraph

```python
class StubAgentGraph:
    def __init__(self, agent_id, ttl, mem, event_logger=None, handoff_tool=None)
    def get_graph(self) -> CompiledGraph
```

LangGraph-compatible agent wrapper.

### StatsMonitor

```python
class StatsMonitor:
    def __init__(self, swarm: list, interval: int = 5, outdir: str = "logs")
    def start(self) -> None
    def stop(self) -> None
    def log_event(self, event: dict) -> None
```

Collects runtime statistics and exports to CSV.

**Parameters:**
- `swarm` (list): List of agent instances
- `interval` (int): Collection interval in seconds
- `outdir` (str): Output directory for logs

## Functions

### build_agents

```python
def build_agents(config: dict) -> list[StubAgentGraph]
```

Creates agents based on configuration pattern.

### run_swarm

```python
def run_swarm(config: dict) -> None
```

Main execution function. Runs the complete stress test.

## Configuration Schema

```python
CONFIG = {
    "num_agents": int,        # Total agents to spawn
    "ttl_range": [int, int],  # [min, max] seconds
    "memory_range": [int, int],  # [min, max] MB
    "pattern": {
        "type": str,          # "linear" | "bursts" | "all_at_once"
        "params": dict        # Pattern-specific parameters
    },
    "log_level": str,         # "DEBUG" | "INFO" | "WARNING" | "ERROR"
    "stats_interval": int,    # Seconds between stats collection
    "log_dir": str            # Output directory path
}
```
