"""盒体六面面积引擎用例：直调纯函数，不经 HTTP。"""

import pytest

from app.engines.box_surface import box_surface, surface_area


def test_book_box_surface():
    # 书型盒 0.30×0.20×0.15：2×(0.06+0.045+0.03)=0.27
    assert surface_area(0.30, 0.20, 0.15) == 0.27
    assert box_surface(0.30, 0.20, 0.15) == {"box_surface": 0.27}


def test_non_positive_side_fails():
    # 可失败用例：边长为 0 或负（含脏数据 -0.1）都必须拒绝
    for dims in [(0, 0.2, 0.15), (0.3, 0, 0.15), (0.3, 0.2, 0), (0.2, 0.2, -0.1)]:
        with pytest.raises(ValueError):
            surface_area(*dims)
        with pytest.raises(ValueError):
            box_surface(*dims)
