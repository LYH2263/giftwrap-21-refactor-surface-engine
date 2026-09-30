import pytest

from app.engines.ribbon_length import ribbon_length


def test_cross_book_box():
    # cross：围长 0.7 ×2 + 长边 0.3 + 0.5 = 2.2（与重构前逐位一致）
    assert ribbon_length(0.30, 0.20, 0.15, "cross") == 2.2


def test_band_book_box():
    # band：围长 0.7 + 0.3 = 1.0
    assert ribbon_length(0.30, 0.20, 0.15, "band") == 1.0


def test_unknown_wrap_style_rejected():
    with pytest.raises(ValueError):
        ribbon_length(0.30, 0.20, 0.15, "diagonal")


@pytest.mark.parametrize("l,w,h", [
    (0, 0.2, 0.15),
    (0.3, 0, 0.15),
    (0.3, 0.2, -0.15),
])
def test_non_positive_dimensions_rejected(l, w, h):
    with pytest.raises(ValueError):
        ribbon_length(l, w, h, "cross")
