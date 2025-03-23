from __future__ import annotations

from pathlib import Path
from typing import Any

from cksync import json_utils


class Lockfile:
    def __init__(self, path: Path):
        self.path = path

    def read(self) -> dict[str, Any]:
        raise NotImplementedError("Subclass must implement this method")

    def parse_dependencies(self) -> list[LockedDependency]:
        raise NotImplementedError("Subclass must implement this method")


class LockedArtifact:
    def __init__(self, name: str, hash: str):
        self.name = name
        self.hash = hash

    def encode(self) -> dict[str, str]:
        return {"name": self.name, "hash": self.hash}

    @classmethod
    def decode(cls, raw_data: json_utils.JSON_PARSABLE) -> LockedArtifact:
        data = json_utils._verify_type(raw_data, dict)
        return cls(
            name=json_utils._verify_type(data["name"], str),
            hash=json_utils._verify_type(data["hash"], str),
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
    def decode(cls, raw_data: json_utils.JSON_PARSABLE) -> LockedDependency:
        data = json_utils._verify_type(raw_data, dict)
        artifacts: list[LockedArtifact] = []
        for artifact in json_utils._verify_type(data["artifacts"], list):
            artifacts.append(LockedArtifact.decode(json_utils._verify_type(artifact, dict)))
        return cls(
            name=json_utils._verify_type(data["name"], str),
            version=json_utils._verify_type(data["version"], str),
            source=json_utils._verify_type(data["source"], str),
            artifacts=artifacts,
        )
