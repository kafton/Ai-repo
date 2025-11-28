# ai_system/core/rewrite_engine.py
import re, os
from datetime import datetime
from ..core.memory import load_memory, save_memory
from ..core.tools import write_file, read_file

MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "generated.py"))
START_TAG = "# === AI_REWRITE_START ==="
END_TAG = "# === AI_REWRITE_END ==="

def generate_code_for_memory(mem):
    lvl = int(mem.get("knowledge", 1))
    reward = int(mem.get("reward", 0))
    code = f'''
def ai_decision_engine():
    """
    Auto-generated engine — Level {lvl}
    """
    knowledge = {lvl}
    reward = {reward}
    # simple heuristic: decision_value uses knowledge+reward
    decision_value = (knowledge * 2.0) + (reward * 0.5)
    return {{"knowledge": knowledge, "reward": reward, "decision_value": float(decision_value)}}
'''
    return code

def rewrite_generated_module():
    text = read_file(MODULE_PATH)
    if text is None:
        raise FileNotFoundError("generated module not found: " + MODULE_PATH)
    pattern = re.compile(re.escape(START_TAG) + r"(.*?)" + re.escape(END_TAG), re.DOTALL)
    m = pattern.search(text)
    if not m:
        raise RuntimeError("Rewrite tags not found in generated module.")
    mem = load_memory()
    new_code = "\n" + generate_code_for_memory(mem) + "\n"
    new_text = text[:m.start(1)] + new_code + text[m.end(1):]
    if START_TAG not in new_text or END_TAG not in new_text:
        raise RuntimeError("Tags missing after substitution.")
    backup = MODULE_PATH + ".bak." + datetime.utcnow().strftime("%Y%m%d%H%M%S")
    write_file(backup, text)
    write_file(MODULE_PATH, new_text)
    mem.setdefault("runs", []).append({"time": datetime.utcnow().isoformat()+"Z", "action":"rewrote_generated"})
    save_memory(mem)
    return True
