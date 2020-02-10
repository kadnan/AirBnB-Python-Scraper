import json
import re

import requests
from bs4 import BeautifulSoup


def get_bed(h):
    _bedroom = '-'
    regex = r"(\d+) bedroom"

    matches = re.finditer(regex, h, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            _bedroom = match.group(groupNum)
            break
    return _bedroom


def get_guests(h):
    regex = r"(\d+) guests"
    _guests = '-'

    matches = re.finditer(regex, h, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            _guests = match.group(groupNum)
            break
    return _guests


def get_price(h):
    regex = r"\$\d+"
    _price = '-'

    matches = re.finditer(regex, h, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        _price = match.group()
        break

    return _price


if __name__ == '__main__':
    price = '-'
    bedroom = '-'
    guests = '-'
    url = '-'
    title = '-'
    records = []

    with open('API_KEY.txt', encoding='utf8') as f:
        API_KEY = f.read()

    URL_TO_SCRAPE = 'https://www.airbnb.com/s/Karachi--Sindh--Pakistan/homes?query=Karachi%2C%20Sindh%2C%20Pakistan'

    payload = {'api_key': API_KEY, 'url': URL_TO_SCRAPE, 'render': 'false'}

    r = requests.get('http://api.scraperapi.com', params=payload, timeout=60)

    if r.status_code == 200:
        html = r.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        listing_section = soup.select('._fhph4u ._8ssblpx')

        for item in listing_section:
            link_section = item.select('a')
            if link_section:
                url = link_section[0]['href']
                title = link_section[0]['aria-label']

            # Extracting HTML per item
            html_ = item.prettify()
            price = get_price(html_)
            guests = get_guests(html_)
            bedroom = get_bed(html_)
            records.append({'title': title, 'url': url, 'guests': guests, 'bedroom': bedroom})

    if len(records) > 0:
        with open('airbnb.json', 'a+', encoding='utf8') as f:
            f.write(json.dumps(records))

    print('Done')
