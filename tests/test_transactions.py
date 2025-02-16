import pytest
from app import create_window

def test_window_creation():
    assert create_window() is None
