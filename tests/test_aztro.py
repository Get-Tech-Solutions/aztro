from .. import app as aztro
import unittest
import json
import os

class AztroTestCase(unittest.TestCase):

    signs = [
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra',
        'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
    ]

    days = [
        'today', 'tomorrow', 'yesterday'
    ]

    def setUp(self):
        aztro.app.testing = True
        self.app = aztro.app.test_client()

    def assertAztroResponse(self, response):
        dict_keys = [
            'current_date', 'compatibility', 'lucky_time', 'lucky_number',
            'color', 'date_range', 'mood', 'description'
        ]

        response_data = json.loads(response.data)

        for dict_key in dict_keys:
            self.assertTrue(
                dict_key in response_data,
                'Key {} not in response'.format(dict_key)
            )
        self.assertEqual(response.status_code, 200)

    def test_landing_page(self):
        response = self.app.get('/', follow_redirects=False)

        expectedPath = 'https://aztro.readthedocs.io/en/latest/'
        self.assertEqual(response.location, expectedPath)
        self.assertEqual(response.status_code, 302)

    def test_page_not_found(self):
        response = self.app.get('/notfound', follow_redirects=False)

        self.assertEqual(
            json.loads(response.data),
            {
                'error': 404,
                'text': '404 Not Found: The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_api(self):
        for sign in self.signs:
            for day in self.days:
                url = '/?sign={sign}&day={day}'.format(sign=sign, day=day)
                response = self.app.post(url)

                self.assertAztroResponse(response)
