# Architecture

## System Overview

The LangGraph Swarm Stress Testing Tool simulates multi-agent workloads using LangGraph's swarm capabilities.

## Components

### Agent Stub (`agent_stub.py`)

Simple agent class that:
- Allocates configured memory on start
- Runs for a configurable TTL (time-to-live)
- Reports lifecycle events

### Agent Graph Wrapper (`agent_stub_graph.py`)

Wraps `StubAgent` as a LangGraph-compatible agent:
- Implements required LangGraph interfaces
- Manages handoff tools for swarm coordination

### Spawn Patterns (`patterns.py`)

Implements three spawn strategies:
1. **Linear**: Sequential agent creation with handoffs
2. **Bursts**: Batch spawning with intervals
3. **All at Once**: Simultaneous creation

### Statistics Monitor (`stats.py`)

Collects runtime metrics:
- System resources (CPU, memory)
- Agent lifecycle events
- CSV/JSON export for analysis

### Swarm Orchestrator (`swarm_app.py`)

Main entry point:
- Builds agent configurations
- Creates LangGraph swarm workflow
- Coordinates pattern execution
- Manages statistics collection

## Data Flow

1. Configuration loaded from `config.py`
2. `build_agents()` creates agents based on pattern
3. `StatsMonitor` starts background collection
4. `spawn_pattern()` executes the spawn strategy
5. Agents run via LangGraph swarm
6. Stats export when complete

## Integration Points

- **LangGraph Swarm**: `create_swarm()` for workflow creation
- **LangGraph Handoffs**: `create_handoff_tool()` for agent transitions
- **psutil**: System resource monitoring
- **matplotlib**: Results visualization
