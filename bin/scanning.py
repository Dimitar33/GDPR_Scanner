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
        browser = pwr.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(4000)

        buttons = page.locator("button").all()
        try:
            for b in buttons:
                if b.inner_text().lower() == "accept all" or b.inner_text().lower() == "consent":
                    b.click()
                    print(b.inner_text())
        except:
            print("button not found")

        # try:
        #     page.wait_for_selector("text=Accept All", timeout=3000)
        #     page.click("text=Accept All", force=True)
        #     print("selector found")
        # except:
        #     print("selector not found")

        # for frame in page.frames:
        #     try:
        #         frame.click("text=Accept All", timeout=10000)
        #         break
        #     except:
        #         pass

        page.wait_for_timeout(3000)
        cookie = context.cookies()

        # with open("page.html", "w", encoding="utf-8") as f:
        #  f.write(page.content())
        # page.screenshot(path="pwr.png")

        print("\nCookies after consent:\n")
        for c in cookie:
            for n in cn.COOKIE_NAMES:
                if c["name"].startswith(n):
                    print(c["name"], c["expires"], c["domain"], cn.COOKIE_NAMES[n])
                    expires = datetime.fromtimestamp(c["expires"]) - datetime.now()

                # bad_cookies[cn.COOKIE_NAMES[n]] = expires.days

        browser.close()
        # return cookie
