from django.conf.urls import url

from . import views

app_name = 'music_inquiries'
urlpatterns = [
    # HTML Pages
    url(r'^$', views.index, name='index'),
    url(r'^inquiry/$', views.inquiries_listing, name='inquiries_listing'),
    url(r'^inquiry/(?P<inquiry_id>[0-9]+)/$', views.inquiry, name='inquiry'),

    # REST Internal API
    url(r'^iapi/inquiry/$', views.inquiry_resource, name='inquiry_resource'),
    url(r'^iapi/inquiry/search/$', views.inquiry_search_resource, name='inquiry_search_resource'),
    url(r'^iapi/inquiry/(?P<inquiry_id>[0-9]+)/report', views.inquiry_report_resource, name='inquiry_report_resource'),
    url(r'^iapi/inquiry/(?P<inquiry_id>[0-9]+)/suggestion/$', views.suggestion_resource, name='suggestion_resource'),
    url(r'^iapi/inquiry/(?P<inquiry_id>[0-9]+)/suggestion/(?P<suggestion_id>[0-9]+)/vote', views.suggestion_vote_resource, name='suggestion_vote_resource'),
    url(r'^iapi/song/$', views.song_resource, name='song_resource'),
]
