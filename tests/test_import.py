"""
Test importing functionality of easy-gpg-to-paper.
"""

import argparse
import glob
import pytest
from gpg2paper import gpg2paper

KEY_PATH = "tests/testkey_pub.gpg"
KEY_ID = "98436C7A"
FILENAME = "tests/testkey*.%s"

@pytest.mark.usefixtures("unload_gpg_keys")
class TestImport:
    @pytest.mark.parametrize("args", [
        (argparse.Namespace(base64=False,
                            command="import",
                            pubkey=KEY_PATH,
                            in_filenames=sorted(glob.glob(FILENAME % "png")),
                            png=True)),
        (argparse.Namespace(base64=True,
                            command="import",
                            pubkey=KEY_PATH,
                            in_filenames=sorted(glob.glob(FILENAME % "txt")),
                            png=False))
    ])
    def test_do_import_with_gpg_v1(self, args):
        (_, stderr) = gpg2paper.do_import(args)
        assert "key %s: secret key imported" % KEY_ID in stderr.decode("utf-8")
