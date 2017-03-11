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

  // Index

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

  // Inquiry

  $('.suggestions-carousel-control').click(function() {
    pauseYoutubeVideos();
  });

});
