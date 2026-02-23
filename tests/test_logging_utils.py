from __future__ import annotations

import importlib

logging_mod = importlib.import_module("hiprfish_plb.logging_utils")
get_logger = logging_mod.get_logger


def test_get_logger_is_idempotent() -> None:
    logger_a = get_logger("hiprfish.tests.logger")
    handler_count = len(logger_a.handlers)
    logger_b = get_logger("hiprfish.tests.logger")
    assert logger_a is logger_b
    assert len(logger_b.handlers) == handler_count
