"""Tests for the Wolt integration __init__ module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.wolt import PLATFORMS
from custom_components.wolt.const import DOMAIN


def test_platforms_constant():
    """Test that PLATFORMS contains expected platforms."""
    assert "sensor" in PLATFORMS
    assert "binary_sensor" in PLATFORMS
    assert "button" in PLATFORMS


def test_platforms_list():
    """Test that PLATFORMS is a list with 3 items."""
    assert len(PLATFORMS) == 3
