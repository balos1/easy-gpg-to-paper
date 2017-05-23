"""
Configuration of pytests.
"""

import fnmatch
import os
import subprocess
import pytest

KEYNAME = 'easy-gpg-to-paper-testenv'
OUTPUT_PATH = 'tests/out/'
OUTPUT_FILE = 'testsout'

@pytest.yield_fixture(autouse=True, scope='session')
def setup_env():
    """
    Tests setup and teardown.
    """
    subprocess.call(['gpg', '--import', 'testkey_sec.asc'], cwd='tests')
    subprocess.call(['gpg', '--import', 'testkey_pub.asc'], cwd='tests')
    yield

@pytest.yield_fixture(autouse=True, scope='function')
def cleanup_after_test():
    """
    Tests setup and teardown.
    """
    yield
    # cleanup output files
    for root, dirnames, filenames in os.walk('./'):
        for filename in fnmatch.filter(filenames, OUTPUT_FILE+'*'):
            os.remove(os.path.join(root, filename))
    if os.path.exists(OUTPUT_PATH):
        os.rmdir(OUTPUT_PATH)
