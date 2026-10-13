# Plan de Desarrollo — Web Movimiento Liberal Estudiantil (MLE)

## 1. Objetivo

Web de campaña/marca para el **Movimiento Liberal Estudiantil (MLE) / Lista Liberal**, candidatura a Centro de Estudiantes (Escuela Experimental con Énfasis en TIC, Córdoba capital).

- **Lema:** «Nada de promesas, puros resultados»
- **Colores:** violeta (principal), blanco, negro
- **Valores:** liberalismo, mérito, transparencia, libertad individual
- **Referencias de diseño:** Que Abuso Córdoba (hero fuerte, secciones ancla, tipografía grande, formularios) + La Libertad Avanza (dark, bold, contraste alto)
- **Deploy:** recursos gratuitos (hosting estático)

---

## 2. Estructura de la página (una sola página, secciones ancla)

| # | Sección (id) | Contenido |
|---|---|---|
| 1 | `#inicio` | Hero: logo MLE, nombre, lema, CTA "Conocé las propuestas" + "Sumate" |
| 2 | `#nosotros` | Qué es MLE, ideología, contexto centro de estudiantes |
| 3 | `#propuestas` | 10 propuestas en tarjetas con detalle |
| 4 | `#equipo` | Comisión directiva + equipos de trabajo |
| 5 | `#plan` | Cronograma primeros 90 días (timeline) |
| 6 | `#transparencia` | Compromiso de rendición + indicadores |
| 7 | `#sumate` | Formulario + canales de contacto |
| 8 | Footer | Lema, disclaimer estatuto, redes |

Nav sticky con links a las anclas. Smooth scroll.

---

## 3. Contenido a trasladar (del PDF, reescrito a MLE/Lista Liberal)

**Header/logo:** "Movimiento Liberal Estudiantil" · "Lista Liberal" · lema.

**#nosotros:**
- Centro de estudiantes transparente, participativo y tecnológico.
- Principios: libertad individual, mérito, transparencia, participación voluntaria, respeto a la diversidad de opiniones, responsabilidad en el uso de recursos.

**#propuestas (10):** cada una con Objetivo / Pasos / Responsable / Plazo / Depende de la escuela.

1. Centro de Estudiantes Digital
2. Transparencia financiera
3. Talleres de programación y tecnología
4. Presupuesto participativo
5. Representantes por curso
6. Torneos entre cursos
7. Banco de proyectos estudiantiles
8. Convivencia y ciberseguridad
9. Mejoras de espacios comunes
10. Comunicación y resolución de problemas entre estudiantes

**#equipo:**
- Presidente: Tomás González Zalazar
- Vicepresidente: Santiago González Zalazar
- Secretarías (por definir): Actas · Finanzas · Prensa, Difusión y Tecnología · Cultura y Eventos · Deportes y Recreación
- Equipos complementarios: Organización · Comunicación y Diseño · Proyectos y Participación · Convivencia y Ciberseguridad

**#plan (90 días):**

| Período | Prioridades |
|---|---|
| Días 1–15 | Representantes por curso; encuesta; diseño web; requisitos institucionales |
| Días 16–30 | Web v1; diagnóstico; banco de proyectos; primer taller; registro financiero |
| Días 31–60 | Presupuesto participativo; primer torneo; mejoras; campaña convivencia |
| Días 61–90 | Informe de gestión; estado de reclamos; evaluación; ajuste |

**#transparencia:** compromiso + 10 indicadores por área (Centro digital, Transparencia, Tecnología, Presupuesto, Representación, Deportes, Proyectos, Convivencia, Espacios comunes, Comunicación).

**Footer disclaimer:** "No prometemos resultados que no dependen exclusivamente de nosotros: nos comprometemos a gestionar, informar y rendir cuentas." + nota sobre revisar estatuto vigente.

---

## 4. Requisitos de diseño

- **Tema:** violeta como **color principal** — fondo/acento dominante. Negro y blanco como secundarios (texto, contraste, superficies).
- **Paleta:**
  - `--violeta` principal (marca, CTAs, headers, acentos)
  - `--violeta-oscuro` / claro para hover, gradientes, bordes
  - `--negro` fondos/texto
  - `--blanco` texto/superficies de contraste
- **Jerarquía:** violeta = color de marca y acción. Negro/blanco = soporte de legibilidad.
- **Tipografía:** sans-serif grande, títulos muy bold (estilo LLA/Que Abuso).
- **Tokens:** CSS variables (`--violeta`, `--violeta-oscuro`, `--negro`, `--blanco`), espaciado, radios.
- **Componentes:** hero full-height, cards de propuesta, timeline, cards de equipo, form, footer.
- **Mobile-first**, responsive.
- **Logo/emblema:** SVG propio con violeta dominante (placeholders si no hay asset).

---

## 5. Requisitos funcionales

- Nav sticky + smooth scroll + menú hamburguesa mobile.
- Cards de propuestas: estado colapsado/expandible o modal.
- Formulario (#sumate): nombre, contacto, mensaje, tipo (sugerencia/reclamo). Validación cliente. Backend a definir (placeholder / Google Form / Formspree).
- Links a redes sociales.
- Botón "Sumate".

## 6. Requisitos no funcionales

- Accesibilidad AA (contraste, focus, aria, alt).
- Performance (imágenes optimizadas, sin deps pesadas).
- SEO + OpenGraph (título, descripción, imagen preview).

---

## 7. Fases sugeridas para los agentes

| Fase | Entregable |
|---|---|
| 0 | Setup proyecto + estructura carpetas + tokens de diseño |
| 1 | Layout base: header, nav, footer, routing de anclas |
| 2 | Hero + sección nosotros |
| 3 | Propuestas (10 cards) |
| 4 | Equipo + cronograma 90 días |
| 5 | Transparencia + formulario sumate |
| 6 | Responsive, accesibilidad, performance |
| 7 | SEO/OG + deploy |

---

