#!/usr/bin/env python3
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://kristall2002-art.github.io/notary-tarakanovsky/"
OUT = Path("/home/sergei/redesign-engine/experiments/notary-tarakanovsky/_shots_fix")
OUT.mkdir(exist_ok=True)

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--no-sandbox"])

        # Desktop 1440x900, light theme, "how" section
        ctx = await b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1, locale="ru-RU")
        page = await ctx.new_page()
        await page.goto(URL)
        await page.wait_for_timeout(2500)
        await page.evaluate("NB.goId('how')")
        await page.wait_for_timeout(2500)
        await page.screenshot(path=OUT / "desk_how_full.png")
        steps = page.locator(".steps")
        await steps.screenshot(path=OUT / "desk_how_steps.png")
        await ctx.close()

        # Mobile 390x844, light theme, "services" section
        ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True, locale="ru-RU")
        page = await ctx.new_page()
        await page.goto(URL)
        await page.wait_for_timeout(2500)
        await page.evaluate("NB.goId('services')")
        await page.wait_for_timeout(2500)
        await page.screenshot(path=OUT / "mob_services_full.png")
        card = page.locator(".svc").first
        await card.screenshot(path=OUT / "mob_services_card.png")
        await ctx.close()

        await b.close()

asyncio.run(run())
