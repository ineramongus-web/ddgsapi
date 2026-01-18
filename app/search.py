from fastapi import FastAPI, Query
from ddgs import DDGS
from urllib.parse import urlparse

app = FastAPI()

ALLOWED_DOMAINS = (
    "devforum.roblox.com",
    "github.com",
    "create.roblox.com",
    "roblox.com"
)

def allowed(url: str) -> bool:
    try:
        netloc = urlparse(url).netloc.lower()
        return any(netloc.endswith(d) for d in ALLOWED_DOMAINS)
    except Exception:
        return False

@app.get("/q")
def search(q: str = Query(..., min_length=3)):
    results = []

    with DDGS() as ddg:
        for r in ddg.text(
            q,
            region="wt-wt",
            safesearch="off",
            max_results=20
        ):
            href = r.get("href", "")
            if not allowed(href):
                continue

            results.append({
                "title": r.get("title"),
                "body": r.get("body"),
                "href": href,
                "source": "duckduckgo-ddgs"
            })

            if len(results) >= 5:
                break

    return {
        "query": q,
        "count": len(results),
        "domains": ALLOWED_DOMAINS,
        "results": results
    }
