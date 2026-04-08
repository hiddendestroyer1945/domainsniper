import dns.resolver
import concurrent.futures
import socket
import os

class Discoverer:
    def __init__(self, tlds=None):
        self.tlds = tlds or self._load_tlds()

    def _load_tlds(self):
        """Loads TLDs from the data file."""
        tld_file = os.path.join(os.path.dirname(__file__), 'tlds.dat')
        if os.path.exists(tld_file):
            with open(tld_file, 'r') as f:
                return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        # Fallback to a very small list if file is missing
        return ['com', 'net', 'org', 'co', 'io', 'info', 'biz']

    def check_existence(self, domains):
        """
        Checks which of the provided domain variants exist across all TLDs.
        """
        results = []
        target_domains = []
        
        for base in domains:
            for tld in self.tlds:
                # Handle cases where TLD might already have a leading dot
                clean_tld = tld.lstrip('.')
                target_domains.append(f"{base}.{clean_tld}")

        print(f"[*] Starting discovery for {len(target_domains)} domain combinations...")
        
        # Increased workers for large-scale TLD scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_domain = {executor.submit(self.resolve_dns, domain): domain for domain in target_domains}
            for future in concurrent.futures.as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    data = future.result()
                    if data:
                        results.append(data)
                except Exception:
                    pass
        
        return results

    def resolve_dns(self, domain):
        """Tries to resolve the A record for a domain."""
        try:
            # Short timeout to keep the scan moving
            resolver = dns.resolver.Resolver()
            resolver.timeout = 2
            resolver.lifetime = 2
            answers = resolver.resolve(domain, 'A')
            return {
                'domain': domain,
                'status': 'registered',
                'ips': [str(rdata) for rdata in answers]
            }
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
            return None
        except Exception:
            return None
