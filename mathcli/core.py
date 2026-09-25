"""Math logic behind the mathcli subcommands: fib, primes and calc."""

import ast
import operator


def fibonacci(count):
    """Return the first `count` Fibonacci numbers, starting 0, 1, 1, 2, 3, ..."""
    if count < 0:
        raise ValueError(f"count must be a non-negative integer, got {count}")
    result = []
    a, b = 0, 1
    for _ in range(count):
        result.append(a)
        a, b = b, a + b
    return result


def _is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def primes_range(start, end):
    """Return the start-th through end-th smallest primes (1-indexed, inclusive)."""
    if start < 1 or end < 1:
        raise ValueError("start and end must be positive integers")
    if start > end:
        raise ValueError(f"start must not be greater than end, got {start} > {end}")
    result = []
    n = 1
    count = 0
    while count < end:
        n += 1
        if _is_prime(n):
            count += 1
            if count >= start:
                result.append(n)
    return result


class CalcError(ValueError):
    """A calc expression could not be evaluated."""


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate(expression):
    """Evaluate an arithmetic expression of +, -, *, /, parentheses and integers."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise CalcError(f"invalid expression: {expression!r}") from exc
    try:
        return _eval_node(tree.body)
    except ZeroDivisionError as exc:
        raise CalcError("division by zero") from exc
    except CalcError:
        raise
    except Exception as exc:
        raise CalcError(f"invalid expression: {expression!r}") from exc


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise CalcError(f"unsupported syntax in expression: {ast.unparse(node)!r}")
