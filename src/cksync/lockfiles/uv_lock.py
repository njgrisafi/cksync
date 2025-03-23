import tomllib
from typing import Any

from cksync.lockfiles._base import LockedArtifact, LockedDependency, Lockfile


class UvLockfile(Lockfile):
    def parse_dependencies(self) -> list[LockedDependency]:
        dependencies: list[LockedDependency] = []

        lock_file = self.read()

        for package in lock_file.get("package", []):
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

        return sorted(dependencies, key=lambda x: x.name)

    def read(self) -> dict[str, Any]:
        return tomllib.load(self.path.open("rb"))
