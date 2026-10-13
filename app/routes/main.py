from flask import Blueprint, Response, current_app, jsonify, render_template, url_for

from content import mle

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    from app.forms import ContactForm

    return render_template("index.html", propuestas=mle.PROPUESTAS, form=ContactForm())


@main_bp.get("/healthz")
def healthz():
    return jsonify(status="ok")


@main_bp.get("/robots.txt")
def robots():
    body = "User-agent: *\nAllow: /\nDisallow: /admin\n"
    return Response(body, mimetype="text/plain")


@main_bp.get("/sitemap.xml")
def sitemap():
    base = current_app.config["SITE_URL"].rstrip("/")
    urls = "".join(f"<url><loc>{base}/#{sid}</loc></url>" for sid, _ in mle.SECCIONES)
    body = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(body, mimetype="application/xml")