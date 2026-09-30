import pytest

from app.engines.box_surface import box_surface


def test_book_box_surface():
    # 书型盒 0.30×0.20×0.15：2×(0.06+0.045+0.03)=0.27
    assert box_surface(0.30, 0.20, 0.15) == 0.27


@pytest.mark.parametrize("l,w,h", [
    (0, 0.2, 0.15),
    (0.3, 0, 0.15),
    (0.3, 0.2, 0),
    (-0.3, 0.2, 0.15),
    (0.3, -0.2, 0.15),
    (0.3, 0.2, -0.15),
])
def test_non_positive_dimensions_rejected(l, w, h):
    with pytest.raises(ValueError):
        box_surface(l, w, h)
