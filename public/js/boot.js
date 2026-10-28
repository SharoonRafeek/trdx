/* Runs first. Marks the page as script-enabled so reveal animations can start hidden,
   and removes that mark again if the main script never loads (content must never stay hidden). */
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  setTimeout(function () {
    if (!window.__siteReady) { root.classList.remove('js'); }
  }, 5000);
})();
