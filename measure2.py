import json, time
from playwright.sync_api import sync_playwright

URL = "https://kristall2002-art.github.io/notary-tarakanovsky/"
IDS = ["home", "services", "about", "how", "reviews", "faq", "contacts"]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    for sid in IDS:
        page.evaluate(f"window.NB.goId('{sid}')")
        time.sleep(2.5)
        metrics = page.evaluate(f"""
        () => {{
            const sec = document.querySelector('#{sid} .sec-scroll');
            const wrap = sec ? sec.querySelector('.wrap') : null;
            if (!sec || !wrap) return null;
            return {{
                scScrollH: sec.scrollHeight,
                scClientH: sec.clientHeight,
                scScrollW: sec.scrollWidth,
                scClientW: sec.clientWidth,
                wrapZoom: getComputedStyle(wrap).zoom,
            }};
        }}
        """)
        results[sid] = metrics
        print(sid, metrics)
    browser.close()

with open("_shots_dark/metrics2.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
