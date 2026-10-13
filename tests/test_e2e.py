import re


def test_full_page_has_landmarks_and_skip_link(client):
    body = client.get("/").get_data(as_text=True)
    assert "<main" in body
    assert "Saltar al contenido" in body
    assert 'aria-label="Principal"' in body


def test_no_inline_script_tag(client):
    body = client.get("/").get_data(as_text=True)
    assert "<script>" not in body
    assert re.search(r'<script src="/static/js/main\.js"', body)


def test_flow_submit_then_admin_sees_it(client, app):
    client.post("/sumate", data={
        "nombre": "E2E Tester",
        "contacto": "e2e@example.com",
        "tipo": "reclamo",
        "mensaje": "Mensaje de prueba end to end",
        "website": "",
    })
    client.post("/admin/login", data={"usuario": "admin", "password": "testpass"})
    listing = client.get("/admin").get_data(as_text=True)
    assert "E2E Tester" in listing