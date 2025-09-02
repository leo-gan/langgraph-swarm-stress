#!/usr/bin/env python3
import logging
from pathlib import Path
from stress.swarm_app import run_swarm
from stress.config import CONFIG

def main():
    # Set up logging
    log_dir = Path(CONFIG.get("log_dir", "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, CONFIG.get("log_level", "INFO")),
        format="[%(asctime)s] %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "swarm_run.log"),
            logging.StreamHandler()
        ]
    )

    logging.info("=== Starting LangGraph Swarm Stress Test ===")
    run_swarm(CONFIG)
    logging.info("=== Finished LangGraph Swarm Stress Test ===")

if __name__ == "__main__":
    main()
