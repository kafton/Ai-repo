# trainer.py
"""
Simple trainer that could consume logs/feedback and update memory or rules.
This is optional scaffold — adapt as needed.
"""
import time, json, os
from ai_system.core.memory import load_memory, save_memory

LOG_PATH = "ai_logs.json"
POLL_INTERVAL = 5

def read_logs():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def trainer_once():
    logs = read_logs()
    if not logs:
        return False
    mem = load_memory()
    changed = False
    # Example: look for feedback events to bump memory
    for ev in logs:
        if ev.get("type") == "feedback":
            r = float(ev.get("reward", 0))
            mem["knowledge"] = mem.get("knowledge", 0) + (r * 0.1)
            mem.setdefault("runs", []).append({"time": ev.get("time"), "event":"trained_feedback"})
            changed = True
    if changed:
        save_memory(mem)
    # clear logs after processing
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)
    return changed

def main():
    print("[trainer] starting")
    while True:
        try:
            trainer_once()
        except Exception as e:
            print("[trainer] error:", e)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
