# Simple Stress Tester v2.0 - Auto API Key Setup

## 🎉 নতুন Features (v2.0):

### ✅ Auto API Key Setup
- First run করলে **automatic config.json** create হবে
- Default API key: `simple-stress-tester-2024`
- আপনি চাইলে custom key set করতে পারবেন

### ✅ No Authentication Mode
- `enable_auth: false` set করলে **কোনো API key লাগবে না**
- Easy testing এর জন্য perfect
- Production এ `enable_auth: true` করুন

### ✅ Configuration File
- সব settings `config.json` এ
- API key, max duration, max threads control করুন
- Server port change করতে পারবেন

---

## 🚀 Quick Start (3 Steps):

### Step 1: Install
```bash
pip install flask flask-cors requests
```

### Step 2: Run
```bash
python api_server_v2.py
```

### Step 3: Open Browser
```
http://localhost:5000
```

**That's it! কোনো API key setup লাগবে না!** 🎉

---

## ⚙️ Configuration (config.json):

```json
{
  "api_key": "simple-stress-tester-2024",
  "enable_auth": false,
  "max_duration": 600,
  "max_threads": 1000,
  "port": 5000
}
```

### Settings বিস্তারিত:

| Setting | Default | Description |
|---------|---------|-------------|
| `api_key` | `simple-stress-tester-2024` | API authentication key |
| `enable_auth` | `false` | API key check করবে কিনা |
| `max_duration` | `600` | Maximum attack duration (seconds) |
| `max_threads` | `1000` | Maximum threads allowed |
| `port` | `5000` | Server port |

---

## 🔐 Authentication Modes:

### Mode 1: No Authentication (Default)
```json
{
  "enable_auth": false
}
```
- কোনো API key লাগবে না
- সবাই access করতে পারবে
- Local testing এর জন্য perfect

### Mode 2: With Authentication
```json
{
  "enable_auth": true,
  "api_key": "your-secret-key-here"
}
```
- API key দিয়ে protect করা
- শুধু authorized users access করতে পারবে
- Production/Remote access এর জন্য

---

## 💻 Usage Examples:

### Web Interface (No API Key Needed):

1. Browser এ open করুন: `http://localhost:5000`
2. Form fill করুন
3. "Start Test" click করুন
4. Done! 🎉

### API Usage (If Auth Enabled):

```bash
# Start attack
curl -X POST http://localhost:5000/api/start \
  -H "Authorization: Bearer simple-stress-tester-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "GET",
    "target": "https://yoursite.com",
    "duration": 60,
    "threads": 100
  }'

# Get stats
curl http://localhost:5000/api/stats \
  -H "Authorization: Bearer simple-stress-tester-2024"
```

### API Usage (If Auth Disabled):

```bash
# Start attack (no auth header needed!)
curl -X POST http://localhost:5000/api/start \
  -H "Content-Type: application/json" \
  -d '{
    "method": "GET",
    "target": "https://yoursite.com",
    "duration": 60,
    "threads": 100
  }'

# Get stats (no auth needed!)
curl http://localhost:5000/api/stats
```

---

## 🎯 Custom Configuration:

### Change API Key:
```json
{
  "api_key": "my-super-secret-key-2024"
}
```

### Increase Limits:
```json
{
  "max_duration": 1800,
  "max_threads": 5000
}
```

### Change Port:
```json
{
  "port": 8080
}
```

### Enable Security:
```json
{
  "enable_auth": true,
  "api_key": "random-secure-key-here"
}
```

---

## 📋 Comparison: v1 vs v2

| Feature | v1 | v2 |
|---------|----|----|
| API Key Setup | Manual (code edit) | **Auto (config file)** |
| Authentication | Always required | **Optional** |
| Configuration | Hard-coded | **File-based** |
| First Run | Need to edit code | **Ready to use** |
| Custom Settings | Edit Python code | **Edit JSON file** |
| Port Change | Edit code | **Edit config** |

---

## 🔄 Migration from v1 to v2:

### Old Way (v1):
```python
# Edit api_server.py
API_KEY = "YOUR_SECRET_TOKEN_HERE"  # Change this!
```

### New Way (v2):
```json
// Edit config.json
{
  "api_key": "your-key-here"
}
```

**Much easier! 🎉**

---

## 🛠️ Advanced Usage:

### Generate Random API Key:

```python
import secrets
print(secrets.token_hex(16))
# Output: 3f7a8b2c9d1e4f5a6b7c8d9e0f1a2b3c
```

### Use Environment Variables:

```bash
export STRESS_API_KEY="my-secret-key"
export STRESS_PORT=8080
python api_server_v2.py
```

### Multiple Instances:

```bash
# Instance 1 (port 5000)
python api_server_v2.py

# Instance 2 (port 5001)
# Edit config.json: "port": 5001
python api_server_v2.py
```

---

## 📊 Features Summary:

### ✅ v2.0 Features:
- Auto config file creation
- No authentication mode
- File-based configuration
- Custom API keys
- Port configuration
- Max limits control
- Better security options
- Easier deployment

### ✅ Original Features:
- 5 attack methods
- Web interface
- REST API
- Real-time stats
- Attack history
- Multi-threading
- Clean code

---

## 🎓 Configuration Examples:

### Example 1: Local Testing (No Security)
```json
{
  "api_key": "test",
  "enable_auth": false,
  "max_duration": 60,
  "max_threads": 100,
  "port": 5000
}
```

### Example 2: Production (High Security)
```json
{
  "api_key": "3f7a8b2c9d1e4f5a6b7c8d9e0f1a2b3c",
  "enable_auth": true,
  "max_duration": 300,
  "max_threads": 500,
  "port": 8080
}
```

### Example 3: High Performance
```json
{
  "api_key": "performance-test",
  "enable_auth": false,
  "max_duration": 1800,
  "max_threads": 5000,
  "port": 5000
}
```

---

## ⚠️ Security Recommendations:

### 🔒 For Production:
1. ✅ Set `enable_auth: true`
2. ✅ Use strong random API key
3. ✅ Use HTTPS (reverse proxy)
4. ✅ Set reasonable limits
5. ✅ Monitor access logs

### 🏠 For Local Testing:
1. ✅ `enable_auth: false` is OK
2. ✅ Use localhost only
3. ✅ Don't expose to internet
4. ✅ Use low thread counts

---

## 🎉 Summary:

### v2.0 এ কি পাচ্ছেন:

✅ **Auto Setup** - কোনো manual configuration লাগবে না
✅ **No Auth Mode** - API key ছাড়াই use করতে পারবেন
✅ **Config File** - সব settings এক জায়গায়
✅ **Easy Deployment** - download করে run করুন
✅ **Flexible** - যেকোনো setting change করতে পারবেন
✅ **Secure** - চাইলে authentication enable করতে পারবেন

---

## 🚀 Quick Commands:

```bash
# Install
pip install flask flask-cors requests

# Run v2
python api_server_v2.py

# Open browser
http://localhost:5000

# Test API (no auth)
curl -X POST http://localhost:5000/api/start \
  -H "Content-Type: application/json" \
  -d '{"method":"GET","target":"https://example.com","duration":10,"threads":50}'

# Get stats (no auth)
curl http://localhost:5000/api/stats
```

---

**Perfect! এখন কোনো manual setup লাগবে না! 🎉**

**Just download, run, and test! 🚀**

