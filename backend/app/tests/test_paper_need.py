import pytest

from app.engines.paper_need import paper_need


def test_book_box_paper_need():
    # 六面面积 0.27 × 折边 1.15 = 0.3105 → 0.31（与重构前逐位一致）
    assert paper_need(0.27, 1.15) == 0.31


def test_overlap_one_keeps_surface():
    assert paper_need(6.0, 1.0) == 6.0


@pytest.mark.parametrize("surface,overlap", [
    (0, 1.15),
    (-0.27, 1.15),
    (0.27, 0),
    (0.27, -1.0),
])
def test_non_positive_inputs_rejected(surface, overlap):
    with pytest.raises(ValueError):
        paper_need(surface, overlap)
