import requests

# Quick Bot Test
url = "http://127.0.0.1:8000/honeypot-login/"

headers = {
    'User-Agent': 'python-requests/2.28.1'
}

data = {
    "username": "admin",
    "password": "12345",
    "website": "bot-test"
}

print("🤖 Testing Bot Attack Against Cyber Defense System...")
print(f"Target: {url}")
print(f"Headers: {headers}")
print(f"Data: {data}")

try:
    response = requests.post(url, data=data, headers=headers)
    print(f"\n📊 Status Code: {response.status_code}")
    print(f"📄 Response Length: {len(response.text)} characters")
    
    if "Invalid credentials" in response.text:
        print("🛡️  SUCCESS: Bot detected and blocked!")
        print("📊 Check dashboard: http://127.0.0.1:8000/dashboard/")
    else:
        print("⚠️  Unexpected response")
        print(f"Response: {response.text[:200]}")

except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Make sure server is running: python manage.py runserver")
