import contextlib
import io
import unittest

from mathcli.cli import main
from mathcli.core import CalcError, evaluate, fibonacci, perfect_range, primes_range


class FibonacciTests(unittest.TestCase):
    def test_first_100(self):
        result = fibonacci(100)
        self.assertEqual(len(result), 100)
        self.assertEqual(result[:10], [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_zero_prints_nothing(self):
        self.assertEqual(fibonacci(0), [])

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)


class PrimesTests(unittest.TestCase):
    def test_first_five(self):
        self.assertEqual(primes_range(1, 5), [2, 3, 5, 7, 11])

    def test_200_to_300(self):
        result = primes_range(200, 300)
        self.assertEqual(len(result), 101)
        self.assertEqual(result, sorted(result))
        self.assertEqual(result[0], primes_range(1, 200)[-1])
        self.assertEqual(result[-1], primes_range(1, 300)[-1])

    def test_start_greater_than_end_raises(self):
        with self.assertRaises(ValueError):
            primes_range(5, 1)

    def test_non_positive_raises(self):
        with self.assertRaises(ValueError):
            primes_range(0, 5)


class PerfectTests(unittest.TestCase):
    def test_first_four(self):
        self.assertEqual(perfect_range(1, 4), [6, 28, 496, 8128])

    def test_2_to_3(self):
        self.assertEqual(perfect_range(2, 3), [28, 496])

    def test_start_greater_than_end_raises(self):
        with self.assertRaises(ValueError):
            perfect_range(3, 1)

    def test_non_positive_raises(self):
        with self.assertRaises(ValueError):
            perfect_range(0, 4)


class CalcTests(unittest.TestCase):
    def test_multiplication(self):
        self.assertEqual(evaluate("100*12307*13971757"), 17195041339900)

    def test_precedence_and_parentheses(self):
        self.assertEqual(evaluate("(2+3)*4"), 20)

    def test_true_division(self):
        self.assertEqual(evaluate("7/2"), 3.5)

    def test_division_by_zero_raises(self):
        with self.assertRaises(CalcError):
            evaluate("1/0")

    def test_malformed_expression_raises(self):
        with self.assertRaises(CalcError):
            evaluate("2+")

    def test_unsupported_syntax_raises(self):
        with self.assertRaises(CalcError):
            evaluate("__import__('os').system('echo hi')")

    def test_leading_negative(self):
        self.assertEqual(evaluate("-5+3"), -2)

    def test_negated_parentheses(self):
        self.assertEqual(evaluate("-(2+3)"), -5)


class CliTests(unittest.TestCase):
    def _run(self, argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(argv)
        return code, out.getvalue()

    def test_fib_command(self):
        code, out = self._run(["fib", "5"])
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), ["0", "1", "1", "2", "3"])

    def test_perfect_command(self):
        code, out = self._run(["perfect", "1", "4"])
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), ["6", "28", "496", "8128"])

    def test_calc_command(self):
        code, out = self._run(["calc", "(2+3)*4"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "20")

    def test_calc_command_leading_negative(self):
        code, out = self._run(["calc", "-5+3"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "-2")

    def test_calc_command_negated_parentheses(self):
        code, out = self._run(["calc", "-(2+3)"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "-5")

    def test_invalid_input_reports_error_without_traceback(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = main(["fib", "-5"])
        self.assertEqual(code, 1)
        self.assertIn("error", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
