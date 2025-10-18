#!/usr/bin/env python3
"""
Enhanced Stress Tester - Auto Port Finder
Automatically finds available port
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import os
import socket
from datetime import datetime
from stress_core_enhanced import EnhancedStressTester

app = Flask(__name__)
CORS(app)

# Global tester instance
tester = EnhancedStressTester()
ATTACK_HISTORY = []
CURRENT_PORT = 5000

def find_free_port(start_port=5000, max_attempts=100):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

# HTML Template (same as before but dynamic port)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Enhanced Stress Tester</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        h1 {
            color: #f5576c;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .badge {
            background: #ff6b6b;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            display: inline-block;
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
        }
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
        }
        .btn-primary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .btn-danger {
            background: #dc3545;
            color: white;
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
        .stat-value {
            font-weight: 700;
            color: #f5576c;
            font-size: 1.2em;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Enhanced Stress Tester</h1>
        <p style="text-align: center; color: #666; margin-bottom: 20px;">
            <span class="badge">Port: {{ port }}</span>
        </p>
        
        <div class="warning">
            <strong>⚠️ WARNING:</strong> Only test YOUR OWN servers! Unauthorized use is ILLEGAL!
        </div>
        
        <div class="form-group">
            <label>Attack Method</label>
            <select id="method">
                <option value="GET">HTTP GET Flood</option>
                <option value="POST">HTTP POST Flood</option>
                <option value="MIXED">Mixed Attack (Powerful!)</option>
                <option value="TCP">TCP Flood</option>
                <option value="UDP">UDP Flood</option>
                <option value="SLOW">Slowloris</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>Target URL or IP:PORT</label>
            <input type="text" id="target" placeholder="https://yoursite.com">
        </div>
        
        <div class="grid">
            <div class="form-group">
                <label>Duration (seconds)</label>
                <input type="number" id="duration" value="120" min="10" max="1800">
            </div>
            
            <div class="form-group">
                <label>Threads</label>
                <input type="number" id="threads" value="1500" min="100" max="5000">
            </div>
        </div>
        
        <button class="btn btn-primary" onclick="startAttack()">⚡ Launch Attack</button>
        <button class="btn btn-danger" onclick="stopAttack()">⏹️ Stop Attack</button>
        
        <div class="stats-box">
            <h3 style="margin-bottom: 15px;">📊 Statistics</h3>
            <div class="stat-item">
                <span>Status:</span>
                <span class="stat-value" id="status">Idle</span>
            </div>
            <div class="stat-item">
                <span>Requests:</span>
                <span class="stat-value" id="requests">0</span>
            </div>
            <div class="stat-item">
                <span>Duration:</span>
                <span class="stat-value" id="duration-stat">0s</span>
            </div>
            <div class="stat-item">
                <span>Requests/sec:</span>
                <span class="stat-value" id="rps">0</span>
            </div>
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
                alert('⚠️ Please enter a target!');
                return;
            }
            
            fetch('/api/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
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
                    alert('⚡ Attack launched!');
                    startStatsUpdate();
                } else {
                    alert('❌ Error: ' + (data.error || 'Unknown'));
                }
            })
            .catch(err => alert('❌ Error: ' + err.message));
        }
        
        function stopAttack() {
            fetch('/api/stop', {method: 'POST'})
            .then(res => res.json())
            .then(data => {
                alert('⏹️ Stopped! Total: ' + data.total_requests.toLocaleString());
                updateStats();
                stopStatsUpdate();
            });
        }
        
        function updateStats() {
            fetch('/api/stats')
            .then(res => res.json())
            .then(data => {
                document.getElementById('status').textContent = data.status.toUpperCase();
                document.getElementById('requests').textContent = data.requests.toLocaleString();
                document.getElementById('duration-stat').textContent = data.duration + 's';
                document.getElementById('rps').textContent = data.rps.toLocaleString();
            });
        }
        
        function startStatsUpdate() {
            updateStats();
            statsInterval = setInterval(updateStats, 1000);
        }
        
        function stopStatsUpdate() {
            if (statsInterval) clearInterval(statsInterval);
        }
        
        updateStats();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, port=CURRENT_PORT)

@app.route('/api/start', methods=['POST'])
def start_attack():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    
    method = data.get('method', 'GET')
    target = data.get('target')
    duration = data.get('duration', 120)
    threads = data.get('threads', 1000)
    
    if not target:
        return jsonify({'error': 'Target required'}), 400
    
    try:
        result = tester.start_attack(method, target, duration, threads)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_attack():
    try:
        return jsonify(tester.stop_attack())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(tester.get_stats())

if __name__ == '__main__':
    # Find free port
    port = find_free_port(5000)
    
    if port is None:
        print("❌ ERROR: No free port found!")
        print("Try: pkill -9 python")
        exit(1)
    
    CURRENT_PORT = port
    
    print("=" * 70)
    print("⚡ Enhanced Stress Tester - AUTO PORT")
    print("=" * 70)
    print(f"✅ Found free port: {port}")
    print(f"🌐 Web Interface: http://localhost:{port}")
    print("")
    print("⚠️  WARNING: Only test YOUR OWN servers!")
    print("=" * 70)
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Try: pkill -9 python")

