# 🤖 Bot Attack Testing Guide

## **🎯 How to Test Bot Attacks**

Your Cyber Defense System has **bot detection** built-in. Here's how to test it:

---

## **📋 Prerequisites**

1. **Server Running**: Make sure Django server is running
   ```bash
   python manage.py runserver
   ```

2. **Python Installed**: Need `requests` library
   ```bash
   pip install requests
   ```

3. **Correct URL**: Use the running server URL
   - Default: `http://127.0.0.1:8000/honeypot-login/`
   - Alternative: `http://0.0.0.0:8000/honeypot-login/`

---

## **🧪 Method 1: Simple Bot Test**

### **Create Test File: `simple_bot.py`**
```python
import requests

# Bot Attack Test
url = "http://127.0.0.1:8000/honeypot-login/"

# Bot headers (this triggers detection)
headers = {
    'User-Agent': 'python-requests/2.28.1'  # This will be detected as bot!
}

# Bot data
data = {
    "username": "admin",
    "password": "12345",
    "website": "bot-test"  # Hidden honeypot field
}

print("🤖 Testing Bot Attack...")

try:
    # Send bot attack
    response = requests.post(url, data=data, headers=headers)
    
    print(f"📊 Status Code: {response.status_code}")
    print(f"📄 Response: {response.text[:200]}...")
    
    # Check if bot was detected
    if response.status_code == 200:
        if "Invalid credentials" in response.text:
            print("🛡️  SUCCESS: Bot detected and blocked!")
        else:
            print("⚠️  Bot NOT detected")
    else:
        print(f"❓ Unexpected status: {response.status_code}")

except Exception as e:
    print(f"❌ Error: {e}")
```

### **Run the Test:**
```bash
python simple_bot.py
```

**Expected Result:**
- **Attack Type**: "Bot Attack"
- **Threat Score**: 8+
- **User Type**: "Suspicious"
- **Response**: "Invalid credentials" message

---

## **🧪 Method 2: Command Line Bot Test**

### **Using curl:**
```bash
curl -X POST \
  -H "User-Agent: python-requests/2.28.1" \
  -d "username=admin&password=12345&website=bot-test" \
  http://127.0.0.1:8000/honeypot-login/
```

### **Using PowerShell:**
```powershell
$headers = @{
    "User-Agent" = "python-requests/2.28.1"
}

$data = @{
    "username" = "admin"
    "password" = "12345"
    "website" = "bot-test"
}

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/honeypot-login/" -Method POST -Headers $headers -Body $data
$response.Content
```

---

## **🧪 Method 3: Advanced Bot Test**

### **Create `advanced_bot.py`:**
```python
import requests
import time
import random

class AdvancedBot:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/honeypot-login/"
        self.session = requests.Session()
        
    def test_bot_detection(self):
        """Test various bot detection methods"""
        
        # Test 1: Python requests user-agent
        print("🤖 Test 1: Python Requests Bot")
        headers = {'User-Agent': 'python-requests/2.28.1'}
        data = {
            "username": "admin",
            "password": "bot123",
            "website": "python-bot"  # Hidden field
        }
        
        try:
            response = self.session.post(self.url, data=data, headers=headers)
            print(f"Status: {response.status_code}")
            if "Invalid credentials" in response.text:
                print("✅ Python bot detected!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def test_curl_bot(self):
        """Test curl-like bot"""
        print("\n🤖 Test 2: Curl Bot")
        headers = {'User-Agent': 'curl/7.68.0'}
        data = {
            "username": "admin",
            "password": "curl123",
            "website": "curl-bot"
        }
        
        try:
            response = self.session.post(self.url, data=data, headers=headers)
            print(f"Status: {response.status_code}")
            if "Invalid credentials" in response.text:
                print("✅ Curl bot detected!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def test_selenium_bot(self):
        """Test selenium-like bot"""
        print("\n🤖 Test 3: Selenium Bot")
        headers = {'User-Agent': 'selenium/3.141.59'}
        data = {
            "username": "admin",
            "password": "selenium123",
            "website": "selenium-bot"
        }
        
        try:
            response = self.session.post(self.url, data=data, headers=headers)
            print(f"Status: {response.status_code}")
            if "Invalid credentials" in response.text:
                print("✅ Selenium bot detected!")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    bot = AdvancedBot()
    
    print("🎯 ADVANCED BOT TESTING")
    print("=" * 50)
    
    # Run all tests
    bot.test_bot_detection()
    time.sleep(1)
    bot.test_curl_bot()
    time.sleep(1)
    bot.test_selenium_bot()
    
    print("\n" + "=" * 50)
    print("🏆 Bot testing completed!")
    print("📊 Check dashboard: http://127.0.0.1:8000/dashboard/")
    print("=" * 50)
```

### **Run Advanced Test:**
```bash
python advanced_bot.py
```

---

## **🎯 What Triggers Bot Detection**

### **1. User-Agent Detection**
Your system detects these user-agents:
- `python-requests`
- `curl`
- `selenium`
- `postman`
- `wget`
- `bot`
- `crawler`

### **2. Hidden Field Detection**
- Field name: `website`
- Style: `display:none;`
- Detection: Any non-empty value

### **3. Timing Analysis**
- Fast submission (< 2 seconds)
- Indicates automated behavior

### **4. Repetitive Patterns**
- Multiple similar requests
- Same IP within short time

---

## **📊 Expected Results**

### **Successful Bot Detection:**
```
🤖 Testing Bot Attack...
📊 Status Code: 200
📄 Response: Invalid credentials...
🛡️  SUCCESS: Bot detected and blocked!
```

### **Dashboard Should Show:**
- **Attack Type**: "Bot Attack"
- **User Type**: "Suspicious" (or "Attacker" if high score)
- **Threat Score**: 8+ points
- **Attack Reason**: "Bot detected: [user-agent]"

### **Attack Logs Should Show:**
- IP address of bot
- Username attempted
- "Bot Attack" classification
- Bot user-agent string
- Timestamp

---

## **🔧 Troubleshooting**

### **If Bot Not Detected:**

1. **Check User-Agent**: Make sure it contains bot indicators
2. **Hidden Field**: Verify `website` field is filled
3. **Server Running**: Confirm Django server is active
4. **Correct URL**: Use the right port and path

### **Common Issues:**
```bash
# Connection refused - server not running
❌ Error: [WinError 10061] No connection could be made

# Fix: Start the server
python manage.py runserver

# Wrong URL - 404 error
❌ Error: 404 Not Found

# Fix: Use correct URL
http://127.0.0.1:8000/honeypot-login/
```

### **Debug Steps:**
1. **Test Manual Access**: Open URL in browser
2. **Check Server Logs**: Look for Django output
3. **Verify Headers**: Check user-agent string
4. **Test Step by Step**: Try one detection method at a time

---

## **🎭 Bot Detection Evasion (For Testing)**

### **Try to Evade Detection:**
```python
# Human-like bot
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Don't fill hidden field
data = {
    "username": "admin",
    "password": "human123",
    # "website": ""  # Leave empty
}

# Slow submission
time.sleep(3)  # Wait 3 seconds
```

### **Expected Result:**
- Should NOT be detected as bot
- Might be classified as "Username Enumeration" or "Brute Force"

---

## **🏆 Success Criteria**

✅ **Bot Detection Works**: 
- Python requests bot detected
- Curl bot detected  
- Selenium bot detected

✅ **Dashboard Updates**:
- Shows "Bot Attack" entries
- Correct threat scores
- Proper classification

✅ **Response Consistent**:
- All bots get "Invalid credentials"
- No information leakage
- Professional handling

---

## **🎓 Learning Points**

### **Cybersecurity Concepts:**
- **Bot Detection**: User-agent analysis
- **Honeypot Fields**: Decoy techniques
- **Behavioral Analysis**: Timing patterns
- **Rate Limiting**: Frequency control

### **Technical Skills:**
- **HTTP Requests**: Python requests library
- **Header Manipulation**: User-agent spoofing
- **Form Analysis**: Hidden field detection
- **Security Testing**: Ethical hacking

---

**🚀 Your Cyber Defense System is ready for comprehensive bot attack testing!**

**Start with `simple_bot.py` and progress to `advanced_bot.py` for complete testing!**
