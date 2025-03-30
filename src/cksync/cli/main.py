import sys
from collections.abc import Sequence
from importlib.metadata import PackageNotFoundError, version

from cksync.check import check_lockfiles
from cksync.cli.parser import CkSyncNamespace, get_arg_parser, validate_arguments
from cksync.cli.result import CLIResult
from cksync.pyproject.lockfiles.poetry_lock import PoetryLockfile
from cksync.pyproject.lockfiles.uv_lock import UvLockfile
from cksync.pyproject.pyproject_toml import PyprojectToml


def get_version(prog: str) -> str:
    try:
        return version(prog)
    except PackageNotFoundError:
        return "(dev)"


def cli(args: Sequence[str]) -> int:
    parser = get_arg_parser()
    namespace = parser.parse_args(args, CkSyncNamespace())

    cli_result = CLIResult(parser.prog, namespace)

    if namespace.version:
        cli_result.output_version(get_version(parser.prog))
        return 0

    validate_arguments(parser, namespace)

    if namespace.pyproject_toml.exists() and namespace.project_name == "":
        pyproject_toml = PyprojectToml.from_file(namespace.pyproject_toml)
        namespace.project_name = pyproject_toml.get_project_name()

    res = check_lockfiles(
        [
            UvLockfile(namespace.uv_lock, namespace.project_name),
            PoetryLockfile(namespace.poetry_lock, namespace.project_name),
        ]
    )
    diffs = res.get_diffs()

    # Success
    if len(diffs) == 0:
        cli_result.output_success(res)
        return 0

    # Error
    cli_result.output_error(diffs)
    return 1


def _main() -> None:
    exit_code = cli(sys.argv[1:])
    sys.exit(exit_code)


if __name__ == "__main__":
    _main()
