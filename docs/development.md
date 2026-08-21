# Development

## Setup

```bash
uv sync --locked --all-groups
```

`uv.lock` is committed so local and CI environments resolve the same toolchain.

## Checks

```bash
uv run ruff format src tests examples
uv run ruff check src tests examples
uv run mypy src
uv run pytest
uv run mkdocs build --strict
uv build
```

## Architecture

`MT5` is the external seam. It owns lifecycle, UTC validation, failure
classification, conversion, and resource cleanup. `MT5Adapter` is an internal
seam around the process-global C extension. Production uses `NativeMT5Adapter`;
tests inject a deterministic fake that returns native-shaped replies.

```python
from syntiq_mt5 import AdapterReply, ErrorInfo, MT5

class FakeAdapter:
    def call(self, operation, /, *args, **kwargs):
        if operation == "initialize":
            return AdapterReply(True, ErrorInfo(code=1, message="Success"))
        if operation == "positions_get":
            return AdapterReply((), ErrorInfo(code=1, message="Success"))
        return AdapterReply(None, ErrorInfo(code=1, message="Success"))

with MT5(adapter=FakeAdapter()) as mt5:
    assert mt5.positions() == ()
```

This is intentionally one deep module rather than a public collection of thin
services. A fix to native error handling or payload conversion applies to every
caller.

## CI/CD

- CI runs Ruff, mypy, pytest, strict MkDocs, and package smoke tests.
- The matrix covers Linux and Windows on Python 3.12 and 3.13.
- `main` deploys the MkDocs site to GitHub Pages.
- `v*` tags rerun all release gates and publish through PyPI trusted publishing.
- Dependabot checks uv and GitHub Actions weekly.

See [CONTRIBUTING.md](https://github.com/Lucifer516-sudoer/syntiq_mt5/blob/main/CONTRIBUTING.md)
for the contribution workflow.
