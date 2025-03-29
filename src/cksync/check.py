import json

from cksync.lockfiles._base import LockedDependency, Lockfile


class DependencyUniverse:
    dependency_system: dict[str, dict[str, str | None]] = {}

    def __init__(self, lockfile_names: list[str]):
        self.lockfile_names = lockfile_names

    def add_dependency(self, dependency: LockedDependency, lockfile_name: str) -> None:
        if dependency.name not in self.dependency_system:
            self.dependency_system[dependency.name] = {}
            for n in self.lockfile_names:
                self.dependency_system[dependency.name][f"{n}_version"] = None
        self.dependency_system[dependency.name][f"{lockfile_name}_version"] = dependency.version

    def get_diffs(self) -> dict[str, dict[str, str | None]]:
        diffs = {}
        for dependency_name, tool_records in self.dependency_system.items():
            seen_record: set[str | None] = set()
            for tool_record in tool_records.values():
                if len(seen_record) == 0:
                    seen_record.add(tool_record)
                    continue
                if tool_record in seen_record:
                    continue
                diffs[dependency_name] = tool_records
                break
        return diffs

    def to_json(self) -> str:
        return json.dumps(self.dependency_system, indent=2)


def check_lockfiles(lockfiles: list[Lockfile]) -> DependencyUniverse:
    dep_universe = DependencyUniverse([lf.name for lf in lockfiles])
    for lockfile in lockfiles:
        locked_dependencies = lockfile.parse_dependencies()
        for dependency in locked_dependencies:
            dep_universe.add_dependency(dependency, lockfile.name)
    return dep_universe
