from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import authenticate
from app.extensions import db
from app.forms import LoginForm
from app.models import Submission
from app.services.ratelimit import check_rate_limit

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

LOGIN_LIMIT = 10
LOGIN_WINDOW = 900

TIPO_LABELS = [("sugerencia", "Sugerencia"), ("reclamo", "Reclamo"), ("idea", "Idea")]


def _client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()[:45]
    return (request.remote_addr or "")[:45]


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.list_submissions"))
    form = LoginForm()
    if form.validate_on_submit():
        ip = _client_ip()
        if not check_rate_limit(ip, "login", LOGIN_LIMIT, LOGIN_WINDOW):
            flash("Demasiados intentos. Probá más tarde.", "error")
            return render_template("admin/login.html", form=form), 429
        user = authenticate(form.usuario.data.strip(), form.password.data)
        if user:
            login_user(user)
            return redirect(url_for("admin.list_submissions"))
        flash("Credenciales inválidas.", "error")
    return render_template("admin/login.html", form=form)


@admin_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@admin_bp.get("")
@login_required
def list_submissions():
    tipo = request.args.get("tipo")
    leido = request.args.get("leido")
    query = Submission.query
    if tipo:
        query = query.filter(Submission.tipo == tipo)
    if leido == "0":
        query = query.filter(Submission.leido.is_(False))
    elif leido == "1":
        query = query.filter(Submission.leido.is_(True))
    submissions = query.order_by(Submission.created_at.desc()).all()
    return render_template(
        "admin/submissions.html",
        submissions=submissions,
        tipo=tipo,
        leido=leido,
        tipo_labels=TIPO_LABELS,
    )


@admin_bp.post("/submissions/<int:submission_id>/read")
@login_required
def mark_read(submission_id):
    submission = db.session.get(Submission, submission_id)
    if submission is None:
        return redirect(url_for("admin.list_submissions"))
    submission.mark_read()
    db.session.commit()
    return redirect(url_for("admin.list_submissions"))