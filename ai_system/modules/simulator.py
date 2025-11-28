# ai_system/modules/simulator.py
"""
Simple scenario simulator to estimate probabilities of broad outcomes.
This is a toy, probabilistic simulator to illustrate the idea.
"""

import random, math
from collections import Counter

def _one_run(seed=None, depth=50):
    # Simulate a simple chain of events; returns outcome label
    rnd = random.Random(seed)
    # hypothetical risk processes:
    climate = rnd.random() * 0.3
    war = rnd.random() * 0.25
    pandemic = rnd.random() * 0.2
    asteroid = rnd.random() * 0.05
    ai_risk = rnd.random() * 0.2
    total_risk = climate + war + pandemic + asteroid + ai_risk
    # map to labels
    if total_risk > 1.0:
        return "civilization_collapse"
    if ai_risk > 0.18:
        return "ai_takeover"
    if asteroid > 0.04:
        return "asteroid_impact"
    if climate > 0.28:
        return "climate_collapse"
    return "survival"

def run_scenarios(query="world", runs=1000):
    cnt = Counter()
    for i in range(runs):
        o = _one_run(seed=i)
        cnt[o]+=1
    totals = dict(cnt)
    for k in totals:
        totals[k] = totals[k]/runs
    return {"runs": runs, "probabilities": totals}
