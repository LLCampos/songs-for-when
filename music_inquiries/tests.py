from django.test import TestCase
from music_inquiries.models import Song

# Test Models


class TestSongModel(TestCase):

    def setUp(self):
        pass

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
