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
