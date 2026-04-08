import os
import json
import sys
from core.permutations import Permutator
from core.discovery import Discoverer
from core.proxy import ProxyManager
from core.enrichment import Enricher

def main():
    print("""
    ========================================
             DOMAIN SNIPER v1.0
    ========================================
    """)

    # Setup directories
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Step 1: User Input
    base_name = input("[?] Enter the domain name (without TLD): ").strip()
    if not base_name:
        print("[!] Domain name cannot be empty.")
        sys.exit(1)

    report_name = input("[?] Enter the report filename (e.g., scan_results.json): ").strip()
    if not report_name.endswith('.json'):
        report_name += '.json'
    
    report_path = os.path.join('reports', report_name)

    # Step 2: Stealth Setup
    use_tor = input("[?] Use Tor for stealth? (y/n): ").lower() == 'y'
    proxy_manager = ProxyManager()
    tor_session = None

    if use_tor:
        print("[*] Setting up Tor proxy...")
        proxy_manager.set_global_proxy()
        if proxy_manager.check_tor_connection():
            print("[+] Tor connection verified.")
            tor_session = proxy_manager.get_tor_session()
        else:
            print("[!] Tor connection failed! Ensure Tor is running on port 9050.")
            cont = input("[?] Continue without Tor? (y/n): ").lower()
            if cont != 'y':
                sys.exit(1)

    # Phase 1: Permutation
    print("\n[*] Phase 1: Generating Permutations...")
    permutator = Permutator(base_name)
    variants = permutator.generate_all()
    print(f"[+] Generated {len(variants)} potential domain variants.")

    # Phase 2: Discovery
    print("\n[*] Phase 2: Discovering Active Domains...")
    discoverer = Discoverer()
    active_domains_data = discoverer.check_existence(variants)
    print(f"[+] Found {len(active_domains_data)} active domains.")

    # Phase 3: Enrichment
    print("\n[*] Phase 3: Deep Intelligence Gathering...")
    enricher = Enricher(tor_session=tor_session)
    final_results = []

    for domain_info in active_domains_data:
        domain = domain_info['domain']
        enriched_data = enricher.enrich_domain(domain)
        # Merge discovery info with enriched info
        enriched_data['ips'] = domain_info.get('ips', [])
        final_results.append(enriched_data)

    # Step 3: Reporting
    print(f"\n[*] Saving results to {report_path}...")
    with open(report_path, 'w') as f:
        json.dump(final_results, f, indent=4)
    
    print("\n[+] Scan complete. Happy hunting!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] User interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
        sys.exit(1)
