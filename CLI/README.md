```bash

# Check for XSS vulnerabilities
python main.py xss -u https://example.com

# Bypass IP blocking
python main.py ipbypass -u https://example.com -l login.php -w passwords.txt

# Brute-force stay-logged-in cookie
python main.py cookie -u https://example.com -c stay_logged_in -n admin -w rockyou.txt

# Enumerate valid usernames
python main.py enum -u https://example.com -l login.php -w usernames.txt
```

```markdown
# Web Security Testing Toolkit

A modular Python script implementing various web security testing techniques described in security research notes. Designed for educational purposes and authorized penetration testing.

## Features

### Original Functions
1. **XSS Vulnerability Checker**  
   - Checks for missing HttpOnly/Secure flags in cookies
   - Suggests basic XSS payload if vulnerable

2. **IP Block Bypass**  
   - Rotates X-Forwarded-For headers
   - Implements sequential delay between attempts
   - Handles connection closure properly

3. **Stay-Logged-In Cookie Brute-forcer**  
   - Automates cookie value generation
   - Supports MD5 + Base64 encoding scheme
   - Handles session cookie removal

4. **Username Enumeration**  
   - Uses timing analysis detection
   - Compares response time differentials
   - Identifies potential valid usernames

### New Additional Functions
5. **Session Cookie Swapping**  
   - Tests session fixation vulnerabilities
   - Validates cookie scope restrictions

6. **Automated XSS Payload Testing**  
   - Tests reflection points with common payloads
   - Verifies external server callbacks

7. **Credential Stuffing**  
   - Implements list-stuffing bypass technique
   - Rotates valid accounts during attacks

8. **Response Analysis Engine**  
   - Detects subtle differences in error messages
   - Identifies enumeration opportunities

9. **Lockout Testing**  
   - Determines login attempt thresholds
   - Maps IP blocking behavior patterns

## Why These Functions?

### Core Rationale
1. **XSS Focus**  
   Chosen because missing HttpOnly/Secure flags enable client-side attacks. The original research emphasized cookie theft via XSS as critical attack vector.

2. **Header Manipulation**  
   Directly addresses the "Weak Walking" concept from notes. X-Forwarded-For rotation helps bypass basic IP-based rate limiting observed in testing.

3. **Cookie Brute-forcing**  
   Implements the documented stay-logged-in cookie pattern (Base64(username:md5(pass))). This matches real-world implementations seen in several CMS platforms.

4. **Timing Analysis**  
   Addresses username enumeration via server response timing differences - a common flaw in authentication implementations.

### New Function Rationale
5. **Session Swapping**  
   Extends cookie testing capabilities to identify session management flaws beyond just stay-logged-in cookies.

6. **XSS Automation**  
   Expands basic XSS detection to active verification, addressing the original research's XSS->cookie theft chain.

7. **Credential Stuffing**  
   Implements the "List Stuffing" bypass technique described in IP-block solutions section.

8. **Response Analysis**  
   Helps identify subtle information leaks crucial for pre-brute-force reconnaissance.

9. **Lockout Testing**  
   Directly supports IP block analysis methodology outlined in original notes.

## Usage

```bash
# New Session Testing
python script.py session -u https://example.com -c PHPSESSID

# XSS Payload Testing
python script.py xss-test -u https://example.com/comment -d "message=TEST"

# Credential Stuffing 
python script.py stuff -u https://example.com/login -v valid_accounts.txt -w passwords.txt

# Lockout Analysis
python script.py lockout -u https://example.com/login -u correct_user -p correct_pass

```


