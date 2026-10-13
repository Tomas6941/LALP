def test_security_headers(client):
    resp = client.get("/")
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert "default-src 'self'" in resp.headers["Content-Security-Policy"]


def test_robots(client):
    resp = client.get("/robots.txt")
    assert resp.status_code == 200
    assert "Disallow: /admin" in resp.get_data(as_text=True)


def test_sitemap(client):
    resp = client.get("/sitemap.xml")
    assert resp.status_code == 200
    assert "sitemap" in resp.get_data(as_text=True)


def test_404(client):
    resp = client.get("/no-existe")
    assert resp.status_code == 404