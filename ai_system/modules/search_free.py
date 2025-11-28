# ai_system/modules/search_free.py
import requests
from urllib.parse import quote, urlparse
import re

def ddg_search(query, timeout=6):
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format":"json", "no_html":1, "no_redirect":1}
    try:
        r = requests.get(url, params=params, timeout=timeout, headers={"User-Agent":"ai-sandbox/1.0"})
        r.raise_for_status()
        d = r.json()
        return {"query": query, "heading": d.get("Heading",""), "abstract": d.get("Abstract",""), "answer": d.get("Answer","")}
    except Exception as e:
        return {"error": str(e)}

def wiki_search(query, timeout=6):
    try:
        q = quote(query.replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        r = requests.get(url, timeout=timeout, headers={"User-Agent":"ai-sandbox/1.0"})
        r.raise_for_status()
        d = r.json()
        return {"title": d.get("title",""), "extract": d.get("extract","")}
    except Exception as e:
        return {"error": str(e)}

BLOCKLIST = {"google.com","www.google.com","facebook.com","twitter.com","instagram.com"}
def safe_scrape(url, timeout=6, max_chars=1500):
    try:
        host = (urlparse(url).hostname or "").lower()
        if any(b in host for b in BLOCKLIST):
            return {"error":"blocked domain"}
        r = requests.get(url, timeout=timeout, headers={"User-Agent":"ai-sandbox/1.0"})
        r.raise_for_status()
        text = re.sub(r"<.*?>", " ", r.text)
        text = re.sub(r"\s+", " ", text)
        return {"text": text[:max_chars]}
    except Exception as e:
        return {"error": str(e)}
