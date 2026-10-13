from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.get("/healthz")
def healthz():
    return jsonify(status="ok")
