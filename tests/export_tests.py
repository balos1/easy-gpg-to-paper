import argparse
import pytest
import os.path
import glob
from gpg2paper import gpg2paper

KEYNAME = 'easy-gpg-to-paper-testenv'
FILENAME = 'tests/out/testkey'

@pytest.mark.parametrize("args", [
    (argparse.Namespace(base64=False, command='export', keyid=KEYNAME, numfiles=4,
                        outfile_name=FILENAME, png=True, size=400)),
    (argparse.Namespace(base64=False, command='export', keyid=KEYNAME, numfiles=8,
                        outfile_name=FILENAME, png=True, size=400)),
    (argparse.Namespace(base64=True, command='export', keyid=KEYNAME, numfiles=4,
                        outfile_name=FILENAME, png=False, size=400)),
    (argparse.Namespace(base64=True, command='export', keyid=KEYNAME, numfiles=8,
                        outfile_name=FILENAME, png=False, size=400)),
])
def test_do_export(args):
    gpg2paper.do_export(args)
    if args.png:
        outfiles = glob.glob('%s*.png' % args.outfile_name)
    elif args.base64:
        outfiles = glob.glob('%s*.txt' % args.outfile_name)
    else:
        assert False
    assert len(outfiles) == args.numfiles
    