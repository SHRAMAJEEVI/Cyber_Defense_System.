# Cyber Defense System - Demo Test Instructions

## Overview
This document provides comprehensive test cases for the upgraded Cyber Defense System with user classification capabilities.

## System Features
- **Normal Users**: Redirected to https://artisan-market-place.onrender.com/
- **Suspicious Users**: Shown blocked page with warning
- **Attackers**: Shown blocked page with high threat alert

## Test Cases

### 1. Normal User Test
**Input:**
- Username: `manikant`
- Password: `12345`

**Expected Result:**
- Threat Score: 0
- User Type: Normal
- Action: Redirect to https://artisan-market-place.onrender.com/

**Steps:**
1. Go to `http://127.0.0.1:8000/honeypot-login/`
2. Enter username: `manikant`
3. Enter password: `12345`
4. Click "Sign In"
5. Verify redirect to artisan marketplace

---

### 2. Suspicious User Test - Common Admin Username
**Input:**
- Username: `admin`
- Password: `123`

**Expected Result:**
- Threat Score: 5
- User Type: Suspicious
- Action: Show blocked page

**Steps:**
1. Go to honeypot login page
2. Enter username: `admin`
3. Enter password: `123`
4. Click "Sign In"
5. Verify blocked page with "Suspicious User" badge
6. Check threat score shows 5
7. Verify reason: "Common admin username used"

---

### 3. Attacker Test - SQL Injection
**Input:**
- Username: `admin' OR 1=1 --`
- Password: `anything`

**Expected Result:**
- Threat Score: 15+ (10 for SQL injection + 5 for admin username)
- User Type: Attacker
- Action: Show blocked page

**Steps:**
1. Go to honeypot login page
2. Enter username: `admin' OR 1=1 --`
3. Enter any password
4. Click "Sign In"
5. Verify blocked page with "Attacker" badge
6. Check threat score is 15 or higher
7. Verify SQL injection detection reason

---

### 4. Bot Detection Test - Hidden Field
**Input:**
- Fill hidden field programmatically

**Expected Result:**
- Threat Score: 10
- User Type: Suspicious (or Attacker if combined with other factors)
- Action: Show blocked page

**Steps:**
1. Open browser developer tools
2. Find hidden input field named `website`
3. Set its value to something (e.g., "test")
4. Submit form normally
5. Verify blocked page
6. Check reason: "Hidden honeypot field filled (bot detected)"

---

### 5. Repeated Attempts Test
**Input:**
- Multiple attempts from same IP within 1 minute

**Expected Result:**
- 3 attempts: +6 points (Suspicious)
- 5 attempts: +10 points (Attacker)

**Steps:**
1. Make 3 rapid attempts with any username/password
2. On 3rd attempt, verify +6 points added
3. Make 2 more attempts (total 5)
4. On 5th attempt, verify +10 points added
5. Check reason: "High frequency attempts from same IP"

---

### 6. Dangerous Symbols Test
**Input:**
- Username: `test'user`
- Password: `password`

**Expected Result:**
- Threat Score: 8
- User Type: Suspicious
- Action: Show blocked page

**Steps:**
1. Enter username with dangerous symbols: `test'user`
2. Enter any password
3. Submit form
4. Verify blocked page
5. Check reason: "Dangerous symbols in username: '"

---

### 7. Typing Speed Test
**Input:**
- Submit form in less than 2 seconds

**Expected Result:**
- Threat Score: +5
- User Type: Suspicious (if combined with other factors)

**Steps:**
1. Fill form quickly and submit within 2 seconds
2. Verify blocked page (if combined with other suspicious factors)
3. Check reason: "Form submitted too quickly (bot-like behavior)"

---

## Dashboard Verification

### 1. Classification Statistics
After running tests, verify dashboard shows:
- **Normal Users**: Count of normal attempts
- **Suspicious Users**: Count of suspicious attempts  
- **Attackers**: Count of attacker attempts

### 2. Classification Table
Verify table shows:
- Username
- IP Address
- Threat Score (color-coded)
- User Type (with appropriate badge)
- Timestamp
- Attack Reason

### 3. Color Coding
- **Green**: Normal users (threat score < 8)
- **Yellow**: Suspicious users (threat score 8-14)
- **Red**: Attackers (threat score >= 15)

## Additional Test Cases

### SQL Injection Variations:
- `' UNION SELECT * FROM users --`
- `'; DROP TABLE users; --`
- `<script>alert('xss')</script>`

### Admin Username Variations:
- `root`
- `administrator`
- `guest`

### Combined Threat Scenarios:
1. Admin username + SQL injection = 15 points (Attacker)
2. Admin username + hidden field = 15 points (Attacker)
3. SQL injection + rapid attempts = 16 points (Attacker)

## Troubleshooting

### Common Issues:
1. **Redirect not working**: Check if threat score calculation is correct
2. **Dashboard not updating**: Run migrations and restart server
3. **Hidden field visible**: Check CSS styling in honeypot_login.html
4. **Threat score incorrect**: Verify scoring logic in views.py

### Database Reset:
If needed, reset database:
```bash
python manage.py migrate honeypot zero
python manage.py migrate
```

### Server Restart:
After code changes, restart server:
```bash
python manage.py runserver
```

## Success Criteria
✅ All test cases produce expected results
✅ Dashboard shows accurate classification statistics
✅ Normal users are redirected correctly
✅ Suspicious users see warning page
✅ Attackers see blocked page
✅ Threat scoring works as specified
✅ All reasons are logged correctly

## Presentation Tips
1. Start with normal user test to show redirect
2. Show SQL injection test for dramatic effect
3. Demonstrate bot detection
4. Show dashboard with classification breakdown
5. Explain threat scoring algorithm
6. Display real-time classification table
