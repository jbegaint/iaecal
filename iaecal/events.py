# events.py

import requests
import json
import os
import pytz
from icalendar import Calendar as iCalendar, Event, Timezone
from datetime import datetime, timedelta

N_WEEKS = 4
TIMEZONE = "Europe/Paris"


def string_to_datetime(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


class Calendar(iCalendar):
    def __init__(self, username, password, *args, **kwargs):
        super(Calendar, self).__init__(*args, **kwargs)

        self.login_url = os.environ.get('CAL_LOGIN_URL')
        self.events_url = os.environ.get('CAL_EVENTS_URL')
        self.username = username
        self.password = password

        if not self.login_url or not self.events_url:
            raise ValueError('Invalid configuration')

        self.n_weeks = N_WEEKS

        self.add('prodid', '-//IAE Calendar//')
        self.add('version', '2.0')

        # Add Timezone info
        self.add('x-wr-timezone', TIMEZONE)
        tzc = Timezone()
        tzc.add('tzid', TIMEZONE)
        tzc.add('x-lic-location', TIMEZONE)
        self.add_component(tzc)

    def update(self):
        data = self.get_data()
        for item in data:
            self.add_event(item)
        return self

    def get_data(self):
        session = requests.Session()
        payload = {
            'username': self.username,
            'password': self.password
        }

        # login
        session.post(self.login_url, data=payload)

        # craft url
        dtstart = datetime.today()
        dtdelta = timedelta(days=(7 * self.n_weeks))
        dtend = dtstart + dtdelta

        start = dtstart.strftime('%s')
        end = dtend.strftime('%s')

        url = self.events_url + '?&start=' + start + '&end=' + end

        # get data
        response = session.get(url)

        # convert to python list
        try:
            data = json.loads(response.text)
        except ValueError:
            return []
        return data

    def add_event(self, e):
        event = Event()
        event.add('summary', e['title'])
        tz = pytz.timezone(TIMEZONE)
        event.add('dtstart', tz.localize(string_to_datetime(e['start'])))
        event.add('dtend', tz.localize(string_to_datetime(e['end'])))

        self.add_component(event)

    def display(self):
        return self.to_ical().replace('\n\r', '\n').strip()
