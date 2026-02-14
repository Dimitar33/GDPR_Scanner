from playwright.sync_api import sync_playwright
import lib.cookie_names as cn

def cookie_before_concent(url):
    with sync_playwright() as pwr:
        browser = pwr.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url, wait_until="load")
        page.wait_for_timeout(5000)

        cookies = context.cookies()

        print("\nCookies before consent:\n")
        for c in cookies:
             for n in cn.COOKIE_NAMES:
                if c["name"].startswith(n):
                    print(c["name"], c["expires"], c["domain"])

        browser.close()
        #return cookie


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
        cookies = context.cookies()

        print("\nCookies before consent:\n")
        for c in cookies:
            print(c["name"], c["expires"], c["domain"])
        
        browser.close()
        #return cookie


