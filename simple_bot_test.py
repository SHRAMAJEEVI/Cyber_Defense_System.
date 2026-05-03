import requests

# Simple Bot Attack Test
url = "http://127.0.0.1:8000/honeypot-login/"

# Bot headers
headers = {
    'User-Agent': 'python-requests/2.28.1'
}

# Simple bot data
data = {
    "username": "admin",
    "password": "12345",
    "website": "bot-test"  # This should trigger honeypot detection
}

print("🤖 Testing Bot Attack...")
print(f"URL: {url}")
print(f"Headers: {headers}")
print(f"Data: {data}")

try:
    # Get the page first to get CSRF token
    session = requests.Session()
    page = session.get(url, headers=headers)
    print(f"✅ Got page with status: {page.status_code}")
    
    # Extract CSRF token (if needed)
    csrf_token = ""
    
    # Add CSRF to data
    if csrf_token:
        data['csrfmiddlewaretoken'] = csrf_token
    
    # Send bot attack
    response = session.post(url, data=data, headers=headers)
    
    print(f"📊 Status Code: {response.status_code}")
    print(f"📄 Response: {response.text[:200]}...")
    
    if response.status_code == 200:
        if "Invalid credentials" in response.text:
            print("🛡️  SUCCESS: Bot detected and blocked!")
        else:
            print("⚠️  Bot NOT detected")
    else:
        print(f"❓ Unexpected status: {response.status_code}")

except Exception as e:
    print(f"❌ Error: {e}")
