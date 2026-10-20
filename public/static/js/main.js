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

  /* --- Disclosures de propuestas --------------------------------------
     La grilla estira cada fila a la card más alta, así que al desplegar una
     propuesta se estiraban también sus compañeras de fila. Para que sólo se
     desplacen las filas de abajo: al abrir se congela la altura previa de las
     cerradas (la fila en su estado normal) y la abierta mide su contenido.
     Al volver a cerrar todo, se liberan las alturas. */
  var panelMs = reduceMotion ? 0 : 340; // duración del panel + margen
  var grillas = [];
  var alturasPorGrilla = new WeakMap(); // grilla -> number[] | null
  var cierresPorCard = new WeakMap(); // card -> timeout del cierre

  var cardsDe = function (grid) {
    return Array.prototype.slice.call(grid.querySelectorAll("[data-card]"));
  };

  // Abierta o cerrándose: las dos siguen creciendo o colapsando con el panel.
  var estaAnimandose = function (card) {
    return (
      card.classList.contains("is-open") ||
      card.classList.contains("is-closing")
    );
  };

  var congelarAlturas = function (grid) {
    var previas = alturasPorGrilla.get(grid);
    if (!previas) return;
    cardsDe(grid).forEach(function (card, i) {
      var alto = previas[i] + "px";
      card.style.minHeight = alto;
      card.style.height = estaAnimandose(card) ? "" : alto;
    });
  };

  var liberarAlturas = function (grid) {
    alturasPorGrilla.set(grid, null);
    cardsDe(grid).forEach(function (card) {
      card.style.height = "";
      card.style.minHeight = "";
      card.style.alignSelf = "";
    });
  };

  var aplicarAlturas = function (grid) {
    if (cardsDe(grid).some(estaAnimandose)) congelarAlturas(grid);
    else liberarAlturas(grid);
  };

  // Con un resize el texto cambia de línea y las alturas congeladas quedan
  // viejas: se remiden las cerradas en su estado natural y se re-congelan.
  var remedirGrilla = function (grid) {
    var previas = alturasPorGrilla.get(grid);
    if (!previas) return;
    var cards = cardsDe(grid);

    cards.forEach(function (card) {
      if (estaAnimandose(card)) return;
      card.style.height = "auto";
      card.style.minHeight = "0";
      card.style.alignSelf = "start";
    });

    // Una sola pasada de layout: posición -> alto natural mayor de esa fila.
    var tops = cards.map(function (card) {
      return card.offsetTop;
    });
    var porFila = {};
    cards.forEach(function (card, i) {
      if (estaAnimandose(card)) return;
      porFila[tops[i]] = Math.max(porFila[tops[i]] || 0, card.offsetHeight);
    });

    var nuevas = cards.map(function (card, i) {
      var alto = porFila[tops[i]];
      var activa = estaAnimandose(card);
      card.style.alignSelf = "";
      if (alto === undefined) {
        // Fila sin compañeras cerradas: sólo la abierta, que mide su contenido.
        card.style.height = activa ? "" : previas[i] + "px";
        card.style.minHeight = activa ? "" : previas[i] + "px";
        return previas[i];
      }
      card.style.height = activa ? "" : alto + "px";
      card.style.minHeight = alto + "px";
      return alto;
    });

    alturasPorGrilla.set(grid, nuevas);
  };

  document.querySelectorAll("[data-card-toggle]").forEach(function (btn) {
    var card = btn.closest("[data-card]");
    if (!card) return;
    var grid = card.closest(".cards");
    var detail = card.querySelector("[data-card-detail]");
    var label = btn.querySelector("[data-card-label]");

    if (grid && grillas.indexOf(grid) === -1) grillas.push(grid);

    btn.addEventListener("click", function () {
      var abierto = !card.classList.contains("is-open");

      // Se mide antes de abrir: es la fila en su estado normal, la altura
      // exacta que sus compañeras tienen que conservar.
      if (abierto && grid && !alturasPorGrilla.get(grid)) {
        alturasPorGrilla.set(
          grid,
          cardsDe(grid).map(function (c) {
            return c.offsetHeight;
          })
        );
      }

      var cierre = cierresPorCard.get(card);
      if (cierre) {
        clearTimeout(cierre);
        cierresPorCard.delete(card);
      }

      card.classList.toggle("is-open", abierto);
      card.classList.toggle("is-closing", !abierto);
      if (detail) detail.classList.toggle("is-open", abierto);
      btn.setAttribute("aria-expanded", String(abierto));
      if (label) label.textContent = abierto ? "Ocultar detalle" : "Ver detalle";

      if (!grid) return;

      if (!abierto) {
        // Sigue "is-closing" hasta que el panel termina de colapsar: si no,
        // sus compañeras se estirarían con la altura que se acaba de soltar.
        cierresPorCard.set(
          card,
          setTimeout(function () {
            cierresPorCard.delete(card);
            card.classList.remove("is-closing");
            aplicarAlturas(grid);
          }, panelMs)
        );
      }

      aplicarAlturas(grid);
    });
  });

  var remedicion = 0;
  window.addEventListener("resize", function () {
    clearTimeout(remedicion);
    remedicion = setTimeout(function () {
      grillas.forEach(remedirGrilla);
    }, 150);
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
