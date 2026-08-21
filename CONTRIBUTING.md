# Contributing

## Setup

Fork and clone the repository, then create a focused branch:

```bash
uv sync --locked --all-groups
```

The native MetaTrader5 package is installed only on Windows. The package and its
fake-adapter tests remain usable on other platforms.

## Before A Pull Request

```bash
uv run ruff format src tests examples
uv run ruff check src tests examples
uv run mypy src
uv run pytest
uv run mkdocs build --strict
uv build
```

Add tests at the public `MT5` seam. Native-shaped fake responses are preferred to
mocking implementation modules because they verify failure classification and
payload conversion.

## Pull Requests

- Explain the user-visible behavior and why the change belongs in the wrapper.
- Link relevant official MQL5 documentation for native semantics.
- Keep trading examples read-only unless execution is the specific subject.
- Never include credentials, account identifiers, terminal paths, or broker data.
- Update `CHANGELOG.md` for user-visible changes.

By contributing, you agree that your contribution is licensed under the MIT
License.
