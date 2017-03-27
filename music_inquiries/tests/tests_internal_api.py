from django.test import TestCase
from django.core.urlresolvers import reverse

from music_inquiries.models import *


USER1_NAME = 'JonSnow'
USER3_NAME = 'MikeP'
USER_PASS = 'iknownothing'


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
            password=USER_PASS
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
            password=USER_PASS
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
            password=USER_PASS
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
            password=USER_PASS
        )

        response = self.client.post(
            self.resource_url,
            {'inquiry_text': inquiry_text}
        )

        self.assertEqual(400, response.status_code)


class TestInquiryReportResource(TestCase):

    fixtures = ['User.json', 'MusicInquiry.json']

    def test_add_complete_report(self):

        self.client.login(username=USER1_NAME, password=USER_PASS)

        response = self.client.post(
            reverse('music_inquiries:inquiry_report_resource', kwargs={'inquiry_id': 3}),
            {'category': 'Duplicate',
             'comment': 'a cool comment'}
        )

        self.assertEqual(201, response.status_code)

    def test_add_report_without_comment(self):

        self.client.login(username=USER1_NAME, password=USER_PASS)

        response = self.client.post(
            reverse('music_inquiries:inquiry_report_resource', kwargs={'inquiry_id': 3}),
            {'category': 'Duplicate'}
        )

        self.assertEqual(201, response.status_code)

    def test_add_report_with_non_valid_category(self):
        self.client.login(username=USER1_NAME, password=USER_PASS)

        response = self.client.post(
            reverse('music_inquiries:inquiry_report_resource', kwargs={'inquiry_id': 3}),
            {'category': 'Bananas'}
        )

        self.assertEqual(400, response.status_code)

    def test_add_report_no_auth(self):

        response = self.client.post(
            reverse('music_inquiries:inquiry_report_resource', kwargs={'inquiry_id': 3}),
            {'category': 'Duplicate',
             'comment': 'a cool comment'}
        )

        self.assertEqual(401, response.status_code)


class TestSongResource(TestCase):

    fixtures = ['Song.json']

    def test_check_if_existent_song_exists(self):

        response = self.client.head(
            reverse('music_inquiries:song_resource'),
            {'song_name': 'Easy',
             'artist_name': 'Son Lux'}
        )

        self.assertEqual(200, response.status_code)

    def test_check_if_non_existent_song_exists(self):

        response = self.client.head(
            reverse('music_inquiries:song_resource'),
            {'song_name': 'asdfsadfsadf',
             'artist_name': 'Son asdfsadfsadf'}
        )

        self.assertEqual(404, response.status_code)


# class TestsInquirySearchResource(TestCase):

#     def test_resource_ok(self):
#         response = self.client.get(
#             reverse('music_inquiries:inquiry_search_resource'),
#             {'q': 'test'}
#         )

#         self.assertEqual(200, response.status_code)


class TestSuggestionResource(TestCase):

    fixtures = [
        'User.json',
        'MusicInquiry.json',
        'SongSuggestion.json',
        'Song.json'
    ]

    def test_add_suggestion_non_existent_song_with_youtube_url(self):

        self.client.login(username=USER1_NAME, password=USER_PASS)

        song_name = 'test song'
        artist_name = 'test artist'
        youtube_url = 'https://www.youtube.com/watch?v=znHpyf1Lolo'

        response = self.client.post(
            reverse('music_inquiries:suggestion_resource', kwargs={'inquiry_id': 4}),
            {'song_name': song_name,
             'artist_name': artist_name,
             'youtube_url': youtube_url}
        )

        self.assertEqual(201, response.status_code)

    def test_add_suggestion_existent_song_with_no_youtube_url(self):

        self.client.login(username=USER1_NAME, password=USER_PASS)

        song_name = 'Easy'
        artist_name = 'Son Lux'

        response = self.client.post(
            reverse('music_inquiries:suggestion_resource', kwargs={'inquiry_id': 4}),
            {'song_name': song_name,
             'artist_name': artist_name}
        )

        self.assertEqual(201, response.status_code)

    def test_add_suggestion_without_auth(self):

        song_name = 'test song'
        artist_name = 'test artist'
        youtube_url = 'https://www.youtube.com/watch?v=znHpyf1Lolo'

        response = self.client.post(
            reverse('music_inquiries:suggestion_resource', kwargs={'inquiry_id': 4}),
            {'song_name': song_name,
             'artist_name': artist_name,
             'youtube_url': youtube_url}
        )

        self.assertEqual(401, response.status_code)


class TestSuggestionVoteResource(TestCase):

    fixtures = [
        'User.json',
        'SongSuggestion.json',
        'MusicInquiry.json',
        'Song.json'
    ]

    def test_post_vote_no_auth(self):

        suggestion = SongSuggestion.objects.get(id=1)

        positive_votes_before = suggestion.number_positive_votes()

        post_params = {
            'inquiry_id': suggestion.music_inquiry.id,
            'suggestion_id': suggestion.id
        }

        response = self.client.post(
            reverse('music_inquiries:suggestion_vote_resource', kwargs=post_params),
            {'modality': 'positive'}
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual(positive_votes_before, suggestion.number_positive_votes())

    def test_post_votes(self):

        self.client.login(username=USER1_NAME, password=USER_PASS)

        suggestion = SongSuggestion.objects.get(id=1)

        positive_votes_before = suggestion.number_positive_votes()
        negative_votes_before = suggestion.number_negative_votes()

        post_params = {
            'inquiry_id': suggestion.music_inquiry.id,
            'suggestion_id': suggestion.id
        }

        response1 = self.client.post(
            reverse('music_inquiries:suggestion_vote_resource', kwargs=post_params),
            {'modality': 'positive'}
        )

        self.assertEqual(201, response1.status_code)
        self.assertEqual(
            positive_votes_before + 1,
            suggestion.number_positive_votes()
        )

        self.client.login(username=USER3_NAME, password=USER_PASS)

        response2 = self.client.post(
            reverse('music_inquiries:suggestion_vote_resource', kwargs=post_params),
            {'modality': 'negative'}
        )
        self.assertEqual(201, response2.status_code)

        self.assertEqual(
            positive_votes_before + 1,
            suggestion.number_positive_votes()
        )

        self.assertEqual(
            negative_votes_before + 1,
            suggestion.number_negative_votes()
        )

    def test_put_votes(self):

        self.client.login(username=USER1_NAME, password=USER_PASS)

        suggestion = SongSuggestion.objects.get(id=1)

        positive_votes_before = suggestion.number_positive_votes()

        post_params = {
            'inquiry_id': suggestion.music_inquiry.id,
            'suggestion_id': suggestion.id
        }

        response = self.client.post(
            reverse('music_inquiries:suggestion_vote_resource', kwargs=post_params),
            {'modality': 'positive'}
        )

        self.assertEqual(201, response.status_code)
        self.assertEqual(
            positive_votes_before + 1,
            suggestion.number_positive_votes()
        )

        response = self.client.put(
            reverse('music_inquiries:suggestion_vote_resource', kwargs=post_params),
        )

        self.assertEqual(201, response.status_code)
        self.assertEqual(
            positive_votes_before,
            suggestion.number_positive_votes()
        )
