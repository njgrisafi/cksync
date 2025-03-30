from collections.abc import Iterator
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import pytest

from cksync.cli import main as main_cli
from cksync.cli.parser import POETRY_LOCK_DEFAULT, UV_LOCK_DEFAULT


@pytest.fixture
def mock_version() -> Iterator[MagicMock]:
    with patch.object(main_cli, main_cli.version.__name__) as mock_version:
        yield mock_version


@pytest.fixture
def mock_cli_result() -> Iterator[MagicMock]:
    with patch.object(main_cli, main_cli.CLIResult.__name__) as mock_cli_result:
        yield mock_cli_result


@pytest.fixture
def mock_check_lockfiles() -> Iterator[MagicMock]:
    with patch.object(main_cli, main_cli.check_lockfiles.__name__) as mock_check_lockfiles:
        yield mock_check_lockfiles


@pytest.fixture
def mock_uv_lockfile() -> Iterator[MagicMock]:
    with patch.object(main_cli, main_cli.UvLockfile.__name__) as mock_uv_lockfile:
        yield mock_uv_lockfile


@pytest.fixture
def mock_poetry_lockfile() -> Iterator[MagicMock]:
    with patch.object(main_cli, main_cli.PoetryLockfile.__name__) as mock_poetry_lockfile:
        yield mock_poetry_lockfile


@pytest.fixture
def mock_pyproject_toml() -> Iterator[MagicMock]:
    with patch.object(main_cli, main_cli.PyprojectToml.__name__) as mock_pyproject_toml:
        yield mock_pyproject_toml


@pytest.fixture
def mock_validate_arguments() -> Iterator[MagicMock]:
    with patch.object(main_cli, main_cli.validate_arguments.__name__) as mock_validate_arguments:
        yield mock_validate_arguments


def test_cli_version(mock_version: MagicMock, mock_cli_result: MagicMock) -> None:
    mock_version.return_value = "1.0.0"

    exit_code = main_cli.cli(["--version"])

    assert exit_code == 0
    mock_version.assert_called_once()
    mock_cli_result.return_value.output_version.assert_called_once_with("1.0.0")


def test_cli_version_dev(mock_version: MagicMock, mock_cli_result: MagicMock) -> None:
    mock_version.side_effect = PackageNotFoundError

    exit_code = main_cli.cli(["--version"])

    assert exit_code == 0
    mock_version.assert_called_once()
    mock_cli_result.return_value.output_version.assert_called_once_with("(dev)")


def test_cli_pyproject_toml_exists(
    mock_validate_arguments: MagicMock,
    mock_cli_result: MagicMock,
    mock_check_lockfiles: MagicMock,
    mock_pyproject_toml: MagicMock,
    mock_uv_lockfile: MagicMock,
    mock_poetry_lockfile: MagicMock,
) -> None:
    mock_pyproject_toml.from_file.return_value = MagicMock(get_project_name=lambda: "pyproject_name")
    mock_cli_result.return_value.get_diffs.return_value = []

    with TemporaryDirectory() as temp_dir:
        pyproject_toml = Path(temp_dir).joinpath("pyproject.toml")
        pyproject_toml.touch()
        exit_code = main_cli.cli(["--pyproject-toml", str(pyproject_toml)])

    assert exit_code == 0
    mock_uv_lockfile.assert_called_once_with(UV_LOCK_DEFAULT, "pyproject_name")
    mock_poetry_lockfile.assert_called_once_with(POETRY_LOCK_DEFAULT, "pyproject_name")


def test_cli_project_name(
    mock_validate_arguments: MagicMock,
    mock_cli_result: MagicMock,
    mock_check_lockfiles: MagicMock,
    mock_pyproject_toml: MagicMock,
    mock_uv_lockfile: MagicMock,
    mock_poetry_lockfile: MagicMock,
) -> None:
    mock_pyproject_toml.from_file.return_value = MagicMock(get_project_name=lambda: "pyproject_name")
    mock_cli_result.return_value.get_diffs.return_value = []

    with TemporaryDirectory() as temp_dir:
        pyproject_toml = Path(temp_dir).joinpath("pyproject.toml")
        pyproject_toml.touch()
        exit_code = main_cli.cli(["--project-name", "test", "--pyproject-toml", str(pyproject_toml)])

    assert exit_code == 0
    mock_uv_lockfile.assert_called_once_with(UV_LOCK_DEFAULT, "test")
    mock_poetry_lockfile.assert_called_once_with(POETRY_LOCK_DEFAULT, "test")


def test_cli_success(
    mock_validate_arguments: MagicMock,
    mock_cli_result: MagicMock,
    mock_check_lockfiles: MagicMock,
) -> None:
    exit_code = main_cli.cli([])

    assert exit_code == 0
    mock_validate_arguments.assert_called_once()
    mock_cli_result.assert_called_once()
    mock_cli_result.return_value.output_success.assert_called_once()


def test_cli_error(
    mock_validate_arguments: MagicMock,
    mock_cli_result: MagicMock,
    mock_check_lockfiles: MagicMock,
) -> None:
    mock_response = MagicMock()
    mock_response.get_diffs.return_value = ["error"]
    mock_check_lockfiles.return_value = mock_response

    exit_code = main_cli.cli([])
    assert exit_code == 1
    mock_validate_arguments.assert_called_once()
    mock_cli_result.assert_called_once()
    mock_cli_result.return_value.output_error.assert_called_once_with(["error"])
