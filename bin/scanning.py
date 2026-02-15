from playwright.sync_api import sync_playwright
import lib.cookie_names as cn
from datetime import datetime

def cookie_before_concent(url):
    with sync_playwright() as pwr:
        browser = pwr.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url, wait_until="load")
        page.wait_for_timeout(5000)

        cookie = context.cookies()

        bad_cookies = {}

        print("\nCookies before consent:\n")
        for c in cookie:
             for n in cn.COOKIE_NAMES:
                if c["name"].startswith(n):
                    print(c["name"], c["expires"], c["domain"], cn.COOKIE_NAMES[n])
                    expires = datetime.fromtimestamp(c["expires"]) - datetime.now()

                    bad_cookies[cn.COOKIE_NAMES[n]] = expires.days

        browser.close()
        return bad_cookies


def cookie_after_concent(url):

    with sync_playwright() as pwr:
        browser = pwr.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url)

        try:
            page.click("text=Accept")
        except:
            pass

        page.wait_for_timeout(3000)
        cookie = context.cookies()

        print("\nCookies before consent:\n")
        for c in cookie:
            print(c["name"], c["expires"], c["domain"])
        
        browser.close()
        #return cookie


