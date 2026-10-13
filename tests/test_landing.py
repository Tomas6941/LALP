from content import mle


def test_index_renders_landing(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Nada de promesas, puros resultados" in body
    assert "Movimiento Liberal Estudiantil" in body


def test_index_has_all_anchors(client):
    body = client.get("/").get_data(as_text=True)
    for section_id, _ in mle.SECCIONES:
        assert f'id="{section_id}"' in body


def test_index_lists_all_propuestas(client):
    body = client.get("/").get_data(as_text=True)
    for p in mle.PROPUESTAS:
        assert p["titulo"] in body
