from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

import urlparse
from django.utils import timezone


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('song_name', 'artist_name',)

    objects = SongManager()

    def __str__(self):
        return self.artist_name + '- ' + self.song_name


class MusicInquiryManager(models.Manager):
    def create_music_inquiry(self, user, text):

        if self.number_inquiries_day(user) >= 5:
            raise ValidationError('User can only make 5 inquiries per day')

        music_inquiry = MusicInquiry(user=user, text=text)
        music_inquiry.clean_fields()
        music_inquiry.save()
        return music_inquiry

    def does_music_inquiry_exist(self, inquiry_text):
        return self.filter(text=inquiry_text).exists()

    def number_inquiries_day(self, user):
        """Return number of Inquiries the User already added today."""
        time_24_hours_ago = timezone.now() - timezone.timedelta(days=1)
        return self.filter(user=user, created_at__gte=time_24_hours_ago).count()


class MusicInquiry(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(10), MaxLengthValidator(80)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MusicInquiryManager()

    def get_active_suggestions(self):
        """Returns the suggestions done for this inquiry for which:
            number positive votes - number negative votes > -5 """

        all_suggestions = SongSuggestion.objects.filter(music_inquiry=self)
        active_suggestions = filter(
            lambda suggestion: suggestion.is_valid(),
            all_suggestions
        )
        return active_suggestions

    def get_number_active_suggestions(self):
        return len(self.get_active_suggestions())

    def __str__(self):
        return self.text


class SongSuggestionManager(models.Manager):

    def create_suggestion(self, music_inquiry, user,
                          artist_name, song_name, youtube_url=None):

        if self.number_suggestions_day(user) >= 10:
            raise ValidationError('User can only make 10 suggestions per day')

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

    def number_suggestions_day(self, user):
        """Return number of Suggestions the User already added today."""
        time_24_hours_ago = timezone.now() - timezone.timedelta(days=1)
        return self.filter(user=user, created_at__gte=time_24_hours_ago).count()


class SongSuggestion(models.Model):
    user = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    music_inquiry = models.ForeignKey(MusicInquiry)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('song', 'music_inquiry',)

    objects = SongSuggestionManager()

    def add_vote(self, user, modality):
        SuggestionVote.objects.create_vote(user, self, modality)

    def remove_vote(self, user):
        SuggestionVote.objects.remove_vote(user, self)

    def _number_votes(self, modality):
        return SuggestionVote.objects.filter(
            suggestion=self,
            modality=modality
        ).count()

    def number_positive_votes(self):
        return self._number_votes('positive')

    def number_negative_votes(self):
        return self._number_votes('negative')

    def is_valid(self):
        """Returns True if:
        number positive votes - number negative votes > -5 """

        if self.number_positive_votes() - self.number_negative_votes() > -5:
            return True
        return False

    def __str__(self):
        return self.song.__str__()


class SuggestionVoteManager(models.Manager):

    def create_vote(self, user, suggestion, modality):

        if modality not in ['positive', 'negative']:
            raise ValidationError('modality must be "positive" or "negative".')

        if user.id == suggestion.user.id:
            raise ValidationError('User can\'t vote in her own Suggestion.')

        return self.create(user=user, suggestion=suggestion, modality=modality)

    def remove_vote(self, user, suggestion):
        suggestion = self.get(user=user, suggestion=suggestion)
        return suggestion.delete()


class SuggestionVote(models.Model):

    user = models.ForeignKey(User)
    suggestion = models.ForeignKey(SongSuggestion)
    modality = models.CharField(
        max_length=8,
        choices=(('positive', 'positive'), ('negative', 'negative'))
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'suggestion',)

    objects = SuggestionVoteManager()

    def revert_modality(self):

        assert self.modality in ['positive', 'negative']

        if self.modality == 'negative':
            self.modality = 'positive'
        else:
            self.modality = 'negative'

        self.save()

        return self.modality


class InquiryProblemReportManager(models.Manager):

    def create_inquiry_report(self, user, inquiry, category, comment=None):

        legal_categories = map(
            lambda choice: choice[0],
            InquiryProblemReport.CATEGORY_CHOICES
        )

        if category not in legal_categories:
            raise ValidationError('Category is not valid.')

        if self.number_reports_day(user) >= 5:
            raise ValidationError('User can only report 5 inquiries per day')

        inquiry = self.create(
            user=user,
            inquiry=inquiry,
            category=category,
            comment=comment
        )

        return inquiry

    def number_reports_day(self, user):
        """Return number of InquieryProblemReports the User already submitted
        today."""
        time_24_hours_ago = timezone.now() - timezone.timedelta(days=1)
        return self.filter(user=user, created_at__gte=time_24_hours_ago).count()


class InquiryProblemReport(models.Model):

    CATEGORY_CHOICES = (
        ('Duplicate', 'Duplicate'),
        ('Unethical', 'Unethical'),
        ('Does not make sense', 'Does not make sense'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey(User)
    inquiry = models.ForeignKey(MusicInquiry)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    comment = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'inquiry')

    objects = InquiryProblemReportManager()
