(function () {
  "use strict";

  const toggle = document.querySelector("[data-nav-toggle]");
  const menu = document.querySelector("[data-nav-menu]");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    menu.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      })
    );
  }

  document.querySelectorAll("[data-card-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const card = btn.closest("[data-card]");
      const detail = card.querySelector("[data-card-detail]");
      const expanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!expanded));
      detail.classList.toggle("is-hidden");
    });
  });
})();