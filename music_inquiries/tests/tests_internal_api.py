from django.test import TestCase
from django.core.urlresolvers import reverse

from music_inquiries.models import *


USER1_NAME = 'JonSnow'
USER1_PASS = 'iknownothing'


class TestsInquiryResource(TestCase):

    fixtures = ['User.json', 'MusicInquiry.json']

    def setUp(self):
        self.resource_url = reverse('music_inquiries:inquiry_resource')

    def test_post_not_auth(self):
        response = self.client.post(
            self.resource_url,
            {'inquiry_text': 'a test is a test is a test'}
        )

        self.assertEqual(401, response.status_code)

    def test_post_repeated_inquiry(self):
        """Inquiry text being sent is equal to the one the fixture, so the POST
        request should return an error"""

        self.client.login(
            username=USER1_NAME,
            password=USER1_PASS
        )
        response = self.client.post(
            self.resource_url,
            {'inquiry_text': 'test inquiry'}
        )
        self.assertEqual(400, response.status_code)

    def test_post_ok_inquiry(self):
        number_inquiries_before = len(MusicInquiry.objects.all())

        self.client.login(
            username=USER1_NAME,
            password=USER1_PASS
        )
        response = self.client.post(
            self.resource_url,
            {'inquiry_text': 'another test inquiry'}
        )

        number_inquiries_after = len(MusicInquiry.objects.all())

        self.assertEqual(201, response.status_code)
        self.assertEqual(number_inquiries_before + 1, number_inquiries_after)

    def test_head_query_method_existent_inquiry(self):
        """Request should return code 200 because inquiry resource already
        exists"""

        response = self.client.head(
            self.resource_url,
            {'q': 'test inquiry'}
        )

        self.assertEqual(200, response.status_code)

    def test_head_query_method_non_existent_inquiry(self):
        """Request should return code 404 because inquiry resource does not
        exist"""

        response = self.client.head(
            self.resource_url,
            {'q': 'test inquiry non existent'}
        )

        self.assertEqual(404, response.status_code)

    def test_post_inquiry_too_short(self):

        inquiry_text = 'short'

        self.client.login(
            username=USER1_NAME,
            password=USER1_PASS
        )

        response = self.client.post(
            self.resource_url,
            {'inquiry_text': inquiry_text}
        )

        self.assertEqual(400, response.status_code)

    def test_post_inquiry_too_big(self):

        inquiry_text = ('this should have more than 80 chars. '
                        'this should have more than 80 chars. '
                        'this should have more than 80 chars.')

        self.client.login(
            username=USER1_NAME,
            password=USER1_PASS
        )

        response = self.client.post(
            self.resource_url,
            {'inquiry_text': inquiry_text}
        )

        self.assertEqual(400, response.status_code)
