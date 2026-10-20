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
     Grilla rígida de 3 columnas. Al abrir una propuesta:
     - las tarjetas de los costados (misma fila) se quedan en su lugar;
     - las filas de abajo bajan; las de arriba no se mueven.

     Cómo: cada tarjeta sale del flujo (position: absolute en CSS) y main.js
     le fija --x/--y según su columna y el borde inferior de la fila previa.
     El CSS compone `transform: translate(var(--x), var(--y))` con transición,
     así que reposicionar es sólo animar transform: sin reflow y sin que las
     filas del grid se estiren entre sí.

     El ancho, que antes daba el grid, lo fija también el JS (y se recalcula
     en `resize`). */
  var grillas = [];

  var cardsDe = function (grid) {
    return Array.prototype.slice.call(grid.querySelectorAll("[data-card]"));
  };

  var aNumero = function (v) {
    var n = parseFloat(v);
    return isNaN(n) ? 0 : n;
  };

  var columnasDe = function (grid) {
    return Math.max(1, parseInt(grid.getAttribute("data-cols"), 10) || 1);
  };

  // Alto que ocupa una card en la grilla. No sirve `offsetHeight` a secas:
  // abrir y cerrar animan grid-template-rows, y en el frame del click el
  // layout todavía es el viejo. En cambio el bloque de arriba (.card__main),
  // el padding y el gap son constantes; sólo el panel varía, y su contenido
  // se mide con scrollHeight (estable en cualquier punto de la animación):
  //
  //   alto = main + padding + gap + (abierto ? contenido del panel : 0)
  var altoDe = function (card) {
    var main = card.querySelector(".card__main");
    var inner = card.querySelector("[data-card-detail] .disclosure__inner");
    if (!main || !inner) return card.offsetHeight;

    var cs = getComputedStyle(card);
    var padding = aNumero(cs.paddingTop) + aNumero(cs.paddingBottom);
    var gap = aNumero(cs.rowGap);
    var abierto = card.classList.contains("is-open");

    return main.offsetHeight + padding + gap + (abierto ? inner.scrollHeight : 0);
  };

  // Recoloca toda la grilla en filas rígidas: cada fila la marca la card más
  // alta de esa fila (x por columna, y por el borde inferior de la anterior).
  // `sinAnimacion` se usa al medir de nuevo (carga, fuentes, resize): ahí el
  // salto debe ser instantáneo, no un deslizamiento.
  var colocar = function (grid, sinAnimacion) {
    var cols = columnasDe(grid);
    var borde = grid.getBoundingClientRect().width;
    var gap = aNumero(getComputedStyle(grid).gap);
    var ancho = (borde - gap * (cols - 1)) / cols;
    var cards = cardsDe(grid);
    var alturas = [];
    var y = 0;
    var i;

    if (sinAnimacion) grid.classList.add("cards--reposicionando");

    // 1) Fijar el ancho antes de medir: cambia el alto del texto.
    for (i = 0; i < cards.length; i++) cards[i].style.width = ancho + "px";

    // 2) Medir el alto real de cada card (estado lógico, no animado).
    for (i = 0; i < cards.length; i++) alturas.push(altoDe(cards[i]));

    // 3) Colocar en filas rígidas y fijar el alto de la grilla.
    for (i = 0; i < cards.length; i++) {
      var fila = Math.floor(i / cols);
      var col = i % cols;

      if (col === 0 && fila > 0) {
        // Borde superior de esta fila: alto máximo de la fila anterior.
        var previo = 0;
        for (var k = (fila - 1) * cols; k < fila * cols && k < cards.length; k++) {
          previo = Math.max(previo, alturas[k]);
        }
        y += previo + gap;
      }

      cards[i].style.setProperty("--x", col * (ancho + gap) + "px");
      cards[i].style.setProperty("--y", y + "px");
    }

    var ultimaFila = Math.floor((cards.length - 1) / cols);
    var ultimoAlto = 0;
    for (i = ultimaFila * cols; i < cards.length; i++) {
      ultimoAlto = Math.max(ultimoAlto, alturas[i]);
    }
    grid.style.height = y + ultimoAlto + "px";

    if (sinAnimacion) {
      void grid.offsetWidth; // fuerza reflow para asentar la posición
      grid.classList.remove("cards--reposicionando");
    }
  };

  var rehacer = function (grid) {
    if (grid) colocar(grid);
  };

  var reposicionar = function (grid) {
    if (grid) colocar(grid, true);
  };

  document.querySelectorAll("[data-card-toggle]").forEach(function (btn) {
    var card = btn.closest("[data-card]");
    if (!card) return;
    var grid = card.closest("[data-card-grid]") || card.closest(".cards");
    var detail = card.querySelector("[data-card-detail]");
    var label = btn.querySelector("[data-card-label]");

    if (grid && grillas.indexOf(grid) === -1) grillas.push(grid);

    btn.addEventListener("click", function () {
      var abierto = !card.classList.contains("is-open");
      card.classList.toggle("is-open", abierto);
      if (detail) detail.classList.toggle("is-open", abierto);
      btn.setAttribute("aria-expanded", String(abierto));
      if (label) label.textContent = abierto ? "Ocultar detalle" : "Ver detalle";
      rehacer(grid);
    });
  });

  // El ancho y las alturas dependen del viewport y de las fuentes: se
  // recoloca al terminar de cargar, cuando las fuentes están listas y al
  // redimensionar.
  var recolocarTodas = function () {
    window.requestAnimationFrame(function () {
      grillas.forEach(reposicionar);
    });
  };

  window.addEventListener("load", recolocarTodas);

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(recolocarTodas);
  }

  var remide = 0;
  window.addEventListener("resize", function () {
    clearTimeout(remide);
    remide = setTimeout(recolocarTodas, 120);
  });

  grillas.forEach(reposicionar);

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
