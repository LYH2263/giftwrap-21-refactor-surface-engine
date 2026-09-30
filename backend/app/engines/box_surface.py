"""盒体六面面积引擎（公式唯一归属）。

输入单位 m，输出为未取整的外表面积 m²。取整由调用方在展示层处理，
以保证后续折边乘法与重构前逐位一致。
"""


def box_surface(length: float, width: float, height: float) -> float:
    L, W, H = float(length), float(width), float(height)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    return 2 * (L * W + L * H + W * H)
