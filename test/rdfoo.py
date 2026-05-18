import sys
import unittest

from pathlib import Path


def main():
    start_path = str(Path(__file__).resolve().parent / "cases")
    sys.path.insert(0, start_path)

    testsuite = unittest.TestLoader().discover(start_path, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(testsuite)

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == '__main__':
    main()
