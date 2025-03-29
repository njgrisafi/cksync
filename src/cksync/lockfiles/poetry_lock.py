import tomllib
from typing import Any

from cksync.lockfiles._base import DEFAULT_SOURCE, LockedArtifact, LockedDependency, Lockfile


class PoetryLockfile(Lockfile):
    @property
    def name(self) -> str:
        return "poetry"

    def _load_dependencies(self) -> list[LockedDependency]:
        lock_file = self._read()
        dependencies: list[LockedDependency] = []
        for package in lock_file.get("package", []):
            artifacts: list[LockedArtifact] = []
            if "files" in package:
                for f in package["files"]:
                    artifacts.append(LockedArtifact(name=f["file"], hash=f["hash"]))
            dependencies.append(
                LockedDependency(
                    name=package["name"],
                    version=package["version"],
                    source=DEFAULT_SOURCE,
                    artifacts=artifacts,
                )
            )
        return dependencies

    def _read(self) -> dict[str, Any]:
        return tomllib.load(self.path.open("rb"))
