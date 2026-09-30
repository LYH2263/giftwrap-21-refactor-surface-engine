from fastapi import HTTPException
from app.engines.box_surface import surface_area
from app.engines.paper_area import paper_result
from app.engines.ribbon import ribbon_estimate
from app.repositories import boxes, history, settings_repo


def run_estimate(box_id: int, overlap: float | None, wrap_style: str, save: bool, note: str):
    # —— 校验：盒存在性、数据质量；公式一律不进服务层 ——
    box = boxes.get_box(box_id)
    if not box:
        raise HTTPException(404)
    if box.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty box")
    ov = float(overlap) if overlap is not None else settings_repo.get_overlap()

    # —— 顺序调用三个纯函数引擎：六面面积 → 折边用纸 → 丝带 ——
    # 本函数体内不允许出现盒面公式或围长丝带的内联算术，全部归引擎。
    try:
        surface = surface_area(box["length"], box["width"], box["height"])
        calc = paper_result(surface, ov)
        ribbon = ribbon_estimate(box["length"], box["width"], box["height"], wrap_style)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

    payload = {**calc, "ribbon": ribbon, "box_id": box_id}
    run_id = history.insert_run(box_id, ov, payload, note) if save else None
    return {"box": box, "run_id": run_id, **calc, "ribbon": ribbon}
