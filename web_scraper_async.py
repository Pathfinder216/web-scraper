"""
Adapted from: https://realpython.com/async-io-python/
"""

import asyncio
import re
import time
from urllib.parse import urljoin

import aiofiles
import aiohttp
from aiohttp import ClientSession

HREF_RE = re.compile(r'href="(.*?)"')

async def fetch_html(url, session):
    """ GET request wrapper to fetch page HTML """
    response = await session.request(method="GET", url=url)
    html = await response.text()
    return html

async def parse_url(url, session):
    """ Find HREFs in the HTML of the given url """
    html = await fetch_html(url, session)
    linked_urls = {urljoin(url, link) for link in HREF_RE.findall(html)}
    return linked_urls

async def process_url(file_path, url, session):
    """ Write to file all the linked urls at the given url """
    linked_urls = await parse_url(url, session)
    if not linked_urls:
        return

    async with aiofiles.open(file_path, "a") as file:
        for linked_url in linked_urls:
            await file.write(f"{url}\t{linked_url}\n")

async def bulk_process_urls(file_path, urls):
    """ Process all urls concurrently """
    async with ClientSession() as session:
        coroutines = [process_url(file_path, url, session) for url in urls]
        await asyncio.gather(*coroutines)

if __name__ == "__main__":
    with open("urls.txt") as file:
        urls = set(line.strip() for line in file)

    outpath = "linked_urls.txt"
    with open(outpath, "w") as file:
        file.write("source_url\tlinked_url\n")

    start = time.time()

    # Using .get_event_loop().run_until_complete() instead of .run() because of weird bug
    asyncio.get_event_loop().run_until_complete(bulk_process_urls(file_path=outpath, urls=urls))

    end = time.time()
    print(f"Completed in {end - start:.02f} seconds")
