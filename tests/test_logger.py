"""Test the core logger instance."""

import pytest

from logaroo import Logger, console
from logaroo import logger as original_logger

LOG_LEVELS = ["trace", "debug", "info", "success", "warning", "error", "critical"]


@pytest.fixture
def plain_logger() -> Logger:
    """Create a logger that logs with builtin print."""
    return Logger(
        level=original_logger.level,
        template=original_logger.template,
        console=console.get_print_console(),
        levels=list(original_logger.levels.values()),
    )


@pytest.fixture
def rich_logger() -> Logger:
    """Create a logger that logs with builtin print."""
    return Logger(
        level=original_logger.level,
        template=original_logger.template,
        console=console.get_rich_console(),
        levels=list(original_logger.levels.values()),
    )


@pytest.fixture
def logger() -> Logger:
    """Create a logger that is reset between each test."""
    return Logger(
        level=original_logger.level,
        template=original_logger.template,
        console=original_logger.console,
        levels=list(original_logger.levels.values()),
    )


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_can_plain_log_to_level(
    plain_logger: Logger, level: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test that logger.trace() is available."""
    plain_logger.level = level
    log = getattr(plain_logger, level)
    log("test")

    stdout = capsys.readouterr().out
    assert "test" in stdout
    assert level.upper() in stdout


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_can_rich_log_to_level(
    rich_logger: Logger, level: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test that logger.trace() is available."""
    rich_logger.level = level
    log = getattr(rich_logger, level)
    log("test")

    stdout = capsys.readouterr().out
    assert "test" in stdout
    assert level.upper() in stdout


def test_logging_to_invisible_level(
    logger: Logger, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test that logging to a level below the current level doesn't print anything."""
    logger.log("debug", "test")

    stdout = capsys.readouterr().out
    assert stdout == ""


def test_formatting_of_log_message(
    plain_logger: Logger, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test that we can use str.format() in log messages."""
    plain_logger.info(
        "This is a {adjective} test: {pi:.3f}", adjective="fun", pi=3.14159
    )

    stdout = capsys.readouterr().out.strip()
    assert stdout.endswith("This is a fun test: 3.142")


def test_setting_new_level(logger: Logger) -> None:
    """Test that we can set a new level."""
    logger.level = "warning"
    assert logger.level == "warning"


def test_setting_nonexistent_level_raises(logger: Logger) -> None:
    """Test that setting a level that doesn't exists raises an error."""
    with pytest.raises(ValueError, match="unknown level 'nonexistent'"):
        logger.level = "nonexistent"


def test_available_errors_shown_in_error(logger: Logger) -> None:
    """Test that error message when setting a level lists all available levels."""
    for level in LOG_LEVELS:
        with pytest.raises(ValueError, match=level):
            logger.level = "nonexistent"


def test_setting_level_with_mixed_case(logger: Logger) -> None:
    """Test that when setting a level, the name is converted to lower case."""
    logger.level = "DeBUg"
    assert logger.level == "debug"


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_level_is_listed_in_dir(logger: Logger, level: str) -> None:
    """Test that all log levels are listed as available methods on the logger."""
    assert level in dir(logger)


def test_add_new_level(logger: Logger, capsys: pytest.CaptureFixture[str]) -> None:
    """Test that a new level can be added."""
    logger.add_level("test", no=42, color="[green]", icon="\N{TEST TUBE}")
    logger.level = "test"
    assert logger.level == "test"

    assert "test" in dir(logger)
    with pytest.raises(ValueError, match="test"):
        logger.level = "nonexistent"

    logger.test("test new level")
    stdout = capsys.readouterr().out
    assert "test new level" in stdout


def test_log_to_all_levels(logger: Logger, capsys: pytest.CaptureFixture[str]) -> None:
    """Test that log_to_all_levels() shows all levels."""
    logger.log_to_all_levels()

    stdout = capsys.readouterr().out
    for level in LOG_LEVELS:
        assert level.upper() in stdout
