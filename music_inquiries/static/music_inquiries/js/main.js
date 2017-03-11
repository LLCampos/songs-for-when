// General

String.prototype.allTrim = String.prototype.allTrim ||
     function(){
        return this.replace(/\s+/g,' ')
                   .replace(/^\s+|\s+$/,'');
     };


// Suggestion

pauseYoutubeVideos = function() {
  const iframe = $('.item.active').find('.iframe-suggestion');
  let src = iframe.attr('src');
  $(iframe).attr('src', '').attr('src', src);
};

// Index

let inquiry = {
  text: function() {
    return $('#inquiry-text-input').val().allTrim();
  },
  clean: function() {
    $('#inquiry-text-input').val('');
  }
};

updateCharsLeftOnInquirySubmitButton = function() {
  let charsLeft = 10 - inquiry.text().length;
  $('#inquiry-submit-form-button').attr('value',  charsLeft.toString() + ' characters left');
};


$(function() {

  // ########### Index ###########


  $('#inquiry-text-input').focusout(function() {
    if (inquiry.text().length === 0) {
      inquiry.clean();
    }
    $('#inquiry-submit-form-button').attr('value', 'Ask for Suggestions');
  });

  // Implement restriction on min length
  $(document).on('keyup focus','#inquiry-text-input',function(e) {
    if (inquiry.text().length >= 10) {
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
      data: {'q': inquiry.text()},
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
