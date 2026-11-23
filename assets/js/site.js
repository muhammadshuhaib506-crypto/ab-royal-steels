/* AB Royal Steels — site behaviour: navigation, hero slider, reveal, filters, forms. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  /* ===== FORM ENDPOINT =====
     Paste a form backend URL here (e.g. Formspree, Getform, Basin, or your own server) to receive enquiries.
     Leave empty to keep forms in preview mode. */
  var FORM_ENDPOINT = '';

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // Header shadow + back-to-top
  var header = $('.site-header'), toTop = $('.to-top');
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (toTop) toTop.classList.toggle('show', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  // Mobile nav
  var burger = $('.burger');
  if (burger) burger.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    var nav = $('.nav'); if (nav && header) nav.style.top = open ? header.getBoundingClientRect().bottom + 'px' : '';
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  $$('.has-menu > .nav-link').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (window.matchMedia('(max-width: 1180px)').matches) {
        e.preventDefault();
        var li = btn.parentElement, open = li.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      }
    });
  });

  // Hero slider
  var hero = $('.hero');
  if (hero) {
    var slides = $$('.slide', hero), dots = $$('.dot', hero), idx = 0, timer, DUR = 7000;
    var counter = $('.counter b', hero);
    hero.style.setProperty('--dur', DUR + 'ms');
    function go(n) {
      slides[idx].classList.remove('is-active'); dots[idx] && dots[idx].classList.remove('is-active');
      idx = (n + slides.length) % slides.length;
      slides[idx].classList.add('is-active');
      if (dots[idx]) { var d = dots[idx]; d.classList.remove('is-active'); void d.offsetWidth; d.classList.add('is-active'); }
      if (counter) counter.textContent = ('0' + (idx + 1)).slice(-2);
      slides.forEach(function (s, i) { s.setAttribute('aria-hidden', i === idx ? 'false' : 'true'); });
      if (window.ABRS_ART) $$('[data-art]', slides[idx]).forEach(window.ABRS_ART.paint);
      restart();
    }
    function restart() { clearTimeout(timer); if (!hero.classList.contains('paused')) timer = setTimeout(function () { go(idx + 1); }, DUR); }
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });
    var prev = $('.arrow.prev', hero), next = $('.arrow.next', hero);
    prev && prev.addEventListener('click', function () { go(idx - 1); });
    next && next.addEventListener('click', function () { go(idx + 1); });
    hero.addEventListener('mouseenter', function () { hero.classList.add('paused'); clearTimeout(timer); });
    hero.addEventListener('mouseleave', function () { hero.classList.remove('paused'); restart(); });
    hero.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') go(idx + 1); if (e.key === 'ArrowLeft') go(idx - 1); });
    var sx = null;
    hero.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) { if (sx == null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) go(idx + (dx < 0 ? 1 : -1)); sx = null; });
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) DUR = 12000;
    restart();
  }

  // Reveal on scroll: only elements below the first screen start hidden
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.remove('pre'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight * 0.95) { el.classList.add('pre'); io.observe(el); }
    });
  }

  // Product category nav highlight
  var catLinks = $$('.cat-nav a');
  if (catLinks.length && 'IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) catLinks.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    $$('.cat-block').forEach(function (b) { co.observe(b); });
  }

  // Project filters
  var filters = $$('.filter');
  filters.forEach(function (f) {
    f.addEventListener('click', function () {
      var cat = f.getAttribute('data-filter');
      filters.forEach(function (x) { x.classList.toggle('is-active', x === f); x.setAttribute('aria-pressed', x === f ? 'true' : 'false'); });
      $$('.proj').forEach(function (p) { p.hidden = !(cat === 'all' || p.getAttribute('data-cat') === cat); });
      if (window.ABRS_ART) window.ABRS_ART.paintAll();
    });
  });

  // Quote form: add / remove product rows
  var addRow = $('#add-item');
  if (addRow) {
    var list = $('#items'), tpl = $('#item-template');
    var n = 1;
    addRow.addEventListener('click', function () {
      n++;
      var html = tpl.innerHTML.replace(/__N__/g, n);
      var div = document.createElement('div'); div.innerHTML = html.trim();
      list.appendChild(div.firstChild);
    });
    list.addEventListener('click', function (e) {
      var b = e.target.closest('.rm'); if (!b) return;
      if ($$('.item-row', list).length > 1) b.closest('.item-row').remove();
    });
  }

  // Prefill product from query (?product=...) on contact/quote pages
  try {
    var params = new URLSearchParams(location.search), prod = params.get('product');
    if (prod) { var pf = $('[name="product"], [name="item_product_1"]'); if (pf) pf.value = prod; }
  } catch (e) {}

  // Forms
  $$('form[data-enquiry]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      $$('[required]', form).forEach(function (input) {
        var field = input.closest('.field'), valid = input.value.trim() !== '' && (input.type !== 'email' || /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(input.value.trim()));
        if (field) field.classList.toggle('invalid', !valid);
        if (!valid) ok = false;
      });
      var status = $('.form-status', form);
      if (!ok) { var first = $('.invalid input, .invalid select, .invalid textarea', form); first && first.focus(); return; }
      function done(title, msg, good) { status.innerHTML = '<b>' + title + '</b>' + msg; status.className = 'form-status show' + (good ? ' ok' : ''); status.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
      if (!FORM_ENDPOINT) {
        done('Thank you', 'Your enquiry details are complete. This form is in preview mode: connect a form endpoint in assets/js/site.js so enquiries reach the AB Royal Steels team.', true);
        return;
      }
      var btn = $('button[type="submit"]', form); btn && (btn.disabled = true);
      fetch(FORM_ENDPOINT, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error(); form.reset(); done('Thank you', 'Your enquiry has been sent. Our team will get back to you shortly.', true); })
        .catch(function () { done('Not sent', 'Something went wrong while sending. Please try again, or contact us by phone or email.', false); })
        .then(function () { btn && (btn.disabled = false); });
    });
    $$('input, select, textarea', form).forEach(function (i) { i.addEventListener('input', function () { var f = i.closest('.field'); f && f.classList.remove('invalid'); }); });
  });

  var y = $('#year'); if (y) y.textContent = new Date().getFullYear();
})();
