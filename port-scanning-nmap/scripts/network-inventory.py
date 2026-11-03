#!/usr/bin/env python3

import nmap
import json
import argparse
from datetime import datetime

def network_inventory(target_network, output_file=None):
    """
    Perform network inventory scan and generate report
    
    Args:
        target_network: Network to scan (e.g., 192.168.1.0/24)
        output_file: Optional output file for JSON report
    
    Returns:
        Dictionary containing inventory data
    """
    
    nm = nmap.PortScanner()
    
    print(f"[*] Starting network inventory for {target_network}")
    print("[*] Phase 1: Host Discovery...")
    
    nm.scan(target_network, arguments='-sn')
    
    live_hosts = nm.all_hosts()
    print(f"[+] Found {len(live_hosts)} live hosts")
    
    inventory = []
    
    print("[*] Phase 2: Port Scanning...")
    for host in live_hosts:
        print(f"    Scanning {host}...")
        nm.scan(host, arguments='-F -sV')
        
        host_info = {
            'ip': host,
            'hostname': nm[host].hostname() if nm[host].hostname() else 'Unknown',
            'state': nm[host].state(),
            'ports': [],
            'services': []
        }
        
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                port_info = {
                    'port': port,
                    'protocol': proto,
                    'state': nm[host][proto][port]['state'],
                    'service': nm[host][proto][port].get('name', 'Unknown'),
                    'product': nm[host][proto][port].get('product', ''),
                    'version': nm[host][proto][port].get('version', ''),
                    'extrainfo': nm[host][proto][port].get('extrainfo', '')
                }
                host_info['ports'].append(port_info)
                
                if nm[host][proto][port]['state'] == 'open':
                    service = f"{nm[host][proto][port].get('product', 'Unknown')} {nm[host][proto][port].get('version', '')}"
                    host_info['services'].append(service.strip())
        
        inventory.append(host_info)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(inventory, f, indent=2)
        print(f"[+] Report saved to {output_file}")
    
    return inventory

def generate_summary(inventory):
    """Generate a summary of the network inventory"""
    
    total_hosts = len(inventory)
    total_open_ports = sum(len([p for p in host['ports'] if p['state'] == 'open']) for host in inventory)
    
    services = set()
    for host in inventory:
        services.update(host['services'])
    
    print("\n" + "="*50)
    print("NETWORK INVENTORY SUMMARY")
    print("="*50)
    print(f"Total Hosts Discovered: {total_hosts}")
    print(f"Total Open Ports: {total_open_ports}")
    print(f"Unique Services: {len(services)}")
    print("\nServices Found:")
    for service in sorted(services):
        if service:
            print(f"  - {service}")
    
    print("\nHosts Summary:")
    for host in inventory:
        open_ports = [p for p in host['ports'] if p['state'] == 'open']
        print(f"  {host['ip']} ({host['hostname']}): {len(open_ports)} open ports")
        for port in open_ports:
            print(f"    - {port['port']}/{port['protocol']}: {port['service']} {port['product']} {port['version']}")
    
    print("="*50)

def export_csv(inventory, csv_file):
    """Export inventory to CSV format"""
    
    with open(csv_file, 'w') as f:
        f.write("IP,Hostname,Port,Protocol,State,Service,Product,Version\n")
        for host in inventory:
            for port in host['ports']:
                f.write(f"{host['ip']},{host['hostname']},{port['port']},{port['protocol']},{port['state']},{port['service']},{port['product']},{port['version']}\n")
    
    print(f"[+] CSV exported to {csv_file}")

def main():
    parser = argparse.ArgumentParser(description='Network Inventory Scanner')
    parser.add_argument('target', help='Target network (e.g., 192.168.1.0/24)')
    parser.add_argument('-o', '--output', help='Output JSON file')
    parser.add_argument('-c', '--csv', help='Output CSV file')
    
    args = parser.parse_args()
    
    print("="*50)
    print("NETWORK INVENTORY SCANNER")
    print("="*50)
    print(f"Target: {args.target}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    inventory = network_inventory(args.target, args.output)
    generate_summary(inventory)
    
    if args.csv:
        export_csv(inventory, args.csv)

if __name__ == '__main__':
    main()
