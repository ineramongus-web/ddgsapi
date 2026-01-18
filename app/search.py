from ddgs import DDGS
from urllib.parse import parse_qs, urlparse

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


def handler(request):
    query = parse_qs(request.query_string.decode()).get("q", [""])[0]

    if len(query) < 3:
        return {
            "statusCode": 400,
            "body": "Missing or invalid query"
        }

    results = []

    with DDGS() as ddg:
        for r in ddg.text(
            query,
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
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": __import__("json").dumps({
            "query": query,
            "count": len(results),
            "results": results
        })
    }            results.append({
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
        "results": results
    }
