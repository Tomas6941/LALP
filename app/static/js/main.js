(function () {
  "use strict";

  // La clase "has-js" la agrega boot.js desde el <head>, antes del primer
  // pintado, para que los reveals no se pinten visibles y luego se oculten.

  var reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  /* --- Menú de navegación (móvil) ------------------------------------- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var menu = document.querySelector("[data-nav-menu]");
  var nav = document.querySelector("[data-nav]");

  if (toggle && menu) {
    var setMenu = function (open) {
      menu.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute(
        "aria-label",
        open ? "Cerrar menú de navegación" : "Abrir menú de navegación"
      );
    };

    // Estado inicial cerrado, y cerrado también al volver desde la caché de
    // ida/vuelta (bfcache), donde el DOM se restaura tal como estaba.
    setMenu(false);
    window.addEventListener("pageshow", function () {
      setMenu(false);
    });

    toggle.addEventListener("click", function () {
      setMenu(!menu.classList.contains("is-open"));
    });

    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        setMenu(false);
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });

    document.addEventListener("click", function (e) {
      if (!menu.classList.contains("is-open")) return;
      if (nav && !nav.contains(e.target)) setMenu(false);
    });
  }

  /* --- Borde de scroll de la barra ------------------------------------ */
  if (nav) {
    var setScrolled = function () {
      nav.classList.toggle("is-scrolled", window.scrollY > 4);
    };
    setScrolled();
    window.addEventListener("scroll", setScrolled, { passive: true });
  }

  /* --- Enlace activo según la sección visible (scrollspy) ------------- */
  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll(".nav__link[href^='#']")
  );
  var targets = navLinks
    .map(function (link) {
      return {
        link: link,
        section: document.querySelector(link.getAttribute("href")),
      };
    })
    .filter(function (t) {
      return t.section;
    });

  if (targets.length) {
    var frame = 0;
    var marcarActivo = function () {
      frame = 0;
      var limite = (nav ? nav.offsetHeight : 0) + 16;
      var activo = targets[0];
      for (var i = 0; i < targets.length; i++) {
        if (targets[i].section.getBoundingClientRect().top <= limite) {
          activo = targets[i];
        }
      }
      targets.forEach(function (t) {
        t.link.classList.toggle("is-active", t === activo);
      });
    };
    var onScroll = function () {
      if (!frame) frame = window.requestAnimationFrame(marcarActivo);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    marcarActivo();
  }

  /* --- Disclosures de propuestas -------------------------------------- */
  document.querySelectorAll("[data-card-toggle]").forEach(function (btn) {
    var card = btn.closest("[data-card]");
    if (!card) return;
    var detail = card.querySelector("[data-card-detail]");
    var label = btn.querySelector("[data-card-label]");

    btn.addEventListener("click", function () {
      var open = !card.classList.contains("is-open");
      card.classList.toggle("is-open", open);
      if (detail) detail.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
      if (label) label.textContent = open ? "Ocultar detalle" : "Ver detalle";
    });
  });

  /* --- Reveals al hacer scroll ---------------------------------------- */
  var reveals = document.querySelectorAll("[data-reveal]");

  if (!("IntersectionObserver" in window) || reduceMotion) {
    reveals.forEach(function (el) {
      el.classList.add("is-visible");
    });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.1 }
    );
    reveals.forEach(function (el) {
      observer.observe(el);
    });
  }
})();
