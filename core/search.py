import asyncio
import re
from urllib.parse import urlparse
from duckduckgo_search import AsyncDDGS
import aiohttp
from aiohttp_socks import ProxyConnector

class SearchScanner:
    def __init__(self, proxy=None):
        self.proxy = proxy # Expected format: "socks5h://127.0.0.1:9050"
        self.found_domains = set()

    async def search_domains(self, keyword, max_results=50):
        """
        Performs an asynchronous search for the keyword and extracts unique domains.
        """
        print(f"[*] Querying DuckDuckGo for '{keyword}' related domains...")
        
        try:
            async with AsyncDDGS(proxies=self.proxy) as ddgs:
                results = await ddgs.text(keyword, max_results=max_results)
                
                for r in results:
                    # Extract from URL
                    url = r.get('href', '')
                    domain = self._extract_domain(url)
                    if domain:
                        self.found_domains.add(domain)
                    
                    # Extract from snippet/title (sometimes full domains are mentioned)
                    text = f"{r.get('title', '')} {r.get('body', '')}"
                    potential_domains = re.findall(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', text.lower())
                    for d in potential_domains:
                        if keyword.lower() in d:
                            self.found_domains.add(d)

        except Exception as e:
            print(f"[!] Search error: {e}")
            
        # Filter to keep only those containing the keyword
        filtered_domains = {d for d in self.found_domains if keyword.lower() in d}
        print(f"[+] Search Recon discovered {len(filtered_domains)} unique domains.")
        return list(filtered_domains)

    def _extract_domain(self, url):
        """Extracts the base domain from a URL."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain.lower()
        except:
            return None

if __name__ == "__main__":
    # Small test harness
    async def test():
        scanner = SearchScanner()
        results = await scanner.search_domains("yahoo", max_results=20)
        print(f"Results: {results}")

    asyncio.run(test())
