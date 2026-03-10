"""Tests for CLI module."""

from pyforge.cli import main


def test_main_runs() -> None:
    """Test that main function runs without error."""
    try:
        main()
    except SystemExit:
        pass
