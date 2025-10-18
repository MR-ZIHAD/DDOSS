#!/usr/bin/env python3
"""
Simple Stress Tester - API Server
Web API for controlling stress tests
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import secrets
import json
from datetime import datetime
from stress_core import StressTester

app = Flask(__name__)
CORS(app)

# Global tester instance
tester = StressTester()

# API configuration
API_KEY = secrets.token_hex(16)  # Generate random API key
ATTACK_HISTORY = []

# HTML Template for web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Stress Tester</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
        }
        .warning {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        .btn-danger:hover {
            background: #c82333;
        }
        .stats-box {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #dee2e6;
        }
        .stat-item:last-child {
            border-bottom: none;
        }
        .stat-label {
            font-weight: 600;
            color: #666;
        }
        .stat-value {
            font-weight: 700;
            color: #667eea;
        }
        .status-running {
            color: #28a745;
            font-weight: 700;
        }
        .status-stopped {
            color: #dc3545;
            font-weight: 700;
        }
        .api-info {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin-top: 20px;
            border-radius: 5px;
        }
        .api-key {
            background: #fff;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            word-break: break-all;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Simple Stress Tester</h1>
        <p style="text-align: center; color: #666; margin-bottom: 20px;">Educational Testing Tool</p>
        
        <div class="warning">
            <strong>⚠️ Legal Warning:</strong> Only test your own servers or servers you have permission to test. 
            Unauthorized testing is illegal!
        </div>
        
        <div class="form-group">
            <label>Attack Method</label>
            <select id="method">
                <option value="GET">HTTP GET Flood</option>
                <option value="POST">HTTP POST Flood</option>
                <option value="TCP">TCP Flood</option>
                <option value="UDP">UDP Flood</option>
                <option value="SLOW">Slowloris</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>Target (URL or IP:PORT)</label>
            <input type="text" id="target" placeholder="https://example.com or 192.168.1.1:80">
        </div>
        
        <div class="form-group">
            <label>Duration (seconds)</label>
            <input type="number" id="duration" value="60" min="1" max="600">
        </div>
        
        <div class="form-group">
            <label>Threads</label>
            <input type="number" id="threads" value="100" min="1" max="1000">
        </div>
        
        <button class="btn btn-primary" onclick="startAttack()">Start Test</button>
        <button class="btn btn-danger" onclick="stopAttack()">Stop Test</button>
        
        <div class="stats-box" id="stats">
            <h3 style="margin-bottom: 15px;">📊 Statistics</h3>
            <div class="stat-item">
                <span class="stat-label">Status:</span>
                <span class="stat-value" id="status">Idle</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Requests Sent:</span>
                <span class="stat-value" id="requests">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Errors:</span>
                <span class="stat-value" id="errors">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Duration:</span>
                <span class="stat-value" id="duration-stat">0s</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Requests/sec:</span>
                <span class="stat-value" id="rps">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Active Threads:</span>
                <span class="stat-value" id="active-threads">0</span>
            </div>
        </div>
        
        <div class="api-info">
            <strong>🔑 API Key:</strong>
            <div class="api-key" id="apiKey">{{ api_key }}</div>
            <p style="margin-top: 10px; font-size: 14px;">
                Use this key for API requests: <code>Authorization: Bearer YOUR_KEY</code>
            </p>
        </div>
    </div>
    
    <script>
        let statsInterval;
        
        function startAttack() {
            const method = document.getElementById('method').value;
            const target = document.getElementById('target').value;
            const duration = document.getElementById('duration').value;
            const threads = document.getElementById('threads').value;
            
            if (!target) {
                alert('Please enter a target!');
                return;
            }
            
            fetch('/api/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {{ api_key }}'
                },
                body: JSON.stringify({
                    method: method,
                    target: target,
                    duration: parseInt(duration),
                    threads: parseInt(threads)
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'started') {
                    alert('Attack started successfully!');
                    startStatsUpdate();
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(err => {
                alert('Error: ' + err.message);
            });
        }
        
        function stopAttack() {
            fetch('/api/stop', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer {{ api_key }}'
                }
            })
            .then(res => res.json())
            .then(data => {
                alert('Attack stopped!');
                updateStats();
                stopStatsUpdate();
            })
            .catch(err => {
                alert('Error: ' + err.message);
            });
        }
        
        function updateStats() {
            fetch('/api/stats', {
                headers: {
                    'Authorization': 'Bearer {{ api_key }}'
                }
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('status').textContent = data.status;
                document.getElementById('status').className = data.status === 'running' ? 'status-running' : 'status-stopped';
                document.getElementById('requests').textContent = data.requests;
                document.getElementById('errors').textContent = data.errors;
                document.getElementById('duration-stat').textContent = data.duration + 's';
                document.getElementById('rps').textContent = data.rps;
                document.getElementById('active-threads').textContent = data.active_threads;
            });
        }
        
        function startStatsUpdate() {
            updateStats();
            statsInterval = setInterval(updateStats, 1000);
        }
        
        function stopStatsUpdate() {
            if (statsInterval) {
                clearInterval(statsInterval);
            }
        }
        
        // Initial stats load
        updateStats();
    </script>
</body>
</html>
'''

def verify_api_key():
    """Verify API key from request"""
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return False
    token = auth.split(' ')[1]
    return token == API_KEY

@app.route('/')
def index():
    """Web interface"""
    return render_template_string(HTML_TEMPLATE, api_key=API_KEY)

@app.route('/api/start', methods=['POST'])
def start_attack():
    """Start attack"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    method = data.get('method', 'GET')
    target = data.get('target')
    duration = data.get('duration', 60)
    threads = data.get('threads', 100)
    
    if not target:
        return jsonify({'error': 'Target is required'}), 400
    
    try:
        result = tester.start_attack(method, target, duration, threads)
        
        # Log to history
        ATTACK_HISTORY.append({
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'target': target,
            'duration': duration,
            'threads': threads
        })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_attack():
    """Stop attack"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        result = tester.stop_attack()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify(tester.get_stats())

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get attack history"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'total': len(ATTACK_HISTORY),
        'history': ATTACK_HISTORY[-20:]  # Last 20 attacks
    })

@app.route('/api/methods', methods=['GET'])
def get_methods():
    """Get available methods"""
    return jsonify({
        'methods': ['GET', 'POST', 'TCP', 'UDP', 'SLOW'],
        'descriptions': {
            'GET': 'HTTP GET flood attack',
            'POST': 'HTTP POST flood attack',
            'TCP': 'TCP connection flood',
            'UDP': 'UDP packet flood',
            'SLOW': 'Slowloris attack (slow HTTP)'
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Simple Stress Tester - API Server")
    print("=" * 60)
    print(f"API Key: {API_KEY}")
    print("")
    print("Web Interface: http://localhost:5000")
    print("API Endpoint: http://localhost:5000/api/")
    print("")
    print("⚠️  WARNING: Only test your own servers!")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

