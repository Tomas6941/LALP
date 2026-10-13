/* Marca "hay JS" ANTES del primer pintado.
 *
 * Los reveals de scroll se ocultan desde el CSS con `html.has-js`. Si esa clase
 * se agregara desde main.js (que va con `defer`), el navegador alcanza a pintar
 * el contenido visible y recién después lo oculta y lo vuelve a mostrar: un
 * parpadeo/lavado al cargar. Este script es bloqueante y vive en el <head>, así
 * que corre antes de que exista el <body> y por lo tanto antes de cualquier
 * pintado. Sin JS la clase no existe y el contenido queda siempre visible.
 */
document.documentElement.classList.add("has-js");
