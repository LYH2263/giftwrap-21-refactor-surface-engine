"""兼容门面：公式已拆至 engines 下三个纯函数文件，本模块只做委托。

- app.engines.box_surface.box_surface  盒体六面面积
- app.engines.paper_need.paper_need    折边乘出的用纸面积
- app.engines.ribbon_length.ribbon_length  丝带米数

保留原有字典返回结构，供历史调用方与旧测例继续 import；新代码请直接引用三个引擎模块。
"""
from app.engines.box_surface import box_surface as _box_surface
from app.engines.paper_need import paper_need as _paper_need
from app.engines.ribbon_length import ribbon_length as _ribbon_length


def paper_area(length: float, width: float, height: float, overlap: float = 1.15) -> dict:
    base = _box_surface(length, width, height)
    ov = float(overlap)
    return {"box_surface": round(base, 3), "overlap": ov, "paper_m2": _paper_need(base, ov)}


def ribbon_estimate(length: float, width: float, height: float, wrap_style: str = "cross") -> dict:
    """Helper: approximate ribbon length in meters (not stored as primary metric)."""
    return {
        "wrap_style": wrap_style,
        "ribbon_m": _ribbon_length(length, width, height, wrap_style),
    }
