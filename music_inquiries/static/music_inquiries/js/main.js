pauseYoutubeVideos = function() {
  const iframe = $('.item.active').find('.iframe-suggestion');
  let src = iframe.attr('src');
  $(iframe).attr('src', '').attr('src', src);
};

// Index

numberCharsInInquiryInput = function() {
  return $('#inquiry-text-input').val().length;
};

updateCharsLeftOnInquirySubmitButton = function() {
  let charsLeft = 10 - numberCharsInInquiryInput();
  $('#inquiry-submit-form-button').attr('value',  charsLeft.toString() + ' characters left');
};


$(function() {

  // ########### Index ###########

  $('#inquiry-text-input').focusout(function() {
    $('#inquiry-submit-form-button').attr('value', 'Ask for Suggestions');
  });

  $(document).on('keyup focus','#inquiry-text-input',function(e) {
    if (numberCharsInInquiryInput() >= 10) {
      $('#inquiry-submit-form-button').attr('value', 'Ask for Suggestions')
                                      .prop('disabled', false);
    } else {
      updateCharsLeftOnInquirySubmitButton();
      $('#inquiry-submit-form-button').prop('disabled', true);
    }
  });

  // Avoid sending of repeated inquiries
  $('#inquiry-form').submit(function(event) {
    thisForm = this;
    $.ajax({
      url: 'http://localhost:8000/inquiry/',
      type: 'HEAD',
      data: {'q': $('#inquiry-text-input').val()},
    })
    .done(function() {
      // If inquiry already exists.
      alert('Inquiry already exists! :)');
    })
    .fail(function() {
      // If inquiry does not exists.
      thisForm.submit();
    });

    event.preventDefault();

  });

  // Inquiry

  $('.suggestions-carousel-control').click(function() {
    pauseYoutubeVideos();
  });

});
