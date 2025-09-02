# stress/agent_stub.py
import time, logging

class StubAgent:
    def __init__(self, agent_id: int, ttl: int, memory_mb: int, event_logger=None):
        self.id = agent_id
        self.ttl = ttl
        self.memory_mb = memory_mb
        self.memory = []
        self.start_time = None
        self.event_logger = event_logger

    def act(self, state: dict) -> dict:
        if self.start_time is None:
            self.start_time = time.time()
            logging.info(f"[Agent-{self.id}] Start | ttl={self.ttl}s | mem={self.memory_mb}MB")
            self.memory = ["x" * 1024 * 1024] * self.memory_mb

            if self.event_logger:
                self.event_logger(
                    {
                        "event": "agent_start",
                        "agent_id": self.id,
                        "ttl": self.ttl,
                        "memory_mb": self.memory_mb,
                        "time_sec": 0.0,
                    }
                )

        elapsed = time.time() - self.start_time
        if elapsed >= self.ttl:
            logging.info(f"[Agent-{self.id}] Stop | lived={elapsed:.1f}s")
            self.memory = []
            if self.event_logger:
                self.event_logger(
                    {
                        "event": "agent_stop",
                        "agent_id": self.id,
                        "ttl": self.ttl,
                        "memory_mb": self.memory_mb,
                        "lived_sec": round(elapsed, 1),
                    }
                )
            return {"done": True}

        time.sleep(1)
        return {"done": False}
