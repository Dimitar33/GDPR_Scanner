from playwright.sync_api import sync_playwright
from datetime import datetime
import lib.cookie_names as cn
import lib.consent_button_text as cbt
import lib.privacy_policy as pp
import lib.security_headers as sh

def scanning(url):
    with sync_playwright() as pwr:
        browser = pwr.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        response = page.goto(url, wait_until="load")
        page.wait_for_timeout(3000)

        headers = response.headers

        security_headers = {}

        for h in headers:
            for s in sh.SECURITY_HEADERS:
                if h.lower() == s:
                    security_headers[s] = sh.SECURITY_HEADERS[s]

        links = page.locator("a").all()
        
        privacy = ""

        for link in links:
            try:
                if any(x in link.inner_text().lower() for x in pp.PRIVACY_POLICY):
                    privacy = link.inner_text()
            except:
                pass

        cookie = context.cookies()

        cookies_b_c = {}
        cookies_a_c = {}

        print("\nCookies before consent:\n")
        for c in cookie:
            for n in cn.COOKIE_NAMES:
                if c["name"].startswith(n):
                    print(c["name"], c["expires"], c["domain"], cn.COOKIE_NAMES[n])
                    expires = datetime.fromtimestamp(c["expires"]) - datetime.now()

                    cookies_b_c[cn.COOKIE_NAMES[n]] = expires.days
            print(c["name"], c["expires"], c["domain"])

        buttons = page.locator("button").all()
        try:
            for b in buttons:
                if any(word in b.inner_text().lower() for word in cbt.CONSENT_BUTTON_TEXT):
                    b.click()
                    page.wait_for_timeout(2000)
        except:
            print("button not found")

        cookie = context.cookies()
        print("\nCookies after consent:\n")
        for c in cookie:
            for n in cn.COOKIE_NAMES:
                if c["name"].startswith(n):
                    print(c["name"], c["expires"], c["domain"], cn.COOKIE_NAMES[n])
                    expires = datetime.fromtimestamp(c["expires"]) - datetime.now()
                    cookies_a_c[cn.COOKIE_NAMES[n]] = expires.days
                    
        browser.close()

        return (cookies_b_c, cookies_a_c, privacy, security_headers)



