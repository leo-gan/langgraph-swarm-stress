# scripts/plot_stats.py
import argparse
import json
import matplotlib.pyplot as plt
from pathlib import Path

def plot_stats(json_file: Path, outdir: Path = None):
    with open(json_file) as f:
        records = json.load(f)

    # Separate event types
    ticks = [r for r in records if r.get("event") == "stats_tick"]
    starts = [r for r in records if r.get("event") == "agent_start"]
    stops = [r for r in records if r.get("event") == "agent_stop"]

    if not ticks:
        print("No stats_tick events found in file.")
        return

    # Extract tick metrics
    times = [r["time_sec"] for r in ticks]
    active = [r["active_agents"] for r in ticks]
    cpu = [r["cpu_percent"] for r in ticks]
    mem = [r["mem_percent"] for r in ticks]

    # Map agent lifetimes
    agent_starts = {s["agent_id"]: s["time_sec"] for s in starts}
    agent_spans = []
    for stop in stops:
        aid = stop["agent_id"]
        if aid in agent_starts:
            agent_spans.append((aid, agent_starts[aid], stop["time_sec"]))
            del agent_starts[aid]
    # If some agents never stopped, shade them up to the last timestamp
    last_time = times[-1]
    for aid, t0 in agent_starts.items():
        agent_spans.append((aid, t0, last_time))

    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Agent spans as shaded regions
    for idx, (_, t0, t1) in enumerate(agent_spans):
        ax1.axvspan(t0, t1, color="green", alpha=0.08)

    # Active agents
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Active Agents", color="tab:blue")
    ax1.plot(times, active, label="Active Agents", color="tab:blue", linewidth=2)
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    # CPU / Memory on secondary axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("CPU / Memory (%)", color="tab:red")
    ax2.plot(times, cpu, label="CPU %", color="tab:red", linestyle="--", linewidth=1.5)
    ax2.plot(times, mem, label="MEM %", color="tab:orange", linestyle=":", linewidth=1.5)
    ax2.tick_params(axis="y", labelcolor="tab:red")

    # Add start/stop markers on top of spans
    for s in starts:
        ax1.axvline(s["time_sec"], color="green", linestyle="--", alpha=0.4)
    for s in stops:
        ax1.axvline(s["time_sec"], color="red", linestyle="--", alpha=0.4)

    # Legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    legend = ax1.legend(
        lines + lines2,
        labels + labels2,
        loc="upper right",
        title="Metrics"
    )

    import matplotlib.patches as mpatches
    span_patch = mpatches.Patch(color="green", alpha=0.1, label="Agent Lifetime")
    ax1.legend(handles=legend.legend_handles + [span_patch], loc="upper right")

    plt.title(f"Swarm Stress Test: {json_file.stem}")
    plt.tight_layout()

    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        outpath = outdir / f"{json_file.stem}.png"
        plt.savefig(outpath)
        print(f"Plot saved to {outpath}")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot swarm stress stats")
    parser.add_argument("json_file", type=Path, help="Path to stats JSON log")
    parser.add_argument("--outdir", type=Path, help="Directory to save plot instead of showing it")
    args = parser.parse_args()

    plot_stats(args.json_file, args.outdir)
