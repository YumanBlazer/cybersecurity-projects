# Port Scanning with Nmap

A small network inventory tool built on Nmap and Python. It discovers live hosts, scans their services, and exports the results as JSON and CSV.

## Overview

<!-- 2-3 sentences: what problem this solves and what you built. -->

## Repository Contents

- `scripts/network-inventory.py`: discovers live hosts, scans open ports and services, prints a summary, and optionally exports JSON and CSV.
- `docs/`: screenshots and trimmed example output.
- `requirements.txt`: Python dependencies.

## Requirements

- Python 3.8+
- Nmap installed and available in `PATH`
- Scan only networks you own or have written permission to test.

## Usage

```bash
pip install -r requirements.txt
python3 scripts/network-inventory.py 192.168.1.0/24 -o inventory.json -c inventory.csv
```

| Option | Description |
| ------ | ----------- |
| `target` | Network or host to scan, e.g. `192.168.1.0/24` |
| `-o`, `--output` | Write the full inventory to a JSON file |
| `-c`, `--csv` | Export one row per port to a CSV file |

## Example Output

<!-- Paste a trimmed summary from a scan you actually ran on your lab network. -->

## Lab Environment

- OS: <!-- e.g. Kali Linux 2026.x in VirtualBox -->
- Nmap version: <!-- run `nmap --version` -->
- Network scanned: <!-- your own lab network only -->

## Findings

<!-- Real numbers from your runs: hosts found, open ports, services identified. -->

## What I Learned

<!-- 2-3 specific things, e.g. how ARP discovery differs from ICMP on a local network, or a bug you hit while parsing Nmap output. -->

## Limitations

- Service and version detection depends on Nmap's fingerprint database and can be wrong.
- <!-- Add limitations you found while testing. -->

## Disclaimer

For educational use on networks you own or are authorized to test.
