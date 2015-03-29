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

        self.n_weeks = self.parse_n_weeks(n_weeks)
        self.add('prodid', '-//IAE Calendar//')
        self.add('version', '2.0')

    def parse_n_weeks(self, n_weeks):
        try:
            n = clamp(int(n_weeks), MAX_N_WEEKS)
        except:
            n = 1

        return n

    def update(self):
        data = self.get_data()
        for item in data:
            self.add_event(item)

    def get_data(self):
        s = requests.Session()
        login_url = os.environ.get('CAL_LOGIN_URL')
        events_url = os.environ.get('CAL_EVENTS_URL')
        res = []

        payload = {
            'username': os.environ.get('CAL_USERNAME'),
            'password': os.environ.get('CAL_PASSWORD')
        }

        # login
        r = s.post(login_url, data=payload)

        # make one week long requests only
        for i in range(0, self.n_weeks):
            # craft url
            dtstart = datetime.today() + timedelta(weeks=i)
            dtdelta = timedelta(days=7)
            dtend = dtstart + dtdelta

            start = dtstart.strftime('%s')
            end = dtend.strftime('%s')

            url = events_url + '?&start=' + start + '&end=' + end

            # get data
            r = s.get(url)
            text = r.text

            # convert to python list
            try:
                data = json.loads(text)
            except ValueError:
                return res
            res = res + data

        return res

    def add_event(self, e):
        event = Event()
        event.add('summary', e['title'])
        event.add('dtstart', string_to_datetime(e['start']))
        event.add('dtend', string_to_datetime(e['end']))

        self.add_component(event)

    def display(self):
        return self.to_ical().replace('\n\r', '\n').strip()
