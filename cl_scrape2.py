import re

import bs4
import requests
import dateparser
import ftfy
from pprint import pprint

class CLScrape:

    def __init__(self, section):
        self.sites_url = "http://www.craigslist.org/about/sites"
        self.sections = {'computer gigs': 'search/cpg?query=%20&s=0&format=rss'}
        self.url_suffix = self.sections[section]
        self.re_link = re.compile(r'(?<=<link/>).+(?=\s)')
        self.re_date = re.compile(r'(?<=<dc:date>).+(?=\</dc:date>)')
        self.re_CDATA = re.compile(r'(?<=CDATA\[).+(?=\]\]|\s)')

    def get_sites(self, country_param=None):
        response = requests.get(self.sites_url)
        soup = bs4.BeautifulSoup(response.text)
        countries = soup.find_all('h1')
        for country in countries:
            country_name = tuple(e for e in country)[0]['name']
            if country_param is not None and country_name != country_param: continue
            country_html = str(country.next_sibling.next_sibling)
            for state in country.next_sibling.next_sibling.find_all('h4'):
                state_soup = bs4.BeautifulSoup(country_html[country_html.find(str(state)):])
                for city in state_soup.ul.find_all("a"):
                    for piece in city:
                        yield {'country': country_name,
                                'state': state.contents[0],
                                'city': str(piece),
                                'city_href': city['href']}

    def get_ads(self, site):
        url = 'http:{}{}'.format(site['city_href'], self.url_suffix)
        print(url)
        response = requests.get(url)
        return response.text

    def parse_ads(self, page):
        soup = bs4.BeautifulSoup(page, "html5lib")
        items = soup.find_all('item')
        for e in items:
            title = e.find('title').contents[0]
            m = self.re_CDATA.search(title)
            title = m.group(0)
            description = e.find('description').contents[0]
            m = self.re_CDATA.search(description)
            description = m.group(0)
            m = self.re_link.search(str(e))
            link = m.group(0)
            m = self.re_date.search(str(e))
            dt = dateparser.parse(m.group(0),
                    settings={'RETURN_AS_TIMEZONE_AWARE': True})
            yield {'title': title,
                    'description': description,
                    'link': link,
                    'dt': dt}


if __name__ == '__main__':
    scraper = CLScrape('computer gigs')
    pprint(scraper.sections)
    for site in scraper.get_sites('US'):
        if site['city'] != 'san francisco bay area': continue
        pprint(site)
        for e in scraper.parse_ads(scraper.get_ads(site)):
            pprint(e)
