# Cyber Defense System - Attack Type Testing Guide

## 🎯 Dynamic Attack Type Detection

The system now correctly classifies attacks using **priority-based detection** instead of hardcoded "Brute Force".

## 🔍 Priority Order

1. **SQL Injection** (Priority 1)
2. **XSS Attempt** (Priority 2) 
3. **Honeypot Trigger** (Priority 3)
4. **Bot Attack** (Priority 4)
5. **Brute Force** (Priority 5)
6. **Username Enumeration** (Priority 6)

---

## 🧪 Test Cases for Each Attack Type

### 1. SQL Injection Detection
**Expected Attack Type:** `SQL Injection`
**Threat Score:** 15+

**Test Inputs:**
- Username: `admin' OR 1=1 --`
- Username: `' UNION SELECT * FROM users --`
- Username: `'; DROP TABLE users; --`
- Password: `admin' OR 1=1 --`
- Password: `' OR '1'='1`

**Detection Patterns:**
- `'` (single quote)
- `;` (semicolon)
- `--` (SQL comment)
- `or 1=1`
- `union select`
- `drop table`
- `insert into`
- `delete from`
- `update set`
- `exec xp_`

---

### 2. XSS Attempt Detection
**Expected Attack Type:** `XSS Attempt`
**Threat Score:** 12+

**Test Inputs:**
- Username: `<script>alert('XSS')</script>`
- Username: `javascript:alert(1)`
- Username: `<img src=x onerror=alert(1)>`
- Password: `<script>document.location='evil.com'</script>`
- Username: `<body onload=alert(1)>`

**Detection Patterns:**
- `<script>`
- `</script>`
- `javascript:`
- `onerror=`
- `onload=`
- `alert(`

---

### 3. Honeypot Trigger Detection
**Expected Attack Type:** `Honeypot Trigger`
**Threat Score:** 10+

**Test Method:**
1. Open browser developer tools
2. Find hidden input: `<input type="text" name="website" style="display:none;">`
3. Set value: `bot-test`
4. Submit form normally

**Detection Logic:**
- Hidden field `website` is filled
- Indicates bot/honeypot trigger

---

### 4. Bot Attack Detection
**Expected Attack Type:** `Bot Attack`
**Threat Score:** 8+

**Test Methods:**

**Using curl:**
```bash
curl -X POST -d "username=admin&password=pass" http://127.0.0.1:8000/honeypot-login/
```

**User-Agent Detection:**
The system detects these user-agents:
- `curl`
- `python`
- `requests`
- `selenium`
- `postman`
- `wget`
- `bot`
- `crawler`

---

### 5. Brute Force Detection
**Expected Attack Type:** `Brute Force`
**Threat Score:** Varies

**Test Method:**
1. Make 3+ rapid attempts from same IP within 1 minute
2. Use any username/password combinations
3. System will classify as "Brute Force"

**Detection Logic:**
- Same IP address
- 3+ attempts within 60 seconds

---

### 6. Username Enumeration Detection
**Expected Attack Type:** `Username Enumeration`
**Threat Score:** 5+

**Test Inputs:**
- Username: `admin`
- Username: `root`
- Username: `administrator`
- Username: `guest`

**Detection Logic:**
- Common admin usernames
- Only if no higher priority attack detected

---

## 🎭 Priority Testing Examples

### Example 1: SQL Injection + Admin Username
**Input:** `admin' OR 1=1 --`
**Result:** `SQL Injection` (Priority 1 overrides Username Enumeration)

### Example 2: XSS + Hidden Field
**Input:** `<script>alert(1)</script>` + hidden field filled
**Result:** `XSS Attempt` (Priority 2 overrides Honeypot Trigger)

### Example 3: Bot + Brute Force
**Input:** curl request with 5 attempts
**Result:** `Bot Attack` (Priority 4 overrides Brute Force)

---

## 📊 Dashboard Verification

After testing, verify dashboard shows:

### Attack Type Breakdown:
- ✅ SQL Injection attempts
- ✅ XSS Attempts
- ✅ Honeypot Triggers
- ✅ Bot Attacks
- ✅ Brute Force attempts
- ✅ Username Enumeration

### Classification Statistics:
- **Normal Users**: Redirected to artisan marketplace
- **Suspicious Users**: Generic "Invalid credentials"
- **Attackers**: Generic "Invalid credentials"

### Attack Type Table:
Shows correct attack types instead of all "Brute Force"

---

## 🔧 Troubleshooting

### If All Attacks Still Show "Brute Force":
1. Check server restart: `python manage.py runserver`
2. Clear browser cache
3. Verify database migrations applied
4. Check views.py logic is updated

### If Wrong Attack Type Detected:
1. Verify priority order in views.py
2. Check detection patterns
3. Test with clean form submission

### If Dashboard Not Updating:
1. Refresh dashboard page
2. Check attack logs for new entries
3. Verify database connection

---

## 🎯 Demo Script for Presentation

### 1. Show SQL Injection Detection:
```
Username: admin' OR 1=1 --
Password: anything
Expected: SQL Injection, Threat Score 15+
```

### 2. Show XSS Detection:
```
Username: <script>alert('XSS')</script>
Password: anything
Expected: XSS Attempt, Threat Score 12+
```

### 3. Show Honeypot Trigger:
```
Fill hidden field via dev tools
Expected: Honeypot Trigger, Threat Score 10+
```

### 4. Show Bot Detection:
```
Use curl or Postman
Expected: Bot Attack, Threat Score 8+
```

### 5. Show Brute Force:
```
Make 3+ rapid attempts
Expected: Brute Force, Threat Score varies
```

### 6. Show Normal User:
```
Username: manikant
Password: 12345
Expected: Redirect to artisan marketplace
```

---

## ✅ Success Criteria

- [ ] SQL Injection attacks show correct type
- [ ] XSS attempts show correct type
- [ ] Honeypot triggers show correct type
- [ ] Bot attacks show correct type
- [ ] Brute force attacks show correct type
- [ ] Username enumeration shows correct type
- [ ] Priority order works correctly
- [ ] Dashboard shows attack type breakdown
- [ ] Normal users still redirect correctly
- [ ] Attackers see generic "Invalid credentials"

**The system now provides accurate attack classification for professional threat intelligence!**
