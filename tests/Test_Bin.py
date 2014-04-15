"""
These tests look at the bin script for the project
"""

import subprocess

import nhlstats


def test_version():
    """
    Ensure that -V results in the version being reported
    """
    assert(subprocess.check_output(['bin/nhlstats', '-V']) == 'Version: %s\n' % nhlstats.__version__)


def test_verbose():
    """
    Ensure that -v results in verbose logging
    """
    assert('DEBUG - root - Setting loglevel to DEBUG' in subprocess.check_output(['bin/nhlstats', '-v', 'testignore'], stderr=subprocess.STDOUT))


def test_incorrect_action():
    """
    Ensure that an incorrect action results in an error.
    """
    caughtError = None
    try:
        subprocess.check_output(['bin/nhlstats', 'foo'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        caughtError = error

    assert(caughtError and caughtError.returncode == 1)
    assert(caughtError and caughtError.output.startswith('ERROR: unknown action "foo"'))
