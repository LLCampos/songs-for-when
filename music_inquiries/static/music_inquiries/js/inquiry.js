// Returns true if both input values (for song artist and song name) are not empty
const suggestionArtistAndSongInputFilled = () => {
  const artistValue = $('#suggestion-input-artist').val().trim();
  const songValue = $('#suggestion-input-song').val().trim();

  if (artistValue !== '' && songValue !== '') {
    return true;
  }
  return false;
};

const getCurrentInquiryID = () => {
  const currentUrl = window.location.href;
  const splittedUrl = currentUrl.split('/');

  const lastElement = splittedUrl[splittedUrl.length - 1];
  const secondToLastElement = splittedUrl[splittedUrl.length - 2];
  if (lastElement !== '') {
    return lastElement;
  }
  return secondToLastElement;
};


$(() => {
  $('.suggestions-carousel-control').click(() => {
    pauseYoutubeVideos();
  });

  $('#suggestion-input-artist, #suggestion-input-song').keyup(() => {
    const submittButton = $('#suggestion-form-submit');
    if (submittButton.prop('disabled') && suggestionArtistAndSongInputFilled()) {
      submittButton.prop('disabled', false);
    } else if (!submittButton.prop('disabled') && !suggestionArtistAndSongInputFilled()) {
      submittButton.prop('disabled', true);
    }
  });

  $('#suggestion-form-submit').click((event) => {
    event.preventDefault();
    const artistValue = $('#suggestion-input-artist').val().trim();
    const songValue = $('#suggestion-input-song').val().trim();
    const currentInquiryID = getCurrentInquiryID();

    const data = {
      artist_name: artistValue,
      song_name: songValue,
    };

    $.ajax('/iapi/song', {
      type: 'HEAD',
      data,
      success: () => {
        $.post(`/iapi/inquiry/${currentInquiryID}/suggestion/`, data, () => {
          location.reload();
        });
      },
      error: () => {
        $('#youtube-url-form-modal').modal('show');
      },
    });
  });

  $('#suggestion-input-youtube-url').keyup(() => {
    const url = $('#suggestion-input-youtube-url').val().trim();
    if (validateYouTubeUrl(url)) {
      $('#youtube-url-not-valid-message').addClass('hidden');
      $('#youtube_url-form-submit').prop('disabled', false);
    } else {
      $('#youtube-url-not-valid-message').removeClass('hidden');
      $('#youtube_url-form-submit').prop('disabled', true);
    }
  });

  $('#youtube_url-form-submit').click((event) => {
    const artistValue = $('#suggestion-input-artist').val().trim();
    const songValue = $('#suggestion-input-song').val().trim();
    const youtubeUrl = $('#suggestion-input-youtube-url').val().trim();
    const currentInquiryID = getCurrentInquiryID();

    const data = {
      artist_name: artistValue,
      song_name: songValue,
      youtube_url: youtubeUrl,
    };

    $.post(`/iapi/inquiry/${currentInquiryID}/suggestion/`, data, () => {
      location.reload();
    });
    event.preventDefault();
  });
});
