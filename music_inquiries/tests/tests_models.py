from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from music_inquiries.models import *


# Test Models
class TestSongModel(TestCase):

    def test_create_song(self):

        song = Song.objects.create_song(
            artist_name='Rihanna',
            song_name='Umbrella',
            youtube_url='https://www.youtube.com/watch?v=CvBfHwUxHIk'
        )

        self.assertEqual(song.song_name, 'Umbrella')
        self.assertEqual(song.artist_name, 'Rihanna')

    def test_does_song_exist(self):

        Song.objects.create_song(
            artist_name='Metallica',
            song_name='Enter Sandman',
            youtube_url='https://www.youtube.com/watch?v=CvBfHwUxHIk'
        )

        self.assertTrue(Song.objects.does_song_exist(
            artist_name='Metallica',
            song_name='Enter Sandman')
        )

        self.assertFalse(Song.objects.does_song_exist(
            artist_name='Megadeth',
            song_name='A Garagem da Vizinha')
        )

    def test_youtube_url_processing(self):

        song = Song.objects.create_song(
            artist_name='Eminem',
            song_name='Love The Way You Lie',
            youtube_url='https://www.youtube.com/watch?v=uelHwf8o7_U'
        )

        self.assertEqual(
            song.youtube_url,
            'https://www.youtube.com/embed/uelHwf8o7_U'
        )

    def test_insert_duplicated_songs(self):
        """Should raise IntegrityError when trying to insert already existent
        song."""

        artist_name = 'Mew'
        song_name = 'Snow Brigade'
        youtube_url = 'https://www.youtube.com/watch?v=ZctGnled2tk'

        Song.objects.create_song(artist_name, song_name, youtube_url)

        self.assertRaises(
            IntegrityError,
            Song.objects.create_song,
            artist_name, song_name, youtube_url
        )


class testMusicInquiry(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('John')
        self.user2 = User.objects.create_user('Anna')

    def test_create_music_inquiry(self):
        inquiry_text = 'Songs for tests.'

        inquiry = MusicInquiry.objects.create_music_inquiry(
            text=inquiry_text,
            user=self.user1
        )

        self.assertEqual(inquiry_text, inquiry.text)
        self.assertEqual(self.user1, inquiry.user)

    def test_insert_duplicated_inquiries(self):
        """Should raise IntegrityError when trying to insert already existent
        inquiry."""

        inquiry_text = 'Another songs for tests.'

        MusicInquiry.objects.create_music_inquiry(
            text=inquiry_text,
            user=self.user1
        )

        self.assertRaises(
            IntegrityError,
            MusicInquiry.objects.create_music_inquiry,
            self.user2, inquiry_text,
        )

    def test_music_inquiry_exists_method(self):

        inquiry_text = 'Songs for tests.'

        MusicInquiry.objects.create_music_inquiry(
            text=inquiry_text,
            user=self.user1
        )

        exists = MusicInquiry.objects.does_music_inquiry_exist(inquiry_text)
        not_exists = MusicInquiry.objects.does_music_inquiry_exist('No exist')

        self.assertTrue(exists)
        self.assertFalse(not_exists)

    def test_add_short_inquiry(self):

        inquiry_text = 'test'

        self.assertRaises(
            ValidationError,
            MusicInquiry.objects.create_music_inquiry,
            self.user1, inquiry_text,
        )

        does_exist = MusicInquiry.objects.does_music_inquiry_exist(inquiry_text)
        self.assertFalse(does_exist)

    def test_add_big_inquiry(self):

        inquiry_text = ('this should have more than 80 chars. '
                        'this should have more than 80 chars. '
                        'this should have more than 80 chars.')

        self.assertRaises(
            ValidationError,
            MusicInquiry.objects.create_music_inquiry,
            self.user1, inquiry_text,
        )

        does_exist = MusicInquiry.objects.does_music_inquiry_exist(inquiry_text)
        self.assertFalse(does_exist)


class testSongSuggestion(TestCase):

    fixtures = [
        'User.json',
        'SongSuggestion.json',
        'MusicInquiry.json',
        'Song.json'
    ]

    def setUp(self):

        self.user = User.objects.create_user('Louis')

        self.song = Song.objects.create_song(
            artist_name='Slayer',
            song_name='Raining Blood',
            youtube_url='https://www.youtube.com/watch?v=z8ZqFlw6hYg'
        )

        self.inquiry = MusicInquiry.objects.create_music_inquiry(
            text='Music for when it\'s raining blood',
            user=self.user
        )

    def test_add_existent_song(self):

        suggestion = SongSuggestion.objects.create_suggestion(
            music_inquiry=self.inquiry,
            user=self.user,
            artist_name='Slayer',
            song_name='Raining Blood',
        )

        self.assertEqual(suggestion.music_inquiry, self.inquiry)
        self.assertEqual(suggestion.user, self.user)
        self.assertEqual(suggestion.song, self.song)

    def test_add_non_existent_song(self):

        artist_name = 'The Weeknd',
        song_name = 'Starboy'
        youtube_url = 'https://www.youtube.com/watch?v=34Na4j8AVgA'

        suggestion = SongSuggestion.objects.create_suggestion(
            music_inquiry=self.inquiry,
            user=self.user,
            artist_name=artist_name,
            song_name=song_name,
            youtube_url=youtube_url,
        )

        self.assertEqual(suggestion.music_inquiry, self.inquiry)
        self.assertEqual(suggestion.user, self.user)
        self.assertEqual(suggestion.song.artist_name, artist_name)
        self.assertEqual(suggestion.song.song_name, song_name)

    def test_add_duplicated_suggestion(self):

        artist_name = 'The Big Pink',
        song_name = 'Dominos'
        youtube_url = 'https://www.youtube.com/watch?v=OGnNlQ-KNv4'

        SongSuggestion.objects.create_suggestion(
            music_inquiry=self.inquiry,
            user=self.user,
            artist_name=artist_name,
            song_name=song_name,
            youtube_url=youtube_url,
        )

        self.assertRaises(
            IntegrityError,
            SongSuggestion.objects.create_suggestion,
            music_inquiry=self.inquiry,
            user=self.user,
            artist_name=artist_name,
            song_name=song_name,
            youtube_url=youtube_url,
        )

    def test_correct_number_votes(self):

        suggestion = SongSuggestion.objects.get(id=1)
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=4)
        user3 = User.objects.get(id=3)

        suggestion.add_vote(user1, 'positive')
        suggestion.add_vote(user2, 'positive')
        suggestion.add_vote(user3, 'negative')

        self.assertEqual(2, suggestion.number_positive_votes())
        self.assertEqual(1, suggestion.number_negative_votes())

    def test_count_suggestions_in_the_day(self):
        user = User.objects.get(id=3)
        inquiry1 = MusicInquiry.objects.get(id=1)
        inquiry2 = MusicInquiry.objects.get(id=2)

        SongSuggestion.objects.create_suggestion(
            inquiry1,
            user,
            'artist1',
            'song1',
            'https://www.youtube.com/watch?v=brRmdqjn-g4'
        )

        SongSuggestion.objects.create_suggestion(
            inquiry2,
            user,
            'artist2',
            'song2',
            'https://www.youtube.com/watch?v=JdhhCCiIx40'
        )

        # Create a suggestion done three days ago. Should no be counted.
        suggestion = SongSuggestion.objects.create(
            music_inquiry=inquiry2,
            user=user,
            song=Song.objects.get(id=1),
        )
        SongSuggestion.objects.filter(id=suggestion.id).update(
            created_at=timezone.now() - timezone.timedelta(days=3)
        )

        self.assertEqual(
            2,
            SongSuggestion.objects.number_suggestions_day(user)
        )


class testSuggestionVote(TestCase):

    fixtures = [
        'User.json',
        'SongSuggestion.json',
        'MusicInquiry.json',
        'Song.json'
    ]

    def setUp(self):
        self.test_user_1 = User.objects.get(id=1)
        self.test_user_2 = User.objects.get(id=2)
        self.test_suggestion = SongSuggestion.objects.get(id=1)

    def test_create_legal_vote(self):

        SuggestionVote.objects.create_vote(
            user=self.test_user_1,
            suggestion=self.test_suggestion,
            modality='positive'
        )

        self.assertTrue(
            SuggestionVote.objects.filter(
                user=self.test_user_1,
                suggestion=self.test_suggestion,
            ).exists()
        )

    def test_create_vote_non_valid_modality(self):

        self.assertRaises(
            ValidationError,
            SuggestionVote.objects.create_vote,
            user=self.test_user_1,
            suggestion=self.test_suggestion,
            modality='neutral'
        )

        self.assertFalse(
            SuggestionVote.objects.filter(
                user=self.test_user_1,
                suggestion=self.test_suggestion,
            ).exists()
        )

    def test_user_vote_two_times_same_suggestion(self):

        SuggestionVote.objects.create_vote(
            user=self.test_user_1,
            suggestion=self.test_suggestion,
            modality='positive'
        )

        self.assertRaises(
            IntegrityError,
            SuggestionVote.objects.create_vote,
            user=self.test_user_1,
            suggestion=self.test_suggestion,
            modality='positive'
        )

    def test_user_vote_her_own_suggestion(self):
        """User can't vote her own suggestion;"""

        self.assertRaises(
            ValidationError,
            SuggestionVote.objects.create_vote,
            user=self.test_user_2,
            suggestion=self.test_suggestion,
            modality='positive'
        )
