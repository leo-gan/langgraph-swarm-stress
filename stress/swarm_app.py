import logging
import random
import time

from langgraph_swarm import create_swarm

from stress.agent_stub_graph import StubAgentGraph
from stress.patterns import spawn_pattern
from stress.stats import StatsMonitor


def build_agents(config):
    agents = []
    for i in range(config["num_agents"]):
        ttl = random.randint(*config["ttl_range"])
        mem = random.randint(*config["memory_range"])
        agent = StubAgentGraph(i, ttl, mem, event_logger=None)
        agents.append(agent)
    return agents


def run_swarm(config):
    logging.info(f"[Swarm] Starting with {config['num_agents']} agents")

    agents = build_agents(config)

    stats = StatsMonitor(
        swarm=agents,
        interval=config.get("stats_interval", 5),
        outdir=config.get("log_dir", "logs"),
    )

    # Set event logger for each agent
    for agent in agents:
        agent.event_logger = stats.log_event

    # Create LangGraph swarm workflow using proper agent objects
    workflow = create_swarm(
        agents,  # list of StubAgentGraph objects
        default_active_agent="agent-0",  # string matching one of the agents
    )

    workflow.compile(checkpointer=None)

    stats.start()

    # Start agent spawning pattern
    spawn_pattern(workflow, config)

    # Wait until all agents finish
    while any(not a.state.get("done", False) for a in agents):
        time.sleep(1)

    stats.stop()
    logging.info("[Swarm] Finished all agents")
