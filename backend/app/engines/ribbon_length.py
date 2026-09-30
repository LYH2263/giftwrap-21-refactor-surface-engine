"""丝带米数引擎（公式唯一归属）。

cross：十字双围，两圈围长加一个长边与蝴蝶结余量；
band：单道围带，一圈围长加余量。
未知捆扎名直接拒绝，不静默退化为 cross。
"""

ALLOWED_STYLES = ("cross", "band")


def ribbon_length(length: float, width: float, height: float, wrap_style: str = "cross") -> float:
    L, W, H = float(length), float(width), float(height)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    style = str(wrap_style)
    girth = 2 * (W + H)
    if style == "band":
        meters = girth + 0.3
    elif style == "cross":
        meters = girth * 2 + L + 0.5
    else:
        raise ValueError(f"unknown wrap style: {wrap_style!r}")
    return round(meters, 2)
