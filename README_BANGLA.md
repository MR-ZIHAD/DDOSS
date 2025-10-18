# Simple Stress Tester - সম্পূর্ণ বাংলা গাইড

## 🎯 এটা কি?

এটি একটি **সম্পূর্ণ নতুন, original code** দিয়ে তৈরি stress testing tool। কোনো copy করা code নেই!

### ✨ Features:

- ✅ **Web Interface** - Browser দিয়ে control করুন
- ✅ **REST API** - Programming করে use করুন
- ✅ **Real-time Stats** - Live statistics দেখুন
- ✅ **5 Attack Methods** - GET, POST, TCP, UDP, Slowloris
- ✅ **Simple & Clean** - সহজ code, easily বোঝা যায়
- ✅ **Educational** - Learning এর জন্য perfect

---

## 🚀 Installation

### Termux এ Install করুন:

```bash
# Step 1: Update করুন
pkg update && pkg upgrade -y

# Step 2: Python install করুন
pkg install python -y

# Step 3: Pip upgrade করুন
pip install --upgrade pip

# Step 4: Dependencies install করুন
pip install flask flask-cors requests

# Step 5: Server চালান
python api_server.py
```

### Linux/VPS এ Install করুন:

```bash
# Step 1: Python check করুন
python3 --version

# Step 2: Dependencies install করুন
pip3 install -r requirements.txt

# Step 3: Server চালান
python3 api_server.py
```

---

## 💻 কিভাবে ব্যবহার করবেন

### Method 1: Web Interface (সবচেয়ে সহজ)

1. Server start করুন:
```bash
python api_server.py
```

2. Browser এ open করুন:
```
http://localhost:5000
```

3. Form fill করুন:
   - **Method**: GET/POST/TCP/UDP/SLOW select করুন
   - **Target**: আপনার website URL বা IP:PORT দিন
   - **Duration**: কত সেকেন্ড চালাবেন (1-600)
   - **Threads**: কত threads use করবেন (1-1000)

4. **"Start Test"** button click করুন

5. Real-time statistics দেখুন!

---

### Method 2: API দিয়ে (Programming)

#### API Key পাবেন:

Server start করলে console এ API key দেখাবে:
```
API Key: abc123def456...
```

#### API Endpoints:

**1. Start Attack**
```bash
curl -X POST http://localhost:5000/api/start \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "GET",
    "target": "https://example.com",
    "duration": 60,
    "threads": 100
  }'
```

**2. Stop Attack**
```bash
curl -X POST http://localhost:5000/api/stop \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**3. Get Statistics**
```bash
curl http://localhost:5000/api/stats \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**4. Get Attack History**
```bash
curl http://localhost:5000/api/history \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**5. Get Available Methods**
```bash
curl http://localhost:5000/api/methods
```

---

## 📖 Attack Methods বিস্তারিত

### 1. GET - HTTP GET Flood
- HTTP GET requests পাঠায়
- Random parameters add করে cache bypass করে
- Web servers test করার জন্য best

**Example:**
```json
{
  "method": "GET",
  "target": "https://yoursite.com",
  "duration": 60,
  "threads": 200
}
```

### 2. POST - HTTP POST Flood
- HTTP POST requests পাঠায়
- Random data send করে
- Form processing test করার জন্য

**Example:**
```json
{
  "method": "POST",
  "target": "https://yoursite.com/api",
  "duration": 120,
  "threads": 150
}
```

### 3. TCP - TCP Flood
- TCP connections create করে
- Random data send করে
- Network layer test করার জন্য

**Example:**
```json
{
  "method": "TCP",
  "target": "192.168.1.1:80",
  "duration": 180,
  "threads": 300
}
```

### 4. UDP - UDP Flood
- UDP packets পাঠায়
- Connectionless protocol
- UDP services test করার জন্য

**Example:**
```json
{
  "method": "UDP",
  "target": "192.168.1.1:53",
  "duration": 120,
  "threads": 500
}
```

### 5. SLOW - Slowloris Attack
- Slow HTTP requests পাঠায়
- Connections open রাখে
- Server timeout test করার জন্য

**Example:**
```json
{
  "method": "SLOW",
  "target": "192.168.1.1:80",
  "duration": 300,
  "threads": 100
}
```

---

## 📊 Statistics Explained

### Web Interface এ দেখাবে:

- **Status**: `running` বা `stopped`
- **Requests Sent**: মোট কত requests পাঠানো হয়েছে
- **Errors**: কত errors হয়েছে
- **Duration**: কত সময় চলছে
- **Requests/sec**: প্রতি সেকেন্ডে কত requests
- **Active Threads**: কত threads active আছে

---

## 🔧 Configuration

### Threads সংখ্যা:

- **Low RAM (1-2GB)**: 50-100 threads
- **Medium RAM (3-4GB)**: 100-300 threads
- **High RAM (6GB+)**: 300-1000 threads

### Duration:

- **Quick Test**: 10-30 seconds
- **Standard Test**: 60-120 seconds
- **Long Test**: 300-600 seconds

### Target Format:

**HTTP/HTTPS:**
```
https://example.com
http://example.com:8080
https://example.com/path
```

**TCP/UDP:**
```
192.168.1.1:80
example.com:443
10.0.0.1:8080
```

---

## 🛡️ Security & Legal

### ⚠️ Legal Warning:

- ✅ **শুধুমাত্র নিজের server test করুন**
- ✅ **অনুমতি নিয়ে test করুন**
- ✅ **Educational purpose এ use করুন**
- ❌ **অন্যের server attack করবেন না**
- ❌ **Illegal activities করবেন না**

### 🔐 API Key Security:

- API key গোপন রাখুন
- Public করবেন না
- প্রতিবার নতুন key generate হয়
- Server restart করলে নতুন key পাবেন

---

## 💡 Tips & Tricks

### 1. Termux এ Background Run:

```bash
# Tmux install করুন
pkg install tmux -y

# New session create করুন
tmux new -s stress

# Server চালান
python api_server.py

# Detach: Ctrl+B then D
# Reattach: tmux attach -t stress
```

### 2. Remote Access:

Server অন্য device থেকে access করতে:

```bash
# আপনার IP খুঁজুন
ifconfig | grep inet

# Browser এ open করুন
http://YOUR_IP:5000
```

### 3. Multiple Targets Test:

Python script লিখে multiple targets test করুন:

```python
import requests
import time

API_KEY = "your_api_key_here"
targets = [
    "https://site1.com",
    "https://site2.com",
    "https://site3.com"
]

for target in targets:
    response = requests.post(
        "http://localhost:5000/api/start",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "method": "GET",
            "target": target,
            "duration": 60,
            "threads": 100
        }
    )
    print(f"Testing {target}: {response.json()}")
    time.sleep(65)  # Wait for completion
```

### 4. Monitoring:

Real-time monitoring করতে:

```bash
# Stats check করুন
watch -n 1 'curl -s http://localhost:5000/api/stats \
  -H "Authorization: Bearer YOUR_KEY" | python -m json.tool'
```

---

## 🐛 Troubleshooting

### Error 1: "Address already in use"

**Solution:**
```bash
# Port 5000 kill করুন
pkill -f api_server.py

# অথবা different port use করুন
# api_server.py তে শেষের line change করুন:
app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
```

### Error 2: "Connection refused"

**Solution:**
- Target URL সঠিক আছে কিনা check করুন
- Internet connection check করুন
- Firewall check করুন

### Error 3: "Too many open files"

**Solution:**
```bash
# Threads কমিয়ে দিন
# অথবা ulimit increase করুন
ulimit -n 4096
```

### Error 4: "Module not found"

**Solution:**
```bash
pip install flask flask-cors requests
```

---

## 📁 File Structure

```
SimpleStressTester/
├── stress_core.py          # Core attack logic
├── api_server.py           # Flask API server
├── requirements.txt        # Python dependencies
└── README_BANGLA.md        # This file
```

---

## 🔄 Updates & Improvements

### Future Features (আপনি add করতে পারেন):

1. **Proxy Support** - Proxy দিয়ে attack
2. **Custom Headers** - নিজের headers set করুন
3. **Attack Scheduling** - Scheduled attacks
4. **Multiple Targets** - একসাথে multiple targets
5. **Report Generation** - PDF reports
6. **Database Logging** - Attack history save করুন

---

## 📞 Support

### যদি problem হয়:

1. **Error message** screenshot নিন
2. **Python version** check করুন: `python --version`
3. **Dependencies** reinstall করুন: `pip install -r requirements.txt`
4. **Server logs** check করুন console এ

---

## ✅ Quick Start Checklist

- [ ] Python installed (3.7+)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server running (`python api_server.py`)
- [ ] Browser opened (`http://localhost:5000`)
- [ ] API key copied
- [ ] Target URL ready (your own server!)
- [ ] Legal permission confirmed

---

## 🎓 Learning Resources

### Code বুঝতে চান?

**stress_core.py** - Core attack logic:
- `http_get_flood()` - GET attack কিভাবে কাজ করে
- `http_post_flood()` - POST attack logic
- `tcp_flood()` - TCP connection flooding
- `udp_flood()` - UDP packet sending
- `slowloris_attack()` - Slow HTTP attack

**api_server.py** - API server:
- Flask routes setup
- API authentication
- Web interface HTML
- Statistics tracking

---

## 🎉 Summary

এই tool দিয়ে আপনি:

✅ **নিজের website** stress test করতে পারবেন
✅ **Server capacity** check করতে পারবেন
✅ **Web interface** দিয়ে easily control করতে পারবেন
✅ **API** দিয়ে automate করতে পারবেন
✅ **Real-time statistics** দেখতে পারবেন
✅ **Code শিখতে** পারবেন (সম্পূর্ণ original!)

---

<p align="center">
  <b>Happy Testing! 🚀</b>
</p>

<p align="center">
  <b>Remember: Only test your own servers! ⚠️</b>
</p>

<p align="center">
  <b>Use Responsibly & Legally! ⚖️</b>
</p>

