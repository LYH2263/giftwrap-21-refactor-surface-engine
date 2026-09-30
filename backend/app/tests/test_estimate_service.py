"""服务层：校验后顺序调用引擎；保存入库读回须与同参预览一致。直接调函数，不经 HTTP。"""
import pytest
from fastapi import HTTPException

from app.repositories import history as history_repo
from app.services import estimate_service

# 种子书型盒 id=1，0.30×0.20×0.15；脏数据盒 id=3
BOOK_BOX_ID = 1
DIRTY_BOX_ID = 3


def test_book_box_preview_bit_identical():
    prev = estimate_service.run_estimate(BOOK_BOX_ID, 1.15, "cross", False, "")
    assert prev["box_surface"] == 0.27
    assert prev["paper_m2"] == 0.31
    assert prev["ribbon"]["ribbon_m"] == 2.2


def test_default_overlap_matches_explicit():
    # settings 种子 overlap=1.15，缺省路径与显式传参必须同值
    prev_default = estimate_service.run_estimate(BOOK_BOX_ID, None, "cross", False, "")
    prev_explicit = estimate_service.run_estimate(BOOK_BOX_ID, 1.15, "cross", False, "")
    assert prev_default["paper_m2"] == prev_explicit["paper_m2"] == 0.31


def test_saved_run_readback_matches_preview():
    preview = estimate_service.run_estimate(BOOK_BOX_ID, 1.15, "cross", False, "")
    saved = estimate_service.run_estimate(BOOK_BOX_ID, 1.15, "cross", True, "一致性核对")
    runs = {r["id"]: r for r in history_repo.list_runs()}
    stored = runs[saved["run_id"]]["result"]
    assert stored["paper_m2"] == preview["paper_m2"]
    assert stored["box_surface"] == preview["box_surface"]
    assert stored["ribbon"]["ribbon_m"] == preview["ribbon"]["ribbon_m"]


def test_unknown_wrap_style_returns_422():
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(BOOK_BOX_ID, 1.15, "diagonal", False, "")
    assert exc.value.status_code == 422


def test_dirty_box_rejected():
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(DIRTY_BOX_ID, 1.15, "cross", False, "")
    assert exc.value.status_code == 422


def test_missing_box_returns_404():
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(9999, 1.15, "cross", False, "")
    assert exc.value.status_code == 404
