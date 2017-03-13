from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from models import MusicInquiry, SongSuggestion

from haystack.query import SearchQuerySet

import json


def index(request):
    return render(request, 'music_inquiries/index.html')


def inquiries_listing(request):

    if request.method == 'HEAD':
        """Method used to check if a certain inquiry text was already
        submitted"""

        query = request.GET['q']

        if MusicInquiry.objects.does_music_inquiry_exist(query):
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

    elif request.method == 'POST':

        if request.user.is_authenticated():
            try:
                inquiry_text = request.POST['inquiry_text']
            except(KeyError):
                raise Http404(
                    "'inquiry_text' parameter was not sent in the request."
                )

            try:
                MusicInquiry.objects.create_music_inquiry(
                    user=request.user,
                    text=inquiry_text
                )

            except(IntegrityError, ValidationError):
                return HttpResponse(
                    'Error when adding inquiry to database',
                    status=400
                )

        else:
            return HttpResponse('Unauthorized', status=401)

    latest_inquiries = MusicInquiry.objects.order_by('-created_at')[:15]
    context = {'inquiries': latest_inquiries}
    return render(request, 'music_inquiries/inquiries_listing.html', context)


def inquiry(request, inquiry_id):

    inquiry = get_object_or_404(MusicInquiry, pk=inquiry_id)
    suggestions = SongSuggestion.objects.filter(music_inquiry=inquiry_id)

    context = {
        'inquiry': inquiry,
        'suggestions': suggestions
    }

    return render(request, 'music_inquiries/inquiry.html', context)


@login_required
def suggestion(request, inquiry_id):

    music_inquiry = get_object_or_404(MusicInquiry, pk=inquiry_id)

    if request.method == 'POST':
        try:
            song_name = request.POST['song_name']
            song_artist = request.POST['song_artist']
            youtube_url = request.POST['youtube_url']
        except(KeyError):
            raise Http404(
                "Some of the requires parameters was not sent in the request."
            )

        suggestion = SongSuggestion.objects.create_suggestion(
            user=request.user,
            music_inquiry=music_inquiry,
            song_name=song_name,
            song_artist=song_artist,
            youtube_url=youtube_url,
        )

        suggestion.save()

        return inquiry(request, inquiry_id)


def inquiry_search(request):
    """Returns a JSON containing information about similar Inquiries to the one
    send in the 'q' property."""

    if request.method == 'GET':

        query = request.GET['q']
        results = SearchQuerySet().filter(content=query)
        results_objects = map(lambda result: result.object, results)

        results_dicts = []

        for result in results_objects:
            result_dict = {}

            result_dict['url'] = reverse(
                'music_inquiries:inquiry',
                kwargs={'inquiry_id': result.id}
            )
            result_dict['text'] = result.text

            results_dicts.append(result_dict)

        results_json = json.dumps(results_dicts)

        return HttpResponse(results_json, content_type='application/json')
