from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from models import SongSuggestion, MusicInquiry


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']


class MusicInquiryResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'user')
    allowed_methods = ['get', 'post']

    class Meta:
        queryset = MusicInquiry.objects.all()
        resource_name = 'music_inquiry'

    def dehydrate(self, bundle):
        bundle.data['number_active_suggestions'] = bundle.obj.get_number_active_suggestions()
        return bundle


class SongSuggestionResource(ModelResource):

    class Meta:
        queryset = SongSuggestion.objects.all()
        resource_name = 'song_suggestion'
