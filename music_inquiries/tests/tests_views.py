from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from selenium import webdriver

from music_inquiries.models import MusicInquiry

HOST = 'http://localhost:8000'
INQUIRIES_LISTING_URL = reverse('music_inquiries:inquiries_listing')
INDEX_URL = reverse('music_inquiries:index')


def login_user(driver, username, password):

    driver.find_element_by_id('login-link').click()
    username_form_input = driver.find_element_by_name('username')
    password_form_input = driver.find_element_by_name('password')

    username_form_input.send_keys(username)
    password_form_input.send_keys(password)

    driver.find_element_by_id('submit-login').click()

    return driver


class TestsIndexView(TestCase):

    fixtures = ['User.json', 'MusicInquiry.json']

    def setUp(self):
        self.client = Client()
        self.driver = webdriver.Chrome()

        self.test_username = 'JonSnow'
        self.test_password = 'iknownothing'

    def test_page_ok(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(200, response.status_code)

    def test_submit_inquiry_button_disabled_no_login(self):
        """If user is not authenticated, button to submit inquiry should be
        disabled."""

        self.driver.get(HOST + INDEX_URL)
        submit_button = self.driver.find_element_by_id('submit-inquiry-form')
        self.assertFalse(submit_button.is_enabled())

    def test_submit_inquiry_login(self):

        self.driver.get(HOST + INDEX_URL)
        login_user(self.driver, self.test_username, self.test_password)
        self.driver.find_element_by_id('submit-inquiry-form').click()

        self.assertIn(INQUIRIES_LISTING_URL, self.driver.current_url)


class TestsInquiriesListingView(TestCase):

    fixtures = ['User.json', 'MusicInquiry.json']

    def setUp(self):
        self.client = Client()

        self.test_username = 'JonSnow'
        self.test_password = 'iknownothing'

    def test_page_ok(self):
        response = self.client.get(INQUIRIES_LISTING_URL)
        self.assertEqual(200, response.status_code)

    def test_post_not_auth(self):
        response = self.client.post(
            INQUIRIES_LISTING_URL,
            {'inquiry_text': 'test'}
        )
        self.assertEqual(401, response.status_code)

    def test_post_repeated_inquiry(self):
        """Inquiry text being sent is equal to the one the fixture, so the POST
        request should return an error"""

        self.client.login(
            username=self.test_username,
            password=self.test_password
        )
        response = self.client.post(
            INQUIRIES_LISTING_URL,
            {'inquiry_text': 'test inquiry'}
        )
        self.assertEqual(400, response.status_code)

    def test_post_ok_inquiry(self):
        """Inquiry text being sent is equal to the one the fixture, so the POST
        request should return an error"""

        number_inquiries_before = len(MusicInquiry.objects.all())

        self.client.login(
            username=self.test_username,
            password=self.test_password
        )
        response = self.client.post(
            INQUIRIES_LISTING_URL,
            {'inquiry_text': 'another test inquiry'}
        )

        number_inquiries_after = len(MusicInquiry.objects.all())

        self.assertEqual(200, response.status_code)
        self.assertEqual(number_inquiries_before + 1, number_inquiries_after)


class TestsInquiryView(TestCase):

    fixtures = ['User.json', 'MusicInquiry.json']

    def setUp(self):
        self.client = Client()

    def test_page_ok(self):
        response = self.client.get(reverse(
            'music_inquiries:inquiry',
            kwargs={'inquiry_id': '1'}
        ))

        self.assertEqual(200, response.status_code)
