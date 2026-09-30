"""Tavily search client and deprecation radar."""

import logging
from typing import Any

import httpx

from backend.app.settings import get_settings

logger = logging.getLogger(__name__)

TAVILY_API_URL = "https://api.tavily.com/search"

# Common known deprecated Python symbols to scan for legacy refactoring
KNOWN_DEPRECATIONS = {
    "datetime.utcnow": "datetime.now(datetime.timezone.utc)",
    "utcnow": "datetime.now(datetime.timezone.utc)",
    "cgi.escape": "html.escape",
    "pipes.quote": "shlex.quote",
    "imp": "importlib",
    "distutils": "setuptools or packaging",
    "asyncio.get_event_loop": "asyncio.get_running_loop() or asyncio.new_event_loop()",
}


class TavilySearcher:
    """Tavily search client for web-informed legacy refactoring."""

    def __init__(self, api_key: str | None = None):
        settings = get_settings()
        self.api_key = api_key or settings.tavily_api_key
        self.enabled = bool(self.api_key)

    async def search(
        self,
        query: str,
        search_depth: str = "basic",
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """Run a web search using Tavily REST API."""
        if not self.enabled:
            return []

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    TAVILY_API_URL,
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "search_depth": search_depth,
                        "max_results": max_results,
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("results", [])
                logger.warning(
                    "Tavily search API returned status %s: %s", resp.status_code, resp.text
                )
                return []
        except Exception as e:
            logger.warning("Tavily search failed: %s", e)
            return []

    async def check_deprecations(self, source_code: str) -> list[dict[str, Any]]:
        """Deprecation Radar: scans source code for deprecated Python patterns

        and fetches modern replacement migration guidance via Tavily.
        """
        findings = []
        for symbol, recommended_replacement in KNOWN_DEPRECATIONS.items():
            if symbol in source_code:
                finding: dict[str, Any] = {
                    "symbol": symbol,
                    "recommended_replacement": recommended_replacement,
                    "tavily_guidance": None,
                }

                if self.enabled:
                    results = await self.search(
                        f"Python {symbol} deprecated migration replacement guidance",
                        max_results=2,
                    )
                    if results:
                        finding["tavily_guidance"] = {
                            "title": results[0].get("title"),
                            "url": results[0].get("url"),
                            "snippet": results[0].get("content", "")[:250],
                        }

                findings.append(finding)

        return findings
