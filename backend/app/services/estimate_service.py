"""算纸服务：只做校验与顺序编排，不持有任何面积/丝带公式。

公式归属引擎（app.engines 下三个纯函数文件）：
1) box_surface  盒体六面面积
2) paper_need   折边乘出用纸面积
3) ribbon_length 丝带米数
"""
from fastapi import HTTPException

from app.engines.box_surface import box_surface
from app.engines.paper_need import paper_need
from app.engines.ribbon_length import ribbon_length
from app.repositories import boxes, history, settings_repo


def run_estimate(box_id: int, overlap: float | None, wrap_style: str, save: bool, note: str):
    box = boxes.get_box(box_id)
    if not box:
        raise HTTPException(404)
    if box.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty box")

    ov = float(overlap) if overlap is not None else settings_repo.get_overlap()
    try:
        surface = box_surface(box["length"], box["width"], box["height"])
        paper_m2 = paper_need(surface, ov)
        ribbon_m = ribbon_length(box["length"], box["width"], box["height"], wrap_style)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

    calc = {"box_surface": round(surface, 3), "overlap": ov, "paper_m2": paper_m2}
    ribbon = {"wrap_style": wrap_style, "ribbon_m": ribbon_m}
    payload = {**calc, "ribbon": ribbon, "box_id": box_id}
    run_id = history.insert_run(box_id, ov, payload, note) if save else None
    return {"box": box, "run_id": run_id, **calc, "ribbon": ribbon}
