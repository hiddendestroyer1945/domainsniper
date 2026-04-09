import os
import json
import sys
import asyncio
from core.permutations import Permutator
from core.discovery import Discoverer
from core.proxy import ProxyManager
from core.enrichment import Enricher
from core.search import SearchScanner

async def run_discovery(base_name, use_tor, proxy_manager):
    """Orchestrates the discovery phase based on user choice."""
    print("\n[?] Select Discovery Mode:")
    print(" 1. DNS Brute-force (Deep TLD scan)")
    print(" 2. Search-Engine Recon (Fast metadata discovery)")
    print(" 3. Both (Recommended for full coverage)")
    
    choice = input("[?] Choice [1-3]: ").strip() or "3"
    
    active_domains_data = []
    
    # Generate Permutations for Brute-force if needed
    permutator = Permutator(base_name)
    variants = permutator.generate_all()

    if choice in ["1", "3"]:
        print("\n[*] Phase 2a: Discovering Active Domains via DNS Brute-force...")
        discoverer = Discoverer(use_tor=use_tor)
        # Pre-scan sanity check
        if discoverer.sanity_check():
            brute_results = discoverer.check_existence(variants)
            active_domains_data.extend(brute_results)
        else:
            print("[!] DNS check failed. Skipping Brute-force phase.")

    if choice in ["2", "3"]:
        print("\n[*] Phase 2b: Discovering Active Domains via Search Recon...")
        proxy_url = proxy_manager.proxy_url if use_tor else None
        scanner = SearchScanner(proxy=proxy_url)
        search_results = await scanner.search_domains(base_name)
        
        # Convert search strings to Discovery format
        for domain in search_results:
            active_domains_data.append({
                'domain': domain,
                'status': 'discovered',
                'ips': []
            })

    # Deduplicate strictly by domain
    unique_domains = {d['domain']: d for d in active_domains_data}.values()
    return list(unique_domains)

async def main():
    print("""
    ========================================
             DOMAIN SNIPER v1.1
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

    report_name = input("[?] Enter the report filename: ").strip()
    if not report_name.endswith('.json'):
        report_name += '.json'
    
    # SECURITY FIX: Prevent Path Traversal (OWASP) by extracting only the base filename
    clean_report_name = os.path.basename(report_name)
    report_path = os.path.join('reports', clean_report_name)

    # Step 2: Stealth Setup
    use_tor = input("[?] Use Tor for stealth? (y/n): ").lower() == 'y'
    proxy_manager = ProxyManager()
    tor_session = None

    if use_tor:
        print("[*] Verifying Tor service...")
        if proxy_manager.check_tor_connection():
            print("[+] Tor service detected. Applying global stealth patch...")
            proxy_manager.set_global_proxy()
            tor_session = proxy_manager.get_tor_session()
        else:
            print("[!] Tor service NOT detected! Ensure Tor is running on port 9050.")
            cont = input("[?] Continue without Tor? (y/n/exit): ").lower()
            if cont == 'exit':
                sys.exit(0)
            elif cont != 'y':
                sys.exit(1)
            use_tor = False

    # Phase 1: Permutation
    print("\n[*] Phase 1: Generating Permutations...")
    permutator = Permutator(base_name)
    variants = permutator.generate_all()
    print(f"[+] Generated {len(variants)} potential domain variants.")

    # Phase 2: Discovery
    active_domains_data = await run_discovery(base_name, use_tor, proxy_manager)
    print(f"[+] Total unique active/discovered domains: {len(active_domains_data)}")

    # Phase 3: Enrichment
    if active_domains_data:
        print("\n[*] Phase 3: Deep Intelligence Gathering...")
        enricher = Enricher(tor_session=tor_session)
        final_results = []

        for domain_info in active_domains_data:
            domain = domain_info['domain']
            enriched_data = enricher.enrich_domain(domain)
            # Merge discovery info with enriched info
            enriched_data['ips'] = list(set(enriched_data.get('ips', []) + domain_info.get('ips', [])))
            final_results.append(enriched_data)

        # Step 3: Reporting
        print(f"\n[*] Saving results to {report_path}...")
        with open(report_path, 'w') as f:
            json.dump(final_results, f, indent=4)
        
        print("\n[+] Scan complete. Happy hunting!")
    else:
        print("\n[!] No active domains found. No report generated.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] User interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
        sys.exit(1)
