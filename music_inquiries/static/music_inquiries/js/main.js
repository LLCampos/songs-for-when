pauseYoutubeVideos = function() {
  const iframe = $('.item.active').find('.iframe-suggestion');
  let src = iframe.attr('src');
  $(iframe).attr('src', '').attr('src', src);
};


$(function() {

  $('.suggestions-carousel-control').click(function() {
    pauseYoutubeVideos();
  });

});
