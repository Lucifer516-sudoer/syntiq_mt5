# Releasing To PyPI

Releases are tag-driven and use PyPI trusted publishing. No long-lived PyPI API
token is stored in GitHub.

## One-Time PyPI Setup

Create a pending publisher for `syntiq-mt5` in PyPI with these values:

| Setting | Value |
| --- | --- |
| Owner | `Lucifer516-sudoer` |
| Repository | `syntiq_mt5` |
| Workflow | `release.yml` |
| Environment | `pypi` |

Create a protected GitHub environment named `pypi`. Requiring a reviewer for
that environment adds a manual approval before publication.

## Release Checklist

1. Update `version` in `pyproject.toml`.
2. Add the dated release entry to `CHANGELOG.md`.
3. Run the complete local verification suite.
4. Merge the release changes to `main`.
5. Create and push an exact matching tag, such as `v0.2.0`.

```bash
uv sync --locked --all-groups
uv run ruff format --check src tests examples scripts
uv run ruff check src tests examples scripts
uv run mypy src
uv run pytest
uv run mkdocs build --strict
uv build --clear
uv run python scripts/check_wheel.py dist/*.whl
```

The release workflow rejects malformed tags, tags that do not match the package
version, and commits that are not already on `main`. It reruns quality checks,
builds wheel and source distributions, checks the wheel architecture, installs
the wheel in isolation, then publishes through OpenID Connect.

!!! warning
    Test the first release against TestPyPI or a disposable package name if you
    want to validate publisher configuration before claiming the final project.
