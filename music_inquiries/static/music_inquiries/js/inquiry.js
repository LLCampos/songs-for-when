// Returns true if both input values (for song artist and song name) are not empty
const suggestionArtistAndSongInputFilled = () => {
  const artistValue = $('#suggestion-input-artist').val().trim();
  const songValue = $('#suggestion-input-song').val().trim();

  if (artistValue !== '' && songValue !== '') {
    return true;
  }
  return false;
};


$(() => {
  $('.suggestions-carousel-control').click(() => {
    pauseYoutubeVideos();
  });

  $('#suggestion-input-artist, #suggestion-input-song').keyup(() => {
    const searchButton = $('#suggestion-input-search');
    if (searchButton.prop('disabled') && suggestionArtistAndSongInputFilled()) {
      searchButton.prop('disabled', false);
    } else if (!searchButton.prop('disabled') && !suggestionArtistAndSongInputFilled()) {
      searchButton.prop('disabled', true);
    }
  });

  $('#suggestion-input-search').click(() => {
    const artistValue = $('#suggestion-input-artist').val().trim();
    const songValue = $('#suggestion-input-song').val().trim();

    $.ajax('/iapi/song', {
      type: 'HEAD',
      data: {
        artist_name: artistValue,
        song_name: songValue,
      },
      success: () => {
        $('#suggestion-form-submit').prop('disabled', false);
      },
      error: () => {
        console.log('not exist');
      },
    });
  });
});
