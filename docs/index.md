---
title: Syntiq MT5
hide:
  - navigation
  - toc
---

<section class="syntiq-hero" markdown>
<div class="syntiq-hero__copy" markdown>

<span class="syntiq-eyebrow">PYTHON &times; METATRADER 5</span>

# Trade the market.<br><span>Not the API.</span>

The typed, testable interface that gives MetaTrader 5 honest lifecycle,
predictable failures, and a Python-native developer experience.

<div class="syntiq-actions" markdown>
[Build your first session](quickstart.md){ .md-button .md-button--primary }
[Explore the design](concepts.md){ .md-button .syntiq-button--quiet }
</div>

<div class="syntiq-badges">
  <span>Python 3.12+</span>
  <span>Fully typed</span>
  <span>Demo-first</span>
</div>

</div>

<div class="syntiq-terminal" markdown>
<div class="syntiq-terminal__bar">
  <span></span><span></span><span></span>
  <strong>strategy.py</strong>
</div>

```python
from syntiq_mt5 import SyntiqMT5, constants

with SyntiqMT5(credentials) as mt5:
    account = mt5.account_info()
    candles = mt5.candles(
        "EURUSD",
        constants.TIMEFRAME_H1,
        count=100,
    )

    print(account.equity)
    print(candles[-1].close)
```

<div class="syntiq-terminal__status">
  <span class="syntiq-pulse"></span>
  Session closed cleanly
</div>
</div>
</section>

<div class="syntiq-install" markdown>
<span>Start with one command</span>
```bash
pip install syntiq-mt5
```
</div>

<section class="syntiq-proof" markdown>
<div><strong>1</strong><span>managed process-global session</span></div>
<div><strong>0</strong><span>ambiguous result wrappers</span></div>
<div><strong>158</strong><span>contract tests</span></div>
<div><strong>100%</strong><span>typed public package</span></div>
</section>

## A small interface with real depth

Syntiq does not mirror thirty native functions behind thirty thin wrappers. One
session concentrates the hard parts: terminal ownership, error capture, UTC
normalization, response conversion, and resource cleanup.

<section class="syntiq-feature-grid">
<article class="syntiq-feature">
  <span class="syntiq-feature__number">01</span>
  <h3>Direct values</h3>
  <p><code>positions()</code> returns <code>tuple[Position, ...]</code>. Empty means empty. Failure means an exception.</p>
</article>
<article class="syntiq-feature">
  <span class="syntiq-feature__number">02</span>
  <h3>Scoped failures</h3>
  <p>Every <code>MT5Error</code> carries the operation, native code, and human-readable message that belong together.</p>
</article>
<article class="syntiq-feature">
  <span class="syntiq-feature__number">03</span>
  <h3>Correct trade semantics</h3>
  <p>Transport failure raises. Broker rejection remains a typed response you can inspect and act on.</p>
</article>
<article class="syntiq-feature">
  <span class="syntiq-feature__number">04</span>
  <h3>Test anywhere</h3>
  <p>Inject an adapter and run deterministic strategy tests on Linux, macOS, Windows, or CI without a terminal.</p>
</article>
</section>

<section class="syntiq-split" markdown>
<div markdown>

## The lifecycle is the architecture

MetaTrader 5 owns one connection and one error state per process. `SyntiqMT5`
makes that constraint visible instead of letting client objects silently fight
over global state.

1. Acquire exclusive process ownership.
2. Initialize and optionally authenticate.
3. Capture each call and `last_error()` atomically.
4. Release subscriptions and shut down on every exit path.

[Understand lifecycle and failures](concepts.md){ .syntiq-text-link }

</div>
<div class="syntiq-flow" aria-label="Syntiq architecture flow">
  <div><small>YOUR CODE</small><strong>SyntiqMT5</strong></div>
  <span>&darr;</span>
  <div><small>PUBLIC SEAM</small><strong>MT5Adapter</strong></div>
  <span>&darr;</span>
  <div><small>NATIVE PROCESS</small><strong>MetaTrader 5</strong></div>
</div>
</section>

## Start where you are

<div class="syntiq-paths" markdown>

[**Connect safely**<br><span>Credentials, context management, and your first account snapshot.</span>](quickstart.md)

[**Read the market**<br><span>Quotes, completed candles, tick history, and managed market depth.</span>](market-data.md)

[**Build trade flows**<br><span>Validate requests, separate transport from broker decisions, and execute deliberately.</span>](trading.md)

[**Ship with confidence**<br><span>Google-style references, strict CI, trusted publishing, and reproducible uv builds.</span>](development.md)

</div>

!!! warning "Designed for deliberate trading"
    Syntiq improves software correctness; it cannot make a trading strategy safe.
    Validate every execution path against a demo account before using live funds.

<div class="syntiq-closing" markdown>

## Less glue. More strategy.

Build on a session that tells the truth about the terminal beneath it.

[Get started](quickstart.md){ .md-button .md-button--primary }
[Read the API](api-session.md){ .md-button .syntiq-button--quiet }

</div>
