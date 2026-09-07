import json, time
from playwright.sync_api import sync_playwright

URL = "https://kristall2002-art.github.io/notary-tarakanovsky/"
IDS = ["home", "services", "about", "how", "reviews", "faq", "contacts"]
OUT = "_shots_dark"

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()

    for label, vw, vh in [("desktop", 1440, 900), ("mobile", 390, 844)]:
        page = browser.new_page(viewport={"width": vw, "height": vh})
        page.goto(URL, wait_until="networkidle")
        time.sleep(1.5)
        for sid in IDS:
            page.evaluate(f"window.NB.goId('{sid}')")
            time.sleep(2.5)
            fname = f"{OUT}/{label}_{sid}.png"
            page.screenshot(path=fname)
            # measure sec-scroll
            metrics = page.evaluate(f"""
            () => {{
                const sec = document.querySelector('#{sid} .sec-scroll');
                if (!sec) return null;
                const cs = getComputedStyle(sec.parentElement); // .sec
                const zoom = getComputedStyle(sec).zoom || null;
                return {{
                    scrollHeight: sec.scrollHeight,
                    clientHeight: sec.clientHeight,
                    scrollWidth: sec.scrollWidth,
                    clientWidth: sec.clientWidth,
                    zoom: zoom,
                    secZoom: getComputedStyle(sec.parentElement).zoom
                }};
            }}
            """)
            results[f"{label}_{sid}"] = metrics
            print(label, sid, metrics)
        page.close()

    browser.close()

with open(f"{OUT}/metrics.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("DONE")
