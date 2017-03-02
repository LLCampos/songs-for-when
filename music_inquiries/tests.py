from django.test import TestCase
from django.db import IntegrityError

from music_inquiries.models import Song


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
