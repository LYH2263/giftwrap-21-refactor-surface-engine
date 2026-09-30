"""折边用纸面积引擎（公式唯一归属）。

六面面积 × 折边系数，输出含重叠余量的用纸面积 m²（保留 3 位小数，
与重构前 round(base * overlap, 3) 逐位一致）。
"""


def paper_need(box_surface_m2: float, overlap: float = 1.15) -> float:
    base = float(box_surface_m2)
    ov = float(overlap)
    if base <= 0:
        raise ValueError("box surface must be positive")
    if ov <= 0:
        raise ValueError("overlap must be positive")
    return round(base * ov, 3)
