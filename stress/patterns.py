# stress/patterns.py
import logging
import time


def spawn_pattern(workflow, config):
    """
    Spawn agents according to the pattern in config.
    workflow: LangGraph compiled workflow returned by create_swarm
    config: {
        "pattern": {"type": ..., "params": ...},
        "num_agents": ...,
    }
    """
    pattern = config.get("pattern", {"type": "all_at_once"})
    pattern_type = pattern.get("type", "all_at_once")
    params = pattern.get("params", {})

    # Adapt to new langgraph_swarm which doesn't have .agents_list
    # The nodes of the swarm graph are the agents.
    agents_list = []
    for name, agent_node_spec in workflow.nodes.items():
        # Heuristic to identify agent nodes
        if "agent-" in name:
            # The value is a StateNodeSpec, the runnable is at .runnable
            agents_list.append({"id": name, "entrypoint": agent_node_spec.runnable})

    if pattern_type == "all_at_once":
        logging.info(f"[Swarm] Launching all {len(agents_list)} agents at once")
        for agent in agents_list:
            # call agent entrypoint asynchronously if needed
            agent["entrypoint"].invoke({})

    elif pattern_type == "bursts":
        burst_size = params.get("agents_per_burst", 5)
        interval = params.get("burst_interval", 3)
        logging.info(
            f"[Swarm] Launching agents in bursts: {burst_size} every {interval}s"
        )

        for i in range(0, len(agents_list), burst_size):
            # For each burst, start only the first agent.
            # The rest will be started by the handoff chain.
            first_agent_in_burst = agents_list[i]
            first_agent_in_burst["entrypoint"].invoke({})
            time.sleep(interval)

    elif pattern_type == "linear":
        # In a linear pattern, agents are chained. We only need to start the first one.
        logging.info("[Swarm] Launching agents in a linear chain")
        if agents_list:
            agents_list[0]["entrypoint"].invoke({})

    else:
        logging.warning(
            f"[Swarm] Unknown pattern type '{pattern_type}', defaulting to all_at_once"
        )
        for agent in agents_list:
            agent["entrypoint"].invoke({})
