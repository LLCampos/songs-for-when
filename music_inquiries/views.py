from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required


from models import MusicInquiry, SongSuggestion


def index(request):
    return render(request, 'music_inquiries/index.html')


def inquiries_listing(request):

    if request.method == 'POST':

        if request.user.is_authenticated():
            try:
                inquiry_text = request.POST['inquiry_text']
            except(KeyError):
                raise Http404("'inquiry' parameter was not sent in the request.")

            inquiry = MusicInquiry.objects.create_music_inquiry(
                user=request.user,
                text=inquiry_text
            )

            inquiry.save()

        else:
            return redirect('/accounts/login/?next=/')

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
            raise Http404("Some of the requires parameters was not sent in the request.")

        suggestion = SongSuggestion.objects.create_suggestion(
            user=request.user,
            music_inquiry=music_inquiry,
            song_name=song_name,
            song_artist=song_artist,
            youtube_url=youtube_url,
        )

        suggestion.save()

        return inquiry(request, inquiry_id)
