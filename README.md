# cksync

<img src="https://raw.githubusercontent.com/njgrisafi/cksync/refs/heads/main/docs/logo.png" alt="cksync Logo" width="250" />

`cksync` verifies that your Python project's lockfiles contain the same packages and versions across different dependency management tools. This is especially useful when migrating between tools.

Dependency management tools can resolve dependencies differently. Fortunately, they all store their resolved dependencies in lockfiles. `cksync` analyzes these lockfiles to:

- Find any version mismatches between tools
- Report detailed differences when found
- Build confidence for safe tool migration

For example, when moving from [Poetry](https://python-poetry.org/docs/) to [uv](https://docs.astral.sh/uv/), `cksync` ensures your `poetry.lock` and `uv.lock` files specify the same versions for all packages, helping you avoid unexpected issues during the migration process.

## Features

- 🚀 **Fast Validation**: Static analysis; no environment creation required
- 🔒 **Build Confidence**: Catch version mismatches before they cause production issues
- 🔄 **Smooth Migrations**: Safely transition between tools like Poetry and uv
- 👥 **Team Flexibility**: Allow team members to use their preferred tools while maintaining consistency

## Installation

```bash
pip install cksync
```

## Usage

Basic comparison of lockfiles in current directory:
```bash
cksync
```

With custom paths:
```bash
cksync --uv-lock uv.lock --poetry-lock poetry.lock --pyproject-toml pyproject.toml
```

if you don't have a `pyproject.toml` you can pass in your project name:
```bash
cksync --uv-lock uv.lock --poetry-lock poetry.lock --project-name my-project
```

Try out our example
```bash
cksync --poetry-lock src/examples/uv-poetry/poetry.lock --uv-lock src/examples/uv-poetry/uv.lock --pyproject-toml src/examples/uv-poetry/pyproject.toml
```

## Recommendations

Migrating between Python dependency management tools can be challenging, especially for large applications. Some recommendations:
- Use [PEP-621](https://peps.python.org/pep-0621/) for cross tool compatibility
- Run both tools in parallel during migration periods
- Support developers using different tools during transition phases
- Pin your dependency versions
- Use `cksync` to validate lockfile consistency before deployments

If you are smaller project likely you don't need `cksync` but it doesn't hurt to check.

## License

`cksync` is licensed under the MIT License. See the [LICENSE](https://raw.githubusercontent.com/njgrisafi/cksync/refs/heads/main/LICENSE) file for more details.

## Authors

- **Nick Grisafi** - [njgrisafi@gmail.com](mailto:njgrisafi@gmail.com)


## Acknowledgments

- Thanks to [Rich](https://github.com/Textualize/rich) for making terminal output beautiful and helping developers create better CLI experiences.
