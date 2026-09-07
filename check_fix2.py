import json, time
from playwright.sync_api import sync_playwright

URL = "https://kristall2002-art.github.io/notary-tarakanovsky/"
OUT = "_shots_fix2"

# (label, vw, vh, [section ids])
PLAN = [
    ("mobile", 390, 844, ["contacts", "about", "faq"]),
    ("desktop", 1440, 900, ["contacts", "about"]),
]

results = {}

def measure(page, sid):
    return page.evaluate(f"""
    () => {{
        const sec = document.querySelector('#{sid} .sec-scroll');
        if (!sec) return null;
        return {{
            scScrollH: sec.scrollHeight,
            scClientH: sec.clientHeight,
            scDiffH: sec.scrollHeight - sec.clientHeight,
            scScrollW: sec.scrollWidth,
            scClientW: sec.clientWidth,
            scDiffW: sec.scrollWidth - sec.clientWidth,
            docScrollW: document.documentElement.scrollWidth,
            docClientW: document.documentElement.clientWidth,
            docDiffW: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        }};
    }}
    """)

with sync_playwright() as p:
    browser = p.chromium.launch()

    for label, vw, vh, ids in PLAN:
        page = browser.new_page(viewport={"width": vw, "height": vh})
        page.goto(URL, wait_until="networkidle")
        time.sleep(1.5)
        for sid in ids:
            page.evaluate(f"window.NB.goId('{sid}')")
            time.sleep(2.5)
            fname = f"{OUT}/{label}_{sid}.png"
            page.screenshot(path=fname)
            m = measure(page, sid)
            results[f"{label}_{sid}"] = m
            print(label, sid, m)

            # extra: for mobile contacts, also shoot just the footer area
            if label == "mobile" and sid == "contacts":
                footer = page.query_selector(f"#{sid} .sec-scroll")
                if footer:
                    # scroll the sec-scroll container to bottom to capture footer
                    page.evaluate(f"""
                    () => {{
                        const sec = document.querySelector('#{sid} .sec-scroll');
                        if (sec) sec.scrollTop = sec.scrollHeight;
                    }}
                    """)
                    time.sleep(0.5)
                    page.screenshot(path=f"{OUT}/{label}_{sid}_footer.png")
                    # scroll back to top for cleanliness
                    page.evaluate(f"""
                    () => {{
                        const sec = document.querySelector('#{sid} .sec-scroll');
                        if (sec) sec.scrollTop = 0;
                    }}
                    """)
        page.close()

    browser.close()

with open(f"{OUT}/metrics.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("DONE")
