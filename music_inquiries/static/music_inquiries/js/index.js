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
    const inquiryResourceUrl = $('#inquiry-form').attr('action');
    $.ajax({
      url: inquiryResourceUrl,
      type: 'HEAD',
      data: { q: inquiry.text() },
    })
    .done(() => {
      // If inquiry already exists.
      $('#repeated-inquiry-modal').modal('show');
    })
    .fail(() => {
      // If inquiry does not exists.
      $.post({
        url: inquiryResourceUrl,
        data: { inquiry_text: inquiry.text() },
        success: () => {
          inquiry.clean();
          $('#success-inquiry-modal').modal('show');
        },
      });
    });

    event.preventDefault();
  });
});
