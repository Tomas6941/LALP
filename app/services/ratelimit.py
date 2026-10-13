from datetime import datetime, timedelta, timezone

from app.extensions import db
from app.models import RateLimitHit


def _now():
    return datetime.now(timezone.utc)


def _as_aware(dt):
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def check_rate_limit(ip: str, scope: str, limit: int, window_seconds: int) -> bool:
    since = _now() - timedelta(seconds=window_seconds)
    count = (
        RateLimitHit.query.filter(
            RateLimitHit.ip == ip,
            RateLimitHit.scope == scope,
        )
        .all()
    )
    recent = [h for h in count if _as_aware(h.created_at) >= since]
    if len(recent) >= limit:
        return False
    db.session.add(RateLimitHit(ip=ip, scope=scope))
    db.session.commit()
    return True
