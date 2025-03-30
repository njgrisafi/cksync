import json
from importlib import resources
from pathlib import Path
from typing import Any

import pytest

from cksync.pyproject.lockfiles.poetry_lock import PoetryLockfile
from cksync.pyproject.lockfiles.tests import test_data


@pytest.fixture
def example_poetry_lockfile() -> Path:
    return Path(str(resources.files(test_data).joinpath("poetry.lock")))


@pytest.fixture
def expected_dependencies() -> Any:
    return json.loads(Path(str(resources.files(test_data).joinpath("poetry_lock_dependencies.json"))).read_text())


def test_read(example_poetry_lockfile: Path) -> None:
    lockfile = PoetryLockfile(example_poetry_lockfile)
    contents = lockfile._read()
    assert contents is not None
    assert isinstance(contents, dict)


def test_parse_dependencies(example_poetry_lockfile: Path, expected_dependencies: Any) -> None:
    lockfile = PoetryLockfile(example_poetry_lockfile)
    dependencies = lockfile.parse_dependencies()
    assert len(dependencies) == len(expected_dependencies)
    encoded_dependencies = [dependency.encode() for dependency in dependencies]
    assert encoded_dependencies == expected_dependencies
