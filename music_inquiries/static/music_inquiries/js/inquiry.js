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

    let data = {
      artist_name: artistValue,
      song_name: songValue,
    };

    $.ajax('/iapi/song', {
      type: 'HEAD',
      data,
      success: () => {
        $.post(`/iapi/inquiry/${currentInquiryID}/suggestion/`, data, () => {
          console.log('ok');
        });
      },
      error: () => {
        console.log('not exist');
      },
    });
  });
});
