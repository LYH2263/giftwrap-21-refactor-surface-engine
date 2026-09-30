"""兼容门面（已不持有任何公式）。

公式归属在本次重构中拍板归引擎，原 wrap_math 的公式已拆为三个
可单独 import 的纯函数文件：

- app.engines.box_surface  盒体六面面积 2×(L×W+L×H+W×H)
- app.engines.paper_area   折边系数乘出 paper_m2
- app.engines.ribbon       捆扎丝带米数 ribbon_m

本模块仅为旧 import 路径转调，算纸服务直接 import 上面三个引擎。
"""

from app.engines.box_surface import box_surface, surface_area
from app.engines.paper_area import paper_area, paper_m2, paper_result
from app.engines.ribbon import ribbon_estimate, ribbon_m

__all__ = [
    "surface_area",
    "box_surface",
    "paper_result",
    "paper_m2",
    "paper_area",
    "ribbon_m",
    "ribbon_estimate",
]
