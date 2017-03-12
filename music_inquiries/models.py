from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

import urlparse


class SongManager(models.Manager):

    def process_youtube_url(self, youtube_url):
        """Assuming that the user will send the Youtube URL in the format seen
        in the browser. Ex: https://www.youtube.com/watch?v=CvBfHwUxHIk

        Transforms this into an URL that can embed in the HTML. Ex:
        https://www.youtube.com/embed/CvBfHwUxHIk
        """
        parsed = urlparse.urlparse(youtube_url)
        video_id = urlparse.parse_qs(parsed.query)['v'][0]

        return 'https://www.youtube.com/embed/{}'.format(video_id)

    def create_song(self, artist_name, song_name, youtube_url):
        song = self.create(
            artist_name=artist_name,
            song_name=song_name,
            youtube_url=self.process_youtube_url(youtube_url)
        )
        return song

    def does_song_exist(self, artist_name, song_name):
        return self.filter(
            artist_name=artist_name,
            song_name=song_name
        ).exists()


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
        music_inquiry = MusicInquiry(user=user, text=text)
        music_inquiry.clean_fields()
        music_inquiry.save()
        return music_inquiry

    def does_music_inquiry_exist(self, inquiry_text):
        return self.filter(text=inquiry_text).exists()


class MusicInquiry(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(10), MaxLengthValidator(80)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MusicInquiryManager()

    def __str__(self):
        return self.text


class SongSuggestionManager(models.Manager):

    def create_suggestion(self, music_inquiry, user,
                          artist_name, song_name, youtube_url=False):

        if Song.objects.does_song_exist(artist_name, song_name):
            song = Song.objects.get(
                song_name=song_name,
                artist_name=artist_name
            )
        else:
            song = Song.objects.create_song(
                artist_name=artist_name,
                song_name=song_name,
                youtube_url=youtube_url
            )

        suggestion = self.create(
            user=user,
            song=song,
            music_inquiry=music_inquiry
        )
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


class SuggestionVoteManager(models.Manager):

    def create_vote(self, user, suggestion, modality):

        if modality not in ['positive', 'negative']:
            raise ValidationError('modality must be "positive" or "negative".')

        if user.id == suggestion.user.id:
            raise ValidationError('User can\'t vote in her own Suggestion.')

        self.create(user=user, suggestion=suggestion, modality=modality)


class SuggestionVote(models.Model):

    user = models.ForeignKey(User)
    suggestion = models.ForeignKey(SongSuggestion)
    modality = models.CharField(
        max_length=8,
        choices=(('positive', 'positive'), ('negative', 'negative'))
    )

    class Meta:
        unique_together = ('user', 'suggestion',)

    objects = SuggestionVoteManager()
