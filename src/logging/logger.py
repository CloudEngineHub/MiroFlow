# SPDX-FileCopyrightText: 2025 MiromindAI
#
# SPDX-License-Identifier: Apache-2.0

import logging
from functools import lru_cache
from typing import Literal

import hydra
from rich.console import Console
from rich.logging import RichHandler


@lru_cache
def bootstrap_logger(
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | int = "INFO",
    logger: logging.Logger | None = None,
) -> logging.Logger:
    """Configure only this logger, not the root logger"""
    if logger is None:
        logger = logging.getLogger("miroflow")
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # use rich for better readability of stack trace.
    handler = RichHandler(
        console=Console(
            stderr=True,
            width=200,
            color_system=None,  # Disable colors to avoid ANSI escape sequences in log files
            force_terminal=False,  # Don't force terminal mode
            legacy_windows=False,
        ),
        rich_tracebacks=True,
        tracebacks_suppress=[hydra],
        tracebacks_show_locals=True,
        show_level=False,
    )
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False

    return logger
