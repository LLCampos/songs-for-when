from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from models import *

from haystack.query import SearchQuerySet

import json


def index(request):
    return render(request, 'music_inquiries/index.html')


def inquiries_listing(request):
    latest_inquiries = MusicInquiry.objects.order_by('-created_at')[:15]
    context = {'inquiries': latest_inquiries}
    return render(request, 'music_inquiries/inquiries_listing.html', context)


def inquiry(request, inquiry_id):
    """Endpoint at /inquiry/{inquiry_id}/

    GET:
        Returns HTML page with info on the Inquiry.

    """

    inquiry = get_object_or_404(MusicInquiry, pk=inquiry_id)
    suggestions = SongSuggestion.objects.filter(music_inquiry=inquiry_id)

    context = {
        'inquiry': inquiry,
        'suggestions': suggestions
    }

    return render(request, 'music_inquiries/inquiry.html', context)


@login_required
def suggestion(request, inquiry_id):
    """Endpoint at /inquiry/{inquiry_id}/suggestion

    POST:
        Submits a new Suggestion to the Inquiry (Auth required);

        Parameters:
            'song_name'
            'song_artist'
            'youtube_url'
    """

    music_inquiry = get_object_or_404(MusicInquiry, pk=inquiry_id)

    if request.method == 'POST':
        try:
            song_name = request.POST['song_name']
            artist_name = request.POST['artist_name']
            youtube_url = request.POST.get('youtube_url')
        except(KeyError):
            raise Http404(
                "Some of the required parameters was not sent in the request."
            )

        try:
            SongSuggestion.objects.create_suggestion(
                user=request.user,
                music_inquiry=music_inquiry,
                song_name=song_name,
                artist_name=artist_name,
                youtube_url=youtube_url,
            )
        except Exception(IntegrityError, ValidationError):
            return HttpResponse(
                'Error when adding suggestion',
                status=400
            )

        return HttpResponse(status=200)


def inquiry_search(request):

    """Endpoint at /search/

    GET:
        Returns a JSON containing information about similar Inquiries to the one
        send in the 'q' property.

        Parameters:
            'q'
    """

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
            result_dict['number_of_suggestions'] = result.get_number_active_suggestions()

            results_dicts.append(result_dict)

        results_json = json.dumps(results_dicts)

        return HttpResponse(results_json, content_type='application/json')


def song(request):

    """Endpoint at /song/

    HEAD:
        Returns status code 200 if song already exists, 404 otherwise.

        Parameters:
            song_name
            artist_name
    """

    if request.method == 'HEAD':
        """Method used to check if a certain inquiry text was already
        submitted"""

        try:
            artist_name = request.GET['artist_name']
            song_name = request.GET['song_name']
        except KeyError:
            raise Http404(
                "Some of the required parameters was not sent in the request."
            )

        song_exists = Song.objects.does_song_exist(
            artist_name=artist_name,
            song_name=song_name,
        )

        if song_exists:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)


@login_required
def inquiry_report(request, inquiry_id):

    """Endpoint at /inquiry/{inquiry_id}/report/

    POST:
        Reports something wrong with an Inquiry

        Parameters:
            category
            comment
    """

    try:
        category = request.POST['category']
        comment = request.POST.get('comment')
    except KeyError:
        raise Http404(
            "Some of the required parameters was not sent in the request."
        )

    try:
        InquiryProblemReport.objects.create_inquiry_report(
            user=request.user,
            inquiry=MusicInquiry.objects.get(id=inquiry_id),
            category=category,
            comment=comment,
        )
    except (IntegrityError, ValidationError):
        return HttpResponse(
            'Error when submitting report',
            status=400
        )

    return HttpResponse(status=200)


def inquiry_resource(request):

    """
    Endpoint at iapi/inquiry/

    POST:
        Creates a new Inquiry. If everything ok, returns HTML page with listing
        of the inquiries. Authentication is required.

        Parameters:
            inquiry_text

    HEAD:
        Returns status code 200 if text sent in the 'q' (for query) parameter
        was already submitted in some Inquiry.

        Parameters:
            q
    """

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
                raise HttpResponse(
                    "'inquiry_text' parameter was not sent in the request.",
                    status=400
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

            return HttpResponse(status=201)

        else:
            return HttpResponse('Unauthorized', status=401)

    else:
        return HttpResponse('Unauthorized', status=405)
