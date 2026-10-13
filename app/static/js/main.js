(function () {
  "use strict";

  const toggle = document.querySelector("[data-nav-toggle]");
  const menu = document.querySelector("[data-nav-menu]");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const open = menu.classList.toggle("hidden") === false;
      toggle.setAttribute("aria-expanded", String(open));
    });
    menu.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        menu.classList.add("hidden");
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
      detail.classList.toggle("hidden");
    });
  });

  const form = document.querySelector("[data-contact-form]");
  if (form) {
    form.addEventListener("submit", (e) => {
      const nombre = form.querySelector('[name="nombre"]').value.trim();
      const contacto = form.querySelector('[name="contacto"]').value.trim();
      const mensaje = form.querySelector('[name="mensaje"]').value.trim();
      const error = form.querySelector("[data-client-error]");
      let msg = "";
      if (nombre.length < 2) msg = "Ingresá tu nombre.";
      else if (contacto.length < 5) msg = "Ingresá un contacto válido.";
      else if (mensaje.length < 10) msg = "Contá tu mensaje (mínimo 10 caracteres).";
      if (msg) {
        e.preventDefault();
        error.textContent = msg;
        error.classList.remove("hidden");
      }
    });
  }
})();
