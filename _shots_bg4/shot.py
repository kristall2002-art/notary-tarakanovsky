import time
from playwright.sync_api import sync_playwright

URL = "https://kristall2002-art.github.io/notary-tarakanovsky/"
OUT = "/home/sergei/redesign-engine/experiments/notary-tarakanovsky/_shots_bg4"

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Desktop, light theme
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    for sec in ["services", "about", "how", "reviews", "faq", "contacts"]:
        page.evaluate(f"window.NB.goId('{sec}')")
        time.sleep(2.5)
        path = f"{OUT}/desktop_light_{sec}.png"
        page.screenshot(path=path, full_page=True)
        print("saved", path)
    page.close()

    # Mobile, light theme
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    for sec in ["services", "about", "faq"]:
        page.evaluate(f"window.NB.goId('{sec}')")
        time.sleep(2.5)
        path = f"{OUT}/mobile_light_{sec}.png"
        page.screenshot(path=path, full_page=True)
        print("saved", path)
    page.close()

    # Desktop, dark theme
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    page.evaluate("document.documentElement.setAttribute('data-theme','dark')")
    time.sleep(0.5)
    for sec in ["services", "about", "faq"]:
        page.evaluate(f"window.NB.goId('{sec}')")
        time.sleep(2.5)
        path = f"{OUT}/desktop_dark_{sec}.png"
        page.screenshot(path=path, full_page=True)
        print("saved", path)
    page.close()

    browser.close()
