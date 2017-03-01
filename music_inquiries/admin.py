from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Song)
admin.site.register(MusicInquiry)
admin.site.register(SongSuggestion)
