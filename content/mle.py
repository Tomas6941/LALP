MLE = {
    "nombre": "Movimiento Liberal Estudiantil",
    "sigla": "MLE",
    "lista": "Lista Liberal",
    "lema": "Nada de promesas, puros resultados",
    "escuela": "Escuela Experimental con Énfasis en TIC — Córdoba capital",
    "contacto": {
        "email": "contacto@mle.local",
        "whatsapp": "#",
        "instagram": "#",
    },
}

SECCIONES = [
    ("inicio", "Inicio"),
    ("nosotros", "Nosotros"),
    ("propuestas", "Propuestas"),
    ("equipo", "Equipo"),
    ("plan", "Plan 90 días"),
    ("transparencia", "Transparencia"),
    ("sumate", "Sumate"),
]

NOSOTROS = {
    "intro": (
        "El Movimiento Liberal Estudiantil (MLE) es una lista que propone un centro "
        "de estudiantes transparente, participativo y tecnológico, construido sobre "
        "la libertad individual, el mérito y la rendición de cuentas."
    ),
    "principios": [
        ("Libertad individual", "Cada estudiante decide, propone y participa sin imposiciones."),
        ("Mérito", "Las ideas y el trabajo valen por su resultado, no por quién las firma."),
        ("Transparencia", "Los recursos y las decisiones se informan públicamente."),
        ("Participación voluntaria", "Nadie es obligado a militar ni a aportar."),
        ("Respeto a la diversidad de opiniones", "El disenso es parte del debate, no un enemigo."),
        ("Responsabilidad en el uso de recursos", "Cada peso del centro rinde cuentas."),
    ],
}

PROPUESTAS = [
    {
        "id": "centro-digital",
        "titulo": "Centro de Estudiantes Digital",
        "icono": "globe",
        "objetivo": "Digitalizar la gestión del centro para que la información esté disponible siempre.",
        "pasos": [
            "Publicar un sitio con propuestas, actas y estado de reclamos.",
            "Canal único de reclamos con seguimiento.",
            "Actas y balances accesibles sin pedirlos.",
        ],
        "responsable": "Secretaría de Prensa, Difusión y Tecnología",
        "plazo": "Días 16–30",
        "depende_escuela": "Sí — acceso a internet y equipo de la escuela.",
    },
    {
        "id": "transparencia-financiera",
        "titulo": "Transparencia financiera",
        "icono": "chart",
        "objetivo": "Que cada peso que maneja el centro sea público y verificable.",
        "pasos": [
            "Registro de ingresos y gastos desde el día uno.",
            "Balance mensual publicado.",
            "Comprobantes disponibles a quien los pida.",
        ],
        "responsable": "Secretaría de Finanzas",
        "plazo": "Continuo desde el día 1",
        "depende_escuela": "Parcial — requiere acceso a la cuenta del centro.",
    },
    {
        "id": "talleres-programacion",
        "titulo": "Talleres de programación y tecnología",
        "icono": "code",
        "objetivo": "Aprovechar el énfasis en TIC con talleres abiertos y gratuitos.",
        "pasos": [
            "Relevar interés y nivel de los cursos.",
            "Coordinar talleristas y espacios.",
            "Dictar un taller introductorio por cuatrimestre.",
        ],
        "responsable": "Equipo de Proyectos y Participación",
        "plazo": "Días 16–30 (primer taller)",
        "depende_escuela": "Sí — espacio físico y autorización.",
    },
    {
        "id": "presupuesto-participativo",
        "titulo": "Presupuesto participativo",
        "icono": "wallet",
        "objetivo": "Que los estudiantes decidan una parte del presupuesto del centro.",
        "pasos": [
            "Definir el porcentaje participativo.",
            "Recibir propuestas de cada curso.",
            "Votación y ejecución de las más votadas.",
        ],
        "responsable": "Secretaría de Finanzas + representantes por curso",
        "plazo": "Días 31–60",
        "depende_escuela": "Parcial — disponibilidad presupuestaria.",
    },
    {
        "id": "representantes-curso",
        "titulo": "Representantes por curso",
        "icono": "users",
        "objetivo": "Que cada curso tenga voz directa en las decisiones del centro.",
        "pasos": [
            "Convocar elección de un representante por curso.",
            "Reunión quincenal de representantes.",
            "Actas y pedidos por curso publicados.",
        ],
        "responsable": "Presidencia + Organización",
        "plazo": "Días 1–15",
        "depende_escuela": "Parcial — aval de la conducción.",
    },
    {
        "id": "torneos",
        "titulo": "Torneos entre cursos",
        "icono": "trophy",
        "objetivo": "Fomentar la convivencia y el deporte entre cursos.",
        "pasos": [
            "Relevar deportes e interés por curso.",
            "Armar fixture y reglamento.",
            "Disputar el primer torneo.",
        ],
        "responsable": "Secretaría de Deportes y Recreación",
        "plazo": "Días 31–60 (primer torneo)",
        "depende_escuela": "Sí — uso de instalaciones.",
    },
    {
        "id": "banco-proyectos",
        "titulo": "Banco de proyectos estudiantiles",
        "icono": "lightbulb",
        "objetivo": "Centralizar ideas de estudiantes para que no se pierdan.",
        "pasos": [
            "Abrir el registro de proyectos con formato simple.",
            "Clasificar por área y viabilidad.",
            "Acompañar la ejecución de las viables.",
        ],
        "responsable": "Equipo de Proyectos y Participación",
        "plazo": "Días 16–30",
        "depende_escuela": "No",
    },
    {
        "id": "convivencia-ciberseguridad",
        "titulo": "Convivencia y ciberseguridad",
        "icono": "shield",
        "objetivo": "Mejorar la convivencia y cuidar los datos de la comunidad.",
        "pasos": [
            "Campaña de buen uso de redes y datos.",
            "Protocolo de convivencia consensuado.",
            "Taller básico de seguridad digital.",
        ],
        "responsable": "Equipo de Convivencia y Ciberseguridad",
        "plazo": "Días 31–60",
        "depende_escuela": "Parcial — apoyo institucional.",
    },
    {
        "id": "espacios-comunes",
        "titulo": "Mejoras de espacios comunes",
        "icono": "sparkles",
        "objetivo": "Recuperar y mejorar los espacios compartidos.",
        "pasos": [
            "Relevar el estado actual de los espacios.",
            "Priorizar con los representantes por curso.",
            "Ejecutar las mejoras de bajo costo.",
        ],
        "responsable": "Organización + representantes por curso",
        "plazo": "Días 31–60",
        "depende_escuela": "Sí — autorización y presupuesto.",
    },
    {
        "id": "comunicacion-problemas",
        "titulo": "Comunicación y resolución de problemas entre estudiantes",
        "icono": "chat",
        "objetivo": "Un canal claro para resolver problemas y evitar rumores.",
        "pasos": [
            "Canal único de reclamos y consultas.",
            "Plazos de respuesta publicados.",
            "Estado de cada reclamo visible.",
        ],
        "responsable": "Secretaría de Prensa, Difusión y Tecnología",
        "plazo": "Continuo desde el día 1",
        "depende_escuela": "No",
    },
]

EQUIPO = {
    "presidente": "Tomás González Zalazar",
    "vicepresidente": "Santiago González Zalazar",
    "secretarias": [
        ("Actas", "Por definir"),
        ("Finanzas", "Por definir"),
        ("Prensa, Difusión y Tecnología", "Por definir"),
        ("Cultura y Eventos", "Por definir"),
        ("Deportes y Recreación", "Por definir"),
    ],
    "equipos": [
        "Organización",
        "Comunicación y Diseño",
        "Proyectos y Participación",
        "Convivencia y Ciberseguridad",
    ],
}

# Puestos a los que se puede postular quien completa el formulario #sumate
# (value, label). El value se guarda en la base de datos.
# Presidente y vicepresidente NO son postulables: se definen por lista/elección.
PUESTOS = [
    ("secretaria-actas", "Secretaría de Actas"),
    ("secretaria-finanzas", "Secretaría de Finanzas"),
    ("secretaria-prensa", "Secretaría de Prensa, Difusión y Tecnología"),
    ("secretaria-cultura", "Secretaría de Cultura y Eventos"),
    ("secretaria-deportes", "Secretaría de Deportes y Recreación"),
    ("equipo-organizacion", "Equipo de Organización"),
    ("equipo-comunicacion", "Equipo de Comunicación y Diseño"),
    ("equipo-proyectos", "Equipo de Proyectos y Participación"),
    ("equipo-convivencia", "Equipo de Convivencia y Ciberseguridad"),
    ("colaborador", "Colaborador (sin puesto definido)"),
]

PLAN_90 = [
    ("Días 1–15", [
        "Elección de representantes por curso",
        "Encuesta inicial a estudiantes",
        "Diseño del sitio web",
        "Relevar requisitos institucionales",
    ]),
    ("Días 16–30", [
        "Publicar web v1",
        "Diagnóstico del estado del centro",
        "Apertura del banco de proyectos",
        "Primer taller de tecnología",
        "Inicio del registro financiero",
    ]),
    ("Días 31–60", [
        "Presupuesto participativo",
        "Primer torneo entre cursos",
        "Mejoras de espacios comunes",
        "Campaña de convivencia y ciberseguridad",
    ]),
    ("Días 61–90", [
        "Informe de gestión público",
        "Estado de todos los reclamos",
        "Evaluación de resultados",
        "Ajustes del plan",
    ]),
]

INDICADORES = [
    ("Centro digital", "Publicaciones y actas subidas al sitio por mes"),
    ("Transparencia", "Balances mensuales publicados en fecha"),
    ("Tecnología", "Talleres dictados y estudiantes alcanzados"),
    ("Presupuesto", "Porcentaje del presupuesto ejecutado con participación"),
    ("Representación", "Cursos con representante activo"),
    ("Deportes", "Torneos realizados y participación"),
    ("Proyectos", "Proyectos presentados y ejecutados"),
    ("Convivencia", "Talleres y protocolos implementados"),
    ("Espacios comunes", "Mejoras concretadas"),
    ("Comunicación", "Reclamos respondidos dentro del plazo"),
]

REDES = [
    {"nombre": "Instagram", "url": "#"},
    {"nombre": "WhatsApp", "url": "#"},
    {"nombre": "Email", "url": "mailto:contacto@mle.local"},
]

FOOTER_DISCLAIMER = (
    "No prometemos resultados que no dependen exclusivamente de nosotros: nos "
    "comprometemos a gestionar, informar y rendir cuentas. Verificar siempre el "
    "estatuto vigente del centro de estudiantes."
)
