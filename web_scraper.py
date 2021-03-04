"""
Adapted from: https://realpython.com/async-io-python/
"""

import re
import time
from urllib.parse import urljoin
from urllib.request import urlopen

import aiofiles
import aiohttp
from aiohttp import ClientSession

HREF_RE = re.compile(r'href="(.*?)"')

def fetch_html(url):
    """ GET request wrapper to fetch page HTML """
    response = urlopen(url)
    html = str(response.read())
    return html

def parse_url(url):
    """ Find HREFs in the HTML of the given url """
    html = fetch_html(url)
    linked_urls = {urljoin(url, link) for link in HREF_RE.findall(html)}
    return linked_urls

def process_url(file_path, url):
    """ Write to file all the linked urls at the given url """
    linked_urls = parse_url(url)
    if not linked_urls:
        return

    with open(file_path, "a") as file:
        for linked_url in linked_urls:
            file.write(f"{url}\t{linked_url}\n")

def bulk_process_urls(file_path, urls):
    """ Process all urls """
    for url in urls:
        process_url(file_path, url)

if __name__ == "__main__":
    with open("urls.txt") as file:
        urls = set(line.strip() for line in file)

    outpath = "linked_urls.txt"
    with open(outpath, "w") as file:
        file.write("source_url\tlinked_url\n")

    start = time.time()

    bulk_process_urls(file_path=outpath, urls=urls)

    end = time.time()
    print(f"Completed in {end - start:.02f} seconds")
