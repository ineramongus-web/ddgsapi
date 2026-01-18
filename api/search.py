from http.server import BaseHTTPRequestHandler
from ddgs import DDGS
from urllib.parse import urlparse, parse_qs
import json

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


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        query = params.get("q", [""])[0]

        if not query or len(query) < 3:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Invalid or missing query"
            }).encode())
            return

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

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({
            "query": query,
            "count": len(results),
            "domains": ALLOWED_DOMAINS,
            "results": results
        }).encode())
