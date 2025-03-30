import json
from typing import IO

from rich.console import Console
from rich.json import JSON
from rich.panel import Panel

from cksync.check import DependencyUniverse
from cksync.cli.parser import CkSyncNamespace


class CLIResult:
    def __init__(self, prog: str, namespace: CkSyncNamespace, out_file: IO[str] | None = None):
        self.prog = prog
        self.namespace = namespace
        self.out_file = out_file
        if out_file is None:
            self.console = Console(stderr=True)
        else:
            self.console = Console(file=out_file)

    def output_version(self, version: str) -> None:
        self.console.print(f"{self.prog} {version}")

    def output_success(self, dependency_universe: DependencyUniverse) -> None:
        if self.namespace.not_pretty:
            self.console.print(f"{self.prog} success.")
            return

        num_packages = len(dependency_universe.dependency_system)
        package_text = self._get_package_text(num_packages)
        self.console.print(
            Panel.fit(
                f"[green bold]Lock files are in sync checked {num_packages} {package_text}[/] :lock:",
                title="Success",
                border_style="green",
            )
        )
        return

    def output_error(self, diffs: dict[str, dict[str, str | None]]) -> None:
        if self.namespace.not_pretty:
            output = json.dumps(diffs, indent=2)
            self.console.print(output)
            return

        num_packages = len(diffs)
        package_text = self._get_package_text(num_packages)
        self.console.print(
            Panel.fit(
                f"[red bold]Lock file differences found in {num_packages} {package_text}[/] :link::broken_heart:",
                title="Error",
                border_style="red",
            )
        )
        output = json.dumps(diffs, indent=2)
        self.console.print(JSON(output))
        return

    @staticmethod
    def _get_package_text(num_packages: int) -> str:
        return "packages" if num_packages > 1 else "package"
