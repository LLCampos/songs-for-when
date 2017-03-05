from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from music_inquiries.models import MusicInquiry

from selenium import webdriver

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

    def setUp(self):
        self.client = Client()
        self.driver = webdriver.Chrome()

        self.user_password = 'iknownothing'
        self.user = User.objects.create_user(
            username='JonSnow',
            password=self.user_password
        )

    def test_page_ok(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(200, response.status_code)

    def test_submit_inquiry_no_login(self):
        """User should be redirected to the login page."""

        login_page_url = reverse('login') + '?next=' + INDEX_URL

        self.driver.get(HOST + INDEX_URL)
        self.driver.find_element_by_id('submit-inquiry-form').click()
        self.assertIn(login_page_url, self.driver.current_url)

    def test_submit_inquiry_login(self):

        self.driver.get(HOST + INDEX_URL)
        login_user(self.driver, self.user.username, self.user_password)
        self.driver.find_element_by_id('submit-inquiry-form').click()

        self.assertIn(INQUIRIES_LISTING_URL, self.driver.current_url)


class TestsInquiriesListingView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_page_ok(self):
        response = self.client.get(INQUIRIES_LISTING_URL)
        self.assertEqual(200, response.status_code)


class TestsInquiryView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('John')

        self.inquiry = MusicInquiry.objects.create_music_inquiry(
            text='test',
            user=self.user
        )

    def test_page_ok(self):
        response = self.client.get(reverse(
            'music_inquiries:inquiry',
            kwargs={'inquiry_id': '1'}
        ))

        self.assertEqual(200, response.status_code)
