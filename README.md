# DomainSniper v1.0

**DomainSniper** is a high-performance OSINT and reconnaissance tool designed to identify domain squatting, typosquatting, and visually deceptive (IDN Homograph) domains. It operates through three distinct phases: **Permutation**, **Discovery**, and **Enrichment**, providing a comprehensive intelligence report for any target domain.

---

## 🚀 Key Features

### 1. Advanced Permutation Engine
- **Typosquatting**: Automated generation of variants via omission, repetition, and keyboard-adjacent swaps.
- **Homograph (IDN) Attacks**: Identification of visually identical domains using Cyrillic or Greek characters.
- **Combosquatting**: Appending common keywords like `-login`, `-secure`, or `-support`.
- **Bitsquatting**: Pinpointing domains that differ by a single bit (targeting hardware memory errors).
- **"Sucks" Domain Auditing**: Targets reputation-damaging strings (e.g., `brand-sucks.com`).

### 2. Stealth Discovery
- **Comprehensive TLD Coverage**: Scans across 1,500+ Top-Level Domains (TLDs).
- **Tor Integration**: Full SOCKS5 support for anonymous DNS resolution and API requests.
- **Asynchronous Execution**: High-speed concurrent scanning for large datasets.

### 3. Deep Intelligence Gathering
- **Registration Data**: Automated WHOIS lookups for registrant details and registrar info.
- **Infrastructure Mapping**: Resolution of **A**, **MX**, and **NS** records.
- **Passive Recon**: Cross-referencing **Certificate Transparency (CT) logs** via `crt.sh`.

---

## 🛠 Prerequisites

- **Python 3.9+**
- **Debian-based Linux** (e.g., Debian 12, Ubuntu, Kali)
- **Tor Service** (Optional, but required for stealth features)
    ```bash
    sudo apt update && sudo apt install -y tor python3 python3-pip python3-venv
    sudo systemctl start tor
    ```

---

## 📥 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/hiddendestroyer1945/domainsniper.git
cd domainsniper
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏁 Launching the Program

Execute the main script to start the interactive CLI:
```bash
python3 domainsniper.py
```

---

## 📖 Usage & Menus

When you launch DomainSniper, you will be prompted with the following inputs:

1.  **Enter the domain name (without TLD)**: Provide the base name (e.g., `google`). The tool will automatically append TLDs from the internal database.
2.  **Enter the report filename**: Specify the name of the output file (e.g., `recon_results.json`).
3.  **Use Tor for stealth? (y/n)**: 
    -   `y`: All network traffic (DNS and CT log queries) will be routed through `localhost:9050`.
    -   `n`: The program uses your direct internet connection.

---

## 📊 Output Format

### Reports Location
All results are stored in the `reports/` directory within the program folder.

### JSON Architecture
The output file uses a structured JSON format to allow easy integration with other tools or automated pipelines.

**Example Entry:**
```json
{
    "domain": "exаmple.com",
    "status": "registered",
    "ips": ["92.12.31.22"],
    "whois": {
        "registrant": "John Doe",
        "organization": "Security Corp",
        "emails": ["admin@securitycorp.com"],
        "creation_date": "2024-01-15",
        "registrar": "NameCheap"
    },
    "infrastructure": {
        "mx": ["mail.exаmple.com"],
        "ns": ["ns1.hostingprovider.com", "ns2.hostingprovider.com"]
    },
    "passive_recon": [
        {
            "id": 12345678,
            "issuer_name": "C=US, O=Let's Encrypt",
            "common_name": "exаmple.com",
            "not_before": "2024-02-01"
        }
    ]
}
```

---

## ⚠️ Disclaimer
This tool is for educational and authorized security auditing purposes only. The author takes no responsibility for any misuse of this software. Always ensure you have legal permission before performing reconnaissance on domains you do not own.

---

## 👤 Author
- **Name**: hiddendestroyer1945
- **GitHub**: [hiddendestroyer1945](https://github.com/hiddendestroyer1945)
- **Repository**: [DomainSniper](https://github.com/hiddendestroyer1945/domainsniper.git)
