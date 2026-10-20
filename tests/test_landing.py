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


def test_index_detalle_propuestas_has_six_blocks(client):
    body = client.get("/").get_data(as_text=True)
    for label in (
        "Qué problema resuelve",
        "Cómo se va a implementar",
        "Quién se responsabiliza",
        "Cuándo se puede realizar",
        "Qué recursos necesita",
        "Qué depende de la autorización de la escuela",
    ):
        assert label in body
    for p in mle.PROPUESTAS:
        assert p["problema"] in body
        assert p["recursos"] in body
