"""Every test runs without the caller's GIT_* variables (HL-64).

Under a pre-commit hook, git exports GIT_DIR, GIT_INDEX_FILE and others; a test whose processes ran git
with them would act on the repository being committed.
"""
import os

import pytest


@pytest.fixture(autouse=True)
def no_inherited_git_environment(monkeypatch):
    for k in [k for k in os.environ if k.startswith("GIT_")]:
        monkeypatch.delenv(k)
