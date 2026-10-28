/* Traversion Dynamics: navigation, scroll reveal and hero parallax. No dependencies. */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var onFrameCallbacks = [];
  var ticking = false;

  function frame() {
    var y = window.pageYOffset || 0;
    for (var i = 0; i < onFrameCallbacks.length; i++) { onFrameCallbacks[i](y); }
    ticking = false;
  }

  function requestFrame() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(frame); }
  }

  /* footer year */
  Array.prototype.forEach.call(doc.querySelectorAll('[data-year]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  /* ---------- navigation ---------- */
  var nav = doc.getElementById('nav');
  if (nav) {
    var toggle = nav.querySelector('.nav__toggle');
    var panel = doc.getElementById('navPanel');
    var label = toggle ? toggle.querySelector('.nav__toggle-label') : null;
    var mq = window.matchMedia('(max-width: 900px)');
    var open = false;
    var lastY = window.pageYOffset || 0;
    var acc = 0;

    var setOpen = function (next, returnFocus) {
      open = next;
      root.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      if (label) { label.textContent = open ? 'Close' : 'Menu'; }
      if (open) {
        nav.classList.remove('is-hidden');
        var first = panel.querySelector('a');
        if (first) { first.focus({ preventScroll: true }); }
      } else if (returnFocus) {
        toggle.focus();
      }
    };

    if (toggle && panel) {
      toggle.addEventListener('click', function () { setOpen(!open); });

      panel.addEventListener('click', function (e) {
        if (e.target.closest && e.target.closest('a')) { setOpen(false); }
      });

      doc.addEventListener('keydown', function (e) {
        if (!open) { return; }
        if (e.key === 'Escape') { setOpen(false, true); return; }
        if (e.key === 'Tab') {
          var items = [toggle].concat(Array.prototype.slice.call(panel.querySelectorAll('a, button')));
          var first = items[0];
          var last = items[items.length - 1];
          if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
          else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
        }
      });

      var onBreakpoint = function (e) { if (!e.matches && open) { setOpen(false); } };
      if (mq.addEventListener) { mq.addEventListener('change', onBreakpoint); }
      else if (mq.addListener) { mq.addListener(onBreakpoint); }
    }

    /* solid background after the first scroll; hide on scroll down, show on scroll up */
    onFrameCallbacks.push(function (y) {
      nav.classList.toggle('is-scrolled', y > 24);
      if (open) { lastY = y; return; }
      var dy = y - lastY;
      if (dy * acc < 0) { acc = 0; }
      acc += dy;
      if (acc > 70 && y > 220) { nav.classList.add('is-hidden'); }
      else if (acc < -24 || y <= 24) { nav.classList.remove('is-hidden'); }
      lastY = y;
    });

    nav.addEventListener('focusin', function () { nav.classList.remove('is-hidden'); });
  }

  /* ---------- hero parallax ---------- */
  var heroMedia = doc.querySelector('.hero__media');
  if (heroMedia && !reduce) {
    onFrameCallbacks.push(function (y) {
      if (y > window.innerHeight * 1.2) { return; }
      heroMedia.style.setProperty('--py', (y * 0.16).toFixed(1) + 'px');
    });
  }

  /* ---------- scroll reveal ---------- */
  var revealEls = Array.prototype.slice.call(doc.querySelectorAll('[data-reveal]'));
  if (revealEls.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      revealEls.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
      revealEls.forEach(function (el) { io.observe(el); });
    }
  }

  window.addEventListener('scroll', requestFrame, { passive: true });
  window.addEventListener('resize', requestFrame);
  requestFrame();

  window.__siteReady = true;
})();
