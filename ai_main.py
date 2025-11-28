#!/usr/bin/env python3
# ai_main.py
"""
Adaptive loop: imports generated module, reads decision_value, evolves when threshold exceeded.
"""
import time, importlib, os
from ai_system.core.memory import load_memory, save_memory
from ai_system.core.rewrite_engine import rewrite_generated_module
from ai_system.modules import generated
from datetime import datetime

MEMORY = load_memory()
THRESHOLD = float(os.environ.get("AI_EVOLVE_THRESHOLD", "5.0"))
SLEEP_SEC = int(os.environ.get("AI_EVOLVE_INTERVAL", "4"))
ITERATIONS = int(os.environ.get("AI_EVOLVE_ITERATIONS", "10"))

def get_decision():
    importlib.reload(generated)
    try:
        return generated.ai_decision_engine()
    except Exception as e:
        return {"error": str(e), "decision_value": 0.0}

def main():
    print("=== Adaptive AI Loop (Mode 2) ===")
    for i in range(ITERATIONS):
        dec = get_decision()
        print(f"[iter {i+1}/{ITERATIONS}] decision:", dec)
        dv = float(dec.get("decision_value", 0.0))
        if dv >= THRESHOLD:
            print(f"decision_value {dv} >= {THRESHOLD} -> rewrite")
            rewrite_generated_module()
            mem = load_memory()
            mem["knowledge"] = mem.get("knowledge",0)+1
            mem["reward"] = mem.get("reward",0)+1
            mem.setdefault("runs", []).append({"time": datetime.utcnow().isoformat()+"Z", "event":"evolved"})
            save_memory(mem)
        else:
            print("no evolution")
        time.sleep(SLEEP_SEC)
    print("=== loop end ===")

if __name__ == "__main__":
    main()
