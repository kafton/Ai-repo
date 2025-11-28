# ai_system/core/agent_router.py
from .tools import run_shell, read_file, write_file
from ..modules import search_free, pi_estimator, simulator

def agent(action, **kwargs):
    """
    Router for actions:
      - search: ddg
      - wiki: wiki summary
      - scrape: safe_scrape
      - pi: pi estimation
      - simulate: future/world-end scenarios
      - run/read/write: local tools
    """
    if action == "search":
        return search_free.ddg_search(kwargs.get("query",""))
    if action == "wiki":
        return search_free.wiki_search(kwargs.get("query",""))
    if action == "scrape":
        return search_free.safe_scrape(kwargs.get("url",""))
    if action == "pi":
        method = kwargs.get("method","ramanujan")
        n = int(kwargs.get("n", 3))
        prec = int(kwargs.get("prec", 80))
        val = pi_estimator.estimate_pi(method=method, n=n, prec=prec)
        return {"method": method, "n": n, "prec": prec, "pi": str(val)}
    if action == "simulate":
        return simulator.run_scenarios(kwargs.get("query","world"), runs=int(kwargs.get("runs",1000)))
    if action == "run":
        return run_shell(kwargs.get("cmd",""))
    if action == "read":
        return read_file(kwargs.get("path",""))
    if action == "write":
        return write_file(kwargs.get("path",""), kwargs.get("content",""))
    return {"error":"unknown action"}
