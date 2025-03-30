import tomllib
from pathlib import Path
from typing import Any

from cksync._type_utils import verify_type


class PyprojectToml:
    def __init__(self, contents: dict[str, Any]):
        self.contents = contents

    @classmethod
    def from_file(cls, path: Path) -> "PyprojectToml":
        contents = tomllib.load(path.open("rb"))
        return cls(contents=contents)

    def get_project_name(self) -> str:
        if "project" in self.contents:
            project = verify_type(self.contents["project"], dict)
            return verify_type(project.get("name", ""), str)
        tools = verify_type(self.contents["tool"], dict)
        if "poetry" in tools:
            poetry = verify_type(tools["poetry"], dict)
            return verify_type(poetry.get("name", ""), str)
        return ""
