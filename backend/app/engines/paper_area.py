"""引擎：折边系数乘出用纸面积 paper_m2（纯函数，可单独 import）。

拆分取舍（本次拍板）：折边乘法归引擎，服务只做校验后顺序调用。
本文件是“表面积 × overlap”这段算术的唯一归属地。

上游 box_surface.surface_area 的未取整原始值通过 paper_result 传入，
取整只在乘法之后做一次，整条链路与拆分前逐位一致。
"""

from app.engines.box_surface import surface_area


def paper_result(surface: float, overlap: float = 1.15) -> dict:
    """接口回包形态：盒面、折边系数、用纸面积一次给齐。

    入参为盒体六面面积原始值（m²）；面积非正抛 ValueError。
    """
    base = float(surface)
    if base <= 0:
        raise ValueError("box surface must be positive")
    ov = float(overlap)
    return {
        "box_surface": round(base, 3),
        "overlap": ov,
        "paper_m2": round(base * ov, 3),
    }


def paper_m2(length: float, width: float, height: float, overlap: float = 1.15) -> float:
    """含折边余量的用纸面积（m²），保留 3 位小数。边长非正抛 ValueError。"""
    return paper_result(surface_area(length, width, height), overlap)["paper_m2"]


def paper_area(length: float, width: float, height: float, overlap: float = 1.15) -> dict:
    """从三边直接出完整回包，供单测与旧入口直接调用。"""
    return paper_result(surface_area(length, width, height), overlap)
