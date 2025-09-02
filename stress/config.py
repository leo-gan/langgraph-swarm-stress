# stress/config.py
CONFIG = {
    "num_agents": 2,
    "ttl_range": [0, 1],  # seconds
    "memory_range": [50, 150],  # MB
    "pattern": {
        "type": "all_at_once",  # all_at_once | bursts | linear
        "params": {"agents_per_burst": 5, "burst_interval": 3},
    },
    "log_level": "INFO",
    "stats_interval": 5,  # seconds
    "log_dir": "logs",  # where to save CSV/JSON
}
