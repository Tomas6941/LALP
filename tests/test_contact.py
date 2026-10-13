from app.extensions import db
from app.models import Submission


def _form(nombre="Ana Pérez", contacto="ana@example.com", tipo="idea",
          mensaje="Esta es una idea de prueba", website=""):
    return {
        "nombre": nombre,
        "contacto": contacto,
        "tipo": tipo,
        "mensaje": mensaje,
        "website": website,
    }


def test_valid_submission_creates_row(client, app):
    resp = client.post("/sumate", data=_form(), follow_redirects=False)
    assert resp.status_code == 302
    with app.app_context():
        assert Submission.query.count() == 1
        s = Submission.query.first()
        assert s.tipo == "idea"
        assert s.leido is False


def test_honeypot_blocks(client, app):
    client.post("/sumate", data=_form(website="http://spam"))
    with app.app_context():
        assert Submission.query.count() == 0


def test_short_mensaje_rejected(client, app):
    client.post("/sumate", data=_form(mensaje="corto"))
    with app.app_context():
        assert Submission.query.count() == 0


def test_rate_limit_blocks_after_five(client, app):
    for i in range(5):
        client.post("/sumate", data=_form(contacto=f"a{i}@example.com"))
    client.post("/sumate", data=_form(contacto="sixth@example.com"))
    with app.app_context():
        assert Submission.query.count() == 5


def test_mailer_called(client, app, monkeypatch):
    called = {}

    def fake(submission):
        called["id"] = submission.id
        return True

    monkeypatch.setattr("app.routes.contact.send_submission_notification", fake)
    client.post("/sumate", data=_form())
    assert "id" in called