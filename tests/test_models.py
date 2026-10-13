from app.extensions import db
from app.models import RateLimitHit, Submission


def test_submission_mark_read(app):
    s = Submission(nombre="Ana", contacto="ana@x.com", tipo="idea", mensaje="Hola mundo testing")
    db.session.add(s)
    db.session.commit()
    assert s.leido is False
    s.mark_read()
    db.session.commit()
    assert db.session.get(Submission, s.id).leido is True


def test_rate_limit_hit_persists(app):
    db.session.add(RateLimitHit(ip="127.0.0.1", scope="contact"))
    db.session.commit()
    assert RateLimitHit.query.count() == 1
