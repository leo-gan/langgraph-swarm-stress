# stress/stats.py
import threading, time, logging, psutil, json, csv
from pathlib import Path

class StatsMonitor:
    def __init__(self, swarm, interval=5, outdir="logs"):
        self.swarm = swarm
        self.interval = interval
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.records = []
        self.outdir = Path(outdir)
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.start_time = None

    def start(self):
        self.start_time = time.time()
        self.thread.start()

    def stop(self):
        self._stop.set()
        self.thread.join()
        self._save()

    def log_event(self, event: dict):
        """Record agent-level events"""
        if "time_sec" not in event:
            event["time_sec"] = round(time.time() - self.start_time, 1)
        self.records.append(event)

    def _run(self):
        while not self._stop.is_set():
            elapsed = time.time() - self.start_time
            active = sum(1 for a in self.swarm if not a.state.get("done"))
            total = len(self.swarm)

            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent

            rec = {
                "event": "stats_tick",
                "time_sec": round(elapsed, 1),
                "active_agents": active,
                "total_agents": total,
                "cpu_percent": cpu,
                "mem_percent": mem,
            }
            self.records.append(rec)

            logging.info(
                f"[Stats] t={elapsed:.1f}s | Active={active}/{total} | CPU={cpu:.1f}% | MEM={mem:.1f}%"
            )
            time.sleep(self.interval)

    def _save(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        json_path = self.outdir / f"stats_{timestamp}.json"
        csv_path = self.outdir / f"stats_{timestamp}.csv"

        with open(json_path, "w") as f:
            json.dump(self.records, f, indent=2)

        if self.records:
            # collect all possible keys from all events
            keys = set()
            for rec in self.records:
                keys.update(rec.keys())
            keys = list(keys)

            with open(csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.records)

        logging.info(f"[Stats] Saved results to {json_path} and {csv_path}")
