import time
from playwright.sync_api import sync_playwright

URL = "https://kristall2002-art.github.io/notary-tarakanovsky/"
OUT = "/home/sergei/redesign-engine/experiments/notary-tarakanovsky/_shots_bg2"
SECTIONS = ["services", "about", "reviews", "contacts", "faq"]
VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "mobile": {"width": 390, "height": 844},
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for vp_name, vp in VIEWPORTS.items():
        page = browser.new_page(viewport=vp)
        page.goto(URL, wait_until="networkidle")
        time.sleep(1.5)
        for sec in SECTIONS:
            page.evaluate(f"window.NB.goId('{sec}')")
            time.sleep(2.5)
            path = f"{OUT}/{sec}_{vp_name}.png"
            page.screenshot(path=path, full_page=True)
            print("saved", path)
        page.close()
    browser.close()
