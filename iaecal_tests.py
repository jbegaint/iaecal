#!/usr/bin/env python2

import json
import unittest

from iaecal import create_app, db


class IAECalTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        rv = self.client.get('/')
        assert rv.status_code == 200

    def test_get_url(self):
        url = '/get-url'

        # Test invalid method (only POST is allowed for this view)
        rv = self.client.get(url)
        assert rv.status_code == 405

        # Test invalid data content_type
        data = {'username': 'foo', 'password': 'bar'}
        rv = self.client.post(url, data=data)
        assert rv.status_code == 400

        # Test invalid data
        data = {'username': 'foo', 'password1': 'bar'}
        rv = self.client.post(url, data=data, content_type='clientlication/json')
        assert rv.status_code == 400

        # Test response on valid request
        data = {'username': 'foo', 'password': 'bar'}
        rv = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert rv.status_code == 200
        assert 'url' in json.loads(rv.get_data())

    def test_events(self):
        # Test missing parameters
        rv = self.client.get('/event/')
        assert rv.status_code == 404

        rv = self.client.get('/event/?session_id=toto')
        assert rv.status_code == 404

        rv = self.client.get('/event/?key=toto')
        assert rv.status_code == 404

        # Test invalid parameters
        rv = self.client.get('/event/?session_id=foo&key=bar')
        assert rv.status_code == 404


if __name__ == '__main__':
    unittest.main()
