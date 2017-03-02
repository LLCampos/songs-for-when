from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User

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
