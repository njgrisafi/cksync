import json
from importlib import resources
from pathlib import Path
from typing import Any

import pytest

from cksync.lockfiles.tests import test_data
from cksync.lockfiles.uv_lock import UvLockfile


@pytest.fixture
def example_uv_lockfile() -> Path:
    return Path(str(resources.files(test_data).joinpath("uv.lock")))


@pytest.fixture
def expected_dependencies() -> Any:
    return json.loads(Path(str(resources.files(test_data).joinpath("uv_lock_dependencies.json"))).read_text())


def test_read(example_uv_lockfile: Path) -> None:
    lockfile = UvLockfile(example_uv_lockfile)
    contents = lockfile._read()
    assert contents is not None
    assert isinstance(contents, dict)


def test_parse_dependencies(example_uv_lockfile: Path, expected_dependencies: Any) -> None:
    lockfile = UvLockfile(example_uv_lockfile)
    dependencies = lockfile.parse_dependencies()
    assert len(dependencies) == len(expected_dependencies)
    encoded_dependencies = [dependency.encode() for dependency in dependencies]
    assert encoded_dependencies == expected_dependencies


def test_parse_dependencies_with_project_name(example_uv_lockfile: Path, expected_dependencies: Any) -> None:
    project_name = "pytest-checkpoint"
    lockfile = UvLockfile(example_uv_lockfile, project_name=project_name)
    dependencies = lockfile.parse_dependencies()

    # remove the project from exptected dependencies
    expected_dependencies = [dep for dep in expected_dependencies if dep["name"] != project_name]

    assert len(dependencies) == len(expected_dependencies)
    encoded_dependencies = [dependency.encode() for dependency in dependencies]
    assert encoded_dependencies == expected_dependencies
