MLE = {
    "nombre": "Movimiento Liberal Estudiantil",
    "sigla": "LALP",
    "lista": "Lista Azul Liberal Proa",
    "lema": "Nada de promesas, puros resultados",
    "escuela": "Escuela Experimental con Énfasis en TIC — Córdoba capital",
    "contacto": {
        "email": "tgonzalezzalazar@escuelasproa.edu.ar",
        "whatsapp": "351 796-2251",
        "instagram": "https://www.instagram.com/lal.proa/",
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
        "La Lista Azul Liberal Proa (LALP) es una lista que propone un centro "
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
        "problema": (
            "Hoy la información del centro vive en pasillos, capturas de WhatsApp y "
            "papeles que se pierden: nadie sabe qué se resolvió, qué está pendiente ni "
            "a quién reclamar. Eso genera desconfianza, rumores y reclamos que se "
            "repiten sin respuesta."
        ),
        "pasos": [
            "Diseñar un sitio con las propuestas, actas, balances y el estado de cada reclamo.",
            "Abrir un canal único de reclamos con número de seguimiento y plazo de respuesta.",
            "Cargar actas y balances en formato abierto, sin tener que pedirlos.",
            "Capacitar al equipo del centro para mantenerlo actualizado cada semana.",
        ],
        "recursos": (
            "Un sitio web gratuito o de bajo costo, un correo institucional, acceso a "
            "internet y equipo de la escuela, y 2 horas semanales del equipo de Prensa "
            "y Tecnología."
        ),
        "responsable": "Secretaría de Prensa, Difusión y Tecnología",
        "plazo": "Días 16–30",
        "depende_escuela": (
            "Sí — requiere acceso a internet, equipos y autorización para publicar "
            "información institucional."
        ),
    },
    {
        "id": "transparencia-fondos",
        "titulo": "Transparencia total de los fondos",
        "icono": "chart",
        "objetivo": (
            "Publicar cada ingreso y gasto del centro, con comprobantes y "
            "balances periódicos. Los estudiantes deben saber dónde va cada peso."
        ),
        "problema": (
            "Sin registro público, cualquier rumor sobre el dinero del centro se vuelve "
            "creíble. Los estudiantes no saben cuánto hay, de dónde viene ni en qué se "
            "gasta, y eso alimenta la desconfianza en el centro."
        ),
        "pasos": [
            "Registrar cada ingreso y gasto desde el día uno, con su comprobante.",
            "Publicar un balance mensual explicado en lenguaje simple.",
            "Mantener el historial completo visible en el sitio del centro.",
            "Responder por escrito cualquier consulta sobre un gasto.",
        ],
        "recursos": (
            "Una planilla o sistema gratuito de registro, acceso a los movimientos de "
            "la cuenta del centro, celular o escáner para digitalizar comprobantes y "
            "el trabajo del Encargado en Finanzas."
        ),
        "responsable": "Encargado en Finanzas",
        "plazo": "Continuo desde el día 1",
        "depende_escuela": "Parcial — requiere acceso a la cuenta y los comprobantes del centro.",
    },
    {
        "id": "presupuesto-participativo",
        "titulo": "Presupuesto participativo",
        "icono": "wallet",
        "objetivo": (
            "Permitir que los estudiantes propongan y voten en qué utilizar los "
            "fondos disponibles, priorizando las necesidades más importantes."
        ),
        "problema": (
            "Las decisiones de gasto se toman entre muy pocos y sin consultar a nadie. "
            "Así se priorizan gastos que no son los más urgentes para el alumnado y el "
            "presupuesto no refleja lo que la escuela realmente necesita."
        ),
        "pasos": [
            "Definir qué porcentaje del presupuesto se decide participativamente.",
            "Abrir la recepción de propuestas de gasto desde cada curso.",
            "Publicar todas las propuestas con su costo estimado.",
            "Votación abierta y ejecución de las más votadas, con seguimiento público.",
        ],
        "recursos": (
            "Presupuesto disponible del centro, un formulario simple de propuestas, "
            "urnas o votación digital y el apoyo de los representantes por curso."
        ),
        "responsable": "Encargado en Finanzas + representantes por curso",
        "plazo": "Días 31–60",
        "depende_escuela": (
            "Parcial — requiere disponibilidad presupuestaria y autorización para "
            "realizar la votación."
        ),
    },
    {
        "id": "menos-burocracia",
        "titulo": "Menos burocracia, más resultados",
        "icono": "sparkles",
        "objetivo": (
            "Eliminar trámites internos innecesarios y simplificar la presentación "
            "de proyectos estudiantiles. Menos reuniones improductivas y más "
            "acciones concretas."
        ),
        "problema": (
            "Un proyecto estudiantil se pierde en formularios, reuniones y aprobaciones "
            "que nadie sabe quién da. Los trámites desaniman a proponer: los alumnos "
            "con buenas ideas se cansan antes de ver un resultado."
        ),
        "pasos": [
            "Relevamiento público de los trámites que hoy frenan un proyecto.",
            "Reuniones con agenda clara, tiempos acotados y decisiones concretas.",
            "Un único formulario breve para presentar una iniciativa.",
            "Regla de oro: todo trámite sin plazo público se elimina.",
        ],
        "recursos": (
            "Ninguno o muy poco: voluntad de la conducción, un formulario digital "
            "gratuito y una lista pública de los trámites vigentes."
        ),
        "responsable": "Presidencia + Organización",
        "plazo": "Días 1–15",
        "depende_escuela": (
            "Parcial — algunos trámites dependen de la conducción de la escuela y se "
            "requiere su aval para simplificarlos."
        ),
    },
    {
        "id": "banco-proyectos",
        "titulo": "Banco de proyectos estudiantiles",
        "icono": "lightbulb",
        "objetivo": (
            "Crear un sistema donde cualquier alumno pueda presentar iniciativas. "
            "Los proyectos se evaluarán por su viabilidad, costo e impacto, sin "
            "importar quién los proponga."
        ),
        "problema": (
            "Las ideas de los alumnos se pierden en el pasillo: no hay lugar donde "
            "cargarlas, ni criterios claros para evaluarlas, ni seguimiento de lo que "
            "se aprobó. Todo depende de quién conoce a quién."
        ),
        "pasos": [
            "Abrir un registro público de proyectos con formato simple.",
            "Evaluar cada proyecto por viabilidad, costo e impacto, con criterios publicados.",
            "Publicar el estado de cada proyecto: evaluado, aprobado o en ejecución, con fundamentos.",
            "Acompañar la ejecución de los aprobados hasta su resultado final.",
        ],
        "recursos": (
            "Un formulario o planilla gratuita, criterios de evaluación escritos, una "
            "reunión mensual de evaluación y el trabajo del Equipo de Proyectos y "
            "Participación."
        ),
        "responsable": "Equipo de Proyectos y Participación",
        "plazo": "Días 16–30",
        "depende_escuela": "No — funciona con los recursos del propio centro.",
    },
    {
        "id": "libertad-expresion",
        "titulo": "Libertad de expresión y pluralismo político",
        "icono": "chat",
        "objetivo": (
            "Garantizar que todas las ideas políticas puedan expresarse "
            "pacíficamente, sin censura partidaria ni discriminación ideológica. "
            "El Centro no debe obligar a nadie a compartir una postura política."
        ),
        "problema": (
            "Cuando el centro se vuelve voz de una sola facción, los estudiantes que "
            "piensan distinto se callan o se desentienden. El centro debe representar "
            "a todo el alumnado; sin pluralismo, la política escolar se vuelve exclusión."
        ),
        "pasos": [
            "Regla interna explícita: el centro no censura ni discrimina por postura política.",
            "Espacios abiertos y pacíficos, con las mismas condiciones para todas las ideas.",
            "Ninguna actividad del centro puede obligar a nadie a compartir una posición.",
            "Canales de disenso respetuosos, sin represalias de ningún tipo.",
        ],
        "recursos": (
            "Ninguno: un reglamento interno claro, su difusión en el sitio del centro y "
            "el compromiso público del equipo electo."
        ),
        "responsable": "Presidencia + Organización",
        "plazo": "Continuo desde el día 1",
        "depende_escuela": (
            "No — el centro es autónomo en su régimen interno, dentro del estatuto "
            "vigente."
        ),
    },
    {
        "id": "meritocracia",
        "titulo": "Meritocracia y reconocimiento del esfuerzo",
        "icono": "trophy",
        "objetivo": (
            "Impulsar reconocimientos para estudiantes que destaquen en "
            "programación, robótica, ciencias, deportes, arte y otros ámbitos."
        ),
        "problema": (
            "Los estudiantes que se esfuerzan en programación, ciencias, deportes o arte "
            "casi nunca reciben reconocimiento público. Sin incentivos transparentes, el "
            "mérito pasa inadvertido y prima la amistad o la militancia."
        ),
        "pasos": [
            "Publicar criterios de reconocimiento transparentes y accesibles para todos.",
            "Organizar competencias de programación, robótica, deportes y resolución de problemas.",
            "Convocar postulaciones abiertas, evaluadas con criterios públicos.",
            "Entregar reconocimientos en un acto abierto al esfuerzo y a los resultados.",
        ],
        "recursos": (
            "Diplomas o insignias simbólicas, espacios de la escuela para las "
            "competencias, apoyo de docentes como jurados y muy poco presupuesto."
        ),
        "responsable": "Cultura y Eventos + Deportes y Recreación",
        "plazo": "Días 31–60",
        "depende_escuela": (
            "Parcial — requiere apoyo institucional para jurados y uso de espacios."
        ),
    },
    {
        "id": "emprendimiento",
        "titulo": "Emprendimiento y libertad económica",
        "icono": "lightbulb",
        "objetivo": (
            "Actividades para aprender a desarrollar, presentar y comercializar "
            "proyectos estudiantiles."
        ),
        "problema": (
            "Muchos alumnos salen de la escuela sin haber presentado ni vendido nunca "
            "algo propio. No hay espacios para aprender a convertir una idea en un "
            "proyecto que otros quieran apoyar o comprar."
        ),
        "pasos": [
            "Organizar una feria de emprendimientos estudiantiles por cuatrimestre.",
            "Dictar talleres breves de educación financiera y de ventas.",
            "Acompañar proyectos desde la idea hasta la presentación y la primera venta.",
            "Vincular emprendedores con ex-alumnos o comercios locales como mentores.",
        ],
        "recursos": (
            "Espacio para la feria, mesas o stands, difusión, inscripción abierta y "
            "apoyo de la escuela para convocar mentores externos."
        ),
        "responsable": "Equipo de Proyectos y Participación",
        "plazo": "Días 31–60",
        "depende_escuela": "Parcial — requiere espacio físico y autorización para la feria.",
    },
    {
        "id": "autonomia-responsable",
        "titulo": "Autonomía estudiantil con responsabilidad",
        "icono": "users",
        "objetivo": (
            "Dar mayor participación a los estudiantes en las decisiones que los "
            "afectan, acompañada de rendición de cuentas y cumplimiento de "
            "compromisos."
        ),
        "problema": (
            "Las decisiones del centro se toman sin consultar y sin rendir cuentas "
            "después. Los estudiantes participan poco porque no ven que su opinión "
            "cambie nada, y los compromisos de campaña quedan en el olvido."
        ),
        "pasos": [
            "Consulta abierta a los cursos antes de cada decisión importante.",
            "Compromisos publicados con un responsable y un plazo concreto.",
            "Rendición de cuentas trimestral: cumplidos, pendientes y motivos.",
            "Mecanismo para que los estudiantes evalúen al equipo del centro.",
        ],
        "recursos": (
            "Encuestas gratuitas, reuniones por curso, difusión en el sitio del centro "
            "y tiempo del equipo para la rendición de cuentas."
        ),
        "responsable": "Presidencia + representantes por curso",
        "plazo": "Continuo desde el día 1",
        "depende_escuela": (
            "Parcial — requiere aval de la conducción para convocar asambleas y "
            "consultas."
        ),
    },
    {
        "id": "control-gestion",
        "titulo": "Control de gestión y evaluación de resultados",
        "icono": "shield",
        "objetivo": (
            "Publicar un informe mensual con las propuestas ejecutadas, las "
            "pendientes, los gastos y los resultados obtenidos."
        ),
        "problema": (
            "Las promesas de campaña se olvidan al día siguiente de las elecciones. "
            "Sin un informe público, nadie puede verificar qué se cumplió, qué quedó "
            "pendiente ni en qué se gastó."
        ),
        "pasos": [
            "Informe mensual público con las propuestas ejecutadas y las pendientes.",
            "Detalle de gastos y resultados concretos, sin letra chica.",
            "Cada promesa con un responsable y un plazo concreto desde el inicio.",
            "Revisión conjunta del informe con los representantes por curso.",
        ],
        "recursos": (
            "Una planilla de seguimiento de compromisos, los datos de gestión del "
            "centro y una hora mensual de trabajo del equipo de Actas y Finanzas."
        ),
        "responsable": "Actas + Finanzas",
        "plazo": "Informe mensual desde el día 30",
        "depende_escuela": "No — el centro controla su propia gestión.",
    },
]

EQUIPO = {
    "presidente": "Tomás González Zalazar",
    "vicepresidente": "Santiago González Zalazar",
    "secretarias": [
        ("Secretarios General", "Genaro Gilardotti y Facundo Bazan"),
        ("Secretario de Prensa, Difusión y Tecnología", "Genaro Gilardotti y Juan Abdala"),
        ("Encargado en Finanzas", "Simón Leonel Campos y Ariadny Valeria Diaz Rodriguez "),
        ("Encargado en Deportes y Recreación", "Juan Pablo Juncos y Maximo Lujan Guzzi"),
        ("Encargado en Cultura y Eventos", "Lorenzo Martínez y Miranda Von Eberan Plutman"),
        ("Encargado en Actas", "Elías Gabriel Arce Martínez y Tobias Hürst Altamirano"),
    ],
    # Equipos de trabajo: (equipo, responsable). Completá el responsable de
    # cada equipo cuando esté definido; hasta entonces deja "" para no mostrar
    # la columna derecha.
    "equipos": [
        ("Organizador de los Equipos de trabajo", "Stefano Sarzotti"),
        ("Comunicación y Diseño", "Malena Celeste Paredes"),
        ("Proyectos y Participación", "Lautaro Valentín Allende"),
        ("Convivencia y Ciberseguridad", ""),
    ],
}

# Puestos a los que se puede postular quien completa el formulario #sumate
# (value, label). El value se guarda en la base de datos.
# Presidente, vicepresidente y secretarías NO son postulables: se definen por
# lista/elección. Solo se puede postular a los equipos de trabajo.
PUESTOS = [
    ("equipo-organizacion", "Equipo de Organización"),
    ("equipo-comunicacion", "Equipo de Comunicación y Diseño"),
    ("equipo-proyectos", "Equipo de Proyectos y Participación"),
    ("equipo-convivencia", "Equipo de Convivencia y Ciberseguridad"),
    ("subencargado-secretaria-general", "Sub-encargado/a de Secretaría General"),
    ("subencargado-secretaria-prensa", "Sub-encargado/a de Secretaría de Prensa y Difusión"),
    ("subencargado-finanzas", "Sub-encargado/a de Finanzas"),
    ("subencargado-deportes", "Sub-encargado/a de Deportes"),
    ("subencargado-cultura-eventos", "Sub-encargado/a de Cultura y Eventos"),
    ("subencargado-actas", "Sub-encargado/a de Actas"),
    ("colaborador", "Colaborador (sin puesto definido)"),
]

PLAN_90 = [
    ("Días 1–15", [
        "Publicar cada ingreso y gasto con comprobante",
        "Eliminar trámites innecesarios y simplificar formularios",
        "Elección de representantes por curso",
        "Reglas claras de libertad de expresión y pluralismo",
    ]),
    ("Días 16–30", [
        "Publicar el Centro de Estudiantes Digital",
        "Canal único de reclamos con seguimiento",
        "Apertura del banco de proyectos estudiantiles",
        "Primer balance público con comprobantes",
    ]),
    ("Días 31–60", [
        "Presupuesto participativo: propuestas y votación",
        "Feria de emprendimientos y talleres de educación financiera",
        "Competencias entre cursos y reconocimiento al mérito",
        "Primera rendición de cuentas de compromisos",
    ]),
    ("Días 61–90", [
        "Informe mensual de gestión con responsable y plazo por promesa",
        "Ejecución de los proyectos más votados",
        "Evaluación de resultados de cada propuesta",
        "Ajustes del plan con participación estudiantil",
    ]),
]

INDICADORES = [
    ("Centro digital", "Publicaciones, actas y reclamos con estado actualizado"),
    ("Transparencia", "Balances mensuales publicados en fecha"),
    ("Presupuesto", "Porcentaje del presupuesto decidido por los estudiantes"),
    ("Burocracia", "Trámites eliminados o simplificados"),
    ("Proyectos", "Proyectos presentados y evaluados por viabilidad e impacto"),
    ("Pluralismo", "Actividades con participación plural, sin censura"),
    ("Mérito", "Reconocimientos entregados con criterios públicos"),
    ("Emprendimiento", "Ferias y talleres realizados"),
    ("Autonomía", "Decisiones tomadas con rendición de cuentas"),
    ("Gestión", "Informes mensuales publicados con compromisos y plazos"),
]

REDES = [
    {"nombre": "Instagram", "url": "https://www.instagram.com/lal.proa/"},
    {"nombre": "WhatsApp", "url": "https://wa.me/3517962251"},
    {"nombre": "Email", "url": "mailto:tgonzalezzalazar@escuelasproa.edu.ar"},
]

FOOTER_DISCLAIMER = (
    "No prometemos resultados que no dependen exclusivamente de nosotros: nos "
    "comprometemos a gestionar, informar y rendir cuentas. Verificar siempre el "
    "estatuto vigente del centro de estudiantes."
)
