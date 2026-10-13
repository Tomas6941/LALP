from content import mle


def test_ten_propuestas_with_required_fields():
    assert len(mle.PROPUESTAS) == 10
    for p in mle.PROPUESTAS:
        for key in ("id", "titulo", "objetivo", "pasos", "responsable", "plazo", "depende_escuela"):
            assert key in p
        assert isinstance(p["pasos"], list) and p["pasos"]


def test_ids_unique():
    ids = [p["id"] for p in mle.PROPUESTAS]
    assert len(ids) == len(set(ids))


def test_lema_exact():
    assert mle.MLE["lema"] == "Nada de promesas, puros resultados"


def test_indicadores_ten():
    assert len(mle.INDICADORES) == 10


def test_puestos_include_all_roles():
    values = [v for v, _ in mle.PUESTOS]
    assert "presidente" in values
    assert "vicepresidente" in values
    assert "colaborador" in values
    # una por cada secretaría
    for slug in ("secretaria-actas", "secretaria-finanzas", "secretaria-cultura", "secretaria-deportes"):
        assert slug in values
    assert len(mle.PUESTOS) == len(set(values))
