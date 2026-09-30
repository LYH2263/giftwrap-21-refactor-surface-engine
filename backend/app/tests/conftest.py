import os
import tempfile

import pytest

# 必须在 app.config 被导入前指向临时库，测试不碰真实数据
_tmp = tempfile.mkdtemp(prefix="giftwrap-test-")
os.environ.setdefault("DATA_DIR", _tmp)

from app import seed  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _seeded_db():
    seed.init_db()
