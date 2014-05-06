"""
Collect concerns itself with the screen scraping functionality.
"""

import os
import re
import pytz
import urllib2
import datetime
from hashlib import sha1
from lxml.html import parse
from urlparse import urljoin


GAME_TYPES = ['PRE', 'REG', 'POST']


class UnexpectedPageContents(Exception):
    """
    Used for when the page is retrieved, but the contents are
    unexpected
    """
    pass


class Collector(object):
    """
    Base scraper object implementing generic functionality.
    """
    def __init__(self, base_url, url_ends=[], cache_dir='cache'):
        self.base_url = base_url
        self.url_ends = url_ends
        self.cache_dir = cache_dir

        # This quirky check is to deal with the empty url_end we add in
        # the scrape method.  But seriously, we don't support this
        # craziness just yet.
        if [item for item in self.url_ends if item.strip()]:
            raise NotImplementedError('We do not currently support this')

    def check_game_type(self, game_type):
        """
        Useful for collectors dealing with games, there are three game
        types, preseason, regular, and postseason. Verify our game_type
        is known.
        """
        if game_type not in GAME_TYPES:
            raise ValueError('Game type of %s is unknown' % game_type)

    def check_season(self, season):
        """
        Useful for season based collectors, this checks the seasonis of
        the correct format.
        """
        if not re.match('[0-9]{8}', season):
            raise ValueError('Season "%s" is not of the correct format, which is two directly concatonated YYYY values, ie 20132014')

    def convert_datetime_to_utc(self, date, tz=pytz.timezone('US/Eastern')):
        """
        Given a datetime object, convert it to utc from tz (defaults to US/Eastern)
        """
        return tz.localize(date).astimezone(pytz.timezone('UTC'))

    def scrape(self):
        if not self.url_ends:
            # If we don't have any url_ends, add one dummy to
            # simplify the iteration logic
            self.url_ends.append(' ')

        for end in self.url_ends:
            url = urljoin(self.base_url, end.strip())
            parsed = parse(self.load_from_cache(url)).getroot()

            # The parse functionality must be implemented by
            # our sub.  We currently aren't
            self.verify(parsed)
            return self.parse(parsed)

    def url_to_filename(self, url):
        hash_file = sha1(url).hexdigest() + '.html'
        return os.path.join(self.cache_dir, hash_file)

    def store_cache(self, url, content):
        """
        Cache a local copy of the file.
        """

        # If the cache directory does not exist, make one.
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir)

        local_path = self.url_to_filename(url)
        with open(local_path, 'wb') as fp:
            fp.write(content)

    def load_from_cache(self, url):
        """
        If we do not have a cached version,
        get one. Return pointer to that.
        """
        local_path = self.url_to_filename(url)
        if not os.path.exists(local_path):
            self.store_cache(url, urllib2.urlopen(url).read())

        return local_path

    def parse(self, data):
        """
        This should be implemented by classes that inherit from us.
        data will be an lxml.etree.parse object.
        """
        return

    def verify(self, data):
        """
        This optional method is for verifying the page contents are as
        expected. Raise UnexpectedPageContents if the contents of data
        are unexpected.
        """
        return


class NHLSeason(Collector):
    """
    This sets up the scaoffold for an NHL season,
    scraping the conferences, divisions, teams.
    """
    def __init__(self, season, base_url='http://www.nhl.com/ice/standings.htm?season=%s&type=DIV'):
        self.check_season(season)
        self.season = season

        super(NHLSeason, self).__init__(base_url % season)

    def parse(self, data):
        conferenceText = 'conferenceHeader'
        i = 0

        # Pick up normal teams
        teams = [item.text for item in data.xpath('//td[@style="text-align:left;"]/a[2]')]

        # Pick up teams that don't exist anymore (they're not links to team pages)
        teams.extend([item.text for item in data.xpath('//span[@class="team"]')])

        results = {}

        for team in teams:
            i += 1
            division = data.xpath('//*[text()="%s"]/parent::td/parent::tr/parent::tbody/preceding-sibling::thead/tr[1]/th[@abbr="DIV"]' % team)[0].text
            conference = [item.get('class').replace(conferenceText, '') for item in data.xpath('//*[text()="%s"]/parent::td/parent::tr/parent::tbody/parent::table/preceding-sibling::div[starts-with(@class, "%s")]' % (team, conferenceText))][-1]

            if not conference in results:
                results[conference] = {}

            if not division in results[conference]:
                results[conference][division] = []

            results[conference][division].append(team)

        return results

    def verify(self, data):
        seasonBlocks = data.xpath('//div[@class="sectionHeader"]/h3')
        expectedSeason = self.season[:4] + '-' + self.season[4:]

        if not (seasonBlocks and seasonBlocks[0].text.strip() == expectedSeason):
            raise UnexpectedPageContents('Expected %s season, found %s' % (expectedSeason, seasonBlocks[0].text.strip()))


class NHLSchedule(Collector):
    """
    Scrapes the season schedule from the NHL, careful to only include
    games with NHL teams (they'll have olympic games in there, for
    instance)
    """
    def __init__(self, season, game_type='REG', base_url='http://www.nhl.com/ice/schedulebyseason.htm?season=%s&gameType=%s&team=&network=&venue='):
        self.check_season(season)
        self.check_game_type(game_type)
        self.season = season
        self.game_type = game_type

        super(NHLSchedule, self).__init__(base_url % (season, GAME_TYPES.index(game_type) + 1))

    def parse(self, data):
        games = []

        # Iterate over the schedule rows
        for row in data.xpath('//table[@class="data schedTbl"]/tbody/tr'):
            teams = [item.text for item in row.xpath('td[@class="team"]/div[@class="teamName"]/a|td[@class="team"]/div[@class="teamName"]') if item.text]

            # If we don't have two teams, we must be in some header row
            if not teams:
                continue
            else:
                if [team for team in teams if u'\xa0' in team]:
                    continue

            date = row.xpath('td[@class="date"]/div[@class="skedStartDateSite"]')[0].text
            startDate = datetime.datetime.strptime(date.strip(), '%a %b %d, %Y').date()

            # If there isn't yet a known time for the game, that's okay, let's just
            # leave it as None, we'll be checking again.
            if 'TBD' not in row.xpath('td[@class="time"]')[0].text_content():
                time = row.xpath('td[@class="time"]/div[@class="skedStartTimeEST"]')[0].text
                localTime = datetime.datetime.strptime(date + ' ' + time.replace('ET', '').strip(),  '%a %b %d, %Y %I:%M %p')
                startTime = self.convert_datetime_to_utc(localTime).time()
            else:
                startTime = None

            games.append({
                'season': self.season,
                'date': startDate,
                'time': startTime,
                'home': teams[1],
                'visitor': teams[0],
                'start': startDate,
                'type': self.game_type
            })

        return games

    def verify(self, data):
        if not data.xpath('//table[@class="data schedTbl"]/tbody/tr'):
            raise UnexpectedPageContents('Now schedule block found on page.')


class NHLTeams(Collector):
    """
    Unfortunately because the NHL is happy to mix in Olympic
    games and the like with their schedule, we must populate
    the teams separately. We do so by looking at pre-season
    games, which presumably only contain NHL teams.
    """
    def __init__(self, base_url='http://www.nhl.com/ice/teams.htm'):
        super(NHLTeams, self).__init__(base_url)

    def parse(self, data):
        teams = data.cssselect('div#teamMenu a')

        data = {}

        # Start from index 1, as 0 is the NHL logo.
        for team in teams[1:]:
            name = team.attrib['title']
            url = team.attrib['href']

            data[name] = url

        return data


class Schedule(Collector):
    def __init__(self, season, base_url):
        self.check_season(season)


class Events(Collector):
    pass
