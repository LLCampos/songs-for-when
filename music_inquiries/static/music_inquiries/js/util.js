// General

const allTrim = function allTrim(string) {
  return string.replace(/\s+/g, ' ')
               .replace(/^\s+|\s+$/, '');
};

const pauseYoutubeVideos = function pauseYoutubeVideos() {
  const iframe = $('.item.active').find('.iframe-suggestion');
  const src = iframe.attr('src');
  $(iframe).attr('src', '').attr('src', src);
};

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

const csrftoken = Cookies.get('csrftoken');

$.ajaxSetup({
  beforeSend: (xhr, settings) => {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  },
});
