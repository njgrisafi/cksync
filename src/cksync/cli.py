import json
import sys
from argparse import ArgumentParser, HelpFormatter, Namespace
from collections.abc import Sequence
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from rich.console import Console
from rich.json import JSON
from rich.panel import Panel

from cksync.check import check_lockfiles
from cksync.lockfiles.poetry_lock import PoetryLockfile
from cksync.lockfiles.uv_lock import UvLockfile

PROG = "cksync"
UV_LOCK_DEFAULT = Path("uv.lock")
POETRY_LOCK_DEFAULT = Path("poetry.lock")


class CkSyncNamespace(Namespace):
    version: str
    verbose: bool
    uv_lock: Path
    poetry_lock: Path
    project_name: str
    not_pretty: bool


def get_version() -> str:
    try:
        return f"{PROG} {version(PROG)}"
    except PackageNotFoundError:
        return f"{PROG} (dev)"


def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(prog=PROG, formatter_class=HelpFormatter)
    parser.add_argument("--version", action="store_true", help="Show version and exit.")
    parser.add_argument("--verbose", action="store_true", help="Show verbose output.")
    parser.add_argument("--uv-lock", type=Path, default=UV_LOCK_DEFAULT, help="Path to uv.lock file.")
    parser.add_argument("--poetry-lock", type=Path, default=POETRY_LOCK_DEFAULT, help="Path to poetry.lock file.")
    parser.add_argument("--project-name", type=str, default="", help="Optional project name to include in parsing.")
    parser.add_argument("--not-pretty", action="store_true", help="Print the json output, none of that fancy stuff.")
    return parser


def main(args: Sequence[str]) -> None:
    console = Console(stderr=True)
    parser = get_arg_parser()
    namespace = parser.parse_args(args, CkSyncNamespace)

    if namespace.version:
        print(get_version())
        return

    errors = []
    if namespace.uv_lock.exists() is False:
        errors.append(f"{namespace.uv_lock} does not exist")
    if namespace.poetry_lock.exists() is False:
        errors.append(f"{namespace.poetry_lock} does not exist")

    if errors:
        parser.error(" and ".join(errors))

    res = check_lockfiles(
        [
            UvLockfile(namespace.uv_lock, namespace.project_name),
            PoetryLockfile(namespace.poetry_lock, namespace.project_name),
        ]
    )
    diffs = res.get_diffs()

    # Success
    if len(diffs) == 0:
        if namespace.not_pretty:
            console.print(f"{parser.prog} success.")
            return

        package_text = "packages" if len(res.dependency_system) > 1 else "package"
        console.print(
            Panel.fit(
                f"[green bold]Lock files are in sync checked {len(res.dependency_system)} {package_text}[/] :lock:",
                title="Success",
                border_style="green",
            )
        )
        return

    # Error
    if namespace.not_pretty:
        output = json.dumps(diffs, indent=2)
        console.print(output)
        return

    package_text = "packages" if len(diffs) > 1 else "package"
    console.print(
        Panel.fit(
            f"[red bold]Lock file differences found in {len(diffs)} {package_text}[/] :link::broken_heart:",
            title="Error",
            border_style="red",
        )
    )
    output = json.dumps(diffs, indent=2)
    console.print(JSON(output))
    sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
