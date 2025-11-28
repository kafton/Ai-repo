# ai_system/core/memory.py
import json, os
from datetime import datetime

MEM_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ai_memory.json"))

def load_memory():
    if not os.path.exists(MEM_FILE):
        m = {"knowledge": 1, "reward": 0, "runs": [], "sim_history": []}
        save_memory(m)
        return m
    with open(MEM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(m):
    m.setdefault("last_updated", datetime.utcnow().isoformat() + "Z")
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)
