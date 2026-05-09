# LangGraph Swarm Stress Testing Tool

A configurable stress testing framework for LangGraph agent swarms. This tool simulates multi-agent workloads with controlled memory consumption, lifecycle patterns, and execution strategies.

## Features

- **Multiple Spawn Patterns**: linear, bursts, all_at_once
- **Resource Simulation**: Configurable TTL and memory allocation per agent
- **Real-time Monitoring**: CPU, memory, and agent lifecycle statistics
- **Visualization**: Matplotlib-based plotting of execution metrics
- **LangGraph Integration**: Built on `langgraph-swarm` for realistic swarm behavior

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd langgraph-swarm-stress

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"
```

### Run a Stress Test

```bash
# Using the run script
python scripts/run_stress.py

# Or using the CLI entry point
swarm-stress
```

## Configuration

Edit `stress/config.py` to customize test parameters:

```python
CONFIG = {
    "num_agents": 3,
    "ttl_range": [1, 3],  # seconds
    "memory_range": [50, 150],  # MB
    "pattern": {
        "type": "linear",  # all_at_once | bursts | linear
        "params": {"agents_per_burst": 5, "burst_interval": 3},
    },
    "log_level": "INFO",
    "stats_interval": 5,  # seconds
    "log_dir": "logs",  # where to save CSV/JSON
}
```

### Spawn Patterns

- **`linear`**: Agents start sequentially, each handing off to the next
- **`bursts`**: Agents spawn in configurable burst sizes with intervals
- **`all_at_once`**: All agents start simultaneously (no handoffs)

## Project Structure

```
langgraph-swarm-stress/
├── stress/
│   ├── __init__.py
│   ├── agent_stub.py         # Basic agent implementation
│   ├── agent_stub_graph.py   # LangGraph-compatible agent wrapper
│   ├── config.py             # Test configuration
│   ├── patterns.py           # Spawn pattern implementations
│   ├── stats.py              # Statistics collection and monitoring
│   └── swarm_app.py          # Main swarm orchestration
├── scripts/
│   ├── plot_stats.py         # Visualization script
│   └── run_stress.py         # Main execution script
├── tests/
│   ├── test_patterns.py      # Pattern unit tests
│   └── test_stats.py         # Stats unit tests
├── docs/                     # Documentation
├── LICENSE                   # MIT License
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Development

### Code Quality

```bash
# Format code
black stress/ scripts/ tests/
isort stress/ scripts/ tests/

# Lint
ruff check stress/ scripts/ tests/
mypy stress/

# Run tests
pytest tests/ -v --cov=stress
```

### Adding New Patterns

1. Implement the pattern function in `stress/patterns.py`
2. Add tests in `tests/test_patterns.py`
3. Update configuration schema in `stress/config.py`

## Documentation

See the `docs/` folder for detailed documentation:

- `docs/usage.md` - Detailed usage guide
- `docs/architecture.md` - System architecture and design
- `docs/api.md` - API reference

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
