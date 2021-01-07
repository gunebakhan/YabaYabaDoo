$('#recipeCarousel').carousel({
  interval: 10000
})

$('.carousel .carousel-item').each(function () {
  var minPerSlide = 4;
  var next = $(this).next();
  if (!next.length) {
    next = $(this).siblings(':first');
  }
  next.children(':first-child').clone().appendTo($(this));

  for (var i = 0; i < minPerSlide; i++) {
    next = next.next();
    if (!next.length) {
      next = $(this).siblings(':first');
    }

    next.children(':first-child').clone().appendTo($(this));
  }
});



// Swiper Configuration

(function ($) {
  $(function () {

    var agSwiper = $('.swiper-container');

    if (agSwiper.length > 0) {

      var sliderView = 1;
      var ww = $(window).width();
      if (ww >= 1700) sliderView = 7;
      if (ww <= 1700) sliderView = 7;
      if (ww <= 1560) sliderView = 6;
      if (ww <= 1400) sliderView = 5;
      if (ww <= 1060) sliderView = 4;
      if (ww <= 800) sliderView = 3;
      if (ww <= 560) sliderView = 2;
      if (ww <= 400) sliderView = 1;

      var swiper = new Swiper('.swiper-container', {
        slidesPerView: sliderView,
        spaceBetween: 0,
        loop: true,
        preventClicks: false,
        loopedSlides: 16,
        speed: 700,
        autoplay: true,
        autoplayDisableOnInteraction: true,
        centeredSlides: true,
        grabCursor: true,
        preventClicksPropagation: false,

        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },
      });

      $(window).resize(function () {
        var ww = $(window).width();
        if (ww >= 1700) swiper.params.slidesPerView = 7;
        if (ww <= 1700) swiper.params.slidesPerView = 7;
        if (ww <= 1560) swiper.params.slidesPerView = 6;
        if (ww <= 1400) swiper.params.slidesPerView = 5;
        if (ww <= 1060) swiper.params.slidesPerView = 4;
        if (ww <= 800) swiper.params.slidesPerView = 3;
        if (ww <= 560) swiper.params.slidesPerView = 2;
        if (ww <= 400) swiper.params.slidesPerView = 1;
      });

      $(window).trigger('resize');

      var mySwiper = document.querySelector('.swiper-container').swiper;

      agSwiper.mouseenter(function () {
        mySwiper.autoplay.stop();
        console.log('slider stopped');
      });

      agSwiper.mouseleave(function () {
        mySwiper.autoplay.start();
        console.log('slider started again');
      });
    }


  });
})(jQuery);