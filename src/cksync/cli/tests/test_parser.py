from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock

from cksync.cli import parser as cli_parser


def test_validate_arguments_success() -> None:
    mock_parser = MagicMock()
    mock_namespace = MagicMock()
    with TemporaryDirectory() as temp_dir:
        mock_namespace.uv_lock = Path(temp_dir).joinpath(cli_parser.UV_LOCK_DEFAULT)
        mock_namespace.poetry_lock = Path(temp_dir).joinpath(cli_parser.POETRY_LOCK_DEFAULT)
        mock_namespace.uv_lock.touch()
        mock_namespace.poetry_lock.touch()
        cli_parser.validate_arguments(mock_parser, mock_namespace)
    mock_parser.error.assert_not_called()


def test_validate_arguments_error() -> None:
    mock_parser = MagicMock()
    mock_namespace = MagicMock()
    mock_poetry_lock = MagicMock()
    mock_uv_lock = MagicMock()
    mock_poetry_lock.exists.return_value = False
    mock_uv_lock.exists.return_value = False
    mock_namespace.uv_lock = mock_uv_lock
    mock_namespace.poetry_lock = mock_poetry_lock
    cli_parser.validate_arguments(mock_parser, mock_namespace)
    mock_parser.error.assert_called_once_with(
        " and ".join([f"{mock_namespace.uv_lock} does not exist", f"{mock_namespace.poetry_lock} does not exist"])
    )
