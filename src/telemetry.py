import json
from datetime import UTC, datetime
from pathlib import Path

LOG_PATH = Path("data/telemetry/run_stats.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_call(batch: int, input_len: int, latency: float):
    log_entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "mode": "Batch No: " + str(batch),
        "input_chars": str(input_len),
        "latency_sec": round(latency, 3)
    }

    # Append to JSON list
    try:
        if LOG_PATH.exists():
            with open(LOG_PATH, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(log_entry)
                f.seek(0)
                json.dump(data, f, indent=2)
        else:
            with open(LOG_PATH, "w", encoding="utf-8") as f:
                json.dump([log_entry], f, indent=2)

    except Exception as e:
        print(f"Failed to write telemetry: {e}")
