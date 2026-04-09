import dns.resolver
import concurrent.futures
import socket
import os
import time

class Discoverer:
    def __init__(self, tlds=None, use_tor=False):
        self.tlds = self._load_tlds(tlds)
        self.resolver = dns.resolver.Resolver()
        # Increased timeouts for Tor stability (Tor DNS can be slow)
        timeout = 7 if use_tor else 3
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout

    def _load_tlds(self, custom_tlds):
        """Loads and cleans TLDs from the data file."""
        if custom_tlds:
            return custom_tlds
            
        tld_file = os.path.join(os.path.dirname(__file__), 'tlds.dat')
        tlds = []
        if os.path.exists(tld_file):
            with open(tld_file, 'r') as f:
                for line in f:
                    clean = line.strip().lstrip('.')
                    # Skip empty lines, comments, and single-letter headers
                    if clean and not clean.startswith('#') and len(clean) > 1:
                        tlds.append(clean)
        
        if not tlds:
            return ['com', 'net', 'org', 'co', 'io', 'info', 'biz']
        return list(set(tlds)) # Ensure uniqueness

    def sanity_check(self):
        """Verifies that DNS resolution is working."""
        test_domains = ['google.com', 'amazon.com', 'yahoo.com']
        for domain in test_domains:
            if self.resolve_dns(domain):
                return True
        return False

    def check_existence(self, domains):
        """
        Checks which of the provided domain variants exist across all TLDs.
        """
        if not self.sanity_check():
            print("[!] CRITICAL: DNS resolution check failed. Please check your internet connection or Tor status.")
            return []

        results = []
        target_domains = []
        
        for base in domains:
            for tld in self.tlds:
                target_domains.append(f"{base}.{tld}")

        print(f"[*] Starting discovery for {len(target_domains)} domain combinations...")
        
        # Use a smaller worker pool to avoid being rate-limited by DNS servers
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            future_to_domain = {executor.submit(self.resolve_dns, domain): domain for domain in target_domains}
            
            completed = 0
            total = len(target_domains)
            
            for future in concurrent.futures.as_completed(future_to_domain):
                completed += 1
                if completed % 100 == 0:
                    print(f"[*] Progress: {completed}/{total} checked...", end='\r')
                    
                try:
                    data = future.result()
                    if data:
                        results.append(data)
                except Exception:
                    pass
        
        print(f"\n[+] Discovery complete. Found {len(results)} registered variants.")
        return results

    def resolve_dns(self, domain):
        """Tries to resolve the A record for a domain."""
        try:
            # We reuse the same resolver but catch exceptions per call
            answers = self.resolver.resolve(domain, 'A')
            return {
                'domain': domain,
                'status': 'registered',
                'ips': [str(rdata) for rdata in answers]
            }
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
            return None
        except Exception:
            return None
