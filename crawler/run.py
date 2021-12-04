from tqdm import tqdm
import json
import datetime
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def get_code(field):
    _html = await field.inner_html()
    if "div" in _html:
        x = await field.query_selector("div")
        codes = await x.get_attribute("class")
        return list(set(codes.split(" ")) - {"sym"})


async def download():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.hvz.baden-wuerttemberg.de/overview.html")

        crawling_time = await page.query_selector("#ID-ZP")
        dt = await crawling_time.inner_html()
        dt_tz = dt.split(" ")[-1]
        # remove timezone from datetime
        _dt = " ".join(dt.split()[:-1])
        dt = datetime.datetime.strptime(_dt, "%d.%m.%Y %H:%M")

        path = Path(f"data/{dt.year}/{dt.month:02}/{dt.day:02}")
        path.mkdir(exist_ok=True, parents=True)
        fn = dt.isoformat() + "_" + dt_tz  # readd timezone
        fn = path / (fn + ".jsonl")

        result = await page.query_selector("#ID-TABLE")
        with fn.open("w") as fp:
            lines = await result.query_selector_all("tr")
            for item in tqdm(lines):

                _html = await item.inner_html()
                if _html.startswith("<th"):
                    # is header
                    continue

                columns = await item.query_selector_all("td")
                col3 = await columns[3].inner_html()
                if "--" in col3:
                    # no (valid) value
                    continue
                if "img" in col3:
                    # mainenance mode
                    continue

                data = {
                    "name": await columns[2].inner_text(),
                    "value": await columns[3].inner_text(),
                    "diff": await columns[4].inner_text(),
                    "warning_value": await columns[5].inner_text(),
                    "warning_code": await get_code(columns[5]),
                    "last_update": await columns[6].inner_text(),
                    "reference_code": await get_code(columns[7]),
                    "highest_navigable_waterlevel": await columns[8].inner_text(),
                    "navigable_code": await get_code(columns[8]),
                }
                fp.write(json.dumps(data, ensure_ascii=False) + "\n")

        await browser.close()


asyncio.run(download())
