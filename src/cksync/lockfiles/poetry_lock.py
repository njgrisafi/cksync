import tomllib
from typing import Any

from cksync.lockfiles._base import LockedArtifact, LockedDependency, Lockfile


class PoetryLockfile(Lockfile):
    def parse_dependencies(self) -> list[LockedDependency]:
        lock_file = self.read()
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
                    source="https://pypi.org/simple",
                    artifacts=artifacts,
                )
            )
        return dependencies

    def read(self) -> dict[str, Any]:
        return tomllib.load(self.path.open("rb"))
