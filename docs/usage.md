# Usage Guide

## Getting Started

### Prerequisites

- Python 3.12+
- uv (recommended) or pip

### Installation

```bash
# Clone and install dependencies
uv sync
```

### Running Tests

```bash
# Run stress test
python scripts/run_stress.py

# Visualize results
python scripts/plot_stats.py
```

## Configuration Options

### Spawn Patterns

**Linear Pattern**
```python
"pattern": {
    "type": "linear",
    "params": {}
}
```
Agents spawn one after another, with each agent handing off to the next.

**Burst Pattern**
```python
"pattern": {
    "type": "bursts",
    "params": {
        "agents_per_burst": 5,
        "burst_interval": 3
    }
}
```
Agents spawn in groups with configurable intervals.

**All at Once**
```python
"pattern": {
    "type": "all_at_once",
    "params": {}
}
```
All agents start simultaneously.

## Output Files

- `logs/swarm_run.log` - Execution logs
- `logs/stats.csv` - Runtime statistics
- `plots/` - Visualization outputs
