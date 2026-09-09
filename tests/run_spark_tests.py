import sys

import pytest


if __name__ == "__main__":
    test_args = sys.argv[1:] or [
        "tests/test_analytics_spark.py",
    ]

    raise SystemExit(
        pytest.main(
            ["-q", *test_args]
        )
    )