from flask import Blueprint, jsonify, render_template

from content import mle

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    from app.forms import ContactForm

    return render_template("index.html", propuestas=mle.PROPUESTAS, form=ContactForm())


@main_bp.get("/healthz")
def healthz():
    return jsonify(status="ok")
