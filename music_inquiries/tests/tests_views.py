from django.test import TestCase, TransactionTestCase, Client
from django.core.urlresolvers import reverse

from selenium import webdriver

from music_inquiries.models import *

HOST = 'http://localhost:8000'
INQUIRIES_LISTING_URL = reverse('music_inquiries:inquiries_listing')
INDEX_URL = reverse('music_inquiries:index')

USER1_NAME = 'JonSnow'
USER1_PASS = 'iknownothing'


def login_user(driver, username, password):

    driver.find_element_by_id('login-link').click()
    username_form_input = driver.find_element_by_name('username')
    password_form_input = driver.find_element_by_name('password')

    username_form_input.send_keys(username)
    password_form_input.send_keys(password)

    driver.find_element_by_id('submit-login').click()

    return driver


class TestsIndexView(TransactionTestCase):

    fixtures = ['User.json', 'MusicInquiry.json']

    def setUp(self):
        self.client = Client()
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_page_ok(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(200, response.status_code)

    def test_submit_inquiry_button_disabled_no_login(self):
        """If user is not authenticated, button should redirect user to login
        page"""

        self.driver.get(HOST + INDEX_URL)
        submit_button = self.driver.find_element_by_id(
            'inquiry-submit-form-button'
        )

        button_message = submit_button.text
        button_href = submit_button.get_property('href')

        login_page_url = HOST + reverse('login') + '?next=' + INDEX_URL

        self.assertEqual('Login to Ask for Suggestions', button_message)
        self.assertEqual(login_page_url, button_href)

    def test_submit_no_min_length(self):

        self.driver.get(HOST + INDEX_URL)
        login_user(self.driver, USER1_NAME, USER1_PASS)

        inquiry_input = self.driver.find_element_by_name('inquiry_text')
        inquiry_input.send_keys('test')

        submit_button = self.driver.find_element_by_id(
            'inquiry-submit-form-button'
        )

        button_message = submit_button.get_attribute('value')

        self.assertFalse(submit_button.is_enabled())
        self.assertEqual('6 characters left', button_message)

    def test_submit_whitespaces(self):
        """Inquiry should only count as having 2 characters. (the letter and
        one space)"""

        self.driver.get(HOST + INDEX_URL)
        login_user(self.driver, USER1_NAME, USER1_PASS)

        inquiry_input = self.driver.find_element_by_name('inquiry_text')
        inquiry_input.send_keys('      a       ')

        submit_button = self.driver.find_element_by_id(
            'inquiry-submit-form-button'
        )

        button_message = submit_button.get_attribute('value')

        self.assertFalse(submit_button.is_enabled())
        self.assertEqual('8 characters left', button_message)

    # def test_submit_legal_inquiry(self):

    #     self.driver.get(HOST + INDEX_URL)
    #     login_user(self.driver, USER1_NAME, USER1_PASS)

    #     inquiry_input = self.driver.find_element_by_name('inquiry_text')
    #     inquiry_input.send_keys('Definitely more than enough characters.')

    #     self.driver.find_element_by_id('inquiry-submit-form-button').click()

    #     self.assertIn(INQUIRIES_LISTING_URL, self.driver.current_url)


class TestsInquiriesListingView(TestCase):

    fixtures = ['User.json', 'MusicInquiry.json']

    def setUp(self):
        self.client = Client()

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
            username=USER1_NAME,
            password=USER1_PASS
        )
        response = self.client.post(
            INQUIRIES_LISTING_URL,
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
            INQUIRIES_LISTING_URL,
            {'inquiry_text': 'another test inquiry'}
        )

        number_inquiries_after = len(MusicInquiry.objects.all())

        self.assertEqual(200, response.status_code)
        self.assertEqual(number_inquiries_before + 1, number_inquiries_after)

    def test_head_query_method_existent_inquiry(self):
        """Request should return code 200 because inquiry resource already
        exists"""

        response = self.client.head(
            INQUIRIES_LISTING_URL,
            {'q': 'test inquiry'}
        )

        self.assertEqual(200, response.status_code)

    def test_head_query_method_non_existent_inquiry(self):
        """Request should return code 404 because inquiry resource does not
        exist"""

        response = self.client.head(
            INQUIRIES_LISTING_URL,
            {'q': 'test inquiry non existent'}
        )

        self.assertEqual(404, response.status_code)

    def test_post_short_inquiry(self):

        inquiry_text = 'short'

        self.client.login(
            username=USER1_NAME,
            password=USER1_PASS
        )

        response = self.client.post(
            INQUIRIES_LISTING_URL,
            {'inquiry_text': inquiry_text}
        )

        self.assertEqual(400, response.status_code)

    def test_post_big_inquiry(self):

        inquiry_text = ('this should have more than 80 chars. '
                        'this should have more than 80 chars. '
                        'this should have more than 80 chars.')

        self.client.login(
            username=USER1_NAME,
            password=USER1_PASS
        )

        response = self.client.post(
            INQUIRIES_LISTING_URL,
            {'inquiry_text': inquiry_text}
        )

        self.assertEqual(400, response.status_code)


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


class TestSuggestionView(TestCase):

    fixtures = [
        'User.json',
        'MusicInquiry.json',
        'SongSuggestion.json',
        'Song.json'
    ]

    def setUp(self):
        self.client = Client()

    def test_add_suggestion_non_existent_song_with_youtube_url(self):

        self.client.login(username=USER1_NAME, password=USER1_PASS)

        song_name = 'test song'
        artist_name = 'test artist'
        youtube_url = 'https://www.youtube.com/watch?v=znHpyf1Lolo'

        response = self.client.post(
            reverse('music_inquiries:suggestion', kwargs={'inquiry_id': 4}),
            {'song_name': song_name,
             'artist_name': artist_name,
             'youtube_url': youtube_url}
        )

        self.assertEqual(200, response.status_code)


class TestsInquirySearchView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_page_ok(self):
        response = self.client.get(
            reverse('music_inquiries:inquiry_search'),
            {'q': 'test'}
        )

        self.assertEqual(200, response.status_code)
