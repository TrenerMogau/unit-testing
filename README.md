<!-- please generate a readme file about an intro to unit testing with python unittest module (simpler version- only testCases and unittest.main()) -->

# Intro to Unittesting
<!-- Intro to unit testing with the Python `unittest` module. This README focuses on the simple, classic style: subclassing `unittest.TestCase` and calling `unittest.main()` from a test runner script. -->

# Intro to Unit Testing (Python unittest)

This guide introduces basic unit testing with Python's built-in `unittest` framework (the simple style that uses `unittest.TestCase` and `unittest.main()`), then surveys testing methods and techniques you should know: glassbox (white-box) testing and black-box testing. Under each approach we cover common strategies: path testing, statement coverage, random testing, exhaustive testing, equivalence partitioning, and boundary class testing — with notes on applicability and examples.

What you'll find here:

- A tiny, runnable `unittest` example (only `TestCase` + `unittest.main()`).
- Clear explanations of testing methods (glassbox / black-box).
- Practical notes and quick patterns you can use when designing unit tests.

## Quick start: minimal unittest example

Create a file named `test_sample.py` with the following content. It shows the classic pattern: a `unittest.TestCase` subclass and `unittest.main()` so the file can be executed directly.

```python
import unittest

def add(a, b):
  return a + b

class TestAdd(unittest.TestCase):
  def test_add_positive(self):
    self.assertEqual(add(2, 3), 5)

  def test_add_negative(self):
    self.assertEqual(add(-1, -1), -2)

if __name__ == '__main__':
  unittest.main()
```

Run it from the shell:

```pwsh
python test_sample.py
```

Or run all tests in the current directory using the unittest discovery mode:

```pwsh
python -m unittest
```

## Contracts, scope and test shapes (tiny checklist)

- Inputs: concrete values or fixtures your unit accepts.
- Outputs: return values, side-effects, exceptions.
- Error modes: invalid input, network/file errors, timeouts.
- Success criteria: assertions about values, types, and state.

Keep tests small and focused: one logical assertion or behaviour per test (you can have several asserts if they represent the same logical property).

---

## Testing approaches: glassbox (white-box) vs black-box

High-level:

- Glassbox (white-box) testing: you design tests knowing the implementation. Useful for exercising internal branches, specific code paths and ensuring coverage metrics.
- Black-box testing: you test based only on program requirements and observable behavior (inputs -> outputs), without looking at the internal code.

Both approaches are complementary; many teams use both.

### Glassbox (white-box) testing

Definition: tests are derived from the implementation and internal structure. The goal is to ensure internal paths and statements are exercised.

Common techniques (and how to apply them with unit tests):

- Path-testing
  - Idea: choose inputs that execute different control-flow paths (if/else branches, loops with different iteration counts).
  - How to use in unit tests: craft inputs to force each branch and loop behavior; assert expected internal outcomes or final outputs.
  - Example: if function has an early-return for empty inputs, write a test for empty input and a test for non-empty.

- Statement coverage
  - Idea: measure which lines/statements of code have been executed by the test suite.
  - How to use: write tests to execute un-covered lines until you reach your target (e.g., 80% or 90%), then use a coverage tool (such as `coverage.py`) to measure.
  - Note: coverage metrics are indicators, not guarantees of correctness.

- Random testing (white-box fuzzing)
  - Idea: generate many random inputs with awareness of internal structure to try to hit unusual paths. Can be guided by knowledge of internal branches.
  - How to use in `unittest`: write a test method that loops over randomly generated inputs and uses assertions or checks for invariants. Limit iterations to keep tests deterministic (seed the RNG).
  - Example (in TestCase): seed the random generator and run 100 iterations asserting invariants.

- Exhaustive testing
  - Idea: try every possible input (or every combination) when the domain is small and feasible.
  - How to use: enumerate all inputs in a test and assert the exact expected output for each. Useful for small algorithms (e.g., bit-twiddling with 8-bit values).
  - Caveat: combinatorial explosion makes this impractical for large inputs.

- Equivalence partitioning & boundary class testing (white-box view)
  - While typically black-box techniques, they are useful in white-box testing to choose representative inputs that exercise different internal branches.
  - Use implementation insight to form partitions that hit different internal code paths (e.g., input size 0, 1..n, >n to force size-related branches), and test boundaries around branch conditions.

When to prefer glassbox: when you need to verify internal logic, fix bugs in complex conditionals, or drive coverage metrics for critical modules.

### Black-box testing

Definition: tests are derived from requirements and observable behavior only. You don't look at the implementation; you validate that the unit meets its specification.

Common techniques (and how to apply them):

- Path-testing (black-box perspective)
  - In strict black-box testing you don't inspect internal control flow, but you can still aim to trigger different 'paths' through the specification by varying inputs that correspond to different behaviors.
  - For example, if a spec says "if input has property A do X, else do Y", write tests for inputs with and without property A.

- Statement coverage (black-box limits)
  - Statement coverage requires instrumentation or access to source, so strictly black-box testers can't directly measure it.
  - However, you can rely on external tools (or a developer-provided coverage report) to evaluate how much of the implementation your black-box tests exercised. The test author should focus on behavioral correctness.

- Random testing (black-box fuzzing)
  - Idea: generate random inputs to discover unexpected failures (crashes, exceptions, incorrect outputs). This is popularly called fuzzing.
  - How to use in unit tests: within a TestCase, run many random inputs and assert expected invariants or that no unhandled exceptions occur (unless expected). Prefer deterministic seeds or save failing inputs.
  - Example: random strings sent to a parser API to ensure it never crashes and gives a reasonable error for invalid input.

- Exhaustive testing
  - Same concept as white-box: enumerate all inputs, but here you do so based only on the input specification. Feasible for tiny domains.

- Equivalence partitioning
  - Idea: split the input domain into classes that are expected to behave similarly, then select representative values from each class.
  - Example partitions for an integer parameter that is defined as "non-negative and <= 100":
    - valid low (0-10), valid mid (11-90), valid high (91-100)
    - invalid negative (<0), invalid >100
  - Write tests that pick a representative from each class.

- Boundary class testing (boundary value analysis)
  - Idea: errors often occur at the edges of partitions. Test values at, just below, and just above boundaries.
  - Example: for the range 0..100 test -1, 0, 1, 99, 100, 101.

When to prefer black-box: when you are validating conformance to requirements, testing external APIs, or when the implementation may change frequently but the contract remains stable.

---

## Practical patterns and examples

1) Random testing inside a unittest TestCase (deterministic seed):

```python
import unittest
import random

def is_palindrome(s: str) -> bool:
  return s == s[::-1]

class TestPalindromeRandom(unittest.TestCase):
  def test_random_strings(self):
    random.seed(0)  # make the test deterministic
    for _ in range(100):
      length = random.randint(0, 10)
      s = ''.join(random.choices('ab', k=length))
      # invariant: reversed reversal equals original
      self.assertEqual(is_palindrome(s), is_palindrome(s[::-1]))

if __name__ == '__main__':
  unittest.main()
```

2) Exhaustive testing for small domains (example: function over 8-bit inputs):

```python
import unittest

def parity(x: int) -> int:
  # returns 0 if even number of set bits, 1 otherwise
  return bin(x).count('1') % 2

class TestParityExhaustive(unittest.TestCase):
  def test_all_byte_values(self):
    for x in range(256):
      # compare against a known-correct but slower implementation
      expected = sum((x >> i) & 1 for i in range(8)) % 2
      self.assertEqual(parity(x), expected)

if __name__ == '__main__':
  unittest.main()
```

3) Equivalence partitioning and boundary testing example (for a clamp function):

```python
import unittest

def clamp(x, low=0, high=100):
  if x < low:
    return low
  if x > high:
    return high
  return x

class TestClamp(unittest.TestCase):
  def test_equivalence_and_boundaries(self):
    # equivalence classes: below range, inside range, above range
    self.assertEqual(clamp(-5, 0, 100), 0)     # below
    self.assertEqual(clamp(50, 0, 100), 50)    # inside
    self.assertEqual(clamp(200, 0, 100), 100)  # above

    # boundary values
    self.assertEqual(clamp(0, 0, 100), 0)
    self.assertEqual(clamp(1, 0, 100), 1)
    self.assertEqual(clamp(99, 0, 100), 99)
    self.assertEqual(clamp(100, 0, 100), 100)

if __name__ == '__main__':
  unittest.main()
```

## Tips for writing effective tests

- Keep tests deterministic: seed randomness or record failing seeds.
- Prefer small, isolated units. Use mocks or fakes only when necessary.
- Use descriptive test names: `test_<condition>_<expected>`.
- When using random/exhaustive tests, make failures reproducible: save the failing input or print it in the assertion message.
- Combine both white-box and black-box techniques: use black-box to validate promise and white-box to ensure internal correctness and coverage.

## Measuring coverage (brief)

Use `coverage.py` to measure statement and branch coverage. Example (outside of `unittest` scope):

```pwsh
pip install coverage
coverage run -m unittest
coverage report -m
```

Coverage helps prioritize tests but doesn't replace thinking about equivalence classes and boundary values.

## Edge cases & common pitfalls

- Over-reliance on coverage numbers (high coverage doesn't guarantee correctness).
- Flaky tests caused by shared mutable state or timing.
- Tests that replicate the same logic as the implementation (tests should validate behavior, not re-implement the code being tested).

## Further reading

- Python unittest docs: <https://docs.python.org/3/library/unittest.html>
- coverage.py: <https://coverage.readthedocs.io/>
- Fuzzing & property testing: Hypothesis library (advanced)

---

If you want, I can also:

- Add these example files into the repository and run a quick local test suite (I can create `test_*.py` files).
- Add a `requirements.txt` or sample `pyproject.toml` if you want to include a coverage or test runner dependency.

Requirements coverage: this README focuses on TestCase + unittest.main() examples (done) and documents the requested testing methods and techniques (glassbox/black-box and the listed techniques).
