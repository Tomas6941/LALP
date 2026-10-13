from app.extensions import db
from app.models import Submission


def _login(client, usuario="admin", password="testpass"):
    return client.post("/admin/login", data={"usuario": usuario, "password": password})


def test_admin_redirects_anonymous(client):
    resp = client.get("/admin")
    assert resp.status_code == 302
    assert "/admin/login" in resp.headers["Location"]


def test_login_wrong_password(client):
    resp = _login(client, password="wrong")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Credenciales inválidas" in body


def test_login_success_and_list(client, app):
    with app.app_context():
        db.session.add(Submission(nombre="Ana", contacto="a@x.com", tipo="idea",
                                  mensaje="mensaje de prueba largo"))
        db.session.commit()
    resp = _login(client)
    assert resp.status_code == 302
    listing = client.get("/admin")
    assert listing.status_code == 200
    assert "Ana" in listing.get_data(as_text=True)


def test_mark_read(client, app):
    with app.app_context():
        db.session.add(Submission(nombre="Ana", contacto="a@x.com", tipo="idea",
                                  mensaje="mensaje de prueba largo"))
        db.session.commit()
        sid = Submission.query.first().id
    _login(client)
    resp = client.post(f"/admin/submissions/{sid}/read")
    assert resp.status_code == 302
    with app.app_context():
        assert db.session.get(Submission, sid).leido is True