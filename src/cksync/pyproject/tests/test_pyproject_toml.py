import textwrap
from pathlib import Path
from tempfile import TemporaryDirectory

from cksync.pyproject.pyproject_toml import PyprojectToml


def test_get_project_name_pep_621() -> None:
    contents = textwrap.dedent(
        """
        [project]
        name = "test"
        """
    )
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir).joinpath("pyproject.toml")
        path.write_text(contents)
        pyproject_toml = PyprojectToml.from_file(path)
    assert pyproject_toml.get_project_name() == "test"


def test_get_project_name_poetry() -> None:
    contents = textwrap.dedent(
        """
        [tool.poetry]
        name = "test"
        """
    )
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir).joinpath("pyproject.toml")
        path.write_text(contents)
        pyproject_toml = PyprojectToml.from_file(path)
    assert pyproject_toml.get_project_name() == "test"
