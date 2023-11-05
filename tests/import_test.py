from __future__ import annotations

import importlib


def test_import():
    import observer

    del observer


def test_version():
    import observer

    assert observer.__version__ == importlib.metadata.version("observer")
