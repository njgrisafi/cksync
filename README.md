# cksync
Concord Lock Sync for Python Dependency Management Tools - Fast static analysis to ensure your Python lockfiles stay in sync.

## Why cksync?

Migrating between Python dependency management tools can be challenging, especially for large applications. Teams often need to:
- Run multiple tools in parallel during migration periods
- Ensure consistent dependencies across different environments
- Validate lockfile consistency before deployments
- Support developers using different tools during transition phases

cksync solves these challenges by statically analyzing your lockfiles to ensure all packages ar ein sycn before you even hit the build phase. This means:

- 🚀 **Fast Validation**: Static analysis without package downloads or environment creation
- 🔒 **Build Confidence**: Catch version mismatches before they cause production issues
- 🔄 **Smooth Migrations**: Safely transition between tools like Poetry and uv
- 👥 **Team Flexibility**: Allow team members to use their preferred tools while maintaining consistency

## Features

- Static comparison of Poetry and uv lockfiles
- Detailed difference reporting with rich terminal output
- CI-friendly with meaningful exit codes

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
cksync --uv-lock uv.lock --poetry-lock poetry.lock --project-name my-project
```
