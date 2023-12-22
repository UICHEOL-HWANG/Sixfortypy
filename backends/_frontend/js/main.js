
$(document).ready(function(){
  $('.post-wrapper').slick({
      slidesToShow: 5,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 2000,
      nextArrow: $('.next'),
      prevArrow: $('.prev'),
  });

  // 이전 버튼 클릭 시 이벤트
  $('.prev').click(function(){
      $('.post-wrapper').slick('slickPrev');
  });

  // 다음 버튼 클릭 시 이벤트
  $('.next').click(function(){
      $('.post-wrapper').slick('slickNext');
  });
});
  