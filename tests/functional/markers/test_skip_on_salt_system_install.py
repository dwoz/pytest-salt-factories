"""
Test the ``@pytest.mark.skip_on_salt_system_install`` marker.
"""
import os
from unittest import mock


def test_skipped_test(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_salt_system_install
        def test_one():
            assert True
        """
    )
    with mock.patch.dict(os.environ, {"SALT_FACTORIES_SYSTEM_INSTALL": "1"}):
        res = pytester.runpytest_subprocess()
    # res.assert_outcomes(passed=1)
    assert res.parseoutcomes()["skipped"] == 1
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_not_skipped_test(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_salt_system_install
        def test_one():
            assert True
        """
    )
    with mock.patch.dict(os.environ, {"SALT_FACTORIES_SYSTEM_INSTALL": "0"}):
        res = pytester.runpytest_subprocess()
    # res.assert_outcomes(passed=1)
    assert res.parseoutcomes()["passed"] == 1
    res.stdout.no_fnmatch_line("*PytestUnknownMarkWarning*")


def test_marker_does_not_accept_arguments(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_salt_system_install("foo")
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    # res.assert_outcomes(errors=1)
    assert res.parseoutcomes()["errors"] == 1
    res.stdout.fnmatch_lines(
        ["*UsageError: The 'skip_on_salt_system_install' marker does not accept any arguments*"]
    )


def test_marker_does_not_accept_keyword_argument(pytester):
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.skip_on_salt_system_install(foo=True)
        def test_one():
            assert True
        """
    )
    res = pytester.runpytest()
    # res.assert_outcomes(errors=1)
    assert res.parseoutcomes()["errors"] == 1
    res.stdout.fnmatch_lines(
        [
            "*UsageError: The 'skip_on_salt_system_install' marker only accepts 'reason' as a keyword argument*"
        ]
    )
