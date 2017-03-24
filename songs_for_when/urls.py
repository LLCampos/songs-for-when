"""songs_for_when URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from tastypie.api import Api

from music_inquiries.internal_api import SongSuggestionResource, MusicInquiryResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(SongSuggestionResource())
v1_api.register(MusicInquiryResource())
v1_api.register(UserResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('music_inquiries.urls')),
    url("^soc/", include("social_django.urls", namespace="social")),
    url('^accounts/', include('django.contrib.auth.urls')),

    url(r'^api/', include(v1_api.urls)),

]
