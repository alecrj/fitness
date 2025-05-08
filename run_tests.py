#!/usr/bin/env python3
"""
Test Runner for Fitness/Food App Backend Tests

Usage:
    python run_tests.py             # Run all tests
    python run_tests.py -v          # Run all tests with verbose output
    python run_tests.py module      # Run tests for a specific module
    
Examples:
    python run_tests.py nutrition   # Run only nutrition module tests
    python run_tests.py validators  # Run only validator tests
"""

import unittest
import sys
import os
import importlib

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def discover_and_run_tests(pattern=None, verbosity=1):
    """Discover and run tests matching the pattern"""
    loader = unittest.TestLoader()
    
    if pattern:
        # Convert pattern to a test module name
        if pattern.startswith("test_"):
            module_name = pattern
        else:
            module_name = f"test_{pattern}"
            
        # Only run tests from the specified module
        try:
            # Try to import the module to verify it exists
            importlib.import_module(f"tests.{module_name}")
            test_suite = loader.loadTestsFromName(f"tests.{module_name}")
        except ImportError:
            # Fall back to discovering any test modules that match the pattern
            test_suite = loader.discover('tests', pattern=f"*{pattern}*.py")
    else:
        # Run all tests
        test_suite = loader.discover('tests')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(test_suite)

def main():
    """Main entry point for the test runner"""
    verbosity = 1
    pattern = None
    
    # Process command line arguments
    for arg in sys.argv[1:]:
        if arg == '-v' or arg == '--verbose':
            verbosity = 2
        elif not arg.startswith('-'):
            pattern = arg
    
    print(f"Running {'all tests' if not pattern else f'tests matching {pattern}'}")
    result = discover_and_run_tests(pattern, verbosity)
    
    # Print summary
    print("\nTest Summary:")
    print(f"  Ran {result.testsRun} tests")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")
    
    # Return non-zero exit code if any tests failed
    sys.exit(len(result.failures) + len(result.errors))

if __name__ == '__main__':
    main()