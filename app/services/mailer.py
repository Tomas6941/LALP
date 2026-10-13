import smtplib
from email.message import EmailMessage

from flask import current_app


def send_submission_notification(submission) -> bool:
    app = current_app
    if app.config.get("MAIL_SUPPRESS_SEND"):
        return True
    host = app.config.get("SMTP_HOST")
    mail_to = app.config.get("MAIL_TO")
    if not host or not mail_to:
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Nuevo mensaje LALP — {submission.puesto}"
    msg["From"] = app.config.get("SMTP_USER") or mail_to
    msg["To"] = mail_to
    msg.set_content(
        "Nuevo mensaje recibido en la web del LALP.\n\n"
        f"Nombre: {submission.nombre}\n"
        f"Contacto: {submission.contacto}\n"
        f"Puesto: {submission.puesto}\n\n"
        f"Mensaje:\n{submission.mensaje}\n"
    )

    try:
        with smtplib.SMTP(host, app.config.get("SMTP_PORT", 587), timeout=10) as smtp:
            smtp.starttls()
            user = app.config.get("SMTP_USER")
            password = app.config.get("SMTP_PASS")
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except Exception:  # best-effort: never break the request
        app.logger.exception("Fallo al enviar notificación de envío")
        return False