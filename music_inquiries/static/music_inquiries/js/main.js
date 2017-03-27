// General

const allTrim = function allTrim(string) {
  return string.replace(/\s+/g, ' ')
               .replace(/^\s+|\s+$/, '');
};

// Suggestion

const pauseYoutubeVideos = function pauseYoutubeVideos() {
  const iframe = $('.item.active').find('.iframe-suggestion');
  const src = iframe.attr('src');
  $(iframe).attr('src', '').attr('src', src);
};

// Index

const inquiry = {
  text: function getText() {
    return allTrim($('#inquiry-text-input').val());
  },
  clean: function cleanInput() {
    $('#inquiry-text-input').val('');
  },
};

const updateCharsLeftOnInquirySubmitButton = function updateCharsLeftOnInquirySubmitButton() {
  const charsLeft = 10 - inquiry.text().length;
  $('#inquiry-submit-form-button').attr('value', `${charsLeft.toString()} characters left`);
};


$(() => {
  // ########### Index ###########
  $('#inquiry-text-input').focusout(() => {
    if (inquiry.text().length === 0) {
      inquiry.clean();
    }
    $('#inquiry-submit-form-button').attr('value', 'Ask for Suggestions');
  });

  // Implement restriction on min length
  $(document).on('keyup focus', '#inquiry-text-input', () => {
    if (inquiry.text().length >= 10) {
      $('#inquiry-submit-form-button').attr('value', 'Ask for Suggestions')
                                      .prop('disabled', false);
    } else {
      updateCharsLeftOnInquirySubmitButton();
      $('#inquiry-submit-form-button').prop('disabled', true);
    }
  });

  // Avoid sending of repeated inquiries
  $('#inquiry-form').submit((event) => {
    const thisForm = this;
    $.ajax({
      url: 'http://localhost:8000/inquiry/',
      type: 'HEAD',
      data: { q: inquiry.text() },
    })
    .done(() => {
      // If inquiry already exists.
      alert('Inquiry already exists! :)');
    })
    .fail(() => {
      // If inquiry does not exists.
      thisForm.submit();
    });

    event.preventDefault();
  });
  // ########## Inquiry Listing ###########
  $('#search-inquiry-input').keyup(() => {
    console.log('test');
  });

  // ########### Inquiry ###########

  $('.suggestions-carousel-control').click(() => {
    pauseYoutubeVideos();
  });
});
