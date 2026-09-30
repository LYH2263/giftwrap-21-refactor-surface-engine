"""丝带米数引擎用例：直调纯函数，不经 HTTP。"""

import pytest

from app.engines.ribbon import ribbon_estimate, ribbon_m


def test_cross_and_band():
    # 书型盒 cross：2×2×(0.2+0.15)+0.3+0.5 = 2.2（与拆分前逐位一致）
    assert ribbon_m(0.30, 0.20, 0.15, "cross") == 2.2
    assert ribbon_estimate(0.30, 0.20, 0.15, "cross") == {
        "wrap_style": "cross",
        "ribbon_m": 2.2,
    }
    # band：2×(0.2+0.15)+0.3 = 1.0
    assert ribbon_m(0.30, 0.20, 0.15, "band") == 1.0


def test_unknown_wrap_style_fails():
    # 可失败用例：未知捆扎名必须抛错，不再默默落到 cross
    for name in ("diagonal", "bow", "", "CROSS"):
        with pytest.raises(ValueError):
            ribbon_m(0.30, 0.20, 0.15, name)
        with pytest.raises(ValueError):
            ribbon_estimate(0.30, 0.20, 0.15, name)


def test_non_positive_side_fails():
    # 可失败用例：边长非正（含脏数据负高 -0.1）必须拒绝
    for dims in [(0, 0.2, 0.15), (0.3, 0, 0.15), (0.2, 0.2, -0.1)]:
        with pytest.raises(ValueError):
            ribbon_m(*dims, "cross")
