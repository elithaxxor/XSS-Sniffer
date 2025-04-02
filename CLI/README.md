```bash

# Check for XSS vulnerabilities
python script.py xss -u https://example.com

# Bypass IP blocking
python script.py ipbypass -u https://example.com -l login.php -w passwords.txt

# Brute-force stay-logged-in cookie
python script.py cookie -u https://example.com -c stay_logged_in -n admin -w rockyou.txt

# Enumerate valid usernames
python script.py enum -u https://example.com -l login.php -w usernames.txt
```
