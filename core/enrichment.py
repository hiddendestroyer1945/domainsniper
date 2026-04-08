import whois
import dns.resolver
import requests
import json
import time

class Enricher:
    def __init__(self, tor_session=None):
        self.session = tor_session or requests.Session()

    def enrich_domain(self, domain):
        """Perform deep intelligence gathering for a single domain."""
        print(f"[*] Enriching data for {domain}...")
        results = {
            'domain': domain,
            'whois': self.get_whois(domain),
            'infrastructure': self.get_infrastructure(domain),
            'passive_recon': self.get_ct_logs(domain)
        }
        return results

    def get_whois(self, domain):
        """Fetches WHOIS registration data."""
        try:
            w = whois.whois(domain)
            return {
                'registrant': w.name,
                'organization': w.org,
                'emails': w.emails,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'registrar': w.registrar
            }
        except Exception as e:
            return {'error': str(e)}

    def get_infrastructure(self, domain):
        """Resolves MX and NS records."""
        infra = {}
        # MX Records
        try:
            mx_answers = dns.resolver.resolve(domain, 'MX')
            infra['mx'] = [str(rdata.exchange) for rdata in mx_answers]
        except Exception:
            infra['mx'] = []

        # NS Records
        try:
            ns_answers = dns.resolver.resolve(domain, 'NS')
            infra['ns'] = [str(rdata) for rdata in ns_answers]
        except Exception:
            infra['ns'] = []

        return infra

    def get_ct_logs(self, domain):
        """Queries crt.sh for Certificate Transparency logs."""
        try:
            url = f"https://crt.sh/?q={domain}&output=json"
            response = self.session.get(url, timeout=20)
            if response.status_code == 200:
                data = response.json()
                # Return a summary of the most recent certificates
                return data[:5] 
            return []
        except Exception as e:
            return {'error': str(e)}
