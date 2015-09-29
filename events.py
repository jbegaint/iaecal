#!/usr/bin/env python2

import requests
import json
import os
from icalendar import Calendar as iCalendar, Event
from datetime import datetime, timedelta

MAX_N_WEEKS = 10


# utils functions
def clamp(val, lo, hi):
    return min(max(val, lo), hi)


def string_to_datetime(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


class Calendar(iCalendar):
    def __init__(self, n_weeks, *args, **kwargs):
        super(Calendar, self).__init__(*args, **kwargs)

        self.login_url = os.environ.get('CAL_LOGIN_URL')
        self.events_url = os.environ.get('CAL_EVENTS_URL')
        self.username = os.environ.get('CAL_USERNAME')
        self.password = os.environ.get('CAL_PASSWORD'),

        if (not self.login_url or not self.events_url or not
                self.username or not self.password):
            raise ValueError('Invalid configuration')

        self.n_weeks = self.parse_n_weeks(n_weeks)

        self.add('prodid', '-//IAE Calendar//')
        self.add('version', '2.0')

    def parse_n_weeks(self, n_weeks):
        try:
            n = clamp(int(n_weeks), 1, MAX_N_WEEKS)
        except ValueError:
            n = 1
        return n

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
        event.add('dtstart', string_to_datetime(e['start']))
        event.add('dtend', string_to_datetime(e['end']))

        self.add_component(event)

    def display(self):
        return self.to_ical().replace('\n\r', '\n').strip()


def main():
    import sys
    try:
        n = int(sys.argv[1])
    except (IndexError, ValueError):
        n = 1

    cal = Calendar(n)
    cal.update()
    print(cal.display())

if __name__ == "__main__":
    main()
