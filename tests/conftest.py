import pytest
import shutil
import subprocess

@pytest.yield_fixture(autouse=True, scope='session')
def setup_and_cleanup():
    subprocess.call(['gpg', '--import', 'testkey_sec.asc'], cwd='tests')
    subprocess.call(['gpg', '--import', 'testkey_pub.asc'], cwd='tests')
    yield
    shutil.rmtree('tests/out')
