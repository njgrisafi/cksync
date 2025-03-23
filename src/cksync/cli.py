import sys
from argparse import ArgumentParser, HelpFormatter, Namespace
from collections.abc import Sequence
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TYPE_CHECKING

from cksync.lockfiles.poetry_lock import PoetryLockfile
from cksync.lockfiles.uv_lock import UvLockfile

if TYPE_CHECKING:
    from cksync.lockfiles._base import Lockfile


class CkSyncNamespace(Namespace):
    version: str
    verbose: bool
    uv_lock: Path
    poetry_lock: Path


def get_version() -> str:
    try:
        return version("cksync")
    except PackageNotFoundError:
        return "dev"


def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(formatter_class=HelpFormatter)
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--uv-lock", type=Path)
    parser.add_argument("--poetry-lock", type=Path)
    return parser


def main(args: Sequence[str]) -> None:
    parser = get_arg_parser()
    namespace = parser.parse_args(args, CkSyncNamespace)

    if namespace.version:
        print(get_version())
        return

    total_lockfiles = 0
    lock_files: list[Lockfile] = []
    if namespace.uv_lock:
        lock_files.append(UvLockfile(namespace.uv_lock))
        total_lockfiles += 1
    if namespace.poetry_lock:
        lock_files.append(PoetryLockfile(namespace.poetry_lock))
        total_lockfiles += 1

    if total_lockfiles == 0:
        parser.error("No lockfile provided")
    elif total_lockfiles == 1:
        parser.error("Only one lockfile provided. We need at least two to compare.")

    first_lockfile_dependencies: dict[str, str] = {}
    for d in lock_files[0].parse_dependencies():
        first_lockfile_dependencies[d.name] = d.version

    second_lockfile_dependencies: dict[str, str] = {}
    for d in lock_files[1].parse_dependencies():
        second_lockfile_dependencies[d.name] = d.version

    for n, v in second_lockfile_dependencies.items():
        if n in first_lockfile_dependencies:
            if v != first_lockfile_dependencies[n]:
                print(f"verison mismatch {n}!")
                print(f"{n} {v} != {first_lockfile_dependencies[n]}")
        else:
            print(f"{n} is not in the first lockfile")
        print("Verified", n)


if __name__ == "__main__":
    main(sys.argv[1:])
