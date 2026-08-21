# Security Policy

## Reporting

Do not open a public issue for a vulnerability. Use GitHub's private vulnerability
reporting for this repository. Include affected versions, impact, and a minimal
reproduction without credentials or account data.

## Trading Safety

- Test order flows on a demo account first.
- Load credentials from a secret manager or environment variables.
- Never log `LoginCredential.password` or raw order/account payloads.
- Treat `order_check()` as validation, not an execution guarantee.
- Inspect every `order_send()` retcode, including partial fills and requotes.
- Do not automatically retry `order_send()` after ambiguous transport failure;
  doing so can duplicate an order.

Only the latest released minor version receives security fixes while the project
is in alpha.
