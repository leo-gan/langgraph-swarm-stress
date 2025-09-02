# stress/swarm_runner.py
import logging, time, random
from stress.agent_stub import StubAgent
from stress.patterns import spawn_agents

def run_swarm(config):
    logging.info(f"[Swarm] Starting with {config['num_agents']} agents")
    agents = spawn_agents(config)

    # Run until all agents expire
    for agent in agents:
        agent.start()
    for agent in agents:
        agent.join()

    logging.info("[Swarm] Finished all agents")
