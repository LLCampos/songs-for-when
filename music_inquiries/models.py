from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    youtube_url = models.URLField()

    class Meta:
        unique_together = ('name', 'artist',)

    def __str__(self):
        return self.artist + '- ' + self.name


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


class SongSuggestion(models.Model):
    user = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    music_inquiry = models.ForeignKey(MusicInquiry)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('song', 'music_inquiry',)

    def __str__(self):
        return self.song.__str__()
