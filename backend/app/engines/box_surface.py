"""引擎：盒体六面外表面积（纯函数，可单独 import）。

拆分取舍（本次拍板）：公式归引擎、服务只编排。
2×(L×W+L×H+W×H) 这段算术在整个代码库中只允许出现在本文件；
算纸服务需要表面积时只能调用这里的函数，不得内联公式。
"""


def surface_area(length: float, width: float, height: float) -> float:
    """盒体六面外表面积（m²）原始值，不在此处取整。

    边长非正（含 0 与负数）抛 ValueError，由调用方决定如何对外报错。
    """
    L, W, H = float(length), float(width), float(height)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    return 2 * (L * W + L * H + W * H)


def box_surface(length: float, width: float, height: float) -> dict:
    """接口回包形态：{"box_surface": 六面面积，保留 3 位小数}。"""
    return {"box_surface": round(surface_area(length, width, height), 3)}
