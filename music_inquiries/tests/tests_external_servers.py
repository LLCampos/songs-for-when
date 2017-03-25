import unittest
import requests


class TestsExternalServers(unittest.TestCase):

    def test_solr_is_on(self):
        response = requests.get('http://127.0.0.1:8983/solr/')
        self.assertEqual(200, response.status_code)
