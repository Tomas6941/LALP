from flask import Blueprint, flash, redirect, request, url_for

from app.extensions import db
from app.forms import ContactForm
from app.models import Submission
from app.services.mailer import send_submission_notification
from app.services.ratelimit import check_rate_limit

contact_bp = Blueprint("contact", __name__)

CONTACT_LIMIT = 5
CONTACT_WINDOW = 900


def _client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()[:45]
    return (request.remote_addr or "")[:45]


@contact_bp.post("/sumate")
def submit():
    form = ContactForm()
    ip = _client_ip()

    # silent drop on honeypot hit — check BEFORE validation so a bot
    # filling the honeypot with otherwise-valid data never persists a row
    if form.website.data:
        flash("Mensaje recibido.", "success")
        return redirect(url_for("main.index") + "#sumate")

    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", "error")
        return redirect(url_for("main.index") + "#sumate")

    if not check_rate_limit(ip, "contact", CONTACT_LIMIT, CONTACT_WINDOW):
        flash("Demasiados envíos. Probá de nuevo más tarde.", "error")
        return redirect(url_for("main.index") + "#sumate")

    submission = Submission(
        nombre=form.nombre.data.strip(),
        contacto=form.contacto.data.strip(),
        tipo=form.tipo.data,
        mensaje=form.mensaje.data.strip(),
        ip=ip,
    )
    db.session.add(submission)
    db.session.commit()

    send_submission_notification(submission)

    flash("¡Gracias! Recibimos tu mensaje.", "success")
    return redirect(url_for("main.index") + "#sumate")