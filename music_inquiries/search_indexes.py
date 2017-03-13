from django.utils import timezone
from haystack import indexes
from music_inquiries.models import MusicInquiry


class MusicInquiryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='text')
    created_at = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return MusicInquiry

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=timezone.now())
