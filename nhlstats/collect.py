"""
Collect concerns itself with the screen scraping functionality.
"""

import os
import re
from hashlib import sha1
from lxml.html import parse
from urlparse import urljoin


class Collector(object):
    """
    Base scraper object implementing generic functionality.
    """
    def __init__(self, base_url, url_ends=[], cache_dir='cache'):
        self.base_url = base_url
        self.url_ends = url_ends
        self.cache_dir = cache_dir

    def check_season(self, season):
        """
        Useful for season based collectors, this checks the seasonis of
        the correct format.
        """
        if not re.match('[0-9]{8}', season):
            raise ValueError('Season "%s" is not of the correct format, which is two directly concatonated YYYY values, ie 20132014')

    def scrape(self):
        if not self.url_ends:
            # If we don't have any url_ends, add one dummy to
            # simplify the iteration logic
            self.url_ends.append(' ')

        results = []

        for end in self.url_ends:
            url = urljoin(self.base_url, end.strip())
            parsed = parse(url).getroot()

            # The parse functionality must be implemented by
            # our sub
            results.extend(self.parse(parsed))

        return results

    def url_to_filename(self, url):
        hash_file = sha1(url).hexdigest() + '.html'
        return os.path.join(self.cache_dir, hash_file)

    def parse(self, data):
        """
        This should be implemented by classes that inherit from us.
        data will be an lxml.etree.parse object.
        """
        return


class NHLSeason(Collector):
    """
    This sets up the scaoffold for an NHL season,
    scraping the conferences, divisions, teams.
    """
    def __init__(self, season, base_url='http://www.nhl.com/ice/standings.htm?season=%s&type=DIV'):
        self.check_season(season)
        super(NHLSeason, self).__init__(base_url % season)

    def parse(self, data):
        conferenceText = 'conferenceHeader'
        i = 0
        
        # Pick up normal teams
        teams = [item.text for item in data.xpath('//td[@style="text-align:left;"]/a[2]')]
        
        # Pick up teams that don't exist anymore (they're not links to team pages)
        teams.extend([item.text for item in data.xpath('//span[@class="team"]')])

        results = []

        for team in teams:
            i += 1
            division = data.xpath('//*[text()="%s"]/parent::td/parent::tr/parent::tbody/preceding-sibling::thead/tr[1]/th[@abbr="DIV"]' % team)[0].text
            conference = [item.get('class').replace(conferenceText, '') for item in data.xpath('//*[text()="%s"]/parent::td/parent::tr/parent::tbody/parent::table/preceding-sibling::div[starts-with(@class, "%s")]' % (team, conferenceText))][-1]
            results.append((team, conference, division))

        return results


class Teams(Collector):
    """
    Unfortunately because the NHL is happy to mix in Olympic
    games and the like with their schedule, we must populate
    the teams separately. We do so by looking at pre-season
    games, which presumably only contain NHL teams.
    """
    def __init__(self, base_url='http://www.nhl.com/ice/teams.htm'):
        super(Teams, self).__init__(base_url)

    def parse(self, data):
        teams = data.cssselect('div#teamMenu a')

        data = []

        # Start from index 1, as 0 is the NHL logo.
        for team in teams[1:]:
            name = team.attrib['title']
            url = team.attrib['href']

            data.append((name, url))

        return data


class Schedule(Collector):
    def __init__(self, season, base_url):
        self.check_season(season)


class Events(Collector):
    pass
