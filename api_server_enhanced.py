#!/usr/bin/env python3
"""
Enhanced Stress Tester - More Powerful Version
Optimized for maximum impact
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import os
from datetime import datetime
from stress_core_enhanced import EnhancedStressTester

app = Flask(__name__)
CORS(app)

# Configuration
CONFIG_FILE = 'config_enhanced.json'

# Global tester instance
tester = EnhancedStressTester()
ATTACK_HISTORY = []

def load_or_create_config():
    """Load config or create default"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        config = {
            'api_key': 'enhanced-stress-2024',
            'enable_auth': False,
            'max_duration': 1800,
            'max_threads': 5000,
            'port': 5000,
            'recommended_threads': {
                'low_ram': 500,
                'medium_ram': 1500,
                'high_ram': 3000
            }
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return config

CONFIG = load_or_create_config()
API_KEY = CONFIG.get('api_key', 'enhanced-stress-2024')
ENABLE_AUTH = CONFIG.get('enable_auth', False)

# HTML Template
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
            margin-left: 10px;
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
        .power-info {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .power-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .power-feature {
            background: rgba(255,255,255,0.2);
            padding: 10px;
            border-radius: 5px;
            text-align: center;
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
            border-color: #f5576c;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
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
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
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
        .status-running {
            color: #28a745;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Enhanced Stress Tester <span class="badge">POWERFUL</span></h1>
        <p class="subtitle">Maximum Impact Testing Tool</p>
        
        <div class="power-info">
            <h3 style="margin-bottom: 10px;">🚀 Enhanced Features:</h3>
            <div class="power-features">
                <div class="power-feature">✅ Keep-Alive Connections</div>
                <div class="power-feature">✅ Cache Bypass</div>
                <div class="power-feature">✅ Large Payloads</div>
                <div class="power-feature">✅ Mixed Attacks</div>
                <div class="power-feature">✅ Optimized Threading</div>
                <div class="power-feature">✅ No Delays</div>
            </div>
        </div>
        
        <div class="warning">
            <strong>⚠️ POWERFUL TOOL:</strong> This enhanced version is significantly more powerful. 
            Use ONLY on your own servers. Unauthorized use is ILLEGAL!
        </div>
        
        <div class="form-group">
            <label>Attack Method</label>
            <select id="method">
                <option value="GET">HTTP GET Flood (Enhanced)</option>
                <option value="POST">HTTP POST Flood (Enhanced)</option>
                <option value="MIXED">Mixed Attack (GET + POST)</option>
                <option value="TCP">TCP Flood (Enhanced)</option>
                <option value="UDP">UDP Flood (Enhanced)</option>
                <option value="SLOW">Slowloris (Enhanced)</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>Target URL or IP:PORT</label>
            <input type="text" id="target" placeholder="https://yoursite.com">
        </div>
        
        <div class="grid">
            <div class="form-group">
                <label>Duration (seconds) - Max: {{ max_duration }}</label>
                <input type="number" id="duration" value="120" min="10" max="{{ max_duration }}">
            </div>
            
            <div class="form-group">
                <label>Threads - Recommended: {{ recommended }}</label>
                <input type="number" id="threads" value="{{ recommended }}" min="100" max="{{ max_threads }}">
            </div>
        </div>
        
        <button class="btn btn-primary" onclick="startAttack()">⚡ Launch Enhanced Attack</button>
        <button class="btn btn-danger" onclick="stopAttack()">⏹️ Stop Attack</button>
        
        <div class="stats-box">
            <h3 style="margin-bottom: 15px;">📊 Real-time Statistics</h3>
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
    </div>
    
    <script>
        let statsInterval;
        const authEnabled = {{ 'true' if auth_enabled else 'false' }};
        const apiKey = "{{ api_key }}";
        
        function getHeaders() {
            const headers = {'Content-Type': 'application/json'};
            if (authEnabled) headers['Authorization'] = 'Bearer ' + apiKey;
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
            
            if (!confirm('⚠️ Are you sure you want to launch this POWERFUL attack?\\n\\nMake sure you have permission to test this target!')) {
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
                    alert('⚡ Enhanced attack launched!\\n\\nMethod: ' + method + '\\nThreads: ' + threads);
                    startStatsUpdate();
                } else {
                    alert('❌ Error: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(err => alert('❌ Error: ' + err.message));
        }
        
        function stopAttack() {
            fetch('/api/stop', {
                method: 'POST',
                headers: getHeaders()
            })
            .then(res => res.json())
            .then(data => {
                alert('⏹️ Attack stopped!\\n\\nTotal: ' + data.total_requests.toLocaleString() + ' requests\\nDuration: ' + data.duration.toFixed(2) + 's');
                updateStats();
                stopStatsUpdate();
            })
            .catch(err => alert('❌ Error: ' + err.message));
        }
        
        function updateStats() {
            fetch('/api/stats', {headers: getHeaders()})
            .then(res => res.json())
            .then(data => {
                document.getElementById('status').textContent = data.status.toUpperCase();
                document.getElementById('status').className = 'stat-value status-' + data.status;
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
            if (statsInterval) clearInterval(statsInterval);
        }
        
        updateStats();
    </script>
</body>
</html>
'''

def verify_api_key():
    if not ENABLE_AUTH:
        return True
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return False
    return auth.split(' ')[1] == API_KEY

@app.route('/')
def index():
    recommended = CONFIG.get('recommended_threads', {}).get('medium_ram', 1500)
    return render_template_string(
        HTML_TEMPLATE,
        api_key=API_KEY,
        auth_enabled=ENABLE_AUTH,
        max_duration=CONFIG.get('max_duration', 1800),
        max_threads=CONFIG.get('max_threads', 5000),
        recommended=recommended
    )

@app.route('/api/start', methods=['POST'])
def start_attack():
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    method = data.get('method', 'GET')
    target = data.get('target')
    duration = data.get('duration', 120)
    threads = data.get('threads', 1000)
    
    if not target:
        return jsonify({'error': 'Target is required'}), 400
    
    try:
        result = tester.start_attack(method, target, duration, threads)
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
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        return jsonify(tester.stop_attack())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(tester.get_stats())

@app.route('/api/methods', methods=['GET'])
def get_methods():
    return jsonify({
        'methods': ['GET', 'POST', 'MIXED', 'TCP', 'UDP', 'SLOW'],
        'descriptions': {
            'GET': 'Enhanced HTTP GET flood with keep-alive',
            'POST': 'Enhanced HTTP POST flood with large payloads',
            'MIXED': 'Mixed attack (GET + POST combined)',
            'TCP': 'Enhanced TCP flood',
            'UDP': 'Enhanced UDP flood with large packets',
            'SLOW': 'Enhanced Slowloris attack'
        }
    })

if __name__ == '__main__':
    print("=" * 70)
    print("⚡ Enhanced Stress Tester - POWERFUL VERSION")
    print("=" * 70)
    print(f"🔑 API Key: {API_KEY}")
    print(f"🔒 Auth: {'Enabled' if ENABLE_AUTH else 'Disabled'}")
    print(f"🧵 Max Threads: {CONFIG.get('max_threads', 5000)}")
    print(f"⏱️  Max Duration: {CONFIG.get('max_duration', 1800)}s")
    print("")
    print(f"🌐 Web: http://localhost:{CONFIG.get('port', 5000)}")
    print("")
    print("⚠️  WARNING: This is a POWERFUL tool!")
    print("   Only test YOUR OWN servers!")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=CONFIG.get('port', 5000), debug=False, threaded=True)

