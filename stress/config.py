# stress/config.py
CONFIG = {
    "num_agents": 20,
    "ttl_range": [5, 15],         # seconds
    "memory_range": [50, 150],    # MB
    "pattern": {
        "type": "bursts",   # all_at_once | bursts | linear
        "params": {
            "agents_per_burst": 5,
            "burst_interval": 3
        }
    },
    "log_level": "INFO",
    "stats_interval": 5,          # seconds
    "log_dir": "logs"             # where to save CSV/JSON
}
