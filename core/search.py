import asyncio
import re
from urllib.parse import urlparse
from playwright.async_api import async_playwright

class SearchScanner:
    def __init__(self, proxy=None):
        self.proxy = proxy # Expected format from ProxyManager
        self.found_domains = set()

    async def search_domains(self, keyword):
        """
        Performs an asynchronous search for the keyword using a headless browser
        (UltraAnalyzer approach) to extract unique domains.
        """
        print(f"[*] Querying DuckDuckGo for '{keyword}' related domains using Web UI Agents...")
        
        try:
            async with async_playwright() as p:
                # Playwright expects standard socks5 URL scheme
                proxy_settings = None
                if self.proxy:
                    clean_proxy = self.proxy.replace('socks5h://', 'socks5://')
                    proxy_settings = {"server": clean_proxy}
                
                browser = await p.chromium.launch(headless=True, proxy=proxy_settings)
                context = await browser.new_context(
                    ignore_https_errors=True,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                # Using the duckduckgo HTML version avoids heavy JS and captchas
                url = f"https://html.duckduckgo.com/html/?q={keyword}"
                await page.goto(url, wait_until="networkidle", timeout=45000)
                
                content = await page.content()
                
                # Extract links directly from hrefs using Javascript injection
                hrefs = await page.evaluate("() => Array.from(document.querySelectorAll('a')).map(a => a.href)")
                
                for href in hrefs:
                    if 'duckduckgo.com' not in href and keyword.lower() in href.lower():
                        domain = self._extract_domain(href)
                        if domain:
                            self.found_domains.add(domain)

                # Optional: Regex matching on raw text as fallback
                potential_domains = re.findall(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', content.lower())
                for d in potential_domains:
                    if keyword.lower() in d and 'duckduckgo' not in d:
                        self.found_domains.add(d)

                await browser.close()

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
