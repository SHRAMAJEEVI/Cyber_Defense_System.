import requests
import time

# Cyber Defense System Bot Attack Test
# This will test if your system correctly detects bot attacks

def test_bot_attack():
    # Correct URL for honeypot login
    url = "http://127.0.0.1:8000/honeypot-login/"
    
    # Bot headers to trigger detection
    headers = {
        'User-Agent': 'python-requests/2.28.1',  # This should trigger "Bot Attack"
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    # Attack data
    data = {
        "username": "admin",
        "password": "12345",
        "csrfmiddlewaretoken": "",  # Will be handled by Django
        "website": "bot-test",  # Hidden honeypot field
        "form_submit_time": "0.5"  # Fast submission (bot-like)
    }
    
    print("🤖 BOT ATTACK TEST")
    print("=" * 50)
    print(f"Target URL: {url}")
    print(f"User-Agent: {headers['User-Agent']}")
    print(f"Attack Data: {data}")
    print("=" * 50)
    
    try:
        # Send bot attack
        response = requests.post(url, data=data, headers=headers, allow_redirects=False)
        
        print(f"✅ Bot attack sent successfully!")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        # Check if bot was detected
        if response.status_code == 200:
            print("🛡️  Bot detected - showing 'Invalid credentials' message")
        elif response.status_code == 302:
            print("⚠️  Bot NOT detected - got redirect (unexpected!)")
        else:
            print(f"❓ Unexpected response code: {response.status_code}")
            
        print(f"📝 Response Content: {response.text[:200]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def test_sql_injection():
    """Test SQL injection detection"""
    url = "http://127.0.0.1:8000/honeypot-login/"
    
    headers = {
        'User-Agent': 'curl/7.68.0',  # Bot user-agent
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    # SQL injection payload
    data = {
        "username": "admin' OR 1=1 --",
        "password": "anything",
        "csrfmiddlewaretoken": "",
        "website": "",  # Don't fill honeypot for this test
        "form_submit_time": "1.5",
    }
    
    print("\n💉 SQL INJECTION TEST")
    print("=" * 50)
    print(f"Payload: {data['username']}")
    
    try:
        response = requests.post(url, data=data, headers=headers)
        print(f"✅ SQL injection sent!")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("🛡️  SQL injection detected - blocked!")
        else:
            print(f"❓ Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def test_xss_attack():
    """Test XSS detection"""
    url = "http://127.0.0.1:8000/honeypot-login/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    # XSS payload
    data = {
        "username": "<script>alert('XSS')</script>",
        "password": "anything",
        "csrfmiddlewaretoken": "",
        "website": "",
        "form_submit_time": "2.0",
    }
    
    print("\n🔥 XSS ATTACK TEST")
    print("=" * 50)
    print(f"Payload: {data['username']}")
    
    try:
        response = requests.post(url, data=data, headers=headers)
        print(f"✅ XSS attack sent!")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("🛡️  XSS detected - blocked!")
        else:
            print(f"❓ Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 CYBER DEFENSE SYSTEM - ATTACK TESTING")
    print("Testing your honeypot security features...")
    print()
    
    # Test 1: Bot Attack
    test_bot_attack()
    time.sleep(2)
    
    # Test 2: SQL Injection
    test_sql_injection()
    time.sleep(2)
    
    # Test 3: XSS Attack
    test_xss_attack()
    
    print("\n" + "=" * 50)
    print("🏆 ALL ATTACKS COMPLETED!")
    print("📊 Check your dashboard: http://127.0.0.1:8000/dashboard/")
    print("📋 Check logs: http://127.0.0.1:8000/logs/")
    print("=" * 50)
