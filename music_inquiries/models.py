from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class SongManager(models.Manager):

    def create_song(self, artist_name, song_name, youtube_url):
        song = self.create(artist_name=artist_name, song_name=song_name, youtube_url=youtube_url)
        return song

    def does_song_exist(self, artist_name, song_name):
        return self.filter(artist_name=artist_name, song_name=song_name).exists()


class Song(models.Model):
    artist_name = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)
    youtube_url = models.URLField()

    class Meta:
        unique_together = ('song_name', 'artist_name',)

    objects = SongManager()

    def __str__(self):
        return self.artist_name + '- ' + self.song_name


class MusicInquiryManager(models.Manager):
    def create_music_inquiry(self, user, text):
        music_inquiry = self.create(user=user, text=text)
        return music_inquiry


class MusicInquiry(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MusicInquiryManager()

    def __str__(self):
        return self.text


class SongSuggestionManager(models.Manager):

    def create_suggestion(self, music_inquiry, user, song_name, artist_name, youtube_url=False):

        if Song.objects.does_song_exist(song_name, artist_name):
            song = Song.objects.get(song_name=song_name, artist_name=artist_name)
        else:
            song = Song.objects.create_song(song_name, artist_name, youtube_url)

        suggestion = self.create(user=user, song=song, music_inquiry=music_inquiry)
        return suggestion


class SongSuggestion(models.Model):
    user = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    music_inquiry = models.ForeignKey(MusicInquiry)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('song', 'music_inquiry',)

    objects = SongSuggestionManager()

    def __str__(self):
        return self.song.__str__()
