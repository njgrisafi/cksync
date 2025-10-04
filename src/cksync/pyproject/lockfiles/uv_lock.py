import tomllib
from typing import Any

from cksync.pyproject.lockfiles._base import LockedArtifact, LockedDependency, Lockfile, LockFileName


class UvLockfile(Lockfile):
    @property
    def name(self) -> LockFileName:
        return LockFileName.UV

    def _load_dependencies(self) -> list[LockedDependency]:
        dependencies: list[LockedDependency] = []

        lock_file = self._read()

        for package in lock_file.get("package", []):
            # UV always include root package in lockfile, some other tools don't.
            # If the user provided this then let's skip it.
            if package.get("name") == self.project_name:
                continue

            artifacts: list[LockedArtifact] = []
            for artifact in package.get("wheels", []):
                artifacts.append(LockedArtifact(name=artifact["url"].split("/")[-1], hash=artifact["hash"]))

            if "sdist" in package:
                artifacts.append(
                    LockedArtifact(name=package["sdist"]["url"].split("/")[-1], hash=package["sdist"]["hash"])
                )

            source = ""
            if "source" in package:
                if "editable" in package["source"]:
                    source = "editable"
                elif "directory" in package["source"]:
                    source = package["source"]["directory"]
                else:
                    source = package["source"]["registry"]

            dependencies.append(
                LockedDependency(
                    name=package["name"],
                    version=package["version"],
                    source=source,
                    artifacts=artifacts,
                )
            )

        return dependencies

    def _read(self) -> dict[str, Any]:
        return tomllib.load(self.path.open("rb"))
