// General

const allTrim = function allTrim(string) {
  return string.replace(/\s+/g, ' ')
               .replace(/^\s+|\s+$/, '');
};

// http://stackoverflow.com/a/28735569/5082718
const validateYouTubeUrl = (url) => {
  if (url !== undefined || url !== '') {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    if (match && match[2].length === 11) {
      return true;
    }
  }
  return false;
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
