# CLI: mathcli

A command-line tool that answers common math questions through explicit subcommands. It does not
parse free-text questions.

## Subcommands

### `mathcli fib <count>`

Prints the first `<count>` Fibonacci numbers, starting `0, 1, 1, 2, 3, …`, one per line, in order.

- `<count>` must be a positive integer. `0` prints nothing.

### `mathcli primes <start> <end>`

Prints the `<start>`-th through `<end>`-th smallest prime numbers (1-indexed, both ends
inclusive), one per line, in ascending order.

- `<start>` and `<end>` must be positive integers with `<start> <= <end>`.
- Example: `mathcli primes 1 5` prints the first 5 primes: `2, 3, 5, 7, 11`.

### `mathcli calc <expression>`

Evaluates `<expression>` as an arithmetic expression and prints the result.

- Supported operators: `+`, `-`, `*`, `/`, and parentheses, with standard precedence and
  left-to-right associativity for operators of equal precedence.
- Operands are arbitrary-precision integers.
- `/` is true division (Python-style): the result is not truncated (e.g. `mathcli calc "7/2"`
  prints `3.5`).
- Example: `mathcli calc "100*12307*13971757"` prints `17195041339900`.
- Example: `mathcli calc "(2+3)*4"` prints `20`.

## Errors

Any invalid input — a negative or non-integer count or range, a range where `<start> > <end>`, a
malformed expression, or an expression using unsupported syntax — prints a clear, human-readable
error message to stderr and exits with a non-zero status. No stack trace is shown.
