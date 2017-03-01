from django.conf.urls import url

from . import views

app_name = 'music_inquiries'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^inquiry/$', views.inquiries_listing, name='inquiries_listing'),
    url(r'^inquiry/(?P<inquiry_id>[0-9]+)/$', views.inquiry, name='inquiry'),
]
