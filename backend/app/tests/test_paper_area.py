"""折边用纸引擎用例：直调纯函数，不经 HTTP。"""

import pytest

from app.engines.paper_area import paper_area, paper_m2, paper_result


def test_book_box_paper():
    # 书型盒 overlap=1.15：0.27×1.15=0.3105 → 0.31（与拆分前逐位一致）
    assert paper_m2(0.30, 0.20, 0.15, 1.15) == 0.31
    assert paper_area(0.30, 0.20, 0.15, 1.15) == {
        "box_surface": 0.27,
        "overlap": 1.15,
        "paper_m2": 0.31,
    }
    assert paper_result(0.27, 1.15)["paper_m2"] == 0.31


def test_non_positive_side_fails():
    # 可失败用例：非正边长沿六面面积引擎向上抛
    for dims in [(0, 0.2, 0.15), (-0.3, 0.2, 0.15), (0.3, 0.2, -0.1)]:
        with pytest.raises(ValueError):
            paper_m2(*dims, 1.15)
        with pytest.raises(ValueError):
            paper_area(*dims, 1.15)


def test_non_positive_surface_fails():
    # 可失败用例：直接喂给折边步骤的表面积也必须为正
    for bad in (0, -0.27):
        with pytest.raises(ValueError):
            paper_result(bad, 1.15)
