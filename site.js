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
