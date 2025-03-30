import textwrap
from io import StringIO
from unittest.mock import Mock

from cksync.check import DependencyUniverse
from cksync.cli import result as cli_result
from cksync.pyproject.lockfiles._base import DEFAULT_SOURCE, LockedDependency, LockFileName


def test_init() -> None:
    mock_namespace = Mock(not_pretty=False)
    cli_result.CLIResult("test", mock_namespace, out_file=None)
    cli_result.CLIResult("test", mock_namespace, out_file=StringIO())


def test_output_success() -> None:
    mock_namespace = Mock(not_pretty=False)
    dep_universe = DependencyUniverse(lockfile_names=[LockFileName.POETRY, LockFileName.UV])
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.UV,
    )
    out_file = StringIO()
    cli_result.CLIResult("test", mock_namespace, out_file=out_file).output_success(dep_universe)
    expected_output = textwrap.dedent(
        """
        ╭────────────────── Success ──────────────────╮
        │ Lock files are in sync checked 1 package 🔒 │
        ╰─────────────────────────────────────────────╯
        """
    ).lstrip()
    assert out_file.getvalue() == expected_output


def test_output_success_not_pretty() -> None:
    mock_namespace = Mock(not_pretty=True)
    dep_universe = DependencyUniverse(lockfile_names=[LockFileName.POETRY, LockFileName.UV])
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.UV,
    )
    out_file = StringIO()
    cli_result.CLIResult("test", mock_namespace, out_file=out_file).output_success(dep_universe)
    assert out_file.getvalue() == "test success.\n"


def test_output_error() -> None:
    mock_namespace = Mock(not_pretty=False)
    dep_universe = DependencyUniverse(lockfile_names=[LockFileName.POETRY, LockFileName.UV])
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    out_file = StringIO()
    cli_result.CLIResult("test", mock_namespace, out_file=out_file).output_error(dep_universe.get_diffs())
    expected_output = textwrap.dedent(
        """
        ╭──────────────────── Error ────────────────────╮
        │ Lock file differences found in 1 package 🔗💔 │
        ╰───────────────────────────────────────────────╯
        {
          "test": {
            "poetry_version": "1.0.0",
            "uv_version": null
          }
        }
        """
    ).lstrip()
    assert out_file.getvalue() == expected_output


def test_output_error_not_pretty() -> None:
    mock_namespace = Mock(not_pretty=True)
    dep_universe = DependencyUniverse(lockfile_names=[LockFileName.POETRY, LockFileName.UV])
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    out_file = StringIO()
    cli_result.CLIResult("test", mock_namespace, out_file=out_file).output_error(dep_universe.get_diffs())
    expected_output = textwrap.dedent(
        """
        {
          "test": {
            "poetry_version": "1.0.0",
            "uv_version": null
          }
        }
        """
    ).lstrip()
    assert out_file.getvalue() == expected_output


def test_get_package_text() -> None:
    assert cli_result.CLIResult._get_package_text(1) == "package"
    assert cli_result.CLIResult._get_package_text(2) == "packages"
