// SMOOTH SCROLLING

$(function() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 720);
        return false;
      }
    }
  });
});

// END SMOOTH SCROLLING

// COPYRIGHT AUTO UPDATE
// Get date
var today = new Date();
var year = today.getFullYear();
console.log(year);

// Set or display year
$('.year').text(year);


// TimelineMax Animation

var tl1 = new TimelineMax({ delay: .7 });

tl1.from('#divide-anim', .3, {opacity:0});
tl1.from('#divide-anim', .7, {y:60}), '=.3';
tl1.from('#divide-anim-two', .7, {y:-30,opacity:0}, '-=.7');
tl1.from('#mobile-hero', .5, {opacity:0}, '=.3');
tl1.from('#logo-anim', .8, {opacity:0,y:17.5, ease: Power4.easeOut});

// End Animation
