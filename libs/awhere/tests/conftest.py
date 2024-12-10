# Copyright 2024 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.
# Adapted from [PyDantic AI](https://github.com/pydantic/pydantic-ai/blob/main/tests/conftest.py)
from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from datetime import datetime
from typing import TYPE_CHECKING, Any

import pytest

_all__ = 'IsNow', 'TestEnv'

if TYPE_CHECKING:

    def IsNow(*args: Any, **kwargs: Any) -> datetime:
        """IsNow fixture."""
        ...
else:
    pass

try:
    from logfire.testing import CaptureLogfire
except ImportError:
    pass
else:

    @pytest.fixture(autouse=True)
    def logfire_disable(capfire: CaptureLogfire):
        """Logfire disable fixture."""
        pass


class TestEnv:
    """Test environment."""

    __test__ = False

    def __init__(self):
        self.envars: dict[str, str | None] = {}

    def set(self, name: str, value: str) -> None:
        self.envars[name] = os.getenv(name)
        os.environ[name] = value

    def remove(self, name: str) -> None:
        self.envars[name] = os.environ.pop(name, None)

    def reset(self) -> None:  # pragma: no cover
        for name, value in self.envars.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


@pytest.fixture
def env() -> Iterator[TestEnv]:
    """Test environment fixture."""
    test_env = TestEnv()

    yield test_env

    test_env.reset()


@pytest.fixture
def anyio_backend():
    """AnyIO backend fixture."""
    return 'asyncio'


@pytest.fixture
def set_event_loop() -> Iterator[None]:
    """Set the event loop fixture."""
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    yield
    new_loop.close()
