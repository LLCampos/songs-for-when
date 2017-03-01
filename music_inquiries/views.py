from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from models import MusicInquiry, SongSuggestion


def index(request):
    return render(request, 'music_inquiries/index.html')


def inquiries_listing(request):

    if request.method == 'POST':

        if request.user.is_authenticated():
            # TODO delete this, here just for testing purposes

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
