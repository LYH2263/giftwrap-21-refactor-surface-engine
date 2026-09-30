"""引擎：捆扎丝带米数 ribbon_m（纯函数，可单独 import）。

拆分取舍（本次拍板）：围长丝带算术归引擎，服务只做校验后顺序调用。
围长、捆扎余量这段算术在整个代码库中只允许出现在本文件。

支持的捆扎名：
- "cross"：十字捆扎，纵横两圈 + 长边 + 蝴蝶结余量 0.5 m；
- "band"：单圈束带 + 0.3 m。
未知捆扎名抛 ValueError，不再默默落到 cross 分支。
"""

# 捆扎名 -> （余量米数，围长倍数，是否再加一条长边）
_STYLES = {
    "cross": (0.5, 2, True),
    "band": (0.3, 1, False),
}


def ribbon_m(length: float, width: float, height: float, wrap_style: str = "cross") -> float:
    """丝带长度（m），保留 2 位小数。边长非正或捆扎名未知均抛 ValueError。"""
    L, W, H = float(length), float(width), float(height)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    style = _STYLES.get(wrap_style)
    if style is None:
        raise ValueError(f"unknown wrap_style: {wrap_style!r}")
    extra, girth_mult, with_length = style
    girth = 2 * (W + H)
    return round(girth * girth_mult + (L if with_length else 0) + extra, 2)


def ribbon_estimate(length: float, width: float, height: float, wrap_style: str = "cross") -> dict:
    """接口回包形态：{"wrap_style": ..., "ribbon_m": ...}。"""
    return {
        "wrap_style": wrap_style,
        "ribbon_m": ribbon_m(length, width, height, wrap_style),
    }
