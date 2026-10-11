// Stratum 137 — shared page behaviour: mobile nav + scroll reveal.
(function () {
  var root = document.documentElement;
  root.classList.add('js');

  var btn = document.querySelector('.nav-toggle');
  var header = document.querySelector('.site-header');
  if (btn && header) {
    btn.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    document.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('nav-open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Arizona hero slideshow: crossfade every 6s, pause when hidden, still under reduced motion.
  var show = document.querySelector('.az-show');
  if (show) {
    var slides = show.querySelectorAll('.az-slide');
    var dots = show.querySelectorAll('.az-dots i');
    var cur = 0, timer = null;
    var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var go = function (n) {
      slides[cur].classList.remove('is-on');
      slides[cur].setAttribute('aria-hidden', 'true');
      if (dots[cur]) dots[cur].classList.remove('on');
      cur = n % slides.length;
      slides[cur].classList.add('is-on');
      slides[cur].removeAttribute('aria-hidden');
      if (dots[cur]) dots[cur].classList.add('on');
    };
    var start = function () { if (!timer) timer = setInterval(function () { go(cur + 1); }, 6000); };
    var stop = function () { clearInterval(timer); timer = null; };
    if (dots[0]) dots[0].classList.add('on');
    if (!still && slides.length > 1) {
      start();
      document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    }
  }

  var targets = document.querySelectorAll('[data-reveal], [data-anim]');
  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  targets.forEach(function (el) { io.observe(el); });
})();
