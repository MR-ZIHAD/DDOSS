#!/usr/bin/env python3
"""
Simple Stress Tester - API Server v2
Auto API Key Setup + No Auth Mode
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import secrets
import json
import os
from datetime import datetime
from stress_core import StressTester

app = Flask(__name__)
CORS(app)

# Configuration
CONFIG_FILE = 'config.json'
ENABLE_AUTH = False  # Set to True to enable authentication

# Global tester instance
tester = StressTester()
ATTACK_HISTORY = []

def load_or_create_config():
    """Load config or create default"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config
    else:
        # Create default config
        config = {
            'api_key': 'simple-stress-tester-2024',
            'enable_auth': False,
            'max_duration': 600,
            'max_threads': 1000,
            'port': 5000
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return config

# Load configuration
CONFIG = load_or_create_config()
API_KEY = CONFIG.get('api_key', 'simple-stress-tester-2024')
ENABLE_AUTH = CONFIG.get('enable_auth', False)

# HTML Template
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
            max-width: 900px;
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
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
            font-size: 1.1em;
        }
        .warning {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }
        .info-box {
            background: #d1ecf1;
            border: 2px solid #17a2b8;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #0c5460;
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
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background: #5a6268;
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
            font-size: 1.1em;
        }
        .status-running {
            color: #28a745;
            animation: pulse 1.5s infinite;
        }
        .status-stopped {
            color: #dc3545;
        }
        .status-idle {
            color: #6c757d;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .method-info {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 14px;
            color: #666;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 10px;
        }
        .badge-success {
            background: #28a745;
            color: white;
        }
        .badge-danger {
            background: #dc3545;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Simple Stress Tester</h1>
        <p class="subtitle">Educational Testing Tool - v2.0</p>
        
        {% if not auth_enabled %}
        <div class="info-box">
            <strong>ℹ️ No Authentication Mode:</strong> API authentication is disabled. 
            Anyone can access this tool. Enable authentication in config.json for security.
        </div>
        {% endif %}
        
        <div class="warning">
            <strong>⚠️ Legal Warning:</strong> Only test your own servers or servers you have permission to test. 
            Unauthorized testing is illegal and punishable by law!
        </div>
        
        <div class="form-group">
            <label>Attack Method</label>
            <select id="method" onchange="updateMethodInfo()">
                <option value="GET">HTTP GET Flood</option>
                <option value="POST">HTTP POST Flood</option>
                <option value="TCP">TCP Flood</option>
                <option value="UDP">UDP Flood</option>
                <option value="SLOW">Slowloris Attack</option>
            </select>
            <div class="method-info" id="method-info">
                Sends multiple HTTP GET requests to test web server capacity
            </div>
        </div>
        
        <div class="form-group">
            <label>Target (URL or IP:PORT)</label>
            <input type="text" id="target" placeholder="https://yoursite.com or 192.168.1.1:80">
        </div>
        
        <div class="grid">
            <div class="form-group">
                <label>Duration (seconds)</label>
                <input type="number" id="duration" value="60" min="1" max="{{ max_duration }}">
            </div>
            
            <div class="form-group">
                <label>Threads</label>
                <input type="number" id="threads" value="100" min="1" max="{{ max_threads }}">
            </div>
        </div>
        
        <button class="btn btn-primary" onclick="startAttack()">▶️ Start Test</button>
        <button class="btn btn-danger" onclick="stopAttack()">⏹️ Stop Test</button>
        
        <div class="stats-box" id="stats">
            <h3 style="margin-bottom: 15px;">📊 Real-time Statistics</h3>
            <div class="stat-item">
                <span class="stat-label">Status:</span>
                <span class="stat-value status-idle" id="status">Idle</span>
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
        
        {% if auth_enabled %}
        <div class="info-box" style="margin-top: 20px;">
            <strong>🔑 API Key:</strong>
            <div style="background: #fff; padding: 10px; border-radius: 5px; font-family: monospace; word-break: break-all; margin-top: 10px;">
                {{ api_key }}
            </div>
            <p style="margin-top: 10px; font-size: 14px;">
                Use this key for API requests: <code>Authorization: Bearer YOUR_KEY</code>
            </p>
        </div>
        {% endif %}
    </div>
    
    <script>
        let statsInterval;
        const authEnabled = {{ 'true' if auth_enabled else 'false' }};
        const apiKey = "{{ api_key }}";
        
        const methodDescriptions = {
            'GET': 'Sends multiple HTTP GET requests to test web server capacity',
            'POST': 'Sends HTTP POST requests with random data to test form processing',
            'TCP': 'Creates TCP connections and sends data to test network layer',
            'UDP': 'Sends UDP packets to test UDP services (connectionless)',
            'SLOW': 'Slowloris attack - keeps connections open with slow requests'
        };
        
        function updateMethodInfo() {
            const method = document.getElementById('method').value;
            document.getElementById('method-info').textContent = methodDescriptions[method];
        }
        
        function getHeaders() {
            const headers = {
                'Content-Type': 'application/json'
            };
            if (authEnabled) {
                headers['Authorization'] = 'Bearer ' + apiKey;
            }
            return headers;
        }
        
        function startAttack() {
            const method = document.getElementById('method').value;
            const target = document.getElementById('target').value;
            const duration = document.getElementById('duration').value;
            const threads = document.getElementById('threads').value;
            
            if (!target) {
                alert('⚠️ Please enter a target!');
                return;
            }
            
            fetch('/api/start', {
                method: 'POST',
                headers: getHeaders(),
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
                    alert('✅ Attack started successfully!');
                    startStatsUpdate();
                } else {
                    alert('❌ Error: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(err => {
                alert('❌ Error: ' + err.message);
            });
        }
        
        function stopAttack() {
            fetch('/api/stop', {
                method: 'POST',
                headers: getHeaders()
            })
            .then(res => res.json())
            .then(data => {
                alert('⏹️ Attack stopped!\\n\\nTotal Requests: ' + data.total_requests + '\\nDuration: ' + data.duration.toFixed(2) + 's');
                updateStats();
                stopStatsUpdate();
            })
            .catch(err => {
                alert('❌ Error: ' + err.message);
            });
        }
        
        function updateStats() {
            fetch('/api/stats', {
                headers: getHeaders()
            })
            .then(res => res.json())
            .then(data => {
                const statusEl = document.getElementById('status');
                statusEl.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
                statusEl.className = 'stat-value status-' + data.status;
                
                document.getElementById('requests').textContent = data.requests.toLocaleString();
                document.getElementById('errors').textContent = data.errors.toLocaleString();
                document.getElementById('duration-stat').textContent = data.duration + 's';
                document.getElementById('rps').textContent = data.rps.toLocaleString();
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
    if not ENABLE_AUTH:
        return True
    
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return False
    token = auth.split(' ')[1]
    return token == API_KEY

@app.route('/')
def index():
    """Web interface"""
    return render_template_string(
        HTML_TEMPLATE, 
        api_key=API_KEY,
        auth_enabled=ENABLE_AUTH,
        max_duration=CONFIG.get('max_duration', 600),
        max_threads=CONFIG.get('max_threads', 1000)
    )

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
    
    # Validate limits
    max_duration = CONFIG.get('max_duration', 600)
    max_threads = CONFIG.get('max_threads', 1000)
    
    if duration > max_duration:
        return jsonify({'error': f'Duration cannot exceed {max_duration} seconds'}), 400
    
    if threads > max_threads:
        return jsonify({'error': f'Threads cannot exceed {max_threads}'}), 400
    
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
        'history': ATTACK_HISTORY[-20:]
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

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'auth_enabled': ENABLE_AUTH,
        'max_duration': CONFIG.get('max_duration', 600),
        'max_threads': CONFIG.get('max_threads', 1000),
        'port': CONFIG.get('port', 5000)
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Simple Stress Tester - API Server v2.0")
    print("=" * 70)
    print(f"📁 Config File: {CONFIG_FILE}")
    print(f"🔑 API Key: {API_KEY}")
    print(f"🔒 Authentication: {'Enabled' if ENABLE_AUTH else 'Disabled (Open Access)'}")
    print(f"⏱️  Max Duration: {CONFIG.get('max_duration', 600)} seconds")
    print(f"🧵 Max Threads: {CONFIG.get('max_threads', 1000)}")
    print("")
    print(f"🌐 Web Interface: http://localhost:{CONFIG.get('port', 5000)}")
    print(f"🔌 API Endpoint: http://localhost:{CONFIG.get('port', 5000)}/api/")
    print("")
    if not ENABLE_AUTH:
        print("⚠️  WARNING: Authentication is DISABLED!")
        print("   Anyone can access this tool. Enable auth in config.json for security.")
    print("")
    print("⚠️  LEGAL: Only test your own servers!")
    print("=" * 70)
    
    app.run(
        host='0.0.0.0', 
        port=CONFIG.get('port', 5000), 
        debug=False, 
        threaded=True
    )

