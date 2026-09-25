"""Argument parsing and dispatch for the mathcli command."""

import argparse
import sys

from .core import evaluate, fibonacci, primes_range


def build_parser():
    parser = argparse.ArgumentParser(prog="mathcli", description="Answers common math questions.")
    sub = parser.add_subparsers(dest="command", required=True)

    fib_p = sub.add_parser("fib", help="Print the first <count> Fibonacci numbers.")
    fib_p.add_argument("count", type=int)

    primes_p = sub.add_parser("primes", help="Print the <start>-th through <end>-th smallest primes.")
    primes_p.add_argument("start", type=int)
    primes_p.add_argument("end", type=int)

    calc_p = sub.add_parser("calc", help="Evaluate an arithmetic expression.")
    calc_p.add_argument("expression")

    return parser


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["calc"] and argv[1:2] != ["--"]:
        # Without "--", argparse treats an expression starting with "-" (e.g. "-5+3")
        # as an unknown option instead of the positional "expression" argument.
        argv = [argv[0], "--", *argv[1:]]
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "fib":
            for n in fibonacci(args.count):
                print(n)
        elif args.command == "primes":
            for p in primes_range(args.start, args.end):
                print(p)
        elif args.command == "calc":
            print(evaluate(args.expression))
    except ValueError as exc:
        print(f"mathcli: error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
