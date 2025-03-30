import json
from unittest.mock import MagicMock

from cksync import check as cksync_check
from cksync.pyproject.lockfiles._base import DEFAULT_SOURCE, LockedDependency, LockFileName


def test_add_dependency() -> None:
    dep_universe = cksync_check.DependencyUniverse([LockFileName.POETRY, LockFileName.UV])
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.UV,
    )
    dep_universe.add_dependency(
        LockedDependency(name="test-2", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    assert dep_universe.dependency_system == {
        "test": {"poetry_version": "1.0.0", "uv_version": "1.0.0"},
        "test-2": {"poetry_version": "1.0.0", "uv_version": None},
    }


def test_get_diffs() -> None:
    dep_universe = cksync_check.DependencyUniverse([LockFileName.POETRY, LockFileName.UV])
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.UV,
    )
    dep_universe.add_dependency(
        LockedDependency(name="test-2", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    assert dep_universe.get_diffs() == {
        "test-2": {"poetry_version": "1.0.0", "uv_version": None},
    }


def test_to_json() -> None:
    dep_universe = cksync_check.DependencyUniverse([LockFileName.POETRY, LockFileName.UV])
    dep_universe.add_dependency(
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
        lockfile_name=LockFileName.POETRY,
    )
    assert dep_universe.to_json() == json.dumps({"test": {"poetry_version": "1.0.0", "uv_version": None}}, indent=2)


def test_check_lockfiles() -> None:
    mock_poetry_lockfile = MagicMock()
    mock_uv_lockfile = MagicMock()
    mock_poetry_lockfile.name = LockFileName.POETRY
    mock_uv_lockfile.name = LockFileName.UV
    mock_poetry_lockfile.parse_dependencies.return_value = [
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
    ]
    mock_uv_lockfile.parse_dependencies.return_value = [
        LockedDependency(name="test", version="1.0.0", source=DEFAULT_SOURCE, artifacts=[]),
    ]
    dep_universe = cksync_check.check_lockfiles([mock_poetry_lockfile, mock_uv_lockfile])
    assert dep_universe.dependency_system == {
        "test": {"poetry_version": "1.0.0", "uv_version": "1.0.0"},
    }
