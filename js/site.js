/* JUDAS · comportamiento mínimo: menú en móvil y marca de página activa */
(function () {
  "use strict";

  var nav = document.querySelector("[data-nav]");
  var toggle = document.querySelector("[data-nav-toggle]");

  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.getAttribute("data-open") === "true";
      nav.setAttribute("data-open", String(!open));
      toggle.setAttribute("aria-expanded", String(!open));
    });
  }

  // Marca el enlace de la página actual sin duplicar clases en cada HTML.
  var here = location.pathname.split("/").pop() || "index.html";
  var link = nav && nav.querySelector('a[href="' + here + '"]');
  if (link) link.setAttribute("aria-current", "page");

  document.querySelectorAll("[data-hero-bg]").forEach(initHeroBg);
})();

function initHeroBg(root) {
  var videos = Array.prototype.slice.call(root.querySelectorAll("video"));
  if (!videos.length) return;

  var interval = Number(root.getAttribute("data-interval")) || 5000;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var index = Math.max(0, videos.findIndex(function (video) {
    return video.classList.contains("is-active");
  }));
  var timer = null;
  var visible = true;

  function show(nextIndex) {
    index = (nextIndex + videos.length) % videos.length;
    videos.forEach(function (video, i) {
      var on = i === index;
      video.classList.toggle("is-active", on);
      video.muted = true;
      video.defaultMuted = true;
      if (on) {
        try { video.currentTime = 0; } catch (err) {}
        if (visible && !reduceMotion) {
          var play = video.play();
          if (play && play.catch) play.catch(function () {});
        } else {
          video.pause();
        }
      } else {
        video.pause();
      }
    });
    restart();
  }

  function restart() {
    if (timer) window.clearInterval(timer);
    timer = null;
    if (reduceMotion || !visible || videos.length < 2) return;
    timer = window.setInterval(function () {
      show(index + 1);
    }, interval);
  }

  document.addEventListener("visibilitychange", function () {
    visible = document.visibilityState === "visible";
    if (visible) show(index);
    else {
      if (timer) window.clearInterval(timer);
      timer = null;
      videos.forEach(function (video) { video.pause(); });
    }
  });

  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      var nowVisible = entries[0].isIntersecting && document.visibilityState === "visible";
      if (nowVisible === visible) return;
      visible = nowVisible;
      if (visible) show(index);
      else {
        if (timer) window.clearInterval(timer);
        timer = null;
        videos.forEach(function (video) { video.pause(); });
      }
    }, { threshold: 0.2 });
    observer.observe(root);
  }

  show(index);
}
