GET_NAME = """//h1[contains(@class, "biz-page-title")]"""
GET_ADDRESS_XPATH = """//div[@class="mapbox-text"]//address/text()"""
GET_WEBSITE_XPATH = """//div[@class="mapbox-text"]//span[contains(@class, "biz-website")]/a/text()"""
GET_PHONE_XPATH = """//div[@class="mapbox-text"]//span[contains(@class, "biz-phone")]/text()"""
GET_REVIEW_HIGHLIGHT = """//div[@class="review-highlights-content"]//p[text()]"""
GET_STAR_RATING = """//div[contains(@class, "rating-info")]//div[contains(@class, "i-stars")]//@title"""
GET_REVIEW_COUNT = """//div[contains(@class, "rating-info")]//span[contains(@class, "review-count")]/text()"""
GET_KEY_WORDS = """//div[contains(@class, "biz-page-header")]//div[@class="price-category"]//span[@class="category-str-list"]//a/text()"""
GET_HOURS = """//div[contains(@class, "biz-hours")]//table//tr/td[not(contains(@class, 'extra'))]"""
GET_LOC = """//div[@class="mapbox"]//img/@src"""
GET_IMG = """(//div[contains(@class, "showcase-photo-box")]//img/@src)[2]"""

SCRAPER = [
    ["name", GET_NAME, True],
    ["address", GET_ADDRESS_XPATH, False],
    ["website", GET_WEBSITE_XPATH, True],
    ["phone", GET_PHONE_XPATH, True],
    ["reviews", GET_REVIEW_HIGHLIGHT, False],
    ["rating", GET_STAR_RATING, True],
    ["count", GET_REVIEW_COUNT, True],
    ["keywords", GET_KEY_WORDS, False],
    ["hours", GET_HOURS, False],
    ["location", GET_LOC, True],
    ["image", GET_IMG, True],
]

import requests
import sys
import os
import time
from lxml import html
import re
from pprint import pprint
import json
import hashlib
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'key'))
import ENV

def get_headers(user_agent):
    headers = {
        "User-Agent": user_agent
    }
    return headers

def scrape(url, identifier, user_agent, proxies=""):
    print(">>> scraping: " + url)
    print(">>> user_agent: " + str(user_agent))
    print(">>> proxies: " + str(proxies))
    info = {}

    try:
        session_request = requests.session()
        proxies = {"http": proxies}
        response = session_request.get(url, proxies=proxies, headers=get_headers(user_agent))

        tree = html.fromstring(response.content)

        for name, xpathstr, isFlatten in SCRAPER:
            vals = tree.xpath(xpathstr)
            if vals:
                # print(name)    
                # print(xpathstr)
                # print(len(vals))
                if not isinstance(vals[0], str):
                    vals = list(map(lambda x:x.text_content(), vals))

                vals = list(map(string_process, vals))
                if isFlatten:
                    vals = vals[0]
                
                if name == "location":
                    match = re.match(r'.*center=(\S+?)%2C(\S+?)&.*', vals)
                    if not match:
                        match = re.match(r'.*%7C(\S+?)%2C(\S+?)&.*', vals)
                    vals = [match.group(1), match.group(2)]

                info[name] = vals

    except Exception as err:
        print("<<< ERROR: " + str(err))
        return {}

    if "name" not in info.keys():
        return {}

    hashcode = hashlib.md5(json.dumps(info, sort_keys=True).encode('utf-8')).hexdigest()
    info["hashcode"] = hashcode

    info["url"] = url
    info["identifier"] = identifier
    info["created_at"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    # pprint(info)
    return info

def string_process(string):
    string = re.sub(r'^\s*\\?n?\s*', r'', string)
    string = re.sub(r'\s*\\?n?\s*$', r'', string)
    return string
