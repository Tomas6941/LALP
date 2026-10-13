from datetime import datetime, timezone

from app.extensions import db


def _utcnow():
    return datetime.now(timezone.utc)


class Submission(db.Model):
    __tablename__ = "submission"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    contacto = db.Column(db.String(200), nullable=False)
    puesto = db.Column(db.String(40), nullable=False, default="colaborador")
    mensaje = db.Column(db.Text, nullable=False)
    ip = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    leido = db.Column(db.Boolean, default=False, nullable=False)

    def mark_read(self):
        self.leido = True


class RateLimitHit(db.Model):
    __tablename__ = "rate_limit_hit"
    __table_args__ = (db.Index("ix_rate_ip_scope_created", "ip", "scope", "created_at"),)

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(45), nullable=False)
    scope = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
