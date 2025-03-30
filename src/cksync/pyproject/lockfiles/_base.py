from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any

from cksync import _type_utils

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

DEFAULT_SOURCE = "https://pypi.org/simple"


class LockFileName(StrEnum):
    POETRY = "poetry"
    UV = "uv"


class Lockfile:
    def __init__(self, path: Path, project_name: str = ""):
        self.project_name = project_name
        self.path = path

    @property
    def name(self) -> LockFileName:
        raise NotImplementedError("Subclass must implement this method")

    def _read(self) -> dict[str, Any]:
        raise NotImplementedError("Subclass must implement this method")

    def _load_dependencies(self) -> list[LockedDependency]:
        raise NotImplementedError("Subclass must implement this method")

    def parse_dependencies(self) -> LockedDependencies:
        return LockedDependencies(dependencies=sorted(self._load_dependencies(), key=lambda x: x.name))


class LockedArtifact:
    def __init__(self, name: str, hash: str):
        self.name = name
        self.hash = hash

    def encode(self) -> dict[str, str]:
        return {"name": self.name, "hash": self.hash}

    @classmethod
    def decode(cls, raw_data: _type_utils.JSON_PARSABLE) -> LockedArtifact:
        data = _type_utils.verify_type(raw_data, dict)
        return cls(
            name=_type_utils.verify_type(data["name"], str),
            hash=_type_utils.verify_type(data["hash"], str),
        )


class LockedDependency:
    def __init__(self, name: str, version: str, source: str, artifacts: list[LockedArtifact]):
        self.name = name
        self.version = version
        self.source = source
        self.artifacts = artifacts

    def encode(self) -> dict[str, str | list[dict[str, str]]]:
        return {
            "name": self.name,
            "version": self.version,
            "source": self.source,
            "artifacts": [artifact.encode() for artifact in self.artifacts],
        }

    @classmethod
    def decode(cls, raw_data: _type_utils.JSON_PARSABLE) -> LockedDependency:
        data = _type_utils.verify_type(raw_data, dict)
        artifacts: list[LockedArtifact] = []
        for artifact in _type_utils.verify_type(data["artifacts"], list):
            artifacts.append(LockedArtifact.decode(_type_utils.verify_type(artifact, dict)))
        return cls(
            name=_type_utils.verify_type(data["name"], str),
            version=_type_utils.verify_type(data["version"], str),
            source=_type_utils.verify_type(data["source"], str),
            artifacts=artifacts,
        )


class LockedDependencies:
    def __init__(self, dependencies: list[LockedDependency]):
        self.dependencies = dependencies

    def encode(self) -> list[dict[str, str | list[dict[str, str]]]]:
        return [dependency.encode() for dependency in self.dependencies]

    @classmethod
    def decode(cls, raw_data: _type_utils.JSON_PARSABLE) -> LockedDependencies:
        data = _type_utils.verify_type(raw_data, list)
        dependencies: list[LockedDependency] = []
        for dependency in data:
            dependencies.append(LockedDependency.decode(_type_utils.verify_type(dependency, dict)))
        return cls(dependencies)

    def __contains__(self, item: Any) -> bool:
        search_name = None
        if isinstance(item, str):
            search_name = item
        elif isinstance(item, LockedDependency):
            search_name = item.name
        else:
            raise ValueError(f"Invalid type: {type(item)} expected str or LockedDependency")

        return any(dependency.name == search_name for dependency in self.dependencies)

    def __getitem__(self, item: Any) -> LockedDependency:
        search_name = None
        if isinstance(item, str):
            search_name = item
        elif isinstance(item, LockedDependency):
            search_name = item.name
        else:
            raise ValueError(f"Invalid type: {type(item)} expected str or LockedDependency")

        for dependency in self.dependencies:
            if dependency.name == search_name:
                return dependency
        raise KeyError(f"Dependency {search_name} not found")

    def __iter__(self) -> Iterator[LockedDependency]:
        return iter(self.dependencies)

    def __len__(self) -> int:
        return len(self.dependencies)
