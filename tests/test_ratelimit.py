from app.services.ratelimit import check_rate_limit


def test_allows_under_limit(app):
    for _ in range(5):
        assert check_rate_limit("1.1.1.1", "contact", limit=5, window_seconds=900) is True


def test_blocks_over_limit(app):
    for _ in range(5):
        check_rate_limit("2.2.2.2", "contact", limit=5, window_seconds=900)
    assert check_rate_limit("2.2.2.2", "contact", limit=5, window_seconds=900) is False


def test_scopes_are_independent(app):
    for _ in range(5):
        check_rate_limit("3.3.3.3", "contact", limit=5, window_seconds=900)
    assert check_rate_limit("3.3.3.3", "login", limit=5, window_seconds=900) is True
