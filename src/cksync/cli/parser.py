from argparse import ArgumentParser, HelpFormatter, Namespace
from pathlib import Path

PROG = "cksync"
UV_LOCK_DEFAULT = Path("uv.lock")
POETRY_LOCK_DEFAULT = Path("poetry.lock")
PYPROJECT_TOML_DEFAULT = Path("pyproject.toml")


class CkSyncNamespace(Namespace):
    version: str
    verbose: bool
    uv_lock: Path
    poetry_lock: Path
    pyproject_toml: Path
    project_name: str
    not_pretty: bool


def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(prog=PROG, formatter_class=HelpFormatter)
    parser.add_argument("--version", action="store_true", help="Show version and exit.")
    parser.add_argument("--verbose", action="store_true", help="Show verbose output.")
    parser.add_argument("--uv-lock", type=Path, default=UV_LOCK_DEFAULT, help="Path to uv.lock file.")
    parser.add_argument("--poetry-lock", type=Path, default=POETRY_LOCK_DEFAULT, help="Path to poetry.lock file.")
    parser.add_argument(
        "--pyproject-toml",
        type=Path,
        default=PYPROJECT_TOML_DEFAULT,
        help="Optional path to pyproject.toml to extract the project details.",
    )
    parser.add_argument("--project-name", type=str, default="", help="Optional project name to include in parsing.")
    parser.add_argument("--not-pretty", action="store_true", help="Print the json output, none of that fancy stuff.")
    return parser


def validate_arguments(parser: ArgumentParser, namespace: CkSyncNamespace) -> None:
    errors = []
    if namespace.uv_lock.exists() is False:
        errors.append(f"{namespace.uv_lock} does not exist")
    if namespace.poetry_lock.exists() is False:
        errors.append(f"{namespace.poetry_lock} does not exist")

    if errors:
        parser.error(" and ".join(errors))
