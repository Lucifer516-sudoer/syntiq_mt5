# Core Concepts

Understand the fundamental patterns that make syntiq-mt5 predictable and safe.

---

## Overview

Every syntiq-mt5 session follows the same lifecycle, every operation returns the same `Result[T]` type, and every error is captured the same way. Learn these three patterns and you know the entire SDK.

---

<div class="grid cards" markdown>

-   :material-timeline-clock: __[Lifecycle](lifecycle.md)__

    ---

    The four-step pattern: `initialize → login → use → shutdown`

    Common mistakes and how to avoid them

-   :material-check-decagram: __[Result\[T\]](results.md)__

    ---

    How every operation returns success or failure

    No exceptions, no surprises

-   :material-alert-circle: __[Error Handling](error-handling.md)__

    ---

    How MT5 errors are captured and surfaced

    Two-level checks for trade operations

</div>
