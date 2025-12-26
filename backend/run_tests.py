#!/usr/bin/env python3
"""
Test runner for the RAG Chatbot backend services
"""

import subprocess
import sys
import os


def run_tests():
    """
    Run all tests for the backend services
    """
    print("Running RAG Chatbot backend tests...")

    # Change to the backend directory
    os.chdir(os.path.join(os.path.dirname(__file__)))

    # Run pytest
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "-x"  # Stop on first failure
    ], capture_output=True, text=True)

    print("STDOUT:")
    print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    print(f"Test exit code: {result.returncode}")

    if result.returncode == 0:
        print("All tests passed! ✓")
    else:
        print("Some tests failed! ✗")

    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)