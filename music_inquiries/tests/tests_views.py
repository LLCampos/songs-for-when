from django.test import TestCase, TransactionTestCase, Client
from django.core.urlresolvers import reverse

from selenium import webdriver

from music_inquiries.models import *

HOST = 'http://localhost:8000'
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
        response = self.client.get(reverse('music_inquiries:inquiries_listing'))
        self.assertEqual(200, response.status_code)


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

    def test_add_suggestion_existent_song_with_no_youtube_url(self):

        self.client.login(username=USER1_NAME, password=USER1_PASS)

        song_name = 'Easy'
        artist_name = 'Son Lux'

        response = self.client.post(
            reverse('music_inquiries:suggestion', kwargs={'inquiry_id': 4}),
            {'song_name': song_name,
             'artist_name': artist_name}
        )

        self.assertEqual(200, response.status_code)

    def test_add_suggestion_without_auth(self):

        song_name = 'test song'
        artist_name = 'test artist'
        youtube_url = 'https://www.youtube.com/watch?v=znHpyf1Lolo'

        response = self.client.post(
            reverse('music_inquiries:suggestion', kwargs={'inquiry_id': 4}),
            {'song_name': song_name,
             'artist_name': artist_name,
             'youtube_url': youtube_url}
        )

        self.assertEqual(302, response.status_code)


class TestsInquirySearchView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_page_ok(self):
        response = self.client.get(
            reverse('music_inquiries:inquiry_search'),
            {'q': 'test'}
        )

        self.assertEqual(200, response.status_code)


class TestSongView(TestCase):

    fixtures = ['Song.json']

    def setUp(self):
        self.client = Client()

    def test_check_if_existent_song_exists(self):

        response = self.client.head(
            reverse('music_inquiries:song'),
            {'song_name': 'Easy',
             'artist_name': 'Son Lux'}
        )

        self.assertEqual(200, response.status_code)

    def test_check_if_non_existent_song_exists(self):

        response = self.client.head(
            reverse('music_inquiries:song'),
            {'song_name': 'asdfsadfsadf',
             'artist_name': 'Son asdfsadfsadf'}
        )

        self.assertEqual(404, response.status_code)


# class TestSuggestionVoteView(Test.Case):

#     fixtures = [
#         'User.json',
#         'SongSuggestion.json',
#         'MusicInquiry.json',
#         'Song.json'
#     ]

#     def setUp(self):
#         self.client = Client()

#     def test_vote_endpoint_ok(self):

#         self.client.login(username=USER1_NAME, password=USER1_PASS)
#         inquiry_id = 1
#         suggestion_id = 1
