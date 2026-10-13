from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from app.extensions import login_manager


class AdminUser(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    if user_id == current_app.config.get("ADMIN_USER"):
        return AdminUser(user_id)
    return None


def authenticate(username: str, password: str):
    cfg_user = current_app.config.get("ADMIN_USER")
    cfg_hash = current_app.config.get("ADMIN_PASSWORD_HASH")
    if not username or not cfg_user or username != cfg_user:
        return None
    if not cfg_hash or not check_password_hash(cfg_hash, password):
        return None
    return AdminUser(username)