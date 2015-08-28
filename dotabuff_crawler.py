from __future__ import print_function
from collections import OrderedDict
import sys
import time
import csv
import json
import requests
from scrapy.selector import Selector

def make_request(user_id):
    cookies = {
        '__qca': 'P0-861033469-1436725711611',
        '_tz': 'America%2FLos_Angeles',
        '_player_token': '2c7f8d6b537012bbae35e9cb73af3788587af1be771cf5f1f65b7b583048cb15',
        '__utmt': '1',
        '_s': 'TzJnNkVoZGk5MEcrVFZ1cEtHQmVWM0ZzQUxTUFRMNlRCVU9FL0xQcGdWT3p5RExRUSsyZDhOb3NRZ2hJM3M3bldqSXVpVXg5KzdkWW93SENPSGNOdExTbVlQdmRrMTR2Y2JnQW45V0d0cm5SUXVNSS9sOUlib2dpUDM3RjdTcnJ3a3N6VEs1enREWWkzVUFJbTVRN2ZzaHNWUXYwK2p2ZTVBNHA4bzhZcTBpdUhkbzY2NlR5OHRtODJQRllzNElXbldDVGtmZHdpa0tBcWRIWVdLSHM3ODRVQ0Q1STZ6U3M3ZURrS2NUMnhtQmErc1RaWlBJMkFZWFlpbjFhOU5mamhPaE5ZMnpQS05SdXBMQU1GMllNQ3F3VnFwYVBWbWcvZFVNN1ByQ1paemZ4Q09TQ2sxQk45UjZyOVE1d0hUbkgvSm5CUG9mMVNObmV1ejlObmtJTFRoeFZvOXduVTdnVUpRSE5NQkRVSERBWWljY2U3OFhIWFFOL01Mb2FUVjVrakFEeVNmamcrdWtlOXRrTTkzWGJpL1VtOFVISUZHVnNTVmh0TnBUZi9CMS80cWNlVjRlM1hHV0c3ZE1EaEFrWW4wdzlQdjFIa1JpWFUrRVJxZ2t1NFpmaWh0NXplaWJGMXdlZmdEZ2RZV2ZTTUVITTFmUitCK1NLVG14RVpTSFZJSWJ4QTgxdE5TTjdpSzg5YU41enFRPT0tLXlRQXlmK3MzS0ptWS9NRXJHeEdNQ2c9PQ%3D%3D--105dfcbf6fbeb8e73b23bdb510f75f316be9b183',
        '__utma': '242922391.1859529123.1436725712.1440695562.1440736562.8',
        '__utmb': '242922391.11.10.1440736562',
        '__utmc': '242922391',
        '__utmz': '242922391.1436725712.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'es,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.dotabuff.com/players/106697296',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }

    return requests.get("http://www.dotabuff.com/players/" + user_id + "/heroes", headers=headers, cookies=cookies)


def extract_from_row(html, xpath):
    content = Selector(text=html).xpath(xpath).extract()[0]
    return content.encode('ascii', 'ignore')

def get_hero_data(html):
    selector = Selector(text=html)
    rows = selector.xpath("//td").extract()
    return {
        'name': extract_from_row(rows[1], "//a/text()"),
        'matches_played': extract_from_row(rows[2], "//td/text()"),
        'win_rate': extract_from_row(rows[3], "//td/@data-value"),
        'kda': extract_from_row(rows[4], "//td/@data-value"),
    }


def get_heroes(user_id):
    selector = Selector(text = make_request(user_id).text)
    return [ get_hero_data(raw_hero) for raw_hero in
            selector.xpath("//tr[@data-link-to]").extract() ]

if __name__ == '__main__':
    ts = str(int(time.time()))
    for user_id in sys.stdin:
        user_id = user_id.strip()
        with open(user_id + "-" + ts + ".csv", 'w') as csvfile:
            heroes = get_heroes(user_id.strip())
            fieldnames = ['name', 'matches_played', 'win_rate', 'kda']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for hero in heroes:
                writer.writerow(hero)
