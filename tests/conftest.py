"""
Configuration of pytests.
"""

import fnmatch
import os
import subprocess
import pytest

KEY_NAME = 'easy-gpg-to-paper-testenv'
KEY_FINGERPRINT = 'E0E4 5E97 6DA6 FDA8 02FB  B9A2 ECA0 274B 9843 6C7A'
OUTPUT_PATH = 'tests/out/'
OUTPUT_FILE = 'testsout'

@pytest.yield_fixture(scope="module")
def load_gpg_keys():
    """
    Tests setup and teardown.
    """
    subprocess.call(['gpg', '--import', 'testkey_sec.asc'], cwd='tests')
    subprocess.call(['gpg', '--import', 'testkey_pub.asc'], cwd='tests')

@pytest.yield_fixture()
def unload_gpg_keys():
    """
    Tests setup and teardown.
    """
    subprocess.call(['gpg', '--batch', '--yes', '--delete-secret-keys', KEY_FINGERPRINT], cwd='tests')
    subprocess.call(['gpg', '--batch', '--yes', '--delete-key', KEY_FINGERPRINT], cwd='tests')

@pytest.yield_fixture(scope='function')
def cleanup_export_output():
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
